class Node:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache = {}
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: str) -> str | None:
        if key not in self.cache:
            return None
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value
    
    def put(self, key: str, value: str) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
            return
        
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add_to_front(new_node)\
        
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

cache = LRUCache(2)

cache.put("a", "apple")
cache.put("b", "banana")

print(cache.get("a"))  # apple

cache.put("c", "cherry")  # evicts b

print(cache.get("b"))  # None

cache.put("d", "date")  # evicts a

print(cache.get("a"))  # None
print(cache.get("c"))  # cherry
print(cache.get("d"))  # date

