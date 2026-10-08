#!/usr/bin/env python3
"""查询已识别意图的最短技能链；只读合同查询，不代替宿主模型理解。"""
import argparse
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True


def route(intent, completed=(), outcome='known', skill=None):
    contract = json.loads((Path(__file__).parents[1] / 'references/routing-contract.json').read_text())
    if outcome == 'unknown' or intent == 'recover':
        return {'action': 'reconcile', 'skills': [], 'replayAllowed': False,
                'recovery': '核对原任务、进程、原生工程与回执；证据不足时保持待核对'}
    available = set(contract['skills'])
    if any(name not in available for name in completed) or (skill and skill not in available):
        raise ValueError('unknown_skill')
    if intent not in contract['intents']:
        raise ValueError('unknown_intent')
    chain = [skill] if skill else contract['intents'][intent]
    return {'action': 'handoff', 'skills': [name for name in chain if name not in completed],
            'replayAllowed': False, 'nativeExecution': 'NOT_RUN', 'hostModelRouting': 'NOT_RUN'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('intent')
    parser.add_argument('--completed', action='append', default=[])
    parser.add_argument('--outcome', choices=['known', 'unknown'], default='known')
    parser.add_argument('--skill')
    args = parser.parse_args()
    try:
        print(json.dumps(route(args.intent, args.completed, args.outcome, args.skill), ensure_ascii=False))
    except (ValueError, OSError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
