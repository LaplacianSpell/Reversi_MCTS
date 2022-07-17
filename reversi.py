#!/usr/bin/env python3

# DO NOT MODIFY THE CODE BELOW
import sys, os
from typing import List, Tuple

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["USE_SIMPLE_THREADED_LEVEL3"] = "1"
# DO NOT MODIFY THE CODE ABOVE


# add your own imports below
import time
from random import choice
import math
import copy

# define your helper functions here

def coord_to_index(x, y):
    '''
    将坐标 (x,y) 点转换为数组下标
    '''
    assert x >= 0 and x < 8 and y >= 0 and y < 8
    return (x << 3) + y 

def index_to_coord(i: int) -> Tuple[int, int]:
    '''
    将数组下标转换为坐标
    '''
    assert i >= 0 and i < 64
    return i >> 3, i & 7

# class for restoration of board and do simulation.
class MCTS(object):
    '''
    实现复盘功能，辅助模拟：
    1. 给定当前棋盘数组，返回当前落子玩家
    2. 给定当前棋盘数组与落子位置，返回新的棋盘数组
    3. 给定当前棋盘数组，返回允许落子的位置下标的数组
    4. 给定当前棋盘数组，返回对棋盘胜负的判断
    
    0. 需要实现模拟算法
    '''
    def __init__(self, player, board, allow):

        # 存储棋盘数组
        self.mctsBoard = board

        # 存储玩家 int 0 or 1
        self.mctsPlayer = player 

        # 存储允许落子的点 list
        self.mcstAllow = allow
        # 存储玩家走秒
        # 计算走秒时间
        self.calculationtime = 2 

        #节点信息
        # 字典，键是（玩家编号，当前节点代表的落子位置, 落子后棋盘），值是获胜次数
        self.wins = {} 
        # 字典，键是（玩家编号，当前节点代表的落子位置， 落子后棋盘），值是触摸当前节点次数
        self.plays = {} 

        # UCB1 评估函数的参数，可调节
        self.C = 1.4 

    def nextBoard(self, board, player, position):
        '''
        renew the board

        arguments: 
        - board (list)
        - player (int)
        - position (int)

        returns: board (list)
        '''
        board[position] = player
        againstPlayer = (player + 1) % 2
        # 检查八个方向是否有翻转
        # 落子位置：
        site = index_to_coord(position)

        # 标记：右上，右中，右下
        rightMark = [1, 1, 1]
        leftMark = [1, 1, 1]
        # 标记： 左上，左中，左下

        for x in range(site[0] + 1, 8):

            if rightMark[1]:
                if board[coord_to_index(x, site[1])] == againstPlayer:
                    pass
                elif board[coord_to_index(x, site[1])] == 2:
                    rightMark[1] = 0
                else:
                    for xagainst in range(x - 1, site[0], -1):
                        board[coord_to_index(xagainst, site[1])] = player

            if rightMark[0] and x - site[0] + site[1] < 8:
                if board[coord_to_index(x, x - site[0] + site[1])] == againstPlayer:
                    pass
                elif board[coord_to_index(x, x - site[0] + site[1])] == 2:
                    rightMark[0] = 0
                else:
                    for xagainst in range(x - 1, site[0], -1):
                        board[coord_to_index(xagainst, xagainst - site[0] + site[1])] = player

            if rightMark[2] and site[0] - x + site[1] >= 0:
                if board[coord_to_index(x, site[0] - x + site[1])] == againstPlayer:
                    pass
                elif board[coord_to_index(x, site[0] - x + site[1])] == 2:
                    rightMark[2] = 0
                else:
                    for xagainst in range(x - 1, site[0], -1):
                        board[coord_to_index(xagainst, site[0] - xagainst + site[1])] = player

            if sum(rightMark) == 0:
                break
        
        for x in range(site[0] - 1, -1, -1):

            if leftMark[1]:
                if board[coord_to_index(x, site[1])] == againstPlayer:
                    pass
                elif board[coord_to_index(x, site[1])] == 2:
                    leftMark[1] = 0
                else:
                    for xagainst in range(x + 1, site[0], 1):
                        board[coord_to_index(xagainst, site[1])] = player

            if leftMark[0] and site[0] - x + site[1] < 8:
                if board[coord_to_index(x, site[0] - x + site[1])] == againstPlayer:
                    pass
                elif board[coord_to_index(x, site[0] - x + site[1])] == 2:
                    leftMark[0] = 0
                else:
                    for xagainst in range(x + 1, site[0], 1):
                        board[coord_to_index(xagainst, - xagainst + site[0] + site[1])] = player

            if leftMark[2] and - site[0] + x + site[1] >= 0:
                if board[coord_to_index(x, - site[0] + x + site[1])] == againstPlayer:
                    pass
                elif board[coord_to_index(x, - site[0] + x + site[1])] == 2:
                    leftMark[2] = 0
                else:
                    for xagainst in range(x + 1, site[0], 1):
                        board[coord_to_index(xagainst, - site[0] + xagainst + site[1])] = player

            if sum(leftMark) == 0:
                break
        
        for y in range(site[1] + 1, 8):
            if board[coord_to_index(site[0], y)] == againstPlayer:
                pass
            elif board[coord_to_index(site[0], y)] == 2:
                break
            else:
                for yagainst in range(y - 1, site[1], -1):
                    board[coord_to_index(site[0], yagainst)] = player
    
        for y in range(site[1] - 1, -1, -1):
            if board[coord_to_index(site[0], y)] == againstPlayer:
                pass
            elif board[coord_to_index(site[0], y)] == 2:
                break
            else:
                for yagainst in range(y + 1, site[1], 1):
                    board[coord_to_index(site[0], yagainst)] = player

        return board    

    def legalPlay(self, board, player):
        '''
        tells where is legal to play

        arguments: 
        - board (list)
        - player (int)

        returns: allow (list)
        '''

        allow = ask_next_pos(board, player)
        return allow

    def winner(self, board):
        '''
        tells who wins the match or still continuing

        arguments:
        - board (tuple)

        return: winner (int)
        0 or 1
        '''
        user0 = 0
        user1 = 0
        noUser = 0
        for i in board:
            if i == 0:
                user0 += 1
            elif i == 1:
                user1 += 1
            else:
                noUser += 1
        
        # 双方都没有棋子可以下时棋局结束，以棋子数目来计算胜负
        # 棋子多的一方获胜。
        # 在棋盘还没有下满时，如果一方的棋子已经被对方吃光，则棋局也结束。
        # 将对手棋子吃光的一方获胜。
        ## 这里保留和棋手段
        if (not True in ask_next_pos(list(board), 0))  and (not True in ask_next_pos(list(board), 1)):
            if user1 > user0:
                return 1
            elif user1 < user0:
                return 0

        else: 
            return 2



    def getMove(self):
        '''
        the main realize of the game AI
        tells how to move next

        return: move (int)
        '''

        # 当前落子的玩家
        player = self.mctsPlayer 

        # 允许的落子地点
        legal = self.mcstAllow[:]

        # 如果所有的位置都不能落子，直接返回
        # if True not in legal:
        #     return

        # 如果只有一个位置可以落子，那么只能下那个位置
        if legal.count(True) == 1:
            return legal.index(True)

        # 如果有多个可能的位置，在允许的时间里一直进行模拟
        begin = time.perf_counter()
        while time.perf_counter() - begin < self.calculationtime:
            self.simulation()

        # 寻找当前的所有允许的落子位置
        possibleMove = [(i, tuple(self.nextBoard(self.mctsBoard[:], player, i))) 
        for i, p in enumerate(legal) if p == True]

        # 计算所有允许落子位置的胜率最大值，并记录下对应的落子点
        winProbability, move = max (
            (self.wins.get((player, p, S), 0) / self.plays.get((player, p, S), 1), p) 
            if (self.plays.get((player, p, S), 1), p) == 0 else (1, p)
            for p, S in possibleMove
        )

        return move

    def simulation(self):
        '''
        the core of AI, where the decisions are made
        '''

        # 拷贝一份树到函数里面
        plays, wins = copy.deepcopy(self.plays), copy.deepcopy(self.wins)

        # 取当前玩家
        player = self.mctsPlayer

        # 取当前棋盘
        state = tuple(self.mctsBoard)

        # 下面是函数内的辅助数据
        # 一个set，装从当前状况（根节点）开始，拜访过的节点
        # 也就是所谓**主路径**，相当于一个cache
        # 之后在树里面信息，需要根据他更新，不在的直接跳过
        visitedStates = set()

        # Playouts 实现
        # 合法落子
        ## TODO simplify
        allow = self.mcstAllow[:]
        
        move = -1

        # possibleMove装的是 [(合法落子的下标， 落子后的棋盘[i.e.: state]),...]
        # 当前节点的子节点
        possibleMove = [(i, tuple(self.nextBoard(list(state), player, i))) 
        for i, p in enumerate(allow[:]) if p == True]

        
        # 此时执行第一步,即使用UCB1算法
        # 看看有没有到叶子节点（没有子节点的节点）
        ## 如果是空的，返回？
        while None not in [plays.get((player, p, B)) for p, B in possibleMove]:
            # 子节点中是否有plays为0的，如果有，她的UCB1为Inf，进入特定子节点
            if 0 in [plays.get((player, p, B)) for p, B in possibleMove]:
                move, state = choice([(p, B) \
                for p, B in possibleMove if plays[(player, p, B)] == 0])
                


            # 如果所有的plays值都不为0，计算评估函数,并取最大的评估函数
            else:
                logTotal = math.log(
                float(sum(plays[(player, p, B)] for p, B in possibleMove)))

                value, move, state = max(
                    ((float(wins[(player, p, B)]) / float(plays[(player, p, B)])) +
                    self.C * math.sqrt(float(logTotal) / float(plays[(player, p, B)])), p, B)
                    for p, B in possibleMove
                    )

            # 并且将状态装入cache
            visitedStates.add((player, move, state))

            # 更新玩家编号, 
            player = (player + 1) % 2

            # 获取下一个玩家可能的落子点
            allow = self.legalPlay(list(state), player)

            possibleMove = [(i, tuple(self.nextBoard(list(state), player, i))) 
            for i, p in enumerate(allow[:]) if p == True]

        
        # 0值叶子
        # 此时，直接Monte Carlo到底
        # 先还原回来
        player = (player + 1) % 2
        if plays.get((player, move, state), -1) == 0:
            while True:

                # 是否获胜（退出循环的判断标准）
                winner = self.winner(state)
                # 如果Monte Carlo结束，直接退出并进入算法第四步
                if winner == 0 or winner == 1:
                    break

                # 如果没有获胜，则更新玩家编号, 
                # 并且将下一个状态装入cache
                player = (player + 1) % 2

                # 获取下一个玩家可能的落子点
                allow = self.legalPlay(list(state), player)

                possibleMove = [(i, tuple(self.nextBoard(list(state), player, i))) 
                for i, p in enumerate(allow[:]) if p == True]

                if len(possibleMove) > 0:
                    move, state = choice(possibleMove)
                    visitedStates.add((player, move, state))
            
            # 这一步是UCT算法的第四步：反向传播
            for player, move, state in visitedStates:

                # 只有已经记录在plays中的节点才更新
                if (player, move, state) not in self.plays: 
                    continue

                # 如果在plays中，则玩过的局+1
                self.plays[(player, move, state)] += 1 

                # 如果当前节点所代表的玩家获胜，则获胜数也+1
                if player == winner:
                    self.wins[(player, move, state)] += 1

        # 非0值叶子，扩张
        else:

            allow = self.legalPlay(list(state), player)
            for i in \
            [((player + 1) % 2, index, tuple(self.nextBoard(list(state), player, index))) 
            for index, p in enumerate(allow) if p]:
                self.wins[i] = 0
                self.plays[i] = 0

            possibleMove = [(i, tuple(self.nextBoard(list(state), player, i))) 
            for i, p in enumerate(allow) if p == True]

            possibleMove = [(p, B) for p, B in possibleMove if plays.get((player, p, B)) == 0]
            if len(possibleMove) > 0:
               move, state = choice(possibleMove)

            # 接着进行Monte Carlo
            while(True):

                # 是否获胜（退出循环的判断标准）
                winner = self.winner(state)
                # 如果Monte Carlo结束，直接退出并进入算法第四步
                if winner == 0 or winner == 1:
                    break

                # 如果没有获胜，则更新玩家编号, 
                # 并且将下一个状态装入cache
                player = (player + 1) % 2

                # 获取下一个玩家可能的落子点
                allow = self.legalPlay(list(state), player)
                possibleMove = [(i, tuple(self.nextBoard(list(state), player, i))) 
                for i, p in enumerate(allow) if p == True]
                if len(possibleMove) > 0:
                    move, state = choice(possibleMove)
                    visitedStates.add((player, move, state))

            # 这一步是UCT算法的第四步：反向传播
            for player, move, state in visitedStates:

                # 只有已经记录在plays中的节点才更新
                if (player, move, state) not in self.plays: 
                    continue

                # 如果在plays中，则玩过的局+1
                self.plays[(player, move, state)] += 1 

                # 如果当前节点所代表的玩家获胜，则获胜数也+1
                if player == winner:
                    self.wins[(player, move, state)] += 1

        # 临时set记录一次模拟的所有节点键，**包括之后模拟的落子信息**



