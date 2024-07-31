import sys
from preprocess import preprocess_text_to_list


class HashTable:
    def __init__(self, number_buckets: int = 1000):
        self.number_buckets = number_buckets
        self.total_words_seen = 0
        self.table = [[] for _ in range(self.number_buckets)]

    def _hash(self, key: str) -> int:
        return sum(ord(char) for char in key) % self.number_buckets

    def insert(self, key: str):
        if self.total_words_seen / self.number_buckets > 0.8:  # Resize when load factor exceeds threshold
            self._resize()

        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                item[1] += 1
                return
        self.table[index].append([key, 1])
        self.total_words_seen += 1

    def _resize(self):
        new_size = self.number_buckets * 2
        new_table = [[] for _ in range(new_size)]
        for bucket in self.table:
            for key, value in bucket:
                new_index = sum(ord(char) for char in key) % new_size
                new_table[new_index].append([key, value])
        self.table = new_table
        self.number_buckets = new_size

    def get_items(self):
        items = []
        for bucket in self.table:
            items.extend(bucket)
        return items


def is_binary(file_path: str) -> bool:
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            return b'\0' in chunk
    except IOError:
        return False


class MinHeap:
    def __init__(self, max_size: int):
        self.heap = []
        self.max_size = max_size

    """
    Tree index reminder (//2 goes down a level, *2 goes up a level):
         0
       /   \
      1     2
     / \   / \
    3   4 5   6
    """

    @staticmethod
    def parent(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def left_child(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def right_child(i: int) -> int:
        return 2 * i + 2

    def swap(self, i: int, j: int):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def push(self, item: tuple[int, str]):
        if len(self.heap) < self.max_size:
            self.heap.append(item)
            self._sift_up(len(self.heap) - 1)
        elif item[0] > self.heap[0][0]:
            self.heap[0] = item
            self._sift_down(0)

    def _sift_up(self, i: int):
        while i > 0 and self.heap[self.parent(i)][0] > self.heap[i][0]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def _sift_down(self, i: int):
        min_index = i
        left = self.left_child(i)
        if left < len(self.heap) and self.heap[left][0] < self.heap[min_index][0]:
            min_index = left
        right = self.right_child(i)
        if right < len(self.heap) and self.heap[right][0] < self.heap[min_index][0]:
            min_index = right
        if i != min_index:
            self.swap(i, min_index)
            self._sift_down(min_index)

    def get_sorted(self) -> list[tuple[int, str]]:
        to_sort = self.heap.copy()

        # Bubble sort implementation
        n = len(to_sort)
        for i in range(n):
            for j in range(0, n - i - 1):
                # Sort descending order by count
                if to_sort[j][0] < to_sort[j + 1][0]:
                    to_sort[j], to_sort[j + 1] = to_sort[j + 1], to_sort[j]

        return to_sort


def process_file(file_path: str) -> list[tuple[int, str]]:
    if is_binary(file_path):
        print(f"Warning: {file_path} appears to be a binary file. Skipping processing.")
        return []

    word_count = HashTable()
    min_heap = MinHeap(20)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                words = preprocess_text_to_list(line)
                for word in words:
                    word_count.insert(word)
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return []

    for word, count in word_count.get_items():
        min_heap.push((count, word))

    return min_heap.get_sorted()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python iteration_2.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    top_words = process_file(filename)

    for count, word in top_words:
        print(f"{count:5d} {word}")
