from enum import Enum
import random


# This is an enum that gives us a name for each
# tile type in the maze
class TileType(Enum):
    FLOOR = 0
    WALL = 1
# TODO: Add type for player start
    START = 2
# TODO: Add types for key, chest, and door
    DOOR = 3
    CHEST = 4
    KEY = 5


# This function will take a width, height, & seed
# and generate a random maze for you using the
# depth-first-search algorithm:
# https://en.wikipedia.org/wiki/Depth-first_search
#
# The maze returned is a 2 dimensional list starting
# with rows and then columns starting with 0:
#
# maze[2][1] is the 3rd row and 2nd column
def maze_generate(width: int, height: int, seed: int) -> list[list[TileType]]:
    # Make sure we have a valid width and height
    if width < 0 or height < 0:
        raise ValueError("width and height must be positive")
    # The width and height need to be odd so we can have an outside wall border
    if width % 2 == 0 or height % 2 == 0:
        raise ValueError("width & neight must be odd")
    # The width and height need to be at least 3 to have any space for floor tiles
    if width < 3 or height < 3:
        raise ValueError("width & height must be greater or equal to 3")

    # Start out creating a maze full of walls
    # Later we will carve out the floor tiles
    maze: list[list[TileType]] = []
    x: int = 0
    y: int = 0
    for y in range(height):
        row: list[TileType] = []
        for x in range(width):
            row.append(TileType.WALL)
        maze.append(row)
    
    # For the depth-first-search we need a stack for the
    # floor tiles we have alreach carved out, so when we
    # can't carve out anymore on the current path, we can
    # backtrack and try from a different direction
    #
    # The stack will be tuples of x & y coordinates in
    # the maze, and we will use append to add a spot and
    # pop to take one off
    carved: list[tuple[int, int]] = []

    # Initialize the random number generation with our seed
    random.seed(seed)
    
    # Start with a random, odd position respecting out outside
    # wall border
    #
    # REMEMBER: Positions in the maze / list start with 0
    x = random.randint(0, (width - 2) // 2) * 2 + 1
    y = random.randint(0, (height - 2) // 2) * 2 + 1
    maze[y][x] = TileType.FLOOR
    carved.append((x, y))
    
    # We can keep carving out floor tiles until the carved
    # stack is empty
    while len(carved) > 0:
        # For each carving step will be dealing with a
        # x & y position and the carvable directions from
        # that position
        carvable: list[tuple[int, int]] = []

        # do-while loop (infinite with break) that will break
        # once we have a spot that has at least one carvable
        # direction
        while True:
            # Break if we don't have any carved spots left
            if len(carved) == 0:
                break
            # Take the deepest spot off of the carved stack
            x, y = carved.pop()
            # When we pick the directions to carve, we move
            # 2 at a time so we're always moving from one
            # odd space to the next odd space.  The even space
            # in between gets carved out with the move.
            #
            # The carvable directions are x & y tuples with
            # 0, 1, or -1 specifying the x & y values to add
            # to the current spot to carve in that direction
            # Up
            if y >= 3 and maze[y - 2][x] == TileType.WALL:
                carvable.append((0, -1))
            # Down
            if y <= (height - 4) and maze[y + 2][x] == TileType.WALL:
                carvable.append((0, 1))
            # Left
            if x >= 3 and maze[y][x - 2] == TileType.WALL:
                carvable.append((-1, 0))
            # right
            if x <= (width - 4) and maze[y][x + 2] == TileType.WALL:
                carvable.append((1, 0))
            # Break if we have at least one carvable direction
            if len(carvable) > 0:
                break
        
        # If we have at least one carvable direction,
        # pick a random one and carve:
        if len(carvable) > 0:
            x_dir, y_dir = random.choice(carvable)
            # Put the current spot back on the carved stack
            carved.append((x, y))
            # Carve out the even floor
            x += x_dir
            y += y_dir
            maze[y][x] = TileType.FLOOR
            # Carve out the odd floor
            x += x_dir
            y += y_dir
            maze[y][x] = TileType.FLOOR
            # Put the new spot on the carved stack
            carved.append((x, y))

    # Find all of the floor tiles in the maze that
    # are dead-ends or part of a hall
    directions: list[tuple[int, int]] = [(0, -1), (0, 1), (-1, 0), (1, 0)] # Up, Down, Left, & Right
    dead_ends: list[tuple[int, int]] = []
    halls: list[tuple[int, int]] = []
    for y in range(height):
        for x in range(width):
            if maze[y][x] == TileType.FLOOR:
                num_floor_directions: int = 0
                for x_dir, y_dir in directions:
                    if maze[y + y_dir][x + x_dir] == TileType.FLOOR:
                        num_floor_directions += 1
                # TODO: Check num_floor_directions and possibly add x & y to dead_ends
                if num_floor_directions == 1:
                    dead_ends.append((x, y))
                # TODO: If it's not a dead-end, add x & y to the halls
                elif num_floor_directions > 1:
                    halls.append((x, y))
    # Shuffle the dead-end and halls lists so if we pop one off we'll get a random one
    random.shuffle(dead_ends)
    random.shuffle(halls)

    # TODO: Pop a random hall floor tile for the player start
    x, y = halls.pop()
    maze[y][x] = TileType.START

    # TODO: Pop a random floor tile that is at a dead-end for the door
    x, y = dead_ends.pop()
    maze[y][x] = TileType.DOOR
    # TODO: Pop a random floor tile that is at a dead-end for the chest
    x, y = dead_ends.pop()
    maze[y][x] = TileType.CHEST
    # TODO: Pop a random hall floor tile for the key to the chest
    x, y = halls.pop()
    maze[y][x] = TileType.KEY

    return maze


# This is a simple test function that will generate a maze
# and print it out as text
def test_maze():
    width = 21
    height = 15
    seed = random.randint(0, 1000000)
    maze = maze_generate(width, height, seed)
    for row in maze:
        for tile in row:
            if tile == TileType.WALL:
                print("#", end="")
            elif tile == TileType.START:
                print("S", end="")
            elif tile == TileType.DOOR:
                print("D", end="")
            elif tile == TileType.CHEST:
                print("C", end="")
            elif tile == TileType.KEY:
                print("K", end="")
            else:
                print(" ", end="")
        print()


# If we're running this module on it's own, run the quick test
if __name__ == "__main__":
    test_maze()