import time
import tkinter as tk

def close_window(root):
    print("返回到控制台！！\n\n")
    root.destroy()

def read_maze(file_path):
    char_map = {
        '*':0,
        '?':0
    }
    maze = []
    with open(file_path,'r') as f:
        for line in f:
            row = []
            for item in line.strip().split():
                if item in char_map:
                    row.append(char_map[item])
                else:
                    row.append(int(item))
            maze.append(row)
    return maze

def draw_to_maze(maze,start=None,end=None,path=None):
    root = tk.Tk()
    root.title("迷宫图形")

    cell_size = 15
    canvas_width = len(maze[0])*cell_size
    canvas_height = len(maze) * cell_size
    canvas = tk.Canvas(root,width=canvas_width,height=canvas_height)
    canvas.pack()

    for i,row in enumerate(maze):
        for j, cell in enumerate(row):
            color = "black" if cell == 1 else "white"
            canvas.create_rectangle(
                j*cell_size,i*cell_size,
                (j+1)*cell_size,(i+1)*cell_size,
                fill=color,outline="gray"
            )
    
    # 绘制起点标识
    if start:
        sx,sy = start
        canvas.create_oval(
            sy*cell_size + 2,sx*cell_size + 2,
            (sy+1)*cell_size - 2,(sx+1)*cell_size - 2,
            fill="green",outline="gray"
        )

    # 绘制终点标识
    if end:
        ex,ey = end
        canvas.create_oval(
            ey*cell_size + 2,ex*cell_size + 2,
            (ey+1)*cell_size - 2,(ex+1)*cell_size - 2,
            fill="red",outline="gray"
        )

    # 绘制路径标识

    if path:
        for (x,y) in path:
            canvas.create_rectangle(
                y*cell_size + 2,x*cell_size + 2,
                (y+1)*cell_size - 2,(x+1)*cell_size - 2,
                fill="blue",outline="gray"
            )
    
    root.protocol("WM_DELETE_WINDOW",lambda:close_window(root))

    root.mainloop()


class MazeGame:
    def __init__(self,maze,start,end):
        self.maze = maze
        self.start = start
        self.end = end
        self.player_pos = list(start) # 将起点转换为列表
        self.root = tk.Tk()
        self.root.title("迷宫游戏")

        self.cell_size = 15
        self.move_down_size = 30
        self.canvas_width = len(maze[0])*self.cell_size
        self.canvas_height = len(maze)*self.cell_size+self.move_down_size
        self.canvas = tk.Canvas(self.root,width=self.canvas_width,height=self.canvas_height)
        self.canvas.pack()

        self.draw_game_maze()
        # 绘制玩家方块
        self.player = self.canvas.create_rectangle(
            self.player_pos[1]*self.cell_size,self.player_pos[0]*self.cell_size + self.move_down_size,
            (self.player_pos[1]+1)*self.cell_size,(self.player_pos[0]+1)*self.cell_size + self.move_down_size,
            fill="blue",outline="black"
       )

        # 绑定键盘事件
        print("绑定键盘事件...")
        self.root.bind("<KeyPress>",self.move_player)

    	# 初始化游戏时长
        self.start_time = time.time()  # 记录游戏开始时间
        self.time_label = tk.Label(self.root, text="游戏时长: 0s", font=("Arial", 14), anchor="ne")
        self.time_label.place(x=0, y=5)  # 将标签放置在右上角
        
        self.after_id=None
        # 更新时长显示
        self.update_time()

    def draw_game_maze(self):
        if not hasattr(self,'canvas') or self.canvas is None:
            print("Canvas 未正确初始化！")
            return
        
        # 清空画布
        self.canvas.delete("all")
        for i,row in enumerate(self.maze):
            for j,cell in enumerate(row):
                color = "black" if cell == 1 else "white"
                self.canvas.create_rectangle(
                    j * self.cell_size,i * self.cell_size+self.move_down_size,
                    (j+1)*self.cell_size,(i+1)*self.cell_size+self.move_down_size,
                    fill=color,outline="gray"
                )
        sx,sy = self.start
        ex,ey = self.end
        
        self.canvas.create_oval(
            sy*self.cell_size + 2,sx*self.cell_size + 2 + self.move_down_size,
            (sy+1)*self.cell_size - 2,(sx+1)*self.cell_size - 2 + self.move_down_size,
            fill="green",outline="gray"
        )
        
        self.canvas.create_oval(
            ey*self.cell_size + 2,ex*self.cell_size + 2 + self.move_down_size,
            (ey+1)*self.cell_size - 2,(ex+1)*self.cell_size - 2 + self.move_down_size,
            fill="red",outline="gray"
        )
        
    def move_player(self,event):
        print(f"Key pressed:{event.keysym}")
        direction = {
            'UP':(-1,0),
            'DOWN':(1,0),
            'LEFT':(0,-1),
            'RIGHT':(0,1)
        }.get(event.keysym.upper())
        if direction:
            new_x = self.player_pos[0]+direction[0]
            new_y = self.player_pos[1]+direction[1]

            if 0<= new_x <len(self.maze) and 0<= new_y <len(self.maze[0]) and self.maze[new_x][new_y] == 0:
                self.player_pos = [new_x,new_y]
                self.canvas.coords(self.player,
                    self.player_pos[1]*self.cell_size,self.player_pos[0]*self.cell_size + self.move_down_size,
                    (self.player_pos[1]+1)*self.cell_size,(self.player_pos[0]+1)*self.cell_size + self.move_down_size
                )

                if self.player_pos[0] == self.end[0] and self.player_pos[1] == self.end[1]:
                    print("到达终点！！！")
                    self.root.destroy()

    def update_time(self):

        if self.root.winfo_exists():
            # 计算经过的时间
            elapsed_time = int(time.time() - self.start_time)

            # 更新标签显示
            self.time_label.config(text=f"游戏时长: {elapsed_time}s")

            # 每1000ms（1秒）更新一次
            self.after_id = self.root.after(1000, self.update_time)

    def close_game_window(self):
        print("返回控制台！！！\n\n")
        if self.after_id:
            try:
                self.root.after_cancel(self.after_id)  # 取消所有排队的回调
            except Exception as e:
                pass
        self.root.destroy()    
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.close_game_window())
        self.root.focus_set()# 获得焦点，可以在其他python中成功获取键盘信息
        print("进入事件循环...")
        self.root.mainloop()

