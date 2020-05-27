#!/usr/bin/env python3
import copy
import sys


class Task:
    def __init__(self, jid, p, r, d):
        self.jid = jid
        self.p = p
        self.r = r
        self.d = d

        self.starting_time = None

    def set_starting_time(self, c):
        if self.r <= c:
            self.starting_time = c
        else:
            self.starting_time = self.r

    def __str__(self):
        return '<Task id={} p={} r={} d={} s={}>'.format(
            self.jid + 1,
            self.p,
            self.r,
            self.d,
            self.starting_time
        )

    def __repr__(self):
        return str(self)


class BB:
    def __init__(self, tasks):
        self.tasks = tasks

        self.upper_bound = sys.maxsize

        self.plan = list()

    @staticmethod
    def _lower_bound(c, unscheduled_tasks):
        tmp_min = sys.maxsize
        tmp_sum = 0
        for task in unscheduled_tasks:
            tmp_min = min(tmp_min, task.r)
            tmp_sum += task.p
        return max(c, tmp_min) + tmp_sum

    def _upper_bound(self, unscheduled_tasks):
        if self.upper_bound == sys.maxsize:
            max_deadline = -sys.maxsize
            for task in unscheduled_tasks:
                max_deadline = max(task.d, max_deadline)
            return max_deadline
        else:
            return self.upper_bound

    @staticmethod
    def _is_missed_deadline(c, unscheduled_tasks):
        for task in unscheduled_tasks:
            if (max(c, task.r) + task.p) > task.d:
                return True
        return False

    def _is_node_pruned(self, c, unscheduled_tasks):
        if self._is_missed_deadline(c, unscheduled_tasks):
            return True

        upper_bound = self._upper_bound(unscheduled_tasks)
        lower_bound = self._lower_bound(c, unscheduled_tasks)
        if lower_bound > upper_bound:
            return True

        return False

    def _is_optimal(self, c, unscheduled_tasks):
        # Decomposition
        min_r = sys.maxsize
        for task in unscheduled_tasks:
            min_r = min(min_r, task.r)
        return c <= min_r

    @staticmethod
    def _is_node_leaf(unscheduled_tasks):
        return len(unscheduled_tasks) == 0

    def _tree_search(self, c, scheduled_tasks, unscheduled_tasks):
        if not self._is_node_leaf(unscheduled_tasks):
            if not self._is_node_pruned(c, unscheduled_tasks):
                is_this_optimal = False
                if self._is_optimal(c, unscheduled_tasks):
                    # do not backtrack
                    print('Optimal', c, scheduled_tasks, unscheduled_tasks)
                    is_this_optimal = True

                for task in unscheduled_tasks:
                    new_c = c
                    if task.r <= c:
                        new_c += task.p
                    else:
                        new_c = task.r + task.p

                    new_unscheduled_tasks = unscheduled_tasks.difference([task])

                    new_scheduled_task = copy.deepcopy(task)
                    new_scheduled_task.set_starting_time(c)

                    new_scheduled_tasks = copy.deepcopy(scheduled_tasks)
                    new_scheduled_tasks.append(new_scheduled_task)

                    is_children_optimal = self._tree_search(new_c, new_scheduled_tasks, new_unscheduled_tasks)
                    if is_children_optimal:
                        # break  # working 5 but time limit reached
                        return is_children_optimal  # time limit reached
                        # return is_this_optimal  # time limit ok, but 5 is not working
                return is_this_optimal
            return False
        else:
            if self.upper_bound > c:
                self.upper_bound = c

                self.plan = copy.deepcopy(scheduled_tasks)
        return False

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
    ofilename = sys.argv[2]

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

    returning_list = [None] * n
    for scheduled_task in schedule:
        returning_list[scheduled_task.jid] = scheduled_task.starting_time

    with open(ofilename, 'w') as ofile:
        if len(schedule) == 0:
            ofile.write('-1')
        else:
            for i in range(n):
                if i != (n - 1):
                    ofile.write(str(returning_list[i]) + '\n')
                else:
                    ofile.write(str(returning_list[i]))
