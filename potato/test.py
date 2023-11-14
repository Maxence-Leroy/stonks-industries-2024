# pyright: reportUnknownMemberType=false

import matplotlib
matplotlib.use('MacOSX')
import math
import numpy as np
import matplotlib.pylab as pl
from nptyping import NDArray, Float, Shape
from queue import PriorityQueue
import time
from typing import Optional, Self

class State:
    value: tuple[int, int]
    succs: list[Self]

    def __init__(self, x: int, y: int):
        self.value = (x, y)
        self.succs = []
    
    def __lt__(self, other: Self) -> bool:
        return self.value < other.value
    
    def __eq__(self, other: Self) -> bool:
        return self.value == other.value
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return str(self.value)


class DStarLight:
    rhs: NDArray[Shape["300,200"], Float]
    g: NDArray[Shape["300,200"], Float]
    s_start: State
    s_goal: State
    s_last: State
    k_m: float
    u: PriorityQueue[tuple[tuple[float, float], State]] 
    costs: NDArray[Shape["300,200"], Float]
    path: list[State]

    def plot(self):
        pl.plot(self.s_goal.value[0], self.s_goal.value[1], "ob")
        pl.plot(self.s_start.value[0], self.s_start.value[1], "og")
        for x in range(0,30):
            for y in range(0,20):
                pl.text(x, y, f"{round(self.g[x, y], 2)}\n{round(self.rhs[x, y], 2)}", color="red", fontsize=6)
        
        pl.pause(0.00000001)
        print("Wait")
        pl.clf()

    def heuristic(self, p: State, q: State) -> float:
        return round(math.sqrt((p.value[0] - q.value[0]) ** 2 + (p.value[1] - q.value[1]) ** 2), 3)

    def calculate_key(self, s: State) -> tuple[float, float]:
        # print(f"{s} {self.g[s.value]} {self.rhs[s.value]} {self.heuristic(self.s_start, s)}")
        (a, b) = (min(self.g[s.value],self.rhs[s.value]) + self.heuristic(self.s_start, s) + self.k_m , min(self.g[s.value], self.rhs[s.value]))
        return (round(a, 20), round(b, 20))
    
    def __init__(self, s_start: State, s_goal: State, costs: NDArray[Shape["300,200"], Float]) -> None:
        self.u = PriorityQueue()
        self.path = []
        self.k_m = 0
        self.s_start = s_start
        self.s_goal = s_goal
        self.costs = costs
        self.rhs = np.ones((30,20)) * np.inf
        self.g = np.ones((30,20)) * np.inf
        self.rhs[self.s_goal.value] = 0
        self.u.put_nowait((self.calculate_key(self.s_goal), self.s_goal))

    def state_is_valid(self, u: State) -> bool:
        (x, y) = u.value
        return 0 <= x < 30 and 0 <= y < 20

    def prev(self, u: State) -> list[State]:
        (x, y) = u.value
        prevs = [
            State(x-1, y-1),
            State(x+1, y+1),
            State(x+1, y-1),
            State(x-1, y+1),
            State(x, y-1),
            State(x, y+1),
            State(x+1, y),
            State(x-1, y),
            
        ]

        return list(filter(lambda u: self.state_is_valid(u), prevs))
    
    def c(self, p: State, q: State) -> float:
        return self.heuristic(p, q) + self.costs[q.value]
    
    def u_contains_state(self, s: State) -> Optional[tuple[float, float]]:
        for item in self.u.queue:
            if item[1] == s:
                return item[0]
        return None

    def update_vertex(self, u: State) -> None:
        # print(f"update {u} {self.rhs[u.value]}")
        if u.value != self.s_goal.value:
            min_value = np.inf
            for s_prime in u.succs:
                value = self.c(u, s_prime) + self.g[s_prime.value]
                if value <= min_value:
                    min_value = value
            if self.rhs[u.value] > min_value:
                # print("Change rhs")
                self.rhs[u.value] = min_value
                # self.plot()

        has_found_u = True
        while has_found_u:
            index = self.u_contains_state(u)
            if index:
                # print(f"Remove {u}")
                self.u.queue.remove((index, u))
            else:
                has_found_u = False

        if self.g[u.value] != self.rhs[u.value]:
            key = self.calculate_key(u)
            if key[0] != np.inf:
                u_key = key
                if (u_key, u) not in self.u.queue:
                    # print(f"Adding {u} update {self.g[u.value]} {self.rhs[u.value]}")
                    self.u.put_nowait((key, u))

    def compute_shortest_path(self):
        while self.u.queue[0][0] < self.calculate_key(self.s_start) or self.rhs[self.s_start.value] != self.g[self.s_start.value]:
            # print(f"queue {self.u.queue[:3]}")
            k_old, u = self.u.get_nowait()
            # print(k_old, u)
            # print(f"compute {u}")
            u_key = self.calculate_key(u)
            if k_old < u_key:
                if (u_key, u) not in self.u.queue:
                    # print(f"Adding {u} kold")
                    self.u.put_nowait((u_key, u))
            elif self.g[u.value] > self.rhs[u.value]:
                self.g[u.value] = self.rhs[u.value]
                #self.plot()

                previouses = self.prev(u)
                # print(f"{previouses} no inf")
                for prev in previouses:
                    prev.succs.append(u)
                    self.update_vertex(prev)
            else:
                self.g[u.value] = np.inf
                #self.plot()
                self.update_vertex(u)
                previouses = self.prev(u)
                # print(f"{previouses} inf")
                for prev in previouses:
                    prev.succs.append(u)
                    self.update_vertex(prev)

    def main(self):
        self.s_last = self.s_start
        self.compute_shortest_path()
        # print(self.g)
        self.path.append(self.s_start)
        while self.s_last.value != self.s_goal.value:
            if self.g[self.s_last.value] == np.inf:
                raise ValueError()
            
            min_value = np.inf
            min_arg: Optional[State] = None
            for s_prime in self.prev(self.s_last):
                value = self.c(self.s_last, s_prime) + self.g[s_prime.value]
                if value < min_value:
                    min_value = value
                    min_arg = s_prime
            if not min_arg:
                raise ValueError()
            self.s_last = min_arg
            self.path.append(self.s_last)

def main():
    # pl.ioff()
    # pl.subplots(1, 1, figsize=(10,10))
    # pl.grid(True)
    # pl.axis("Equal")
    # pl.xlim([0,30])
    # pl.ylim([0,20])
    # pl.margins(0)
    start = time.time()
    costs = np.ones((30,20)) * 0
    costs[28, 10:20] = np.inf
    costs[5:30, 8] = np.inf
    costs[0:25, 5] = np.inf
    d_star = DStarLight(State(0,0),State(29,19), costs)
    d_star.main()
    # pl.plot(0, 0, "ob")
    # pl.plot(29, 19, "og")
    end = time.time()
    print(end-start)
    x: list[int] = []
    y: list[int] = []
    for u in d_star.path:
        x.append(u.value[0])
        y.append(u.value[1])
        # print(u.value)

    # pl.plot(x, y, '-r')
    # pl.imshow(costs.transpose() > 1, aspect='auto', interpolation='nearest' )
    # pl.show()
    


if __name__ == "__main__":
    main()