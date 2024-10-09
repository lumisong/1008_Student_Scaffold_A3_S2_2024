# 测试

交流内容：开始。

## 文件结构

1008_STUDENT_SCAFFOLD_A3_S2_2024
│  .gitignore
│  betterbst.py
│  config.py
│  hollows.py
│  JetBrains.gitignore
│  maze.py
│  random_gen.py
│  readme.md
│  run_tests.py
│  treasure.py
│
├─.vscode
│      settings.json
│
├─algorithms
│      binary_search.py
│      mergesort.py
│      quicksort.py
│      __init__.py
│
├─data_structures
│      abstract_list.py
│      aset.py
│      bset.py
│      bst.py
│      hash_table.py
│      heap.py
│      linked_list.py
│      linked_queue.py
│      linked_stack.py
│      node.py
│      printer.py
│      queue_adt.py
│      referential_array.py
│      set_adt.py
│      stack_adt.py
│      __init__.py
│
├─ed_utils
│      decorators.py
│      __init__.py
│
├─mazes
│  │  positions_sample.txt
│  │  sample.txt
│  │  sample2.txt
│  │
│  └─task3
│      │  maze1.txt
│      │  maze2.txt
│      │  maze3.txt
│      │  maze4.txt
│      │  no_valid_exit.txt
│      │  visit_all.txt
│      │
│      └─treasures
│              maze1.txt
│              maze2.txt
│
└─tests
        test_clone.py
        test_task1.py
        test_task2.py
        test_task3.py
        __init__.py

## 文件解析

从你提供的文件结构可以看出，这个作业脚手架包含了与迷宫逃脱任务相关的多个模块和辅助文件。以下是对这些文件及其可能用途的分析：

### 根目录

- __`.gitignore`__: 用于Git版本控制，忽略某些不需要提交的文件。
- __`betterbst.py`__: 与任务1中的平衡二叉搜索树（BST）相关，需要你修改以优化树的构建和操作。
- __`config.py`__: 可能包含任务配置或全局变量，用于迷宫中的方向配置等。
- __`hollows.py`__: 与任务2相关，定义了“神秘洞”和“恐怖洞”的类，涉及宝物的选择和处理逻辑。
- __`maze.py`__: 核心迷宫逻辑文件，包含路径查找、迷宫表示和相关功能的实现，涉及任务3。
- __`random_gen.py`__: 用于生成随机数，可能在测试或迷宫构建过程中使用。
- __`readme.md`__: 提供项目的总体说明，指导如何运行脚手架或作业。
- __`run_tests.py`__: 运行所有测试的入口点，用于检验各任务的实现是否正确。
- __`treasure.py`__: 与宝物（treasures）相关的类或数据结构的定义，支持任务2中的宝物处理。

### `.vscode` 文件夹

- __`settings.json`__: 可能是Visual Studio Code的项目设置文件，配置了编辑器的特定行为或调试选项。

### `algorithms` 文件夹

- __`binary_search.py`, `mergesort.py`, `quicksort.py`__: 这些是经典的算法实现，可能供你在BST构建和迷宫任务中使用，但需要符合作业中的限制。
- __`__init__.py`__: 表示这个目录是一个Python包。

### `data_structures` 文件夹

- __各种ADT实现文件__: 如链表、栈、队列、集合、堆、BST等数据结构的实现。你可以在作业中引用这些数据结构，但不能修改它们。

### `ed_utils` 文件夹

- __`decorators.py`__: 可能包含装饰器函数，用于简化某些功能或测试的实现。

### `mazes` 文件夹

- __迷宫文件__: 包含了一些迷宫示例文件如`sample.txt`，供你加载并测试迷宫逃脱算法。`task3`文件夹中可能是为任务3专门准备的迷宫测试用例。

### `tests` 文件夹

- __各种测试文件__: 测试脚本，用于验证你对各个任务的实现是否正确。建议在完成每个任务后运行相应的测试文件来确保代码的正确性。

### 任务分析

- __任务1__: 主要涉及对`betterbst.py`的修改，需要你实现平衡二叉树的构建，保证时间复杂度为`O(n log n)`。
- __任务2__: 需要你在`hollows.py`中处理“神秘洞”和“恐怖洞”中的宝物选择，要求基于价值/重量比选择最佳宝物，并遵守复杂度要求。
- __任务3__: 在`maze.py`中实现迷宫路径查找，使用深度优先搜索算法（DFS）找到迷宫出口并从路径上的洞穴中提取宝物。

该脚手架文件提供了你完成这些任务所需的所有基础代码和测试文件。你的任务是在指定文件中进行修改，并确保符合时间复杂度和功能要求。
