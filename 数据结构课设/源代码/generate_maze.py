import random
import os
import tkinter as tk
import draw_maze as dm
import solve_maze as sm

def print_maze(maze):
    print()
    for row in maze:
        for cell in row:
            if str(cell) == '1':
                print(" \033[5;36m1\033[0m",end=" ")
            elif str(cell) == '*':
                print(" *",end=" ")
            elif str(cell) == '?':
                print(" ?",end=" ")
            else:
                print(" 0",end=" ")
        print()


def create_maze(m,n):
    
    if m != n:
        return
    maze=[[1 for _ in range(n)]for _ in range(m)]
    print_maze(maze)
    X=list()
    Y=list()
    X.append(2)
    Y.append(2)
    while len(X)>0:
        r=random.randint(0,len(X))%len(X)
        x=X[r]
        y=Y[r]
        count=0
        for i in range(x-1,x+2):
            for k in range(y-1,y+2):
                if 0 <= i < m and 0 <= k < n:
                    if  abs(x-i)+abs(y-k)==1 and maze[i][k]==0:
                        count+=0.5
        if count<=0.5:
            maze[x][y]=0
            #print(f"x,y:({x},{y})")
            for i in range(x-1,x+2):
                for j in range(y-1,y+2):
                    if 0 <= i < m and 0 <= j < n:
                        if  abs(x-i)+abs(y-j)==1 and maze[i][j]==1:
                            
                            X.append(i)
                            Y.append(j)                 
                            #print(f"count<=1:({i},{j})")
                            
            #print("\n\n")
        del X[r]
        del Y[r]       
    maze[1][1]='*'
    maze[m-2][n-2]='?'
    
    # 设置四周为墙壁
    for i in range(m):
        maze[i][0] = 1
        maze[i][n - 1] = 1
    for j in range(n):
        maze[0][j] = 1
        maze[m - 1][j] = 1
    
    
    return maze
def generate_maze(m,n):
    if m%2 == 0:
        m += 1
    if n%2 == 0:
        n += 1
    maze = [[1 for _ in range(n)]for _ in range(m)]
    print_maze(maze)

    direction = [(0,1),(1,0),(0,-1),(-1,0)]
    
    
    def carve_passages(x,y):
        #print(f"挖掘的坐标({x},{y})")
        random.shuffle(direction)
        for dx,dy in direction:
            nx,ny = x + dx*2, y + dy*2
            #print(f"({dx},{dy})")
            #print(f"挖掘的坐标({nx},{ny})\n")
            if 0 <= nx < m and 0 <= ny < n and maze[nx][ny] == 1:
                maze[nx][ny] = 0
                maze[x + dx][y + dy] = 0
                #print(f"\033[3;32m通({x+dx},{y+dy})\033[0m\n\n")
                carve_passages(nx,ny)
                
                if random.random() < 0.2 and 0 <= nx < m and 0 <= ny < n:
                    maze[x + dx][y + dy] = 0
    maze[1][1] = "*"
    carve_passages(1,1)
    maze[m-2][n-2] = "?"
    return maze

def save_maze_to_file(maze,filename):
    with open(filename,'w') as f:
        for row in maze:
            f.write(" ".join(str(cell) for cell in row) + "\n")
