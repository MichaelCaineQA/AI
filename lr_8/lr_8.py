class Maze:
    CELL_OCCUPIED = True

    def __init__(self, maze):
        if maze is None:
            raise ValueError("Input maze is empty.")

        number_of_rows = len(maze)

        if number_of_rows == 0:
            raise ValueError("Input maze is empty.")

        number_of_columns = max(len(row) for row in maze)
        self.maze = [[False] * number_of_columns for _ in range(number_of_rows)]

        for row in range(number_of_rows):
            for column in range(min(number_of_columns, len(maze[row]))):
                self.maze[row][column] = maze[row][column]

    def get_width(self):
        return len(self.maze[0])

    def get_height(self):
        return len(self.maze)

    def cell_is_free(self, x, y):
        self.check_x_coordinate(x)
        self.check_y_coordinate(y)
        return not self.maze[y][x] == self.CELL_OCCUPIED

    def cell_is_within_maze(self, x, y):
        return 0 <= x < self.get_width() and 0 <= y < self.get_height()

    def cell_is_traversable(self, x, y):
        return self.cell_is_within_maze(x, y) and self.cell_is_free(x, y)

    def with_path(self, path):
        matrix = [['x' if self.maze[i][j] else '.' for j in range(self.get_width())] for i in range(self.get_height())]

        for p in path:
            matrix[p[1]][p[0]] = 'o'

        return '\n'.join(''.join(row) for row in matrix)

    def check_x_coordinate(self, x):
        if x < 0:
            raise IndexError(f"Coordinate x is negative: {x}.")
        if x >= self.get_width():
            raise IndexError(f"x-coordinate is too large ({x}). The number of columns in this maze is {self.get_width()}.")

    def check_y_coordinate(self, y):
        if y < 0:
            raise IndexError(f"Coordinate y is negative: {y}.")
        if y >= self.get_height():
            raise IndexError(f"y-coordinate is too large ({y}). The number of rows in this maze is {self.get_height()}.")


class MazePathFinder:
    def __init__(self, maze, source, target):
        if maze is None:
            raise ValueError("Input maze is empty.")
        if source is None:
            raise ValueError("Source point is None.")
        if target is None:
            raise ValueError("Target point is None.")

        self.maze = maze
        self.source = source
        self.target = target
        self.check_source_node()
        self.check_target_node()

        self.visited = [[False] * maze.get_width() for _ in range(maze.get_height())]
        self.parents = {source: None}
        self.parents[source] = None

    def find_path(self):
        queue = [self.source]
        distances = {}

        while queue:
            current = queue.pop(0)

            if current == self.target:
                path = self.construct_path()
                distances[len(path)] = path

                for value in distances.values():
                    if value is not None:
                        return value

                raise RuntimeError("Can't find path")

            for child in self.generate_children(current):
                if child not in self.parents:
                    self.parents[child] = current
                    queue.append(child)

    def construct_path(self):
        current = self.target
        path = []

        while current is not None:
            path.append(current)
            current = self.parents[current]

        path.reverse()
        return path

    def generate_children(self, current):
        x, y = current

        north = (x, y - 1)
        south = (x, y + 1)
        west = (x - 1, y)
        east = (x + 1, y)

        children = []

        if self.maze.cell_is_traversable(*north):
            children.append(north)
        if self.maze.cell_is_traversable(*south):
            children.append(south)
        if self.maze.cell_is_traversable(*west):
            children.append(west)
        if self.maze.cell_is_traversable(*east):
            children.append(east)

        return children

    def check_source_node(self):
        if not (0 <= self.source[0] < self.maze.get_width() and 0 <= self.source[1] < self.maze.get_height()):
            raise ValueError(f"Source point ({self.source}) is out of maze. Maze width {self.maze.get_width()} and maze height {self.maze.get_height()}.")

        if not self.maze.cell_is_free(*self.source):
            raise ValueError(f"Source point ({self.source}) is not in a free cell.")

    def check_target_node(self):
        if not (0 <= self.target[0] < self.maze.get_width() and 0 <= self.target[1] < self.maze.get_height()):
            raise ValueError(f"Target point ({self.target}) is out of maze. Maze width {self.maze.get_width()} and maze height {self.maze.get_height()}.")

        if not self.maze.cell_is_free(*self.target):
            raise ValueError(f"Target point ({self.target}) is not in a free cell.")


if __name__ == "__main__":
    maze_plan = [
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0]
    ]

    maze2 = [[cell > 0 for cell in row] for row in maze_plan]

    maze = Maze(maze2)
    source = (2, 0)
    target = (7, 5)
    second_target = (0, 5)

    import time
    start_time = time.time()
    path = MazePathFinder(maze, source, target).find_path()
    second_path = MazePathFinder(maze, source, second_target).find_path()
    end_time = time.time()

    shortest_path = path if len(path) < len(second_path) else second_path

    print(f"Search maze BFS in {(end_time - start_time) * 1000:.2f} milliseconds.")
    print(f"Path to point [x='{target[0]}', y='{target[1]}']: {len(path) - 1} steps")
    print(maze.with_path(path))
    print(f"Path to point [x='{second_target[0]}', y='{second_target[1]}']: {len(second_path) - 1} steps")
