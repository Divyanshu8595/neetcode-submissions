"""Curated DSA interview portfolio: 55 readable Python implementations.

Each function is self-contained and uses standard-library data structures.
Assumes inputs satisfy the corresponding problem constraints.
"""
from collections import Counter, defaultdict, deque, OrderedDict
from bisect import bisect_left
import heapq

# ARRAYS / HASHING
def contains_duplicate(nums): return len(nums) != len(set(nums))
def is_anagram(s, t): return Counter(s) == Counter(t)
def two_sum(nums, target):
    seen={}
    for i,x in enumerate(nums):
        if target-x in seen: return [seen[target-x],i]
        seen[x]=i
    return []
def group_anagrams(words):
    d=defaultdict(list)
    for w in words: d[tuple(sorted(w))].append(w)
    return list(d.values())
def top_k_frequent(nums,k):
    return [x for x,_ in Counter(nums).most_common(k)]
def product_except_self(nums):
    out=[1]*len(nums); p=1
    for i,x in enumerate(nums): out[i]=p; p*=x
    p=1
    for i in range(len(nums)-1,-1,-1): out[i]*=p; p*=nums[i]
    return out
def is_valid_sudoku(board):
    rows=[set() for _ in range(9)]; cols=[set() for _ in range(9)]; boxes=[set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            x=board[r][c]
            if x=='.': continue
            b=(r//3)*3+c//3
            if x in rows[r] or x in cols[c] or x in boxes[b]: return False
            rows[r].add(x); cols[c].add(x); boxes[b].add(x)
    return True
def longest_consecutive(nums):
    s=set(nums); best=0
    for x in s:
        if x-1 not in s:
            y=x
            while y in s: y+=1
            best=max(best,y-x)
    return best

# TWO POINTERS
def is_palindrome(s):
    t=[c.lower() for c in s if c.isalnum()]
    return t==t[::-1]
def two_sum_sorted(a,target):
    l,r=0,len(a)-1
    while l<r:
        z=a[l]+a[r]
        if z==target: return [l+1,r+1]
        if z<target: l+=1
        else: r-=1
    return []
def three_sum(nums):
    a=sorted(nums); out=[]
    for i in range(len(a)-2):
        if i and a[i]==a[i-1]: continue
        l,r=i+1,len(a)-1
        while l<r:
            z=a[i]+a[l]+a[r]
            if z<0: l+=1
            elif z>0: r-=1
            else:
                out.append([a[i],a[l],a[r]]); l+=1; r-=1
                while l<r and a[l]==a[l-1]: l+=1
                while l<r and a[r]==a[r+1]: r-=1
    return out
def max_area(h):
    l,r=0,len(h)-1; ans=0
    while l<r:
        ans=max(ans,(r-l)*min(h[l],h[r]))
        if h[l]<h[r]: l+=1
        else: r-=1
    return ans
def trap_rain_water(h):
    l,r=0,len(h)-1; lm=rm=ans=0
    while l<r:
        if h[l]<h[r]:
            lm=max(lm,h[l]); ans+=lm-h[l]; l+=1
        else:
            rm=max(rm,h[r]); ans+=rm-h[r]; r-=1
    return ans

# SLIDING WINDOW
def max_profit(prices):
    low=float('inf'); best=0
    for p in prices: low=min(low,p); best=max(best,p-low)
    return best
def length_of_longest_substring(s):
    last={}; left=best=0
    for right,c in enumerate(s):
        if c in last and last[c]>=left: left=last[c]+1
        last[c]=right; best=max(best,right-left+1)
    return best
def character_replacement(s,k):
    count=defaultdict(int); left=mx=ans=0
    for right,c in enumerate(s):
        count[c]+=1; mx=max(mx,count[c])
        if right-left+1-mx>k: count[s[left]]-=1; left+=1
        ans=max(ans,right-left+1)
    return ans
def check_inclusion(p,s):
    n=len(p)
    if n>len(s): return False
    need=Counter(p); win=Counter(s[:n])
    if need==win: return True
    for i in range(n,len(s)):
        win[s[i]]+=1; win[s[i-n]]-=1
        if win[s[i-n]]==0: del win[s[i-n]]
        if win==need: return True
    return False
def min_window(s,t):
    if not t: return ''
    need=Counter(t); missing=len(t); left=0; best=(float('inf'),0,0)
    for right,c in enumerate(s):
        if need[c]>0: missing-=1
        need[c]-=1
        while missing==0:
            if right-left+1<best[0]: best=(right-left+1,left,right+1)
            need[s[left]]+=1
            if need[s[left]]>0: missing+=1
            left+=1
    return '' if best[0]==float('inf') else s[best[1]:best[2]]

# STACKS
def is_valid_parentheses(s):
    pairs={')':'(',']':'[','}':'{'}; st=[]
    for c in s:
        if c in pairs:
            if not st or st.pop()!=pairs[c]: return False
        else: st.append(c)
    return not st
class MinStack:
    def __init__(self): self.data=[]
    def push(self,x): self.data.append((x,min(x,self.data[-1][1]) if self.data else x))
    def pop(self): return self.data.pop()[0]
    def top(self): return self.data[-1][0]
    def get_min(self): return self.data[-1][1]
def eval_rpn(tokens):
    st=[]
    for x in tokens:
        if x in '+-*/':
            b,a=st.pop(),st.pop()
            st.append(a+b if x=='+' else a-b if x=='-' else a*b if x=='*' else int(a/b))
        else: st.append(int(x))
    return st[-1]
def daily_temperatures(t):
    ans=[0]*len(t); st=[]
    for i,x in enumerate(t):
        while st and t[st[-1]]<x:
            j=st.pop(); ans[j]=i-j
        st.append(i)
    return ans
def largest_rectangle_area(h):
    st=[]; best=0
    for i,x in enumerate(h+[0]):
        start=i
        while st and st[-1][1]>x:
            j,height=st.pop(); best=max(best,height*(i-j)); start=j
        st.append((start,x))
    return best

# BINARY SEARCH
def binary_search(a,target):
    l,r=0,len(a)-1
    while l<=r:
        m=(l+r)//2
        if a[m]==target: return m
        if a[m]<target: l=m+1
        else: r=m-1
    return -1
def search_matrix(m,target):
    if not m or not m[0]: return False
    rows,cols=len(m),len(m[0]); l,r=0,rows*cols-1
    while l<=r:
        x=(l+r)//2; v=m[x//cols][x%cols]
        if v==target: return True
        if v<target: l=x+1
        else: r=x-1
    return False
def min_eating_speed(piles,h):
    l,r=1,max(piles)
    while l<r:
        m=(l+r)//2
        if sum((p+m-1)//m for p in piles)<=h: r=m
        else: l=m+1
    return l
def find_min_rotated(a):
    l,r=0,len(a)-1
    while l<r:
        m=(l+r)//2
        if a[m]>a[r]: l=m+1
        else: r=m
    return a[l]
def search_rotated(a,target):
    l,r=0,len(a)-1
    while l<=r:
        m=(l+r)//2
        if a[m]==target: return m
        if a[l]<=a[m]:
            if a[l]<=target<a[m]: r=m-1
            else: l=m+1
        elif a[m]<target<=a[r]: l=m+1
        else: r=m-1
    return -1

# LINKED LISTS
class ListNode:
    def __init__(self,val=0,next=None): self.val,self.next=val,next
def reverse_list(head):
    prev=None
    while head:
        nxt=head.next; head.next=prev; prev,head=head,nxt
    return prev
def merge_two_lists(a,b):
    dummy=tail=ListNode()
    while a and b:
        if a.val<=b.val: tail.next,a=a,a.next
        else: tail.next,b=b,b.next
        tail=tail.next
    tail.next=a or b
    return dummy.next
def has_cycle(head):
    slow=fast=head
    while fast and fast.next:
        slow,fast=slow.next,fast.next.next
        if slow is fast: return True
    return False
def remove_nth_from_end(head,n):
    dummy=ListNode(0,head); slow=fast=dummy
    for _ in range(n): fast=fast.next
    while fast.next: slow,fast=slow.next,fast.next
    slow.next=slow.next.next
    return dummy.next

# TREES
class TreeNode:
    def __init__(self,val=0,left=None,right=None): self.val,self.left,self.right=val,left,right
def max_depth(root):
    return 0 if not root else 1+max(max_depth(root.left),max_depth(root.right))
def invert_tree(root):
    if root: root.left,root.right=invert_tree(root.right),invert_tree(root.left)
    return root
def is_same_tree(p,q):
    if not p or not q: return p is q
    return p.val==q.val and is_same_tree(p.left,q.left) and is_same_tree(p.right,q.right)
def level_order(root):
    if not root: return []
    q=deque([root]); out=[]
    while q:
        level=[]
        for _ in range(len(q)):
            n=q.popleft(); level.append(n.val)
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        out.append(level)
    return out
def is_valid_bst(root):
    def dfs(n,lo,hi):
        if not n: return True
        return lo<n.val<hi and dfs(n.left,lo,n.val) and dfs(n.right,n.val,hi)
    return dfs(root,float('-inf'),float('inf'))
def kth_smallest(root,k):
    st=[]; node=root
    while True:
        while node: st.append(node); node=node.left
        node=st.pop(); k-=1
        if k==0: return node.val
        node=node.right

# HEAPS / BACKTRACKING / TRIE
def find_kth_largest(nums,k): return heapq.nlargest(k,nums)[-1]
def least_interval(tasks,n):
    heap=[-x for x in Counter(tasks).values()]; heapq.heapify(heap); wait=deque(); time=0
    while heap or wait:
        time+=1
        if heap:
            x=heapq.heappop(heap)+1
            if x: wait.append((time+n,x))
        if wait and wait[0][0]==time: heapq.heappush(heap,wait.popleft()[1])
    return time
def subsets(nums):
    out=[[]]
    for x in nums: out += [v+[x] for v in out]
    return out
def combination_sum(candidates,target):
    candidates=sorted(candidates); out=[]
    def dfs(i,left,path):
        if left==0: out.append(path); return
        for j in range(i,len(candidates)):
            x=candidates[j]
            if x>left: break
            dfs(j,left-x,path+[x])
    dfs(0,target,[]); return out
def permute(nums):
    out=[]; path=[]; used=[False]*len(nums)
    def dfs():
        if len(path)==len(nums): out.append(path[:]); return
        for i,x in enumerate(nums):
            if not used[i]:
                used[i]=True; path.append(x); dfs(); path.pop(); used[i]=False
    dfs(); return out
class TrieNode:
    def __init__(self): self.children={}; self.word=False
class Trie:
    def __init__(self): self.root=TrieNode()
    def insert(self,w):
        n=self.root
        for c in w: n=n.children.setdefault(c,TrieNode())
        n.word=True
    def search(self,w):
        n=self._walk(w); return bool(n and n.word)
    def starts_with(self,p): return self._walk(p) is not None
    def _walk(self,s):
        n=self.root
        for c in s:
            if c not in n.children: return None
            n=n.children[c]
        return n

# GRAPHS
def num_islands(grid):
    if not grid: return 0
    R,C=len(grid),len(grid[0]); seen=set(); count=0
    for r in range(R):
        for c in range(C):
            if grid[r][c]!='1' or (r,c) in seen: continue
            count+=1; stack=[(r,c)]; seen.add((r,c))
            while stack:
                x,y=stack.pop()
                for a,b in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                    if 0<=a<R and 0<=b<C and grid[a][b]=='1' and (a,b) not in seen:
                        seen.add((a,b)); stack.append((a,b))
    return count
def can_finish(n,prerequisites):
    g=[[] for _ in range(n)]; indeg=[0]*n
    for a,b in prerequisites: g[b].append(a); indeg[a]+=1
    q=deque(i for i,x in enumerate(indeg) if x==0); done=0
    while q:
        x=q.popleft(); done+=1
        for y in g[x]:
            indeg[y]-=1
            if indeg[y]==0: q.append(y)
    return done==n
def oranges_rotting(grid):
    R,C=len(grid),len(grid[0]); q=deque(); fresh=0
    for r in range(R):
        for c in range(C):
            if grid[r][c]==2: q.append((r,c,0))
            elif grid[r][c]==1: fresh+=1
    minutes=0
    while q:
        r,c,t=q.popleft(); minutes=max(minutes,t)
        for a,b in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
            if 0<=a<R and 0<=b<C and grid[a][b]==1:
                grid[a][b]=2; fresh-=1; q.append((a,b,t+1))
    return minutes if fresh==0 else -1
def clone_graph(node):
    if not node: return None
    class Node:
        def __init__(self,val): self.val=val; self.neighbors=[]
    clones={node:Node(node.val)}; q=deque([node])
    while q:
        x=q.popleft()
        for y in x.neighbors:
            if y not in clones: clones[y]=Node(y.val); q.append(y)
            clones[x].neighbors.append(clones[y])
    return clones[node]

# DYNAMIC PROGRAMMING / GREEDY / INTERVALS / BIT / MISC
def climb_stairs(n):
    a=b=1
    for _ in range(n-1): a,b=a+b,a
    return a
def rob(nums):
    prev=curr=0
    for x in nums: prev,curr=curr,max(curr,prev+x)
    return curr
def coin_change(coins,amount):
    dp=[0]+[amount+1]*amount
    for x in range(1,amount+1):
        for c in coins:
            if c<=x: dp[x]=min(dp[x],dp[x-c]+1)
    return -1 if dp[amount]>amount else dp[amount]
def length_of_lis(nums):
    tails=[]
    for x in nums:
        i=bisect_left(tails,x)
        if i==len(tails): tails.append(x)
        else: tails[i]=x
    return len(tails)
def unique_paths(m,n):
    dp=[1]*n
    for _ in range(1,m):
        for j in range(1,n): dp[j]+=dp[j-1]
    return dp[-1]
def can_jump(nums):
    reach=0
    for i,x in enumerate(nums):
        if i>reach: return False
        reach=max(reach,i+x)
    return True
def can_complete_circuit(gas,cost):
    if sum(gas)<sum(cost): return -1
    start=tank=0
    for i,(g,c) in enumerate(zip(gas,cost)):
        tank+=g-c
        if tank<0: start=i+1; tank=0
    return start
def merge_intervals(intervals):
    out=[]
    for s,e in sorted(intervals):
        if out and s<=out[-1][1]: out[-1][1]=max(out[-1][1],e)
        else: out.append([s,e])
    return out
def insert_interval(intervals,new):
    out=[]; i=0; s,e=new
    while i<len(intervals) and intervals[i][1]<s: out.append(intervals[i]); i+=1
    while i<len(intervals) and intervals[i][0]<=e:
        s=min(s,intervals[i][0]); e=max(e,intervals[i][1]); i+=1
    return out+[[s,e]]+intervals[i:]
def single_number(nums):
    x=0
    for n in nums: x^=n
    return x
def count_bits(n):
    dp=[0]*(n+1)
    for x in range(1,n+1): dp[x]=dp[x>>1]+(x&1)
    return dp
def rotate_image(matrix):
    n=len(matrix)
    for i in range(n):
        for j in range(i+1,n): matrix[i][j],matrix[j][i]=matrix[j][i],matrix[i][j]
    for row in matrix: row.reverse()
def lru_cache_class():
    class LRUCache:
        def __init__(self,capacity): self.capacity=capacity; self.data=OrderedDict()
        def get(self,key):
            if key not in self.data: return -1
            self.data.move_to_end(key); return self.data[key]
        def put(self,key,value):
            self.data[key]=value; self.data.move_to_end(key)
            if len(self.data)>self.capacity: self.data.popitem(last=False)
    return LRUCache
