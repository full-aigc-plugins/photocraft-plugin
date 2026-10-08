/** 错误展示与恢复决策分离；只有明确的执行前检查可声明未执行。 */
export class OperationError extends Error {
 code: string;
 phase: string;
 outcome: string;
 retryable = false;
 recoveryAction: string;
 category?: string;
 fieldPath?: string;
 constructor(message: string, details: {code:string;phase:string;outcome:string;recoveryAction:string;category?:string;fieldPath?:string}) {
  super(message);
  this.name='OperationError';
  this.code=details.code;this.phase=details.phase;this.outcome=details.outcome;this.recoveryAction=details.recoveryAction;
  this.category=details.category;this.fieldPath=details.fieldPath;
 }
}

/** 返回严格输入校验错误，字段位置不依赖错误展示文字。 */
export function validationError(code:string,fieldPath='$',message=code):OperationError {
 return new OperationError(message,{code,fieldPath,phase:'validation',outcome:'not_executed',category:'validation_failed',recoveryAction:'correct_plan'});
}
