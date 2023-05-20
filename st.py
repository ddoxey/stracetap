#!/usr/bin/env python3
"""
    This grabs data being written to a file via the hex
    encoded data reported by strace attached to the
    writing process.

    logger.py --+             +--> st.py --> stdout
                |             |
          /tmp/time.log --> strace
"""
import re
import sys
import subprocess

LogFile = '/tmp/time.log'


def get_pid():
    cmd = ['lsof', '-c', 'python3', '-a', LogFile]
    p = subprocess.run(cmd,
                       encoding='UTF8',
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    if p.returncode == 0:
        line = p.stdout.split("\n")[1]
        tokens = re.split(r'\s+', line)
        return {'pid': tokens[1],
                'fd': re.sub(r'\D$', "", tokens[3])}
    return None


def run():
    logger = get_pid()
    if logger is None:
        print('program not running', file=sys.stderr)
        return 1

    strace = ['strace',
              '--write', logger['fd'],
              '-p', logger['pid'],
              '-P', LogFile,
              '-s', '4096',
              '-xx']

    p = subprocess.Popen(strace,
                         encoding='UTF8',
                         universal_newlines=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    while p.poll() is None:
        line = p.stderr.readline()
        if line.startswith('write('):
            data = line.split(" ")[1].rstrip(',').strip('"').lstrip('\\').split('\\')
            print(data)
            I = int(f'0{data[0]}', base=16)
            M = int(f'0{data[1]}', base=16)
            S = int(f'0{data[2]}', base=16)
            f = int(f'0x{"".join([n.lstrip("x0") for n in data[3:8]])}', base=16)
            Y = int(f'0x{"".join([n.lstrip("x0") for n in data[8:11]])}', base=16)
            m = int(f'0{data[11]}', base=16)
            d = int(f'0{data[12]}', base=16)
            null = int(f'0{data[13]}', base=16)
            print(f'{I:02d}:{M:02d}:{S:02d}.{f:06d} {Y:04d}/{m:02d}/{d:02d} ({null:02d})')
    p.kill()

    return p.wait()


if __name__ == '__main__':
    run()
