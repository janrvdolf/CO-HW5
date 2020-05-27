#!/usr/bin/env python3

import sys
import copy


class Task:
    def __init__(self, id, rd, pt, dd):
        self.id = id
        self.rd = rd
        self.pt = pt
        self.dd = dd


class Schedule:
    def __init__(self, tasks, in_tasks=None, t=None, to_assign=0, lower_bound=0):

        # Default init
        if in_tasks is None:

            # Tasks
            self.tasks = copy.copy(tasks)
            self.unprocessed_tasks = copy.copy(tasks)
            self.in_tasks = list()

            # Other
            self.solution = False
            self.current_time = 0
            self.to_assign = 0

            for t in self.tasks:
                self.to_assign += t.pt
            print('SCH1 {}'.format(self.to_assign))

        else:
            self.tasks = copy.copy(tasks)
            self.in_tasks = copy.copy(in_tasks)
            self.in_tasks.append(t)
            self.unprocessed_tasks = copy.copy(tasks)

            for t in self.in_tasks:
                if t in self.unprocessed_tasks:
                    self.unprocessed_tasks.remove(t)

            self.to_assign = to_assign
            self.current_time = max(lower_bound + t.pt, t.rd + t.pt)
            print('SCH2 {} {}'.format(len(self.in_tasks), len(self.unprocessed_tasks)))

    def add_unprocessed_task(self, ub):
        scheds = list()
        if not self.is_arbitrary_task():
            return scheds
        if not (max(self.current_time, self.min_rj()) + self.time_remaining() < ub):
            return scheds
        for t in self.unprocessed_tasks:
            scheds.append(Schedule(self.tasks, self.in_tasks, t, self.time_remaining() - t.pt, self.current_time))
        return scheds

    def is_arbitrary_task(self):
        ret = True
        print("~~~")
        for t in self.unprocessed_tasks:
            lb = max(self.current_time + t.pt, t.rd + t.pt)
            print("{} {}".format(lb, t.dd))
            if lb <= t.dd:
                print("TRUE")
            else:
                print("FALSE")

            ret = ret and (lb <= t.dd)
        print("~ {}".format(ret))
        print("~~~")
        return ret

    def time_remaining(self):
        total_pt = 0
        for t in self.unprocessed_tasks:
            total_pt += t.pt
        return total_pt

    def min_rj(self):
        ret = 9999999
        for t in self.unprocessed_tasks:
            if t.rd < ret:
                ret = t.rd
        return ret

    def is_opt(self):
        return self.min_rj() >= self.current_time

    def is_complete(self):
        return len(self.unprocessed_tasks) == 0


class Housing:

    def __init__(self, tasks):
        self.completed = []
        self.ub = 999999
        self.tasks = tasks

    def construct(self, schedule):
        if schedule.is_complete():
            ub_new = min(self.ub, schedule.current_time)
            if ub_new < self.ub:
                self.ub = ub_new
                self.completed = list()
                self.completed.append(schedule)
            return 0

        ss = schedule.add_unprocessed_task(self.ub)
        opt = None
        ret = 0

        for s in ss:
            if s.is_opt():
                print('OPTIMAL')
                opt = s
                break

        if opt is not None:
            ss = list()
            ss.append(opt)
            ret = 1

        print("LLL {}".format(len(ss)))
        for s in ss:
            rt = self.construct(s)
            if rt == 1:
                ret = 1
                break
        return ret

    def solution(self, file):
        with open(file, "w+") as out_file:
            if len(self.completed) == 0:
                print('-1')
                out_file.write('-1')
            else:
                sch = self.completed.pop()
                st = {}
                time = 0
                for t in sch.in_tasks:
                    st[t.id] = max(time, t.rd)
                    time = max(time + t.pt, t.rd + t.pt)
                for i in range(self.tasks):
                    print("{}".format(st[i + 1]))
                    out_file.write("{}\n".format(st[i + 1]))


# Input parameters
input_file = sys.argv[1]
output_file = sys.argv[2]

# Load data
with open(input_file, 'r') as fin:
    # Initial row (number of tasks)
    task_count = int(fin.readline())

    # Load tasks
    tasks = list()
    for t in range(task_count):
        # Read whole line of ints
        pt, rd, dd = [int(_) for _ in fin.readline().strip().split(' ')]

        task = Task(t + 1, rd, pt, dd)
        tasks.append(task)

# Construct problem
h = Housing(task_count)
h.construct(Schedule(tasks))
h.solution(output_file)
