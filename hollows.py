from __future__ import annotations
"""
Ensure you have read the introduction and task 1 and understand what
is prohibited in this task.
This includes:
The ban on inbuilt sort methods .sort() or sorted() in this task.
And ensure your treasure data structure is not banned.

"""
from abc import ABC, abstractmethod
from typing import List

from config import Tiles
from treasure import Treasure, generate_treasures
from data_structures.bst import BinarySearchTree
from data_structures.bset import BSet
from algorithms.mergesort import mergesort

class Hollow(ABC):
    """
    DO NOT MODIFY THIS CLASS
    Mystical troves of treasure that can be found in the maze
    There are two types of hollows that can be found in the maze:
    - Spooky Hollows: Each of these hollows contains unique treasures that can be found nowhere else in the maze.
    - Mystical Hollows: These hollows contain a random assortment of treasures like the spooky hollow however all mystical hollows are connected, so if you remove a treasure from one mystical hollow, it will be removed from all other mystical hollows.
    """

    # DO NOT MODIFY THIS ABSTRACT CLASS
    """
    Initialises the treasures in this hollow
    """

    def __init__(self) -> None:
        self.treasures = self.gen_treasures()
        self.restructure_hollow()

    @staticmethod
    def gen_treasures() -> List[Treasure]:
        """
        This is done here, so we can replace it later on in the auto marker.
        This method contains the logic to generate treasures for the hollows.

        Returns:
            List[Treasure]: A list of treasures that can be found in the maze
        """
        return generate_treasures()

    @abstractmethod
    def restructure_hollow(self):
        pass

    @abstractmethod
    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        pass

    def __len__(self) -> int:
        """
        After the restructure_hollow method is called, the treasures attribute should be updated
        don't create an additional attribute to store the number of treasures in the hollow.
        """
        return len(self.treasures)


class SpookyHollow(Hollow):

    def restructure_hollow(self) -> None:
        """
        Re-arranges the treasures in the hollow from a list to a new
        data structure that is better suited for the get_optimal_treasure method.

        The new treasures data structure can't be an ArrayR or list variant (LinkedList, python list, sorted list, ...).
        No lists! Breaching this will count as a major error and lose up to 100% of the marks of the task!

        Returns:
            None - This method should update the treasures attribute of the hollow

        Complexity:
            Best Case Complexity: O(n log n)
            Worst Case Complexity: O(n log n)

        Complexity requirements for full marks:
            Best Case Complexity: O(n log n)
            Worst Case Complexity: O(n log n)
            Where n is the number of treasures in the hollow
        """
        self.treasures_bst = BinarySearchTree()

        # Insert all treasures into the BST, keyed by ratio
        for treasure in self.treasures:
            ratio = treasure.value / treasure.weight
            self.treasures_bst[ratio] = treasure

        # Replace self.treasures with the BST
        self.treasures = self.treasures_bst

    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        """
        Removes the ideal treasure from the hollow
        Takes the treasure which has the greatest value / weight ratio
        that is less than or equal to the backpack_capacity of the player as
        we can't carry treasures that are heavier than our backpack capacity.

        Ensure there are only changes to the treasures contained in the hollow
        if there is a viable treasure to take. If there is a viable treasure
        only remove that treasure from the hollow, no other treasures should be removed.

        Returns:
            Treasure - the ideal treasure that the player should take.
            None - if all treasures are heavier than the backpack_capacity
            or the hollow is empty

        Complexity:
            Best Case Complexity: O(log n)
            Worst Case Complexity: O(n)

        Complexity requirements for full marks:
            Best Case Complexity: O(log(n))
            Worst Case Complexity: O(n)
            n is the number of treasures in the hollow
        """
        current = self.treasures.root
        stack = []

        # Initialize by finding the maximum node
        while current:
            stack.append(current)
            current = current.right

        # Traverse the BST in reverse in-order
        while stack:
            current = stack.pop()
            treasure = current.item
            if treasure.weight <= backpack_capacity:
                # Remove the treasure from the BST
                del self.treasures[current.key]
                return treasure
            # Move to the left subtree
            if current.left:
                node = current.left
                while node:
                    stack.append(node)
                    node = node.right

        # No treasure found
        return None

    def __str__(self) -> str:
        return Tiles.SPOOKY_HOLLOW.value

    def __repr__(self) -> str:
        return str(self)


class MysticalHollow(Hollow):

    def restructure_hollow(self):
        """
        Re-arranges the treasures in the hollow from a list to a new
        data structure that is better suited for the get_optimal_treasure method.

        The new treasures data structure can't be an ArrayR or list variant (LinkedList, python list, sorted list, ...).
        No lists! Breaching this will count as a major error and lose up to 100% of the marks of the task!

        Returns:
            None - This method should update the treasures attribute of the hollow

        Complexity:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)
            Where n is the number of treasures in the hollow
        """


        self.treasure_set = BSet()
        self.treasure_map = BinarySearchTree()

        for treasure in self.treasures:
            ratio = treasure.value / treasure.weight
            ratio_int = int(ratio * 100) + 1  # Ensures ratio_int >= 1
            self.treasure_set.add(ratio_int)
            self.treasure_map[ratio_int] = treasure

        # Replace self.treasures with the BSet
        self.treasures = self.treasure_set

    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        """
        Removes the ideal treasure from the hollow
        Takes the treasure which has the greatest value / weight ratio
        that is less than or equal to the backpack_capacity of the player as
        we can't carry treasures that are heavier than our backpack capacity.

        Ensure there are only changes to the treasures contained in the hollow
        if there is a viable treasure to take. If there is a viable treasure
        only remove that treasure from the hollow, no other treasures should be removed.

        Returns:
            Treasure - the ideal treasure that the player should take.
            None - if all treasures are heavier than the backpack_capacity
            or the hollow is empty

        Complexity:
            Best Case Complexity: O(log n)
            Worst Case Complexity: O(n log n)
            Where n is the number of treasures in the hollow
        """
        # Get all ratios from the set
        ratios = []
        current_bit = self.treasures.elems
        idx = 1
        while current_bit:
            if current_bit & 1:
                ratios.append(idx)
            current_bit >>= 1
            idx += 1

        # Sort ratios in descending order

        sorted_ratios = mergesort(ratios, sort_key=lambda x: -x)

        for ratio_int in sorted_ratios:
            treasure = self.treasure_map[ratio_int]
            if treasure.weight <= backpack_capacity:
                # Remove from the set and BST
                self.treasures.remove(ratio_int)
                del self.treasure_map[ratio_int]
                return treasure

        return None

    def __str__(self) -> str:
        return Tiles.MYSTICAL_HOLLOW.value

    def __repr__(self) -> str:
        return str(self)
