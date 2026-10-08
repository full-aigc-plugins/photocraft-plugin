import { copyFileSync, existsSync, mkdtempSync, rmSync, chmodSync, realpathSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { canonical, fileDigest, safePath } from '../protocol/files.ts';
import { OperationError } from '../protocol/operation_error.ts';

/** 只读查询使用私有数据库与日志副本，不在用户账本旁生成共享内存文件。 */
export function readLedgerSnapshot(sourceRoot:string):{root:string;file:string} {
 const source=safePath(sourceRoot);const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-ledger-read-')));
 const identity=()=>{
  const files:Record<string,string>={};
  for(const name of ['tasks.sqlite','tasks.sqlite-wal','tasks.sqlite-journal']) {
   const path=safePath(join(source,name));
   if(existsSync(path))files[name]=fileDigest(path);
  }
  return files;
 };
 try {
  const before=identity();if(!before['tasks.sqlite'])throw new Error('ledger_missing');
  for(const name of Object.keys(before)) {
   const path=join(root,name);copyFileSync(safePath(join(source,name)),path);chmodSync(path,0o600);
  }
  // WAL可能被追加或检查点合并；拒绝移动中的副本，不能返回猜测的旧状态。
  if(canonical(identity())!==canonical(before) || Object.entries(before).some(([name,sha])=>fileDigest(join(root,name))!==sha))
   throw new OperationError('ledger_read_conflict',{code:'ledger_read_conflict',phase:'validation',outcome:'not_executed',category:'state_conflict',fieldPath:'$.stateDirectory',recoveryAction:'inspect'});
  return {root,file:join(root,'tasks.sqlite')};
 } catch(error) {rmSync(root,{recursive:true,force:true});throw error;}
}
