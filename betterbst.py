from __future__ import annotations
from typing import List, Tuple, TypeVar
import math

from data_structures.bst import BinarySearchTree

K = TypeVar('K')
I = TypeVar('I')


class BetterBST(BinarySearchTree[K, I]):
    def __init__(self, elements: List[Tuple[K, I]]) -> None:
        """
        Initialiser for the BetterBST class.
        We assume that the all the elements that will be inserted
        into the tree are contained within the elements list.

        As such you can assume the length of elements to be non-zero.
        The elements list will contain tuples of key, item pairs.

        First sort the elements list and then build a balanced tree from the sorted elements
        using the corresponding methods below.

        Args:
            elements(List[tuple[K, I]]): The elements to be inserted into the tree.

        Complexity:
            Best Case Complexity: O(n log n)
            Worst Case Complexity: O(n log n)
        """
        super().__init__()
        new_elements: List[Tuple[K, I]] = self.__sort_elements(elements)
        self.__build_balanced_tree(new_elements)

    def __sort_elements(self, elements: List[Tuple[K, I]]) -> List[Tuple[K, I]]:
        """
        Recall one of the drawbacks to using a binary search tree is that it can become unbalanced.
        If we know the elements ahead of time, we can sort them and then build a balanced tree.
        This will help us maintain the O(log n) complexity for searching, inserting, and deleting elements.

        Args:
            elements (List[Tuple[K, I]]): The elements we wish to sort.

        Returns:
            list(Tuple[K, I]]) - elements after being sorted.

        Complexity:
            Best Case Complexity: O(n log n)
            Worst Case Complexity: O(n log n)
        """
        if len(elements) <= 1:
            return elements

        mid = len(elements) // 2
        left_half = self.__sort_elements(elements[:mid])  # 递归对左半部分进行排序
        right_half = self.__sort_elements(elements[mid:])  # 递归对右半部分进行排序

        return self.__merge(left_half, right_half)

    def __merge(self, left: List[Tuple[K, I]], right: List[Tuple[K, I]]) -> List[Tuple[K, I]]:
        """
        Merges two sorted lists into one sorted list.

        Args:
            left (List[Tuple[K, I]]): The left sorted list.
            right (List[Tuple[K, I]]): The right sorted list.

        Returns:
            List[Tuple[K, I]]: The merged sorted list.
        """
        merged = []
        left_index, right_index = 0, 0

        while left_index < len(left) and right_index < len(right):
            if left[left_index][0] < right[right_index][0]:
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1

        # 如果左侧或右侧还有剩余元素，则加入到合并列表中
        merged.extend(left[left_index:])
        merged.extend(right[right_index:])

        return merged

    def __build_balanced_tree(self, elements: List[Tuple[K, I]]) -> None:
        """
        This method will build a balanced binary search tree from the sorted elements.

        Args:
            elements (List[Tuple[K, I]]): The elements we wish to use to build our balanced tree.

        Returns:
            None

        Complexity:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)

        Justification:
            Each node is inserted into the tree exactly once, leading to a linear complexity.

        Complexity requirements for full marks:
            Best Case Complexity: O(n * log(n))
            Worst Case Complexity: O(n * log(n))
            where n is the number of elements in the list.
        """

        def build_tree(start: int, end: int) -> None:
            if start > end:
                return

            mid = (start + end) // 2
            key, item = elements[mid]
            self[key] = item  # 使用父类的 __setitem__ 方法插入节点

            # 递归构建左子树和右子树
            build_tree(start, mid - 1)
            build_tree(mid + 1, end)

        build_tree(0, len(elements) - 1)
