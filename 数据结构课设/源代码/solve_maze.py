import time
from collections import deque
import draw_maze as dm

class Stack:
    def __init__(self):
        self.items = []

    def push(self,item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


# 使用自己实现的栈求解(DFS)
def stack_rule(maze,start,end):
    # 栈求解
    stack=Stack()
    stack.push(start)
    
    # 移动的方向
    directions=[(1,0),(0,1),(-1,0),(0,-1)]

    # 位置是否被访问
    visted=[[False]*len(maze[0]) for _ in range(len(maze))]

    visted[start[0]][start[1]]=True

    # 存储路径
    path=[]

    while not stack.is_empty():
        current=stack.peek()
        # 不覆盖起点和终点的图形

        if current != start and current != end:
            path.append(current)

        if current == end:
            return path
        

        found=False
        for direction in directions:
            x,y = current[0]+direction[0],current[1]+direction[1]
            if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0 and visted[x][y] != True:
                stack.push((x,y))
                #print(f"已找到的路径({x},{y})")
                visted[x][y]=True
                found=True
                break

        # 回溯
        if not found:
            stack.pop()
            if path:
                path.pop()
        
    return None

# BFS 求解
def bfs(maze,start,end):
    # 使用deque双端队列：左右两边同时可以进行入队和出队
    queue=deque([start])
    parent={start:None}
    # 四个方向
    directions = {(1,0),(0,1),(-1,0),(0,-1)}
    
    path=[]

    while queue:
        # 广度，每次探索都使用已探索的位置返回给current
        current = queue.popleft()


        if current == end:
            while current:
            # 不覆盖起点和终点的图形
                if current != start and current != end:
                    path.append(current)
                current = parent[current]
            # -1 反转队列从最后开始打印
            return path[::-1]

        for direction in directions:
            nx,ny = current[0]+direction[0],current[1]+direction[1]
            if 0<= nx <len(maze) and 0<= ny <len(maze[0]) and maze[nx][ny] == 0 and (nx,ny) not in parent:
                parent[(nx,ny)]=current
                queue.append((nx,ny))

    return None 

# DFS 求解
def dfs(maze,start,end):
    # deque双端队列，但使用过程但只是使用了它的 pop() 方法来从队尾弹出元素，并使用 append() 方法来向队尾添加元素，当做栈使用。
    stack=deque([start])
    parent={start:None}
    # 方向
    directions = {(1,0),(0,1),(-1,0),(0,-1)}

    path=[]

    while stack:
        # 深度，每次探索返回最深的返回给current
        current = stack.pop()
        

        if current == end:
            while current:
                if current != start and current != end:
                    path.append(current)
                current = parent[current]
            return path[::-1]

        for direction in directions:
            nx,ny = current[0]+direction[0],current[1]+direction[1]
            if 0<= nx <len(maze) and 0<= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx,ny) not in parent:
                parent[(nx,ny)] = current
                stack.append((nx,ny))

    return None

# A* 求解
def heuristic(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def a_start(maze,start,end):
    # 存储待访问的节点位置
    open_set={start}
    # 起点到当前节点的代价
    g_score={start:0}
    # 估算当前节点的总代价
    f_score={start:heuristic(start,end)}
    parent = {start:None}
    directions = [(1,0),(0,1),(-1,0),(0,-1)]

    path=[]

    while open_set:
        # 估算当前节点的总代价，取估算的最小代价的位置
        current=min(open_set,key=lambda x:f_score[x])
        
        if current == end:
            while current:
                if current != start and current != end:
                    path.append(current)
                current = parent[current]
            return path[::-1]
        # 移除估算完的节点
        open_set.remove(current)

        for direction in directions:
            nx,ny = current[0]+direction[0],current[1]+direction[1]
            if 0<= nx <len(maze) and 0<= ny <len(maze[0]) and maze[nx][ny] == 0:
                tentative_g_score = g_score[current] + 1
                if (nx,ny) not in g_score or tentative_g_score < g_score[(nx,ny)]:
                    parent[(nx,ny)]=current
                    g_score[(nx,ny)]=tentative_g_score
                    f_score[(nx,ny)]=g_score[(nx,ny)]+heuristic((nx,ny),end)
                    open_set.add((nx,ny))

    return None



# 右手求解
def right_hand_rule(maze,start,end):
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    current_direction = 0 # 0 右 1 下 2 左 3 上
    current = start
    path=[]
    # 记录已经访问的节点
    visted = set([start])

    while current != end:
        for i in range(4):
            current_direction = (current_direction + 1)%4
            direction = directions[current_direction]
            nx,ny = current[0]+direction[0],current[1]+direction[1]
            if 0<= nx <len(maze) and 0<= ny <len(maze[0]) and maze[nx][ny]==0 and (nx,ny) not in visted:
                visted.add((nx,ny))
                current = (nx,ny)
                if current != start and current != end:
                    path.append(current)
                break
        else:
            current = (current[0]-directions[(current_direction+2)%4][0],current[1]-directions[(current_direction+2)%4][1])
            if current != start and current != end:
                path.append(current)
               
    return path


# 打印路径
def print_path(path):
    result = []
    for (x,y) in path:
        col = chr(y + 64)
        row = x
        result.append(f"{col}{row}")
    return result

# 求解选择
def solve_maze(maze):
    start=(1,1)
    end=(len(maze)-2,len(maze[0])-2)

    algorithms = [
        ("栈求解",stack_rule),
        ("BFS求解)",bfs),
        ("DFS求解",dfs),
        ("A*求解",a_start),
        ("右手求解",right_hand_rule)
    ]
    
    print("1.栈求解\t2.BFS求解\n3.DFS求解\t4.A*求解\n5.右手求解")
    is_solve = int(input())

    if is_solve == 1:
        name = algorithms[is_solve-1][0]
        algorithm = algorithms[is_solve-1][1]
    elif is_solve == 2:
        name = algorithms[is_solve-1][0]
        algorithm = algorithms[is_solve-1][1]

    elif is_solve == 3:
        name = algorithms[is_solve-1][0]
        algorithm = algorithms[is_solve-1][1]

    elif is_solve == 4:
        name = algorithms[is_solve-1][0]
        algorithm = algorithms[is_solve-1][1]

    elif is_solve == 5:
        name = algorithms[is_solve-1][0]
        algorithm = algorithms[is_solve-1][1]
    else:
        print("没有此算法！！")

    start_time = time.time()
    path = algorithm(maze,start,end)
    end_time = time.time()

    if path:
        print(f"{name}路径：")
        print(print_path(path))
        print(f"{name}时间：{end_time - start_time:.6f}秒")
    else:
        print("没有找到路径！！")


    print()
    

    file_name = "generate_maze.txt"
    maze_data = dm.read_maze(file_name)
    dm.draw_to_maze(maze_data,start,end,path)

