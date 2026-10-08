import { randomUUID } from 'node:crypto';
import { canonical, digest, fileDigest, readJson } from '../protocol/files.ts';
import { Ledger } from '../harness/ledger.ts';

/** 评估只消费固定产物，不能直接编辑或替代技术验收。 */
export class Review {
  ledger: Ledger;
  constructor(ledger: Ledger) { this.ledger = ledger; }

  current(task: any) {
    if (task.technical.status !== 'PASS') throw new Error('technical_verification_required');
    for(const ref of task.request.references??[])if(fileDigest(ref.path)!==ref.sha256)throw new Error('reference_identity_mismatch');
    for (const [path, sha256] of Object.entries(task.technical.files ?? {})) {
      if (fileDigest(path) !== sha256) throw new Error('candidate_changed');
    }
  }

  request(id: string, rubricVersion = 'photocraft-review/v1'): any {
    const task = this.ledger.status(id); this.current(task);
    if (task.state !== 'verifying') throw new Error('review_not_ready');
    if (task.reviewRequest && !task.reviewConsumed) return task.reviewRequest;
    const request = { id: randomUUID(), taskId: id, round: task.revisions,
      projectSha256: task.technical.projectSha256, previewSha256: task.technical.previewSha256,
      manifestSha256: task.technical.manifestSha256, referencesSha256:digest(canonical(task.request.references??[])),references:task.request.references??[],briefSha256: digest(task.request.brief), rubricVersion,
      brief: task.request.brief, contextRequirement: 'independent-artifact-review',
      inputs: ['brief', 'reference', 'native-project', 'preview'], executorSelfAssessmentAllowed: false };
    this.ledger.update(id, task.epoch, current => { current.reviewRequest = request; current.reviewConsumed = false; current.reviewRevisionReserved=false; });
    return request;
  }

  import(id: string, receipt: any): any {
    const task = this.ledger.status(id); this.current(task);
    if (task.reviewConsumed) throw new Error('review_already_consumed');
    const request = task.reviewRequest;
    if (!request || task.state !== 'verifying') throw new Error('review_request_required');
    const fields = ['requestId', 'projectSha256', 'previewSha256', 'manifestSha256', 'referencesSha256', 'briefSha256', 'rubricVersion', 'evaluator', 'verdict', 'gaps'];
    if (!receipt || typeof receipt !== 'object' || Object.keys(receipt).some(key => !fields.includes(key))) throw new Error('invalid_review_receipt');
    if (receipt.requestId !== request.id || ['projectSha256', 'previewSha256', 'manifestSha256', 'referencesSha256', 'briefSha256', 'rubricVersion'].some(key => receipt[key] !== request[key])) throw new Error('review_binding_mismatch');
    const evaluator = receipt.evaluator;
    if(evaluator?.identity==='photocraft-harness' || evaluator?.identity===task.worker?.token)throw new Error('executor_self_review_refused');
    if (!evaluator || !['human', 'host', 'external'].includes(evaluator.kind)
        || typeof evaluator.identity !== 'string' || !evaluator.identity.trim()
        || typeof evaluator.version !== 'string' || !evaluator.version.trim()
        || typeof evaluator.contextIsolation !== 'string' || !evaluator.contextIsolation.trim()) throw new Error('independent_evaluator_required');
    if (!['PASS', 'FAIL'].includes(receipt.verdict) || !Array.isArray(receipt.gaps)
        || (receipt.verdict === 'PASS' && receipt.gaps.length) || (receipt.verdict === 'FAIL' && !receipt.gaps.length)) throw new Error('invalid_review_verdict');
    const gapIds = new Set();
    for (const gap of receipt.gaps) {
      if (!gap || typeof gap.id !== 'string' || gapIds.has(gap.id) || !gap.reason || !gap.property
          || !Number.isSafeInteger(gap.layer) || gap.layer<=0) throw new Error('invalid_review_gap');
      gapIds.add(gap.id);
    }
    this.ledger.update(id, task.epoch, current => {
      current.reviewConsumed = true; current.reviewReceipt = receipt;
      current.creative = { status: receipt.verdict, receiptSha256: digest(canonical(receipt)), requestId: request.id };
    });
    if (receipt.verdict === 'PASS') return this.ledger.transition(id, task.epoch, 'review_ready');
    return this.ledger.status(id);
  }

  accept(id: string, requestId: string): any {
    const task = this.ledger.status(id); this.current(task);
    if (task.state !== 'review_ready' || task.creative.status !== 'PASS' || requestId !== task.reviewRequest?.id) throw new Error('acceptance_binding_mismatch');
    this.ledger.update(id, task.epoch, current => { current.acceptance = { status: 'PASS', requestId, at: Date.now() }; });
    return this.ledger.transition(id, task.epoch, 'completed');
  }

