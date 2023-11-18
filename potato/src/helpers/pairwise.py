
from typing import TypeVar

T = TypeVar("T")
def pairwise(t: list[T]) -> list[tuple[T, T]]:
    pair_list: list[tuple[T, T]] = []
    for i in range (0, len(t) - 1):
        pair_list.append((t[i], t[i+1]))
    return pair_list