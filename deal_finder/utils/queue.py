from typing import Any


class CircularQueue:
    def __init__(self, size: int = 100):
        self._size: int = size
        self._queue: list = [None for i in range(size)] 
        self._front: int = -1
        self._rear: int = -1
 
    def _increment(self, val: int):
        if not isinstance(val, int):
            raise TypeError(f"Incorrect type for \"val\": {type(val)}")

        return val + 1 % self._size 

    def is_full(self) -> bool:
        return (self._rear + 1) % self._size == self._front

    def is_empty(self) -> bool:
        return self._front == -1

    def __delete_at_index(self, index: int) -> None:
        if self._front == self._rear:
            self._front = self._rear = -1
            return

        prev_index = index
        index = self._increment(index)

        while index != self._rear:
            self._queue[prev_index] = self._queue[index]
            prev_index = index
            index = self._increment(index)

        self._queue[prev_index] = self._queue[index]
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
            self._queue[self._rear] = data
            return self._rear

        self._rear = self._increment(self._rear)
        self._queue[self._rear] = data
        return self._rear

    def dequeue(self) -> str:
        if (self.is_empty()):
            raise Exception("Dequeuing when queue is Empty")
             
        if (self._front == self._rear): 
            value = self._queue[self._front]
            self._front = self._rear = -1
            return value

        value = self._queue[self._front]
        self._front = self._increment(self._front)
        return value