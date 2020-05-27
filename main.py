#!/usr/bin/env python3
import copy
import sys


class Task:
    def __init__(self, jid, p, r, d):
        self.jid = jid
        self.p = p
        self.r = r
        self.d = d

        self.start = None

    def __str__(self):
        return '<Task id={} p={} r={} d={}>'.format(
            self.jid,
            self.p,
            self.r,
            self.d
        )

    def __repr__(self):
        return str(self)


class BB:
    def __init__(self, tasks):
        self.tasks = tasks

        self.upper_bound = None

        self.plan = list()

    def _upper_bound(self, unscheduled_tasks):
        if self.upper_bound is None:
            max_deadline = -sys.maxsize
            for task in unscheduled_tasks:
                max_deadline = max(task.d, max_deadline)
            return max_deadline
        else:
            return self.upper_bound

    def _is_node_pruned(self, scheduled_tasks, unscheduled_tasks):
        pass

    @staticmethod
    def _is_node_leaf(unscheduled_tasks):
        return len(unscheduled_tasks) == 0

    def _tree_search(self, c, scheduled_tasks, unscheduled_tasks):
        if not self._is_node_pruned(scheduled_tasks, unscheduled_tasks):
            if not self._is_node_leaf(unscheduled_tasks):
                for task in unscheduled_tasks:
                    new_scheduled_tasks = copy.deepcopy(scheduled_tasks)
                    new_scheduled_tasks.append(task)

                    new_unscheduled_tasks = unscheduled_tasks.difference([task])

                    self._tree_search(c, scheduled_tasks, new_unscheduled_tasks)
            else:
                pass
                """
                upper_bound = self._upper_bound()
                
                if self._upper_bound > upper_bound:
                    self.plan = copy.deepcopy(scheduled_tasks)
                """
        return

    def create_schedule(self):
        c = 0
        scheduled_tasks = list()
        unscheduled_tasks = set(self.tasks)
        # tree search of branch and bound
        self._tree_search(c, scheduled_tasks, unscheduled_tasks)
        # the best plan from the tree search
        return self.plan


if __name__ == '__main__':
    ifilename = sys.argv[1]
    ofilename = sys.argv[0]

    with open(ifilename) as ifile:
        line = ifile.readline().strip().split()

        n = int(line[0])

        tasks = list()
        for idx in range(n):
            line = ifile.readline().strip().split()

            p, r, d = [int(x) for x in line]

            tasks.append(Task(idx, p, r, d))

    branch_and_bound = BB(tasks)
    schedule = branch_and_bound.create_schedule()

    with open(ofilename) as ofile:
        for i in range(n):
            if i == (n - 1):
                ofile.write(str(schedule[i]) + '\n')
            else:
                ofile.write(str(schedule[i]))
