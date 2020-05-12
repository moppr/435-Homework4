from functools import *


# Below classes adapted from my own implementations of Graph.


@total_ordering
class WeightedNode:

    def __init__(self, value):
        self.value = value
        self.edges = {}

    def __str__(self):
        return f"{self.value}: {[(node.value, self.edges[node]) for node in self.edges]}"

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def add(self, other, weight=0):
        self.edges[other] = weight

    def remove(self, other):
        if other in self.edges:
            self.edges.pop(other)


class WeightedGraph:

    def __init__(self):
        self.adjacency_list = {}

    def __str__(self):
        result = ""
        for node in sorted(self.get_all_nodes()):
            result += f"{str(node)}\n"
        return result[:-1]

    def add_node(self, value):
        node = WeightedNode(value)
        self.adjacency_list[node] = node

    def get_random_node(self):
        return next(iter(self.adjacency_list))

    @staticmethod
    def add_undirected_edge(first, second, weight):
        if first == second:
            return

        first.add(second, weight)
        second.add(first, weight)

    def get_node(self, value):
        if isinstance(value, WeightedNode):
            return self.adjacency_list[value]
        return self.adjacency_list[WeightedNode(value)]


if __name__ == "__main__":
    num_towns = int(input())
    towns = [input() for _ in range(num_towns)]
    num_roads = int(input())
    roads = [input() for _ in range(num_roads)]

    graph = WeightedGraph()

    for town in towns:
        graph.add_node(town.strip())

    for road in roads:
        town, dest, weight = road.split(", ")
        graph.add_undirected_edge(graph.get_node(town), graph.get_node(dest), int(weight))

    # Prim's Algorithm.
    start = graph.get_random_node()
    min_times = {}
    mst = {start}
    total = 0

    for other in start.edges:
        min_times[other] = start.edges[other]

    while len(mst) < num_towns:
        # Code to get key of min value in dict adapted from
        # https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-15.php
        min_node = min(min_times.keys(), key=(lambda k: min_times[k]))
        total += min_times.pop(min_node)
        if min_node not in mst:
            mst.add(min_node)
            for other in min_node.edges:
                if other not in mst:
                    min_times[other] = min(min_node.edges[other], min_times[other]) if other in min_times else min_node.edges[other]

    print(total)
