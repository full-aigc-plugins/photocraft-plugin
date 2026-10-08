"""Verify registered MCP scope refuses an old project's external smart link."""
import argparse, hashlib, importlib.util, json, subprocess, tempfile
from pathlib import Path

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(skill, binary):
    spec=importlib.util.spec_from_file_location('fixed_link_guard_session',skill/'scripts/mcp_session.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    from PIL import Image
    baseline={str(p.relative_to(skill)):sha(p) for p in skill.rglob('*') if p.is_file()}
    lock=json.loads((skill/'scripts/runtime.lock.json').read_text())
    assert sha(binary)==lock['artifacts']['darwin-arm64']['binarySha256']
    version=subprocess.check_output([str(binary),'--version'],text=True).strip()
    assert version==lock['artifacts']['darwin-arm64']['versionOutput']
    rows=[]
    with tempfile.TemporaryDirectory() as temporary:
        base=Path(temporary).resolve(); root=base/'registered'; root.mkdir(); outside=base/'unregistered.png'
        Image.new('RGBA',(16,16),(220,10,20,255)).save(outside); outside_sha=sha(outside)
        for linked in [True,False]:
            project=root/('linked.pcraft' if linked else 'embedded.pcraft')
            cmd='file.placeLinked' if linked else 'file.placeEmbedded'
            result=subprocess.run([str(binary),'run','--new',json.dumps({'width':64,'height':64,'name':'External link guard'}),'--cmd',cmd,'--params',json.dumps({'path':str(outside)}),'--out',str(project)],capture_output=True,text=True)
            assert result.returncode==0,result.stderr
            original_sha=sha(project)
            def data(reply):
                assert not reply.get('isError'),reply
                return json.loads(next(c['text'] for c in reply['content'] if c['type']=='text'))
            with module.Session([str(binary),'mcp','--automation-read-root',str(root),'--automation-write-root',str(root)]) as connection:
                def call(tool,args):return connection.request('tools/call',{'name':tool,'arguments':args})
                data(call('doc_open',{'path':project.name}))
                before=data(call('doc_inspect',{}))
                smart=next(l for l in before['layers'] if 'smart' in l['kind'].lower())
                assert smart['smartSourceKind']==('linked' if linked else 'embedded'),smart
                reply=call('command_run',{'id':'layer.smartObjects.convertToEmbedded','params':{'layer':smart['id']}})
                if linked:
                    assert reply.get('isError'),reply
                    assert 'scoped linked content must be replaced with registered bytes before embedding' in json.dumps(reply),reply
                else:
                    assert data(reply)['embedded'] is True
                after=data(call('doc_inspect',{})); assert before==after,(before,after)
            assert sha(project)==original_sha and sha(outside)==outside_sha
            if linked:
                # Same actual fixture succeeds through trusted local CLI; the scoped
                # refusal is not caused by a missing, unreadable or invalid image.
                converted=base/'trusted-embedded.pcraft'
                trusted=subprocess.run([str(binary),'run',str(project),'--cmd','layer.smartObjects.convertToEmbedded','--params',json.dumps({'layer':smart['id']}),'--out',str(converted)],capture_output=True,text=True)
                assert trusted.returncode==0,trusted.stderr
                state=json.loads(subprocess.check_output([str(binary),'info',str(converted),'--compact'],text=True))
                assert next(l for l in state['layers'] if l['id']==smart['id'])['smartSourceKind']=='embedded'
            rows.append({'sourceKind':'linked' if linked else 'embedded','scopedConversion':'REFUSED' if linked else 'PASS','inMemoryStateUnchanged':True,'projectBytesUnchanged':True,'externalAssetUnchanged':True,'trustedLocalControlPassed':True if linked else None,'projectSha256':original_sha})
        assert set(p.name for p in root.iterdir())=={'linked.pcraft','embedded.pcraft'}
    assert baseline=={str(p.relative_to(skill)):sha(p) for p in skill.rglob('*') if p.is_file()}
    return {'installedSkillUnchanged':True,'schema':'photocraft-smart-external-link-guard/v1','status':'PASS','platform':'darwin-arm64','runtimeVersion':lock['resolvedVersion'],'binarySha256':sha(binary),'cases':rows,'scope':'Actual old linked native fixture outside registered root refused by fixed installed MCP; embedded fixture accepted; trusted local control proves valid external source','fullV1':'NOT_RUN'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--skill-root',type=Path,required=True);parser.add_argument('--runtime',type=Path,required=True);parser.add_argument('--evidence',type=Path,required=True);args=parser.parse_args()
    proof=verify(args.skill_root.resolve(),args.runtime.resolve());proof['driverSha256']=sha(Path(__file__));args.evidence.write_text(json.dumps(proof,indent=2)+'\n');print('Native external-link refusal and embedded control: PASS')
