# HONOR-CODE

+ 对于MCTS算法的理解，参考了[UCT算法介绍和模板](https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/)，同时也参考了[MCTS的维基百科](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)，代码的框架借鉴了模板，但是后面函数的具体实现基本上已经脱离了模板的相关内容，经过了多代的迭代和debug.

+ 之后由于发现单纯MCTS由于时间限制，开局效果并不理想，于是参考了并添加了[权重函数](https://zhuanlan.zhihu.com/p/35121997)的相关内容，对Monte Carlo进行了方向上的优化