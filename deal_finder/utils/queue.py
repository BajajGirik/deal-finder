from typing import Any


class CircularQueue:
    def __init__(self, max_size: int = 50):
        self._max_size: int = max_size
        self.__reset()

    def __reset(self):
        self._queue: list = []
        self._front: int = -1
        self._rear: int = -1

    def _increment(self, val: int):
        if not isinstance(val, int):
            raise TypeError(f'Incorrect type for "val": {type(val)}')

        return (val + 1) % self._max_size

    def is_full(self) -> bool:
        return (self._rear + 1) % self._max_size == self._front

    def is_empty(self) -> bool:
        return self._front == -1

    def __insert_at(self, index: int, val: Any):
        if index >= self._max_size:
            raise Exception(
                f"Inserting data in queue at index: {index} (Queue max size: {self._max_size})"
            )

        if index == len(self._queue):
            self._queue.append(val)
        else:
            self._queue[index] = val

    def __delete_at_index(self, index: int) -> None:
        if self._front == self._rear:
            return self.__reset()

        prev_index = index
        index = self._increment(index)

        while index != self._rear:
            self.__insert_at(prev_index, self._queue[index])
            prev_index = index
            index = self._increment(index)

        self._queue[prev_index] = self._queue[index]

        if self._front < self._rear:
            # Remove empty space created at end
            self._queue.pop(self._rear)

        self._rear = prev_index

    def delete(self, key: str) -> None:
        found_at = -1
        curr_index = self._front

        while curr_index != self._rear:
            if self._queue[curr_index] == key:
                found_at = curr_index
                break
            curr_index = self._increment(curr_index)

        if self._queue[curr_index] == key:
            found_at = curr_index

        if found_at != -1:
            self.__delete_at_index(found_at)

    def peek(self) -> Any:
        if self.is_empty():
            return None

        return self._queue[self._front]

    def enqueue(self, data: Any) -> None:
        if self.is_full():
            raise Exception("Enqueuing when queue is full")

        if self.is_empty():
            self._front = self._rear = 0
            self.__insert_at(self._rear, data)
            return self._rear

        self._rear = self._increment(self._rear)
        self.__insert_at(self._rear, data)
        return self._rear

    def dequeue(self) -> str:
        if self.is_empty():
            raise Exception("Dequeuing when queue is Empty")

        if self._front == self._rear:
            value = self._queue[self._front]
            self.__reset()
            return value

        value = self._queue[self._front]
        self._front = self._increment(self._front)
        return value
