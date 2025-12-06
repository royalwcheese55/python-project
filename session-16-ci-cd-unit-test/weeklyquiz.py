#1 shallow copy create a new object but the nested object are the same, deep copy copy the whole object and no shared reference.
#2 python use reference counting as its memory management, and when it go through reference cycles, a cyclic garbage collector finds and free them
#3 threads use threadpool and good for parallel task, coroutine use await and good for io bound task, it can pause itself and we use async def to run it
#4 first search the sys.path and then load it into caaching in sys.modules, all future import can return the cache module instead of rerunning the code.
#5 its also called lifespan event system, for start up it let you connect to db and create engine/ cache. shutdown is disconnet with db and clean all the files and stop the app.
#6 for smallertask we can use the backgroundtask, which you add function to your endpoint, for bigger task we can use rabbitmq with celery, so the task can be process quicker and seperately.
#7 startup runs before the app having request, and shutdown runs when server stop, its simple and easy but you have to impleemnt a lot of startup and shutdown if you have more tasks. lifespan is newer and it unify startup and shutdown, just runs before and after the yield, we can use lifespan when working on newer task or need to manage multi resources.
#8 it allow django to store user info on server while the user just store a cookie with sesssion ID. it also support multi backend storage such as cache or server db
#9 django serve static files by collect from each apps static folder, media files by user uploads


#1
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def ReverseBetween(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy

    for _ in range(left - 1):
        prev = prev.next

    curr = prev.next

    for _ in range(right - left):
        temp = curr.next
        curr.next = temp.next
        temp.next = prev.next
        prev.next = temp

    return dummy.next

# Helper: build linked list from Python list
def build_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    curr = head
    for v in values[1:]:
        curr.next = ListNode(v)
        curr = curr.next
    return head

# Helper: print linked list
def print_list(head):
    curr = head
    while curr:
        print(curr.val, end=" ")
        curr = curr.next
    print()


if __name__ == "__main__":
    # Example: [1,2,3,4,5], left = 2, right = 4
    head = build_list([1, 2, 3, 4, 5])
    new_head = ReverseBetween(head, 2, 4)

    print_list(new_head)   # expected output: 1 4 3 2 5




#2
def ismatch(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    for j in range(2, n+1):
        if p[j-1] == '*':
            dp[0][j] =dp[0][j-2]
    
    for i in range(1, m+1):
        for j in range(1, n+1):
            if p[j-1] == s[i-1] or p[j-1] == '.':
                dp[i][j] = dp[i-1][j-1]

            elif p[j-1] == '*':
                dp[i][j] = dp[i][j-2]

                if p[j-2] == s[i-1] or p[j-2] == '.':
                    dp[i][j] = dp[i-1][j]
    return dp[m][n]
    
print(ismatch("aa", "a"))

#3
def maxFreq(nums):
    from collections import Counter

    freq = Counter(nums)
    max_freq = max(freq.values())

    total = sum(count for count in freq.values() if count == max_freq)
    return total

print(maxFreq([1,1,1,1,2,3,1]))


