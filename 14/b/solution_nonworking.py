# import json
# import time
from queue import Queue
from threading import Thread
from typing import Dict, List, Optional, Tuple

# this solution attempts to brute-force the sequences by chucking a bunch of
# threads at the problem. even so, this solution fails to work in anything close
# to acceptable time. This is clearly the wrong approach


def parse_input(filename: str = "input.txt") -> Tuple[str, Dict[Tuple[str, ...], str]]:
    polymer: str = ""
    rules: Dict[Tuple[str, ...], str] = {}

    with open(filename, mode="rt") as inputfile:
        chunks = inputfile.read().split("\n\n")
        polymer = chunks[0]
        for rule_str in chunks[1].strip().split("\n"):
            rule_split = rule_str.split(" -> ")
            rules[tuple(list(rule_split[0]))] = rule_split[1]

    return polymer, rules


input, rules = parse_input()


class RuleWorker(Thread):
    def __init__(self, rules: Dict[Tuple[str, ...], str], pair_q: Queue, count_q: Queue, limit: int):
        super(RuleWorker, self).__init__()
        self.rules = rules
        self.pair_q = pair_q
        self.count_q = count_q
        self.limit = limit

    def run(self):
        while True:
            item: Optional[Tuple[int, Tuple[str, ...]]] = self.pair_q.get()

            if item is None:
                return

            if item[0] < self.limit:
                self.count_q.put(self.rules[item[1]])
                self.pair_q.put((item[0] + 1, (item[1][0], self.rules[item[1]])))
                self.pair_q.put((item[0] + 1, (self.rules[item[1]], item[1][1])))

            self.pair_q.task_done()


class Coordinator(Thread):
    def __init__(self, count_q: Queue[Optional[str]], output: Dict[str, int]):
        super(Coordinator, self).__init__()
        self.count_q = count_q
        self.output: Dict[str, int] = output

    def run(self):
        while True:
            item: Optional[str] = self.count_q.get()

            if item is None:
                return

            if item in self.output:
                self.output[item] += 1
            else:
                self.output[item] = 1

            self.count_q.task_done()


def process_step(polymer: str, thread_count: int = 4, step_limit: int = 10):
    pair_q: Queue = Queue()
    count_q: Queue = Queue()
    counts: Dict[str, int] = {}

    # spin up worker threads
    worker_threads: List[Thread] = []
    for thread_idx in range(thread_count):
        worker = RuleWorker(rules, pair_q, count_q, step_limit)
        worker.name = f"RuleWorker[{thread_idx:03d}]"
        worker.start()
        worker_threads.append(worker)

    # populate initial counts
    for c in polymer:
        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1

    # spin up coordinator thread
    coord = Coordinator(count_q, counts)
    coord.name = "Coordinator[000]"
    coord.start()

    # populate work list
    for i in range(1, len(polymer)):
        pair_q.put((0, (input[i - 1], input[i])))

    # blocks until work is complete
    # while (not pair_q.empty()) or (not count_q.empty()):
    #     print("pair_q:", pair_q.qsize(), "count_q:", count_q.qsize(), json.dumps(counts))
    #     time.sleep(15)

    pair_q.join()
    count_q.join()

    # shutdown threads
    count_q.put(None)
    for _thread in worker_threads:
        pair_q.put(None)

    # evaluate thread state
    for t in [*worker_threads, coord]:
        t.join(timeout=2)
        if t.is_alive():
            print(f"WARNING: {t.name} did not shutdown properly, timeout applied")

    # del all thread/queue references
    for t in [*worker_threads, coord]:
        del t
    del pair_q
    del count_q

    return counts


counts = process_step(input, 20, 1)
print(counts)


with open("result.txt", mode="wt") as result:
    result.write("")

with open("output.txt", mode="wt") as outfile:
    outfile.write("")
