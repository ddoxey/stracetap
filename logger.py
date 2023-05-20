#!/usr/bin/env python3
"""
    This program appends a current date/time value
    in bytes (as opposed to a character string).
"""
import os
import time
from datetime import datetime

LogFile = '/tmp/time.log'

def run():

    if os.path.exists(LogFile):
        os.remove(LogFile)

    with open(LogFile, 'ab') as log:
        while True:
            now = datetime.now()
            I = int(now.strftime("%I"))
            M = int(now.strftime("%M"))
            S = int(now.strftime("%S"))
            f = int(now.strftime("%f"))
            Y = int(now.strftime("%Y"))
            m = int(now.strftime("%m"))
            d = int(now.strftime("%d"))
            data = [I, M, S]
            data.append(f >> 16 & 0xF)
            data.append(f >> 12 & 0xF)
            data.append(f >> 8 & 0xF)
            data.append(f >> 4 & 0xF)
            data.append(f >> 0 & 0xF)
            data.append(Y >> 8 & 0xF)
            data.append(Y >> 4 & 0xF)
            data.append(Y >> 0 & 0xF)
            data.extend([m, d, 0])
            print(f'{I:02d}:{M:02d}:{S:02d}.{f:04d} {Y:04d}/{m:02d}/{d:02d} (00)')
            print([f'x{n:02X}' for n in data])
            log.write(bytes(data))
            log.flush()
            time.sleep(1)

if __name__ == '__main__':
    run()
