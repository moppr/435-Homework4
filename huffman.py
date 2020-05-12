# Node/Heap provided by prompt
class Node:

    def __init__(self, c, freq):
        self.c = c
        self.freq = freq
        self.left = None
        self.right = None

    def is_leaf(self):
        return not (self.left or self.right)


class MinHeap:

    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def empty(self):
        return len(self) == 0

    def print(self):
        for x in self.data:
            print(x.c + str(x.freq))

    def insert(self, val):
        self.data.append(val)
        self._heapify_up(len(self.data) - 1)

    def extract_min(self):
        temp = self.data[0]
        self._swap(0, -1)
        self.data.remove(self.data[-1])
        self._heapify_down(0)
        return temp

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _heapify_up(self, idx):
        if idx > 0:
            parent = (idx - 1) // 2
            if self.data[parent].freq > self.data[idx].freq:
                self._swap(parent, idx)
                self._heapify_up(parent)

    def _heapify_down(self, idx):
        data = self.data
        left = 2 * idx + 1
        right = 2 * idx + 2
        mini = idx
        if left < len(data) and (data[left].freq < data[mini].freq):
            mini = left
        if right < len(data) and (data[right].freq < data[mini].freq):
            mini = right
        if mini is not idx:
            self._swap(mini, idx)
            self._heapify_down(mini)


def in_order(node, map, code):
    if node.left:
        in_order(node.left, map, code + "0")
    if node.right:
        in_order(node.right, map, code + "1")
    if node.is_leaf():
        map[node.c] = code


def build_tree(text_input):
    # Build huffman tree.
    heap = MinHeap()
    for character in sorted(set(text_input)):
        heap.insert(Node(character, text_input.count(character)))

    while len(heap) > 1:
        dummy_node = Node("*", -1)
        dummy_node.left = heap.extract_min()
        dummy_node.right = heap.extract_min()
        dummy_node.freq = dummy_node.left.freq + dummy_node.right.freq
        heap.insert(dummy_node)

    return heap


if __name__ == "__main__":
    text_input = input().strip()
    binary_input = input().strip()

    heap = build_tree(text_input)

    # Encode string.
    root = heap.extract_min()
    encoding_map = {}
    in_order(root, encoding_map, "")
    print("".join([encoding_map[character] for character in text_input]))

    heap = build_tree(text_input)

    # Decode string.
    node = heap.data[0]
    for character in binary_input:
        if character == "0":
            node = node.left
        else:
            node = node.right
        if node.is_leaf():
            print(node.c, end="")
            node = heap.data[0]
    print()
