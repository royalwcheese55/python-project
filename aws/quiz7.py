import heapq
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)
        self.following = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.time += 1
        self.tweets[userId].append((self.time, tweetId))

    def getNewsFeed(self, userId: int):
        users = set(self.following[userId])
        users.add(userId)

        heap = []
        for uid in users:
            arr = self.tweets[uid]
            if arr:
                t, tid = arr[-1]
                heapq.heappush(heap, (-t, tid, uid, len(arr) - 1))

        res = []
        while heap and len(res) < 10:
            neg_t, tid, uid, idx = heapq.heappop(heap)
            res.append(tid)
            if idx - 1 >= 0:
                t2, tid2 = self.tweets[uid][idx - 1]
                heapq.heappush(heap, (-t2, tid, uid, idx - 1))
        return res
    
    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followerId:
            self.following[followerId].add(followerId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)