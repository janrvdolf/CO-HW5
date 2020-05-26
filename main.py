#!/usr/bin/env python3
import sys


class Task:
    def __init__(self, jid, p, r, d):
        self.jid = jid
        self.p = p
        self.r = r
        self.d = d


if __name__ == '__main__':
    ifilename = sys.argv[1]
    ofilename = sys.argv[0]

    with open(ifilename) as ifile:
        line = ifile.readline().strip().split()

        n = int(line[0])

        data = list()
        tasks = list()
        for idx in range(n):
            line = ifile.readline().strip().split()

            p, r, d = [int(x) for x in line]

            tasks.append(Task(idx, p, r, d))

            data.append([p, r, d])

        start_times = [0] * len(data)

    with open(ofilename) as ofile:
        for i in range(n):
            ofile.write(start_times[i])
