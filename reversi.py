#!/usr/bin/env python3

# DO NOT MODIFY THE CODE BELOW
import sys, os
from typing import List, Tuple

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["USE_SIMPLE_THREADED_LEVEL3"] = "1"
# DO NOT MODIFY THE CODE ABOVE


# add your own imports below
import datetime
from random import choice
import math
import numpy as np

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
    需要实现复盘功能，辅助模拟：
    1. 给定当前棋盘数组，返回当前落子玩家
    2. 给定当前棋盘数组与落子位置，返回新的棋盘数组
    3. 给定当前棋盘数组，返回允许落子的位置下标的数组
    4. 给定当前棋盘数组，返回对棋盘胜负的判断
    
    0. 需要实现模拟算法
    '''
    def __init__(self, player, board, allow):

        # 存储棋盘数组 numpy
        self.mctsBoard = np.array(board) 

        # 存储玩家 int 0 or 1
        self.mctsPlayer = player 

        # 存储允许落子的点 list
        self.mcstAllow = np.array(list) 

        # 存储状态树(记录每次落子的位置 int，也就是游戏过程)
        self.states = [] 

        # 存储玩家走秒
        # 计算走秒时间
        self.seconds = 180 
        self.calculation_time = 18 

        #节点信息
        # 字典，键是（玩家编号，当前节点代表的落子位置），值是获胜次数
        self.wins = {} 
        # 字典，键是（玩家编号，当前节点代表的落子位置），值是触摸当前节点次数
        self.plays = {} 

        # UCB1 评估函数的参数，可调节
        self.C = 1.4 

    # def currentPlayer(self, board): # 似乎可以用一个标记变量实现
    #     '''
    #     arguments: board (numpy array)

    #     returns: the player (0 or 1)
    #     '''

    def nextBoard(self, board, player, position):
        '''
        renew the board

        arguments: 
        - board (numpy array)
        - player (int)
        - position (int)

        returns: board (numpy array)
        '''
        board[position] = player
        return board    

    def legalPlay(self, board, player):
        '''
        arguments: 
        - board (numpy array)
        - player (int)

        returns: allow (numpy array)
        '''
        ######
        allow = np.zeros(64)
        return allow

    def winner(self, board):
        '''
        arguments:
        - board

        return: winner (int)
        '''
        ######
        return 1
    
    def getMove(self):
        '''
        the main realize of the game AI

        return: move (int)
        '''

        # 落子记录的副本，避免直接修改
        states = self.states[-1] 

        # 当前落子的玩家
        player = self.mctsPlayer 

        # 允许的落子地点
        legal = self.mcstAllow 

        # 如果所有的位置都不能落子，直接返回
        if not all(legal):
            return

        # 如果只有一个位置可以落子，那么只能下那个位置
        if legal.count(True) == 1:
            return legal.index(True)

        # 如果有多个可能的位置，在允许的时间里一直进行模拟
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()

        # 寻找当前的所有允许的落子位置
        possibleMove = [(i, self.nextBoard(self.board, player, p)) for i, p in enumerate(legal) if p == True]

        # 计算所有允许落子位置的胜率最大值，并记录
        winPossibility, move = max(
            (
            self.wins.get((player, S), 0) /
            self.plays.get((player, S), 1),
            p
            )
            for p, S in possibleMove 
        )

        return move


# modify reversi_ai function to implement your algorithm

def reversi_ai(player: int, board: List[int], allow: List[bool]) -> Tuple[int, int]:
    '''
    AI 用户逻辑
    参数：player: 当前玩家编号（0 或者 1）
         board:  当前棋盘，长度为 64，0 表示 player0 的子, 1 表示 player1 的子, 2 表示没有落子
         allow:  棋盘允许下子情况，长度为 64，这里面已经指明了可以选的坐标

    return: 落子坐标元组
    '''
    MyBoard = MCTS(player, board, allow)
    return MyBoard.getMove()

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
