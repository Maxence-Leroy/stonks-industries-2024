from math import sqrt, inf
import numpy as np
from nptyping import NDArray, Float, Int, Shape
from typing import Optional, Self

from src.constants import PLAYING_AREA_DEPTH, PLAYING_AREA_WIDTH
from src.logging import logging_info, logging_warning, logging_error

class Node:
    x: int
    y: int
    cost: float

    def __init__(self, x:int, y:int, cost: float = 0) -> None:
        self.x = x
        self.y = y
        self.cost = cost
    
    def __add__(self, other: Self) -> Self:
        return Node(self.x + other.x, self.y + other.y, self.cost + other.cost)
    
def nodes_have_same_coordinates(node1: Node, node2: Node) -> bool:
    return node1.x == node2.x and node1.y == node2.y

class DStarLite:
    motions: list[Node] = [
        Node(1, 0, 1),
        Node(0, 1, 1),
        Node(-1, 0, 1),
        Node(0, -1, 1),
        Node(1, 1, sqrt(2)),
        Node(1, -1, sqrt(2)),
        Node(-1, 1, sqrt(2)),
        Node(-1, -1, sqrt(2))
    ]

    obstacles: list[Node]
    obstacles_xy: NDArray[Shape["*, 2"], Int]
    start: Node
    goal: Node
    u: list[tuple[Node, tuple[float, float]]]
    km: float
    kold: tuple[float, float]
    rhs: NDArray[Shape["300, 200"], Float]
    g: NDArray[Shape["300, 200"], Float]
    detected_obstacles_xy: NDArray[Shape["*, 2"], Int]
    spoofed_obstacles: list[Node]
    path: list[tuple[int, int]]

    def __init__(self) -> None:
        self.obstacles = []
        self.obstacles_xy = np.array([])
        self.u = []
        self.km = 0.0
        self.kold = (0.0, 0.0)

    def set_start(self, x: float, y: float):
        self.start = Node(int(x / 10), int(y/10))

    def init(self, obstacles: list[tuple[int, int]], start_x: float, start_y: float, goal_x: float, goal_y: float) -> None:
        obstacle_set = set(obstacles)
        print(len(obstacle_set))
        self.obstacles = [Node(obstacle[0], obstacle[1]) for obstacle in obstacle_set]
        self.obstacles_xy = np.array(
            [[obstacle.x, obstacle.y] for obstacle in self.obstacles]
        )
        self.start = Node(int(start_x/10), int(start_y/10))
        self.goal = Node(int(goal_x/10), int(goal_y/10))
        self.u = []
        self.km = 0.0
        self.kold = (0.0, 0.0)
        self.rhs = self.create_grid(float("inf"))
        self.g = self.create_grid(float("inf"))
        self.detected_obstacles_xy = np.empty((0, 2), dtype=int)
        self.rhs[self.goal.x][self.goal.y] = 0
        self.u.append((self.goal, self.calculate_key(self.goal)))
        self.spoofed_obstacles = list()
        self.path = []

    def create_grid(self, val: float):
        return np.full((int(PLAYING_AREA_WIDTH / 10), int(PLAYING_AREA_DEPTH /10)), val)
    
    def is_obstacle(self, node: Node) -> bool:
        x = np.array([node.x])
        y = np.array([node.y])
        obstacle_x_equal = self.obstacles_xy[:, 0] == x
        obstacle_y_equal = self.obstacles_xy[:, 1] == y
        is_in_obstacles = (obstacle_x_equal & obstacle_y_equal).any()

        is_in_detected_obstacles = False
        if self.detected_obstacles_xy.shape[0] > 0:
            is_x_equal = self.detected_obstacles_xy[:, 0] == x
            is_y_equal = self.detected_obstacles_xy[:, 1] == y
            is_in_detected_obstacles = (is_x_equal & is_y_equal).any()

        return is_in_obstacles or is_in_detected_obstacles
    
    def cost(self, node1: Node, node2: Node) -> float:
        if self.is_obstacle(node2):
            # Attempting to move from or to an obstacle
            return inf
        new_node = Node(node1.x-node2.x, node1.y-node2.y)
        detected_motion: Optional[Node] = None
        for motion in self.motions:
            if nodes_have_same_coordinates(motion, new_node):
                detected_motion = motion
                break
        if detected_motion == None:
            logging_error("No motion found")
            raise KeyError()
        
        return detected_motion.cost
    
    def h(self, s: Node) -> float:
        # Cannot use the 2nd euclidean norm as this might sometimes generate
        # heuristics that overestimate the cost, making them inadmissible,
        # due to rounding errors etc (when combined with calculate_key)
        # To be admissible heuristic should
        # never overestimate the cost of a move
        # hence not using the line below
        # return math.hypot(self.start.x - s.x, self.start.y - s.y)

        # Below is the same as 1; modify if you modify the cost of each move in
        # motion
        # return max(abs(self.start.x - s.x), abs(self.start.y - s.y))
        return 1

    def calculate_key(self, s: Node) -> tuple[float, float] :
        return (
                min(
                    self.g[s.x][s.y], 
                    self.rhs[s.x][s.y]
                ) + self.h(s) + self.km, 

                min(self.g[s.x][s.y], self.rhs[s.x][s.y])
            )

    def is_valid(self, node: Node) -> bool:
        if 0 <= node.x < PLAYING_AREA_WIDTH / 10 and 0 <= node.y < PLAYING_AREA_DEPTH / 10:
            return True
        return False

    def get_neighbours(self, u: Node) -> list[Node]:
        return [u + motion for motion in self.motions
                if self.is_valid(u + motion)]

    def pred(self, u: Node) -> list[Node]:
        # Grid, so each vertex is connected to the ones around it
        return self.get_neighbours(u)

    def succ(self, u: Node) -> list[Node]:
        # Grid, so each vertex is connected to the ones around it
        return self.get_neighbours(u)
    
    def update_vertex(self, u: Node):
        if not nodes_have_same_coordinates(u, self.goal):
            self.rhs[u.x][u.y] = min(
                [self.cost(u, sprime) + self.g[sprime.x][sprime.y] for sprime in self.succ(u)]
            )

        if any([nodes_have_same_coordinates(u, node) for node, _ in self.u]):
            self.u = [
                (node, key) for node, key in self.u if not nodes_have_same_coordinates(node, u)
                ]
            self.u.sort(key=lambda x: x[1])

        if self.g[u.x][u.y] != self.rhs[u.x][u.y]:
            self.u.append((u, self.calculate_key(u)))
            self.u.sort(key=lambda x: x[1])

    
    def compare_keys(self, key_pair1: tuple[float, float], key_pair2: tuple[float, float]) -> bool:
        return key_pair1[0] < key_pair2[0] or \
               (key_pair1[0] == key_pair2[0] and key_pair1[1] < key_pair2[1])

    def compute_shortest_path(self):
        self.u.sort(key=lambda x: x[1])
        has_elements = len(self.u) > 0
        start_key_not_updated = self.compare_keys(
            self.u[0][1], self.calculate_key(self.start)
        )
        rhs_not_equal_to_g = self.rhs[self.start.x][self.start.y] != \
            self.g[self.start.x][self.start.y]
        while has_elements and start_key_not_updated or rhs_not_equal_to_g:
            self.kold = self.u[0][1]
            u = self.u[0][0]
            self.u.pop(0)
            if self.compare_keys(self.kold, self.calculate_key(u)):
                self.u.append((u, self.calculate_key(u)))
                self.u.sort(key=lambda x: x[1])
            elif (self.g[u.x, u.y] > self.rhs[u.x, u.y]).any():
                self.g[u.x, u.y] = self.rhs[u.x, u.y]
                for s in self.pred(u):
                    self.update_vertex(s)
            else:
                self.g[u.x, u.y] = inf
                for s in self.pred(u) + [u]:
                    self.update_vertex(s)
            self.u.sort(key=lambda x: x[1])
            start_key_not_updated = self.compare_keys(
                self.u[0][1], self.calculate_key(self.start)
            )
            rhs_not_equal_to_g = self.rhs[self.start.x][self.start.y] != \
                self.g[self.start.x][self.start.y]
            
    def add_obstacle(self, x: float, y: float) -> None:
        self.spoofed_obstacles.append(Node(int(x/10),int(y/10)))
            
    def detect_changes(self) -> list[Node]:
        changed_vertices: list[Node] = list()
        if len(self.spoofed_obstacles) > 0:
            for spoofed_obstacle in self.spoofed_obstacles:
                if nodes_have_same_coordinates(spoofed_obstacle, self.start) or nodes_have_same_coordinates(spoofed_obstacle, self.goal):
                    continue
                changed_vertices.append(spoofed_obstacle)
                self.detected_obstacles_xy = np.concatenate(
                    (
                        self.detected_obstacles_xy,
                        [[spoofed_obstacle.x, spoofed_obstacle.y]]
                    )
                )
            self.spoofed_obstacles = list()
        return changed_vertices
    
    def compute_current_path(self) -> list[tuple[int, int]]:
        path: list[tuple[int, int]] = list()
        current_point = Node(self.start.x, self.start.y)
        while not nodes_have_same_coordinates(current_point, self.goal):
            path.append((current_point.x, current_point.y))
            current_point = min(self.succ(current_point),
                                key=lambda sprime:
                                self.cost(current_point, sprime) +
                                self.g[sprime.x][sprime.y])
        path.append((self.goal.x, self.goal.y))
        return path

    def compare_paths(self, path1: list[Node], path2: list[Node]):
        if len(path1) != len(path2):
            return False
        for node1, node2 in zip(path1, path2):
            if not nodes_have_same_coordinates(node1, node2):
                return False
        return True

    def main(self) -> None:
        last = self.start
        self.compute_shortest_path()

        while not nodes_have_same_coordinates(self.goal, self.start):
            if self.g[self.start.x][self.start.y] == inf:
                logging_error("No path possible")
                return
            changed_vertices = self.detect_changes()
            if len(changed_vertices) != 0:
                logging_warning("New obstacle detected")
                self.km += self.h(last)
                last = self.start
                for u in changed_vertices:
                    if nodes_have_same_coordinates(u, self.start):
                        continue
                    self.rhs[u.x][u.y] = inf
                    self.g[u.x][u.y] = inf
                    self.update_vertex(u)
                self.compute_shortest_path()
        logging_info("Path ended")