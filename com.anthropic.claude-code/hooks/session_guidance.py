#!/usr/bin/env python3
"""Claude Code 会话提示；不访问、启动或关闭 PhotoCraft 进程。"""
import sys


def main():
    try:
        sys.stdin.buffer.read(65536)
    except OSError:
        pass
    print("PhotoCraft：连续任务复用所属原实例和连接；超时先核对原操作。命令按名称转交对应技能，钩子不管理原生进程。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
