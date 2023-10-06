package eight;

import java.awt.*;
import java.util.List;
import java.util.Objects;

public class Maze {
    private static final boolean CELL_OCCUPIED = true;//позиция занята
    private final boolean[][] maze;

    public Maze(final boolean[][] maze) {
        Objects.requireNonNull(maze, "Входной лабиринт пуст.");
        final int numberOfRows = maze.length; //кол-во ячеек

        if (numberOfRows == 0) {
            throw new IllegalArgumentException("Входной лабиринт пуст");
        }
        int numberOfColumns = 0;
        for (int row = 0; row < maze.length; ++row) {
            numberOfColumns = Math.max(numberOfColumns, maze[row].length);
        }
        this.maze = new boolean[numberOfRows][numberOfColumns];
        for (int row = 0; row < numberOfRows; ++row) {
            for (int column = 0;
                 column < Math.min(numberOfColumns, maze[row].length);
                 column++) {
                this.maze[row][column] = maze[row][column];
            }
        }
    }

    public int getWidth() {
        return maze[0].length;
    }

    public int getHeight() {
        return maze.length;
    }

    public boolean cellIsFree(final Point p) {
        return cellIsFree(p.x, p.y);
    }

    public boolean cellIsWithinMaze(final Point p) {
        return p.x >= 0 && p.x < getWidth() && p.y >= 0 && p.y < getHeight();
    }

    public boolean cellIsTraversible(final Point p) {
        return cellIsWithinMaze(p) && cellIsFree(p);
    }

    public boolean cellIsFree(final int x, final int y) {
        checkXCoordinate(x);
        checkYCoordinate(y);
        return maze[y][x] != CELL_OCCUPIED;
    }

    public String withPath(final List<Point> path) {
        final char[][] matrix = new char[getHeight()][getWidth()];

        for (int i = 0; i < matrix.length; ++i) {
            for (int j = 0; j < matrix[0].length; ++j) {
                matrix[i][j] = maze[i][j] ? 'x' : '.';
            }
        }

        for (final Point p : path) {
            matrix[p.y][p.x] = 'o';
        }

        final StringBuilder sb = new StringBuilder();

        sb.append(new String(matrix[0]));

        for (int i = 1; i < matrix.length; ++i) {
            sb.append('\n');
            sb.append(new String(matrix[i]));
        }

        return sb.toString();
    }

    private void checkXCoordinate(final int x) {
        if (x < 0) {
            throw new IndexOutOfBoundsException(
                    "Координата x отрицательна: " + x + ".");
        }

        if (x >= maze[0].length) {
            throw new IndexOutOfBoundsException(
                    "x-координата слишком велика (" + x +
                            "). Количество столбцов в этом лабиринте равно " +
                            maze[0].length + ".");
        }
    }

    private void checkYCoordinate(final int y) {
        if (y < 0) {
            throw new IndexOutOfBoundsException(
                    "Координата y отрицательна:: " + y + ".");
        }

        if (y >= maze.length) {
            throw new IndexOutOfBoundsException(
                    "x-координата слишком велика (" + y +
                            "). Количество столбцов в этом лабиринте равно " +
                            maze.length + ".");
        }
    }

}
