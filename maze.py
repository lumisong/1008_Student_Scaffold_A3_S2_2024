from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Tuple

from config import Directions, Tiles
from hollows import Hollow, MysticalHollow, SpookyHollow
from treasure import Treasure


class Position:
    def __init__(self, row: int, col: int) -> None:
        """
        Args:
            row(int): Row number in this maze cell position
            col(int): Column number in this maze cell position
        """
        self.row: int = row
        self.col: int = col

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Position) and value.row == self.row and value.col == self.col

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"


@dataclass
class MazeCell:
    tile: str | Hollow
    position: Position
    visited: bool = False

    def __str__(self) -> str:
        return str(self.tile)

    def __repr__(self) -> str:
        return f"'{self.tile}'"


class Maze:
    directions: dict[Directions, Tuple[int, int]] = {
        Directions.UP: (-1, 0),
        Directions.DOWN: (1, 0),
        Directions.LEFT: (0, -1),
        Directions.RIGHT: (0, 1),
    }

    def __init__(self, start_position: Position, end_positions: List[Position], walls: List[Position], hollows: List[tuple[Hollow, Position]], rows: int, cols: int) -> None:
        """
        Constructs the maze you should never be interacting with this method.
        Please take a look at `load_maze_from_file` & `sample1`

        Args:
            start_position(Position): Starting position in the maze.
            end_positions(List[Position]): End positions in the maze.
            walls(List[Position]): Walls in the maze.
            hollows(List[Position]): Hollows in the maze.
            rows(int): Number of rows in the maze.
            cols(int): Number of columns in the maze.

        Complexity:
            Best Case Complexity: O(_create_grid)
            Worst Case Complexity: O(_create_grid)
        """
        self.start_position: Position = start_position
        self.end_positions: List[Position] = end_positions
        self.rows: int = rows
        self.cols: int = cols
        self.grid: List[List[MazeCell]] = self._create_grid(walls, hollows, end_positions)

    def _create_grid(self, walls: List[Position], hollows: List[(Hollow, Position)], end_positions: List[Position]) -> List[List[MazeCell]]:
        """
        Args:
            walls(List[Position]): Walls in the maze.
            hollows(List[Position]): Hollows in the maze.
            end_positions(List[Position]): End positions in the maze.

        Return:
            List[MazeCell]: The generated maze grid.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.
        """
        grid: List[List[MazeCell]] = [[MazeCell(' ', Position(i, j))
                                       for j in range(self.cols)] for i in range(self.rows)]
        grid[self.start_position.row][self.start_position.col] = MazeCell(
            Tiles.START_POSITION.value, self.start_position)
        for wall in walls:
            grid[wall.row][wall.col].tile = Tiles.WALL.value
        for hollow, pos in hollows:
            grid[pos.row][pos.col].tile = hollow
        for end_position in end_positions:
            grid[end_position.row][end_position.col].tile = Tiles.EXIT.value
        return grid

    @staticmethod
    def validate_maze_file(maze_name: str) -> None:
        """
        Mazes must have the following:
        - A start position (P)
        - At least one exit (E)
        - All rows must have the same number of columns
        - Tiles are representations can be found in config.py
        - At least one treasure

        Args:
            maze_name(str): The name of the maze.

        Raises:
            ValueError: If maze_name is invalid.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.

            Assuming dictionary operations can be done on O(1) time.
        """
        maze_name = maze_name.lstrip('/\\')  # Remove leading slashes
        maze_dir = os.path.join(os.path.dirname(__file__), 'mazes')
        maze_path = os.path.join(maze_dir, maze_name)
        tile_count: dict[str, int] = {}
        with open(maze_path, 'r') as f:
            lines: List[str] = f.readlines()
            cols: int = len(lines[0].strip())
            for line in lines:
                if len(line.strip()) != cols:
                    raise ValueError(f"Uneven columns in {maze_name} ensure all rows have the same number of columns")
                # Check tiles
                for tile in line.strip():
                    if tile not in tile_count:
                        tile_count[tile] = 1
                    else:
                        tile_count[tile] += 1
        if 'P' not in tile_count or 'E' not in tile_count:
            raise ValueError(f"Missing start or end position in {maze_name}")

        if tile_count['P'] > 1:
            raise ValueError(f"Multiple start positions found in {maze_name}")

        # Check we have at least one treasure
        if not (Tiles.SPOOKY_HOLLOW.value in tile_count or Tiles.MYSTICAL_HOLLOW.value in tile_count):
            raise ValueError(f"No treasures found in {maze_name}")

        valid_types: List[str] = [tile.value for tile in Tiles]
        invalid_tiles: List[str] = [tile for tile in tile_count if tile not in valid_types]
        if invalid_tiles:
            raise ValueError(f"Invalid tile(s) found in {maze_name} ({invalid_tiles})")

    @classmethod
    def load_maze_from_file(cls, maze_name: str) -> Maze:
        """
        Args:
            maze_name(str): The maze name to load the maze from.

        Return:
            Maze: The newly created maze instance.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.

            For small mazes we assume the lists we not need to resize.
        """
        maze_name = maze_name.lstrip('/\\')  # Remove leading slashes
        maze_dir = os.path.join(os.path.dirname(__file__), 'mazes')
        maze_path = os.path.join(maze_dir, maze_name)
        cls.validate_maze_file(maze_name)

        # **Reset the MysticalHollow treasures before loading the maze**

        MysticalHollow.treasures = []
        MysticalHollow.treasure_map = None

        end_positions, walls, hollows = [], [], []
        mystical_hollow: MysticalHollow = MysticalHollow()
        start_position: Position | None = None
        with open(maze_path, 'r') as f:
            lines: List[str] = f.readlines()
            rows: int = len(lines)
            cols: int = len(lines[0].strip())
            for i, line in enumerate(lines):
                for j, tile in enumerate(line.strip()):
                    if tile == Tiles.START_POSITION.value:
                        start_position: Position = Position(i, j)
                    elif tile == Tiles.EXIT.value:
                        end_positions.append(Position(i, j))
                    elif tile == Tiles.WALL.value:
                        walls.append(Position(i, j))
                    elif tile == Tiles.SPOOKY_HOLLOW.value:
                        hollows.append((SpookyHollow(), Position(i, j)))
                    elif tile == Tiles.MYSTICAL_HOLLOW.value:
                        hollows.append((mystical_hollow, Position(i, j)))
        assert start_position is not None
        return Maze(start_position, end_positions, walls, hollows, rows, cols)

    def is_valid_position(self, position: Position) -> bool:
        """
        Checks if the position is within the maze and not blocked by a wall.

        Args:
            position (Position): The position to check.

        Returns:
            bool - True if the position is within the maze and not blocked by a wall.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        if 0 <= position.row < self.rows and 0 <= position.col < self.cols:
            tile = self.grid[position.row][position.col].tile
            if tile != Tiles.WALL.value:
                return True
        return False

    def get_available_positions(self, current_position: Position) -> List[Position]:
        """
        Returns a list of all the new possible positions you can move to from your current position.

        Args:
            current_position (Position): Your current position.

        Returns:
            List[Position] - A list of all the new possible positions you can move to from your current position.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        available_positions = []
        for direction in Directions:
            delta_row, delta_col = self.directions[direction]
            new_row = current_position.row + delta_row
            new_col = current_position.col + delta_col
            new_position = Position(new_row, new_col)
            if self.is_valid_position(new_position):
                available_positions.append(new_position)
        return available_positions

    def find_way_out(self) -> List[Position] | None:
        """
        Finds a way out of the maze. In some cases there may be multiple exits
        or no exits at all.

        Returns:
            List[Position]: If there is a way out of the maze,
            the path will be made up of the coordinates starting at
            your original starting point and ending at the exit.

            None: Unable to find a path to the exit, simply return None.

        Complexity:
            Best Case Complexity: O(N)
            Worst Case Complexity: O(N)
            Where N is the number of cells in the maze.
        """
        path = []
        self.reset_visited()
        if self._dfs(self.start_position, path):
            return path
        else:
            return None

    def _dfs(self, position: Position, path: List[Position]) -> bool:
        """
        Helper method for find_way_out using recursive depth-first search.

        Args:
            position (Position): Current position in the maze.
            path (List[Position]): The current path taken.

        Returns:
            bool: True if an exit has been found, False otherwise.

        Complexity:
            Best Case Complexity: O(N)
            Worst Case Complexity: O(N)
            Where N is the number of cells in the maze.
        """
        # Base cases
        if position in self.end_positions:
            path.append(position)
            return True

        cell = self.grid[position.row][position.col]
        if cell.visited:
            return False

        # Mark the cell as visited
        cell.visited = True
        path.append(position)

        # Movement priorities: up, down, left, right
        for direction in [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]:
            delta_row, delta_col = self.directions[direction]
            new_row = position.row + delta_row
            new_col = position.col + delta_col
            new_position = Position(new_row, new_col)
            if self.is_valid_position(new_position):
                next_cell = self.grid[new_row][new_col]
                if not next_cell.visited:
                    if self._dfs(new_position, path):
                        return True

        # Backtrack
        path.pop()
        return False

    def reset_visited(self) -> None:
        """
        Resets the visited status of all cells in the maze.

        Complexity:
            Best Case Complexity: O(N)
            Worst Case Complexity: O(N)
            Where N is the number of cells in the maze.
        """
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def take_treasures(self, path: List[MazeCell], backpack_capacity: int) -> List[Treasure] | None:
        """
        You must take the treasures in the order they appear in the path selecting treasures
        that have the highest value / weight ratio. Remember the total of treasures cannot
        exceed backpack_capacity, which means individual treasures cannot exceed this value either.

        Should there be no treasures that are viable please return None.

        You do not have to validate the path, it is guaranteed to be a valid path.

        Args:
            path (List[MazeCell]): The path you took to reach the exit.
            backpack_capacity (int): The maximum weight you can carry.

        Returns:
            List[Treasure] - List of the most optimal treasures.
            None - If there are no treasures to take.

        Complexity:
            Best Case Complexity: O(M)
            Worst Case Complexity: O(M * log N)
            Where M is the length of the path and N is the number of treasures in a hollow.
        """
        treasures_taken = []
        remaining_capacity = backpack_capacity
        for cell in path:
            tile = cell.tile
            if isinstance(tile, Hollow):
                treasure = tile.get_optimal_treasure(remaining_capacity)
                if treasure is not None:
                    treasures_taken.append(treasure)
                    remaining_capacity -= treasure.weight
        if len(treasures_taken) == 0:
            return None
        else:
            return treasures_taken

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        """
        Returns the grid in a human-readable format.

        Complexity:
        Best Case Complexity: O(N) where N is the number of cells in the maze.
        Worst Case Complexity: O(N) where N is the number of cells in the maze.
        """
        my_grid: str = ""
        for row in self.grid:
            my_grid += "" if my_grid == "" else "\n"
            my_grid += ''.join(str(cell) for cell in row)

        return my_grid


def sample1() -> None:
    maze = Maze.load_maze_from_file("sample.txt")
    print(maze)


def sample2() -> None:
    maze = Maze.load_maze_from_file("sample2.txt")
    print(maze)
    # Samples as to how the grid / maze cells work
    r, c = 4, 0  # row 4, col 0
    print(maze.grid[r][c].position, type(maze.grid[r][c]), f"Visited: {maze.grid[r][c].visited}")
    print(maze.grid[r][c].tile, type(maze.grid[r][c].tile))
    r, c = 2, 3  # row 2, col 3
    print(maze.grid[r][c].position, type(maze.grid[r][c]), f"Visited: {maze.grid[r][c].visited}")
    print(maze.grid[r][c].tile, type(maze.grid[r][c].tile))


if __name__ == "__main__":
    sample1()
