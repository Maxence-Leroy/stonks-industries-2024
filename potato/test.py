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
        return str(self.to_float())
    
    def __repr__(self) -> str:
        return str(self.to_float())
    
    def __hash__(self) -> int:
        return hash(self.to_float())
    
    def to_float(self) -> tuple[float, float]:
        return self.value

class InterpolatedState(State):
    float_value: tuple[float, float]

    def __init__(self, x: float, y: float):
        super().__init__(int(x), int(y))
        self.float_value = (x,y)

    def to_float(self) -> tuple[float, float]:
        return self.float_value

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
    points_in_u: dict[State, list[tuple[float, float]]]

    def plot(self):
        pl.subplots(1, 1, figsize=(10,10))
        pl.plot(self.s_goal.value[0], self.s_goal.value[1], "ob")
        pl.plot(self.s_start.value[0], self.s_start.value[1], "og")
        for x in range(0,30):
            for y in range(0,20):
                pl.text(x, y, f"{round(self.g[x, y], 2)}\n{round(self.rhs[x, y], 2)}", color="red", fontsize=6)
        
        pl.pause(0.00000001)
        print("Wait")

    def heuristic(self, p: State, q: State) -> float:
        return round(math.sqrt((p.to_float()[0] - q.to_float()[0]) ** 2 + (p.to_float()[1] - q.to_float()[1]) ** 2), 3)

    def calculate_key(self, s: State) -> tuple[float, float]:
        # print(f"{s} {self.g[s.value]} {self.rhs[s.value]} {self.heuristic(self.s_start, s)}")
        (a, b) = (min(self.g[s.value],self.rhs[s.value]) + self.heuristic(self.s_start, s) + self.k_m , min(self.g[s.value], self.rhs[s.value]))
        return (round(a, 20), round(b, 20))
    
    def __init__(self, s_start: State, s_goal: State, costs: NDArray[Shape["300,200"], Float]) -> None:
        self.u = PriorityQueue()
        self.points_in_u = {}
        self.path = []
        self.k_m = 0
        self.s_start = s_start
        self.s_goal = s_goal
        self.costs = costs
        self.rhs = np.ones((30,20)) * np.inf
        self.g = np.ones((30,20)) * np.inf
        self.rhs[self.s_goal.value] = 0
        goal_key = self.calculate_key(self.s_goal)
        self.points_in_u[self.s_goal] = [goal_key]
        self.u.put_nowait((goal_key, self.s_goal))

    def state_is_valid(self, u: State) -> bool:
        (x, y) = u.to_float()
        return 0 <= x <= 29 and 0 <= y <= 19

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
    
    def is_diagonal(self, s1: State, s2: State) -> bool:
        diff_x = abs(s2.value[0] - s1.value[0])
        diff_y = abs(s2.value[1] - s1.value[1])
        return diff_x + diff_y == 2

    def c(self, s: State, s_a: State, s_b: State) -> float:
        if self.is_diagonal(s_a, s):
            s_1 = s_b
            s_2 = s_a
        else:
            s_1 = s_a
            s_2 = s_b
        c = self.costs[s.value]
        b = self.costs[s.value]
        if min(b, c) == np.inf:
            v_s = np.inf
        elif self.g[s_1.value] <= self.g[s_2.value]:
            v_s = min(b, c) + self.g[s_1.value]
        else:
            f = self.g[s_1.value] - self.g[s_2.value]
            if f <= b:
                if c <= f:
                    v_s = c * math.sqrt(2) + self.g[s_2.value]
                else:
                    y = min(f / math.sqrt(c*c-f*f), 1)
                    v_s = c* math.sqrt(1 + y*y) + f * (1-y) + self.g[s_2.value]
            else:
                if c <= b:
                    v_s = c * math.sqrt(2) + self.g[s_2.value]
                else:
                    x = 1 - min(b/ math.sqrt(c*c-b*b), 1)
                    v_s = c * math.sqrt(1 + (1-x)**2) + b * x + self.g[s_2.value]

        return v_s
    
    def connbrs(self, s:State) -> list[tuple[State, State]]:
        nbrs: list[tuple[State, State]] = []
        s_1 = State(s.value[0] + 1, s.value[1])
        s_2 =  State(s.value[0] + 1, s.value[1] + 1)
        s_3 =  State(s.value[0], s.value[1] + 1)
        s_4 =  State(s.value[0] - 1, s.value[1] + 1)
        s_5 =  State(s.value[0] - 1, s.value[1])
        s_6 =  State(s.value[0] - 1, s.value[1] - 1)
        s_7 =  State(s.value[0], s.value[1] - 1)
        s_8 =  State(s.value[0] + 1, s.value[1] - 1)

        if self.state_is_valid(s_1) and self.state_is_valid(s_2):
            nbrs.append((s_1, s_2))

        if self.state_is_valid(s_2) and self.state_is_valid(s_3):
            nbrs.append((s_2, s_3))

        if self.state_is_valid(s_3) and self.state_is_valid(s_4):
            nbrs.append((s_3, s_4))

        if self.state_is_valid(s_4) and self.state_is_valid(s_5):
            nbrs.append((s_4, s_5))

        if self.state_is_valid(s_5) and self.state_is_valid(s_6):
            nbrs.append((s_5, s_6))

        if self.state_is_valid(s_6) and self.state_is_valid(s_7):
            nbrs.append((s_6, s_7))

        if self.state_is_valid(s_7) and self.state_is_valid(s_8):
            nbrs.append((s_7, s_8))

        if self.state_is_valid(s_8) and self.state_is_valid(s_1):
            nbrs.append((s_8, s_1))

        return nbrs

    def update_vertex(self, u: State) -> None:
        # print(f"update {u} {self.rhs[u.value]}")
        if u.value != self.s_goal.value:
            min_value = np.inf
            for (s_prime, s_prime_prime) in self.connbrs(u):
                value = self.c(u, s_prime, s_prime_prime)
                if value <= min_value:
                    min_value = value
            if self.rhs[u.value] > min_value:
                # print("Change rhs")
                self.rhs[u.value] = min_value
                #elf.plot()

        points_in_u = self.points_in_u.pop(u, [])
        if len(points_in_u) > 0:
            for key in points_in_u:
                self.u.queue.remove((key, u))

        if self.g[u.value] != self.rhs[u.value]:
            key = self.calculate_key(u)
            if key[0] != np.inf:
                u_key = key
                if (u_key, u) not in self.u.queue:
                    # print(f"Adding {u} update {self.g[u.value]} {self.rhs[u.value]}")
                    if u in self.points_in_u:
                        self.points_in_u[u].append(key)
                    else:
                        self.points_in_u[u] = [key]
                    self.u.put_nowait((key, u))

    def compute_shortest_path(self):
        while self.u.queue[0][0] < self.calculate_key(self.s_start) or self.rhs[self.s_start.value] != self.g[self.s_start.value]:
            # print(f"queue {self.u.queue[:3]}")
            k_old, u = self.u.get_nowait()
            self.points_in_u[u].remove(k_old)
            if len(self.points_in_u[u]) == 0:
                self.points_in_u.pop(u)
            # print(k_old, u)
            # print(f"compute {u}")
            u_key = self.calculate_key(u)
            if k_old < u_key:
                if (u_key, u) not in self.u.queue:
                    # print(f"Adding {u} kold")
                    self.u.put_nowait((u_key, u))
                    if u in self.points_in_u:
                        self.points_in_u[u].append(u_key)
                    else:
                        self.points_in_u[u] = [u_key]
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

    def get_best_interpolated_child(self, s: State) -> InterpolatedState:
        interpolated_children: PriorityQueue[tuple[float, InterpolatedState]] = PriorityQueue()
        x, y = s.value
        division = 25
        for j in range(-division,division + 1):
            child = InterpolatedState(x+1, y + j/division)
            if self.state_is_valid(child):
                if j < 0:
                    cost = self.heuristic(child, s) + abs(j/division) * self.rhs[x+1,y-1] + (1-abs(j/division)) * self.rhs[x+1, y]
                elif j > 0:
                    cost = self.heuristic(child, s) + abs(j/division) * self.rhs[x+1, y+1] + (1-abs(j/division)) * self.rhs[x+1, y]
                else:
                    cost = 1 + self.rhs[x+1, y]
                if not math.isnan(cost):
                    interpolated_children.put_nowait((cost, child))
            
            child = InterpolatedState(x-1, y+j/division)
            if self.state_is_valid(child):
                if j < 0:
                    cost = self.heuristic(child, s) + abs(j/division) * self.rhs[x-1,y-1] + (1-abs(j/division)) * self.rhs[x-1, y]
                elif j > 0:
                    cost = self.heuristic(child, s) + abs(j/division) * self.rhs[x-1, y+1] + (1-abs(j/division)) * self.rhs[x-1, y]
                else:
                    cost = 1 + self.rhs[x-1, y]
                if not math.isnan(cost):
                    interpolated_children.put_nowait((cost, child))


        for i in range(-division,division + 1):
            child = InterpolatedState(x + i /division, y + 1)
            if self.state_is_valid(child):
                if i < 0:
                    cost = self.heuristic(child, s) + abs(i/division) * self.g[x-1,y+1] + (1-abs(i/division)) * self.g[x, y+1]
                elif i > 0:
                    cost = self.heuristic(child, s) + abs(i/division) * self.g[x+1, y+1] + (1-abs(i/division)) * self.g[x, y+1]
                else:
                    cost = 1 + self.g[x, y + 1]
                if not math.isnan(cost):
                    interpolated_children.put_nowait((cost, child))
            
            child = InterpolatedState(x + i /division, y - 1)
            if self.state_is_valid(child):
                if i < 0:
                    cost = self.heuristic(child, s) + abs(i/division) * self.g[x-1,y-1] + (1-abs(i/division)) * self.g[x, y-1]
                elif i > 0:
                    cost = self.heuristic(child, s) + abs(i/division) * self.g[x+1, y-1] + (1-abs(i/division)) * self.g[x, y-1]
                else:
                    cost = 1 + self.g[x, y - 1]
                if not math.isnan(cost):
                    interpolated_children.put_nowait((cost, child))

        (_, best) = interpolated_children.get_nowait()
        return best
    
    def get_path(self) -> list[State]:
        s = self.s_start
        path = [s]
        while s != self.s_goal:
            s = self.get_best_interpolated_child(s)
            path.append(s)
        return path


    def main(self):
        self.s_last = self.s_start
        self.compute_shortest_path()

def main():
    pl.ioff()
    pl.subplots(1, 1, figsize=(10,10))
    pl.grid(True)
    pl.axis("Equal")
    pl.xlim([0,30])
    pl.ylim([0,20])
    pl.margins(0)
    start = time.time()
    costs = np.ones((30,20))
    costs[28, 10:20] = np.inf
    costs[5:30, 8] = np.inf
    costs[0:25, 5] = np.inf
    d_star = DStarLight(State(0,0),State(29,19), costs)
    d_star.main()
    # d_star.plot()
    pl.plot(0, 0, "ob")
    pl.plot(29, 19, "og")
    path = d_star.get_path()
    end = time.time()
    print(end-start)
    x: list[float] = []
    y: list[float] = []
    for u in path:
        x.append(u.to_float()[0])
        y.append(u.to_float()[1])
        # print(u.to_float())

    pl.plot(x, y, '-r')
    pl.imshow(costs.transpose() > 1, aspect='auto', interpolation='nearest' )
    pl.show()
    


if __name__ == "__main__":
    main()