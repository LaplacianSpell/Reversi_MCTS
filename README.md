# 黑白棋游戏

## 背景

黑白棋（Reversi，又名翻转棋）是简单有趣的小游戏，其详细规则可见 [维基百科](https://zh.wikipedia.org/zh-cn/%E9%BB%91%E7%99%BD%E6%A3%8B)、[百度百科](https://baike.baidu.com/item/%E9%BB%91%E7%99%BD%E6%A3%8B/80689)。

## 平台

本次作业的评测完全在 [Saiblo 平台](https://www.saiblo.net/) 上进行.

## 算法

使用了基本的UCT算法 + 利用权重棋盘对playout减枝 + 在没有占角的时候，尽量不下星位与C位的策略

实际效果上个人感觉由于平台限制步时3s，模拟的效果并不太好，一步甚至不能模拟完一层，不过已经形成了对黑白棋的一定智能🥰🥰🥰.

最后，AI真挺有意思的，希望多学点Hacking Skills
