import time
from collections import namedtuple
from queue import Queue
from threading import Thread
from typing import List, Optional, Set, Tuple

floor_map: List[List[int]] = []
with open("input.txt", mode="rt") as inputfile:
    for line in inputfile:
        floor_map.append([int(h) for h in line.split()[0]])
limits: Tuple[int, int] = (len(floor_map) - 1, len(floor_map[0]) - 1)

PointValue = namedtuple("PointValue", ["row", "column", "value"])


def is_local_minimum(row, column):
    #                      [top, bottom, left, right, value]
    positions: List[int] = [99, 99, 99, 99, floor_map[row][column]]

    # avoid edge cases
    if row > 0:
        # top
        positions[0] = floor_map[row - 1][column]

    if row < limits[0]:
        # bottom
        positions[1] = floor_map[row + 1][column]

    if column > 0:
        # left
        positions[2] = floor_map[row][column - 1]

    if column < limits[1]:
        # right
        positions[3] = floor_map[row][column + 1]

    if all(map(lambda v: v == floor_map[row][column] or v == 99, [v for v in positions[:4]])):
        return (False, positions)

    return (floor_map[row][column] == min(positions), positions)


minima: List[PointValue] = []
for row, columns in enumerate(floor_map):
    for column, value in enumerate(columns):
        is_min, positions = is_local_minimum(row, column)
        if is_min:
            minima.append(PointValue(row, column, value))


class DataFrame(object):
    def __init__(self, src: PointValue, top: Optional[PointValue], bottom: Optional[PointValue], left: Optional[PointValue], right: Optional[PointValue]):
        self.exclude: Tuple[int, ...] = (9,)
        self.src: PointValue = src
        self.positions: Tuple[Optional[PointValue], ...] = (top, bottom, left, right)

    def evaluate(self) -> List[PointValue]:
        return [i for i in self.positions if i is not None and i.value > self.src.value and i.value not in self.exclude]


class PointsWorker(Thread):
    def __init__(self, src_queue: Queue[Optional[PointValue]], tgt_queue: Queue[Optional[DataFrame]], basin: Set[PointValue]):
        super(PointsWorker, self).__init__()
        self.src_queue: Queue[Optional[PointValue]] = src_queue
        self.tgt_queue: Queue[Optional[DataFrame]] = tgt_queue
        self.basin: Set[PointValue] = basin

    def run(self):
        global output_set
        while True:
            point: Optional[PointValue] = self.src_queue.get()
            if point is None:
                return

            if point not in self.basin:
                self.basin.add(point)
                self.tgt_queue.put(self._convertPointToFrame(point))

    def _convertPointToFrame(self, point: PointValue) -> DataFrame:
        top: Optional[PointValue] = None
        bottom: Optional[PointValue] = None
        left: Optional[PointValue] = None
        right: Optional[PointValue] = None

        if point.row > 0:
            top = PointValue(point.row - 1, point.column, floor_map[point.row - 1][point.column])

        if point.row < limits[0]:
            bottom = PointValue(point.row + 1, point.column, floor_map[point.row + 1][point.column])

        if point.column > 0:
            left = PointValue(point.row, point.column - 1, floor_map[point.row][point.column - 1])

        if point.column < limits[1]:
            right = PointValue(point.row, point.column + 1, floor_map[point.row][point.column + 1])

        return DataFrame(point, top, bottom, left, right)


class DataFrameWorker(Thread):
    def __init__(self, src_queue: Queue[Optional[DataFrame]], tgt_queue: Queue[Optional[PointValue]]):
        super(DataFrameWorker, self).__init__()
        self.src_queue: Queue[Optional[DataFrame]] = src_queue
        self.tgt_queue: Queue[Optional[PointValue]] = tgt_queue

    def run(self):
        while True:
            frame: Optional[DataFrame] = self.src_queue.get()
            if frame is None:
                return

            for valid_point in frame.evaluate():
                self.tgt_queue.put(valid_point)

            del frame


def process_minima_point(minima_point: PointValue):
    """
    this code is most definitely overkill...

    an initial minima point is provided

    all adjacent values to that point are evaluated

    an adjacent value is considered "valid" if:
     - not beyond the size bounds of source array
     - less than 9 (nines are not included, per the problem description)
     - it is higher than current value (must be higher, not equal to)

    valid points then have their own adjacent values evaluated, repeat ad nauseum

    any valid points already seen are not evaluated again (once "valid" always "valid)

    all "valid" points make up the "basin" described in the problem

    this function fires up "evaluation" threads and "coordinator" thread. the
    "coordinator" ensures we are only passing new points to the "evaluation" threads.
    The "evaluation" threads' job is to decide if an adjacent point is valid or
    not. Valid points are passed back to the coordinator
    """
    basin: Set[PointValue] = set()
    points_queue: Queue[Optional[PointValue]] = Queue()
    dataframe_queue: Queue[Optional[DataFrame]] = Queue()
    dataframe_threads: List[Thread] = []
    for thread_idx in range(4):
        dataframe_worker = DataFrameWorker(src_queue=dataframe_queue, tgt_queue=points_queue)
        dataframe_worker.name = f"DataFrameWorker[{thread_idx}]"
        # worker.daemon = True
        dataframe_worker.start()
        dataframe_threads.append(dataframe_worker)

    points_worker = PointsWorker(src_queue=points_queue, tgt_queue=dataframe_queue, basin=basin)
    points_worker.name = "PointsWorker[0]"
    points_worker.start()

    points_queue.put(minima_point)

    while True:
        if points_queue.empty():
            break
        time.sleep(0.1)

    points_queue.put(None, block=False)
    for _t in dataframe_threads:
        dataframe_queue.put(None, block=False)

    for t in [*dataframe_threads, points_worker]:
        t.join(timeout=2)
        if t.is_alive():
            print(f"WARNING: {t.name} did not shutdown properly, timeout applied")

    for t in [*dataframe_threads, points_worker]:
        del t
    del points_queue
    del dataframe_queue

    return minima_point, basin


basins: List[Tuple[PointValue, Set[PointValue]]] = []
for idx, minima_point in enumerate(minima):
    if idx % 40 == 0:
        print(f"processing low point [{idx}]")
    basins.append(process_minima_point(minima_point))

basin_sizes: List[int] = sorted([len(s[1]) for s in basins], reverse=True)
print(basin_sizes[0:3], basin_sizes[0] * basin_sizes[1] * basin_sizes[2])


with open("result.txt", mode="wt") as result:
    result.write(f"total basins: {len(basins)}\n")
    result.write(f"top three highest basin sizes: {repr([basin_sizes[0:3]])}\n")
    result.write(f"top three, multiplied: {basin_sizes[0] * basin_sizes[1] * basin_sizes[2]}\n")


with open("output.txt", mode="wt") as outfile:
    all_basins: Set[PointValue] = set()
    all_minima: Set[PointValue] = set()
    for basin in basins:
        for point in basin[1]:
            all_basins.add(point)
        all_minima.add(basin[0])
    # ░▒▓█
    for row, columns in enumerate(floor_map):
        for column, value in enumerate(columns):
            pv = PointValue(row, column, value)
            if pv in all_basins:
                if pv in all_minima:
                    outfile.write("█")  # ("░")
                else:
                    if pv.value < 4:
                        outfile.write("▓")  # ("▒")
                    elif pv.value < 7:
                        outfile.write("▒")  # ("▓")
                    else:
                        outfile.write("░")  # ("█")
            else:
                outfile.write("‧")
        outfile.write("\n")