# modify reversi_ai function to implement your algorithm

def reversi_ai(player: int, board: List[int], allow: List[bool]) -> Tuple[int, int]:
    '''
    AI 用户逻辑
    参数：player: 当前玩家编号（0 或者 1）
         board:  当前棋盘，长度为 64，0 表示 player0 的子, 1 表示 player1 的子, 2 表示没有落子
         allow:  棋盘允许下子情况，长度为 64，这里面已经指明了可以选的坐标

    return: 落子坐标元组
    '''
    MyBoard = MCTS(player, board[:], allow[:])


    # 初始化搜索树
    if board.count(0) + board.count(1) == 4 or board.count(0) + board.count(1) == 5:
        # 初始化根节点
        MyBoard.wins[((player + 1) % 2,  -1, tuple(board))] = 0
        MyBoard.plays[((player + 1) % 2,  -1, tuple(board))] = 0

        # 初始化根节点之后可能落子的节点
        for t in \
        [(player, i, tuple(MyBoard.nextBoard(board, player, i))) 
        for i, p in enumerate(allow[:]) if p == True]:
            MyBoard.wins[t] = 0
            MyBoard.plays[t] = 0

    return index_to_coord(MyBoard.getMove())

# DO NOT MODIFY ANY CODE BELOW
# **不要修改**以下的代码

