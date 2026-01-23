#1
from collections import defaultdict

def invalidTransactions(transactions):
    by = defaultdict(list)
    bad = set()

    for s in transactions:
        name, t, amt, city = s.split(",")
        t, amt = int(t), int(amt)
        by[name].append((t, city, s))
        if amt > 1000:
            bad.add(s)

    for arry in by.values():
        arry.sort
        for i in range(len(arry)):
            for j in range(i + 1, len(arry)):
                if arry[j][0] - arry[i][0] > 60:
                    break
                if arry[i][0] != arry[j][1]:
                    bad.add(arry[i][2])
                    bad.add(arry[j][2])
    return list(bad)

print(sorted(invalidTransactions(["alice,20,800,mtv","alice,50,100,beijing"])))

#2
import heapq

def mostBooked(n, meetings):
    meetings.sort()
    free = list(range(n))
    heapq.heapify(free)

    busy = []
    used = [0] * n
    
    for start, end in meetings:
        duration = end - start
        while busy and busy[0][0] <= start:
            t, room = heapq.heappop(busy)
            heapq.heappush(free, room)

        if free:
            room = heapq.heappop(free)
            heapq.heappush(busy, (end, room))
        else:
            t, room = heapq.heappop(busy)
            heapq.heappush(busy, (t+ duration, room))

        used[room] += 1

    return used.index(max(used))

print(mostBooked(2, [[0,10],[1,5],[2,7],[3,4]]))          
print(mostBooked(3, [[1,20],[2,10],[3,5],[4,9],[6,8]]))



