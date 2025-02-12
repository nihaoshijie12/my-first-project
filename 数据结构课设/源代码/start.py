import os
import generate_maze as gm
import draw_maze as dm
import solve_maze as sm

def create_to_maze():
    print("请选择生成迷宫的算法(prim有难度哦！！)\n1.dfs\t2.prim(prim算法行和列需要一致):")
    collect = int(input())
    if collect == 1:
        user_input = input("请输入迷宫的行、列（空格隔开）：")
        numbers = list(map(int,user_input.split()))
        end = (numbers[0]-1,numbers[1]-1)
        maze = gm.generate_maze(numbers[0],numbers[1])
    elif collect == 2:
        user_input = input("请输入迷宫的行、列（空格隔开）：")
        numbers = list(map(int,user_input.split()))
        end = (numbers[0]-2,numbers[1]-2)
        maze = gm.create_maze(numbers[0],numbers[1])
    else:
        print("没有此算法！！")
    gm.print_maze(maze)
    print()

    file_name = "generate_maze.txt"
    file_path = os.path.abspath(file_name)
    gm.save_maze_to_file(maze,file_name)
    print(f"生成成功！！！\n\nPATH:{file_name}\n")
    return end

if __name__ == "__main__":
    file_name = "generate_maze.txt"
    is_exit = True
    
    p = "*"*6
    
    start = (1,1)
    end = create_to_maze()
    
    maze_data = dm.read_maze(file_name)

    while is_exit:
        print(f"{p}请选择需要使用的功能{p}\n\t1:重新生成迷宫\t2:绘制迷宫\n\t3:求解迷宫\t4:游戏形式\n\t5:退出：")

        collect = int(input())

        if collect == 1:
            end = create_to_maze()
        elif collect == 2:
            dm.draw_to_maze(maze_data,start,end)
        elif collect == 3:
            sm.solve_maze(maze_data)
        elif collect == 4:
            game = dm.MazeGame(maze_data,start,end)
            game.run()
        elif collect == 5:
            print("退出成功！！")
            is_exit = False
        else:
            print("没有此功能！！")
        if collect == 1:
            maze_data = dm.read_maze(file_name)
            
