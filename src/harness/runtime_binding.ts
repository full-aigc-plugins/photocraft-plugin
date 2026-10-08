import {canonical,readJson,fileDigest,safePath} from '../protocol/files.ts';
import type {Ledger} from './ledger.ts';

/** 显式受管账本的活动组合；历史账本不因普通查询产生升级状态。 */
export function runtimeBinding(ledger:Ledger):any|undefined {
 if(!ledger.db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='runtime_selection'").get())return undefined;
 const row=ledger.db.prepare('SELECT data FROM runtime_selection WHERE singleton=1').get() as any;
 if(!row)throw new Error('runtime_selection_invalid');
 const value=JSON.parse(row.data),active=value?.active;
 if(value.schema!=='photocraft-runtime-selection/v1' || !Number.isSafeInteger(value.generation) || value.generation<1 || !Array.isArray(value.previous)
  || !active || !/^[a-f0-9]{64}$/.test(active.sourceSha256) || !/^[a-f0-9]{64}$/.test(active.runtimeLockSha256) || active.stateSchema!==1 || !['headless','bridge'].includes(active.backend))throw new Error('runtime_selection_invalid');
 safePath(active.skillRoot);safePath(active.runtimeHome);
 if(fileDigest(active.skillRoot+'/scripts/runtime.lock.json')!==active.runtimeLockSha256)throw new Error('runtime_selection_changed');
 const lock=readJson(active.skillRoot+'/scripts/runtime.lock.json');if(lock.resolvedVersion!==active.runtimeVersion)throw new Error('runtime_selection_changed');
 if(canonical(value)!==row.data)throw new Error('runtime_selection_invalid');
 return value;
}

/** 由认领事务调用；显式外来技能目录不能绕过已激活的固定组合。 */
export function assertRuntimeBinding(ledger:Ledger,sourceSha256?:string) {
 const selection=runtimeBinding(ledger);
 if(selection && selection.active.sourceSha256!==sourceSha256)throw new Error('runtime_selection_conflict');
 if(selection && selection.active.backend!=='headless')throw new Error('runtime_backend_conflict');
}