  propose(id: string, proposal: any): any {
    const task = this.ledger.status(id); this.current(task);
    if(!proposal || typeof proposal!=='object' || Array.isArray(proposal) || Object.keys(proposal).some(key=>!['baseProjectSha256','baseManifestSha256','authorizationRef','operations','protectedRegions'].includes(key)))throw new Error('revision_scope_violation');
    if(task.reviewRevisionReserved)throw new Error('revision_already_reserved');
    if (task.creative.status !== 'FAIL' || !task.reviewConsumed) throw new Error('verified_gaps_required');
    const ancestors=this.ledger.lineage(task);const root=ancestors.at(-1)??task;
    if([task,...ancestors].some(parent=>parent.stopRequestedAt || ['cancel_requested','cancelled','failed'].includes(parent.state)))throw new Error('parent_task_stopped');
    if(root.revisions>=root.request.budget.maxRevisions || Date.now()>=root.request.budget.deadline)throw new Error('budget_exhausted');
    if (task.revisions >= task.request.budget.maxRevisions || Date.now() >= task.request.budget.deadline) throw new Error('budget_exhausted');
    if (proposal.baseProjectSha256 !== task.technical.projectSha256 || proposal.baseManifestSha256 !== task.technical.manifestSha256) throw new Error('revision_conflict');
    if (proposal.authorizationRef !== task.request.authorization.ref) throw new Error('authorization_scope_changed');
    if (!Array.isArray(proposal.operations) || !proposal.operations.length || proposal.operations.length > 100) throw new Error('revision_operations_required');
    const nativePath=Object.keys(task.technical.files??{}).find(path=>path.endsWith('/native.json'));
    const objects=new Map<number,any>();
    const walk=(layers:any[])=>{for(const row of layers){if(objects.has(row.id))throw new Error('duplicate_layer_identity');objects.set(row.id,row);if(row.children)walk(row.children);}};
    if(nativePath)walk(readJson(nativePath).layers);
    const allowed: Record<string, string[]> = {
      'type.edit': ['text'], 'type.setStyle': ['font', 'size'],
      'layer.renameLayer': ['name'], 'layer.setAdjustment': ['brightness', 'contrast']
    };
    if(proposal.protectedRegions!==undefined) {
     const regions=proposal.protectedRegions;const ids=new Set();
     if(!Array.isArray(regions) || regions.length>128)throw new Error('revision_protection_invalid');
     for(const region of regions){
      if(!region || typeof region!=='object' || Object.keys(region).some(key=>!['id','rect'].includes(key)) || typeof region.id!=='string' || !region.id.trim() || region.id.length>64 || ids.has(region.id) || !Array.isArray(region.rect) || region.rect.length!==4 || region.rect.some((value:any)=>!Number.isSafeInteger(value) || value<0 || value>16384) || region.rect[2]<=0 || region.rect[3]<=0)throw new Error('revision_protection_invalid');
      ids.add(region.id);
     }
    }
    const protectedRegions=[...(task.request.plan.protectedRegions??[]),...(proposal.protectedRegions??[])];
    const factsPath=Object.keys(task.technical.files??{}).find(path=>path.endsWith('/native-facts.json'));
    const facts=factsPath?readJson(factsPath):undefined;
    for (const operation of proposal.operations) {
      if (!operation || Object.keys(operation).some(key => !['command', 'params'].includes(key))) throw new Error('revision_scope_violation');
      const fields = Object.hasOwn(allowed,operation.command)?allowed[operation.command]:undefined; const params = operation.params;
      if (!fields || !params || typeof params!=='object' || Array.isArray(params) || !Number.isSafeInteger(params.layer) || params.layer<=0 || Object.keys(params).some(key => key !== 'layer' && !fields.includes(key))) throw new Error('revision_scope_violation');
      const changes = Object.keys(params).filter(key => key !== 'layer');
      if (!changes.length || changes.some(property => !task.reviewReceipt.gaps.some((gap: any) => gap.layer === params.layer && gap.property === property))) throw new Error('revision_gap_mismatch');
      if(operation.command==='layer.setAdjustment' && !nativePath)throw new Error('revision_object_not_editable');
      if(nativePath) {
       const row=objects.get(params.layer);if(!row)throw new Error('revision_object_missing');
       if(operation.command.startsWith('type.') && row.kind!=='Type')throw new Error('revision_object_not_editable');
       if(operation.command==='layer.setAdjustment') {
        const values=row.adjustment?.BrightnessContrast;const mask=facts?.objects?.[String(params.layer)];
        if(row.kind!=='Adjustment' || !values || !row.hasMask || !mask?.maskEnabled || !/^[a-f0-9]{64}$/.test(mask.maskSurfaceSha256??''))throw new Error('revision_object_not_editable');
        if(!protectedRegions.length)throw new Error('revision_protection_required');
        for(const field of changes){const value=params[field];const range=field==='brightness'?[-150,150]:[values.legacy?-100:-50,100];if(typeof value!=='number' || !Number.isFinite(value) || value<range[0] || value>range[1])throw new Error('revision_parameter_invalid');}
        if(changes.every(key=>values[key]===params[key]))throw new Error('revision_no_improvement');
       } else if(changes.every(key=>(operation.command.startsWith('type.')?row.text?.[key==='size'?'sizePt':key]:row[key])===params[key]))throw new Error('revision_no_improvement');
      }
      const scope = task.request.authorization.objects;
      if (scope && !scope.includes(params.layer)) throw new Error('authorization_scope_changed');
    }
    return { schema: 'photocraft-revision/v1', taskId: id, baseProjectSha256: proposal.baseProjectSha256,
      baseManifestSha256: proposal.baseManifestSha256, authorizationRef: proposal.authorizationRef,
      operations: proposal.operations, protectedRegions,
      gapReceiptSha256: task.creative.receiptSha256, briefSha256:digest(task.request.brief), referencesSha256:digest(canonical(task.request.references??[])), planSha256: digest(canonical(proposal.operations)) };
  }
}
