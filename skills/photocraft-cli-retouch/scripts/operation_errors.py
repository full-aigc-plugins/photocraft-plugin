"""副作用错误携带稳定恢复字段；展示文字不参与恢复判断。"""


class OperationError(RuntimeError):
    def __init__(self, message, code, phase='submitted', outcome='unknown', recovery_action='reconcile'):
        super().__init__(message)
        self.code = code
        self.phase = phase
        self.outcome = outcome
        self.retryable = False
        self.recoveryAction = recovery_action

    def as_dict(self):
        return {'error': str(self), 'code': self.code, 'phase': self.phase,
                'outcome': self.outcome, 'retryable': self.retryable, 'recoveryAction': self.recoveryAction}


def error(message):
    """只解析本模块调用点的固定错误码；后续正文是不可解释的数据。"""
    code = message.partition(':')[0]
    unknown = code in {'outcome_unknown', 'mcp_disconnected', 'mcp_response_too_large', 'unexpected_command_result'}
    return OperationError(message, code, outcome='unknown' if unknown else 'failed',
                          recovery_action='reconcile' if unknown else 'inspect')


def describe(exception, phase='validation'):
    if isinstance(exception, OperationError) or hasattr(exception, 'outcome'):
        return {'error': str(exception), 'code': exception.code, 'phase': exception.phase,
                'outcome': exception.outcome, 'retryable': False, 'recoveryAction': exception.recoveryAction}
    message=str(exception);code=message.partition(':')[0]
    # 旧公开重复键错误码保持不变；新增定位字段避免消费方解析展示文案。
    location={'fieldPath':message.split(': ',1)[1].split(' expected ',1)[0]} if ': $' in message else {}
    if phase=='validation' and code=='duplicate_json_key':location['message']=message
    return {'error':code if phase=='validation' and code=='duplicate_json_key' else message, 'code':code, 'phase': phase,**location,
            'outcome': 'not_executed' if phase == 'validation' else 'unknown',
            'retryable': False, 'recoveryAction': 'correct_plan' if phase == 'validation' else 'reconcile'}