def ask_next_pos(board, player):
    '''
    返回player在当前board下的可落子点
    '''
    ask_message = ['#', str(player)]
    for i in board:
        ask_message.append(str(i))
    ask_message.append('#')
    sys.stdout.buffer.write(ai_convert_byte("".join(ask_message)))
    sys.stdout.flush()
    data = sys.stdin.buffer.read(64)
    str_list = list(data.decode())
    return [int(i) == 1 for i in str_list]


def ai_convert_byte(data_str):
    '''
    传输数据的时候加数据长度作为数据头
    '''
    message_len = len(data_str)
    message = message_len.to_bytes(4, byteorder='big', signed=True)
    message += bytes(data_str, encoding="utf8")
    return message

def send_opt(data_str):
    '''
    发送自己的操作
    '''
    sys.stdout.buffer.write(ai_convert_byte(data_str))
    sys.stdout.flush()


def start():
    '''
    循环入口
    '''
    read_buffer = sys.stdin.buffer
    while True:
        data = read_buffer.read(67)
        now_player = int(data.decode()[1])
        str_list = list(data.decode()[2:-1])
        board_list = [int(i) for i in str_list]
        next_list = ask_next_pos(board_list, now_player)
        x, y = reversi_ai(now_player, board_list, next_list)
        send_opt(str(x)+str(y))

if __name__ == '__main__':
    start()
