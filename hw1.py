
"""

Name: Rishita Chawla
ID: 003982023


This code was done with the help of ChatGPT.
Collaborated with Pratap Patil with general logic and approach for the local search algorithm, 
including the objective function, neighbor generation and restart strategy


Chatgpt: Took the help for what variables are most important that must be considered in the objective function
which helped in deciding the current states and the neighboring states


Also, took help of Chatgpt for Q1 part4 of drawing the flowchart of randomizing and first hill climbing algorithm
which helped in coding further


"""

import time
import numpy as np
from gridgame import *
import random

##############################################################################################################################

# You can visualize what your code is doing by setting the GUI argument in the following line to true.
# The render_delay_sec argument allows you to slow down the animation, to be able to see each step more clearly.

# For your final submission, please set the GUI option to False.

# The gs argument controls the grid size. You should experiment with various sizes to ensure your code generalizes.
# Please do not modify or remove lines 18 and 19.

##############################################################################################################################



game = ShapePlacementGrid(GUI=True, render_delay_sec=0, gs=6, num_colored_boxes=5)

shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute("export")



##############################################################################################################################

# Initialization

# shapePos is the current position of the brush.

# currentShapeIndex is the index of the current brush type being placed (order specified in gridgame.py, and assignment instructions).

# currentColorIndex is the index of the current color being placed (order specified in gridgame.py, and assignment instructions).

# grid represents the current state of the board. 
    
    # -1 indicates an empty cell
    # 0 indicates a cell colored in the first color (indigo by default)
    # 1 indicates a cell colored in the second color (taupe by default)
    # 2 indicates a cell colored in the third color (veridian by default)
    # 3 indicates a cell colored in the fourth color (peach by default)

# placedShapes is a list of shapes that have currently been placed on the board.
    
    # Each shape is represented as a list containing three elements: a) the brush type (number between 0-8), 
    # b) the location of the shape (coordinates of top-left cell of the shape) and c) color of the shape (number between 0-3)

    # For instance [0, (0,0), 2] represents a shape spanning a single cell in the color 2=veridian, placed at the top left cell in the grid.

# done is a Boolean that represents whether coloring constraints are satisfied. Updated by the gridgames.py file.

##############################################################################################################################

initial_shape_count = len(placedShapes)

np.savetxt("initial_grid.txt", grid, fmt="%d")

####################################################
# Timing your code's execution for the leaderboard.
####################################################
start = time.time()


def colors_number(g):
    used_colors = set()
    for cell in g.flatten():
        if cell != -1:
            used_colors.add(int(cell))
    return len(used_colors)



def conflicts_number(g):

    conflict_count = 0
    rows, columns = g.shape
    
    for row in range(rows):

        for column in range(columns):

            current_value = g[row, column]

            if current_value == -1:
                continue

            if column + 1 < columns:

                right_value = g[row, column + 1]

                if right_value != -1 and current_value == right_value:
                    conflict_count += 1

            if row + 1 < rows:

                bottom_value = g[row + 1, column]

                if bottom_value != -1 and current_value == bottom_value:
                    conflict_count += 1

    return conflict_count


def empty_cells(g):
    return int(np.sum(g == -1))



def obj_function(g, shapes):

    empty_count = empty_cells(g)

    conflict_count = conflicts_number(g)

    shape_count = len(shapes)

    color_count = colors_number(g)

    return (
        1000 * empty_count
        + 500 * conflict_count
        + 10 * shape_count
        + color_count
    )


def move_brush(current_position, target_position):

    current_x, current_y = current_position

    target_x, target_y = target_position

    while current_x < target_x:

        game.execute("right")
        current_x = current_x + 1

    while current_x > target_x:

        game.execute("left")
        current_x = current_x - 1

    while current_y < target_y:

        game.execute("down")
        current_y = current_y + 1

    while current_y > target_y:

        game.execute("up")
        current_y = current_y - 1

    return [current_x, current_y]


def switch_shape(current_index, target_index):

    shape_count = len(game.shapes)

    while current_index != target_index:

        game.execute("switchshape")

        current_index = (
            current_index + 1
        ) % shape_count

    return current_index



def switch_color(current_index, target_index):

    color_count = len(game.colors)

    while current_index != target_index:

        game.execute("switchcolor")

        current_index = (
            current_index + 1
        ) % color_count

    return current_index


# Input: current grid, shape index, position, and color index.
# Simulates placing the shape on a copy of the grid.
# Returns the updated grid if the placement is valid; otherwise returns None.

def simulate_shape_placement(g, shape_index, position, color_index):

    trial_board = g.copy()

    selected_shape = game.shapes[shape_index]

    start_x, start_y = position

    shape_height, shape_width = selected_shape.shape


    if start_x < 0 or start_y < 0:
        return None

    if start_x + shape_width > trial_board.shape[1]:
        return None

    if start_y + shape_height > trial_board.shape[0]:
        return None

    for shape_y in range(shape_height):

        for shape_x in range(shape_width):

            if selected_shape[shape_y, shape_x] == 1:

                board_y = start_y + shape_y
                board_x = start_x + shape_x

                if trial_board[board_y, board_x] != -1:
                    return None

    for shape_y in range(shape_height):

        for shape_x in range(shape_width):

            if selected_shape[shape_y, shape_x] == 1:

                board_y = start_y + shape_y
                board_x = start_x + shape_x

                trial_board[board_y, board_x] = color_index


    if conflicts_number(trial_board) > 0:
        return None

    return trial_board




def reset_agent_placements():

    while True:

        current_state = game.execute("export")

        current_placements = current_state[4]

        if len(current_placements) <= initial_shape_count:
            break

        game.execute("undo")


# Input: current grid and the list of already placed shapes.
# Searches for a valid move that improves the current cost.
# Returns the first improving shape, position, and color; otherwise returns None.

def search_next_move(g, current_shapes): 

    current_cost = obj_function(g, current_shapes)

    board_size = g.shape[0]
    trial_positions = []

    for y in range(board_size):
        for x in range(board_size):
            trial_positions.append((x, y))

    random.shuffle(trial_positions)


    trial_shapes = list(range(len(game.shapes)))

    random.shuffle(trial_shapes)

    trial_colors = list(range(len(game.colors)))
    random.shuffle(trial_colors)

    for position in trial_positions[:20]:

        x, y = position

        for shape_index in trial_shapes:

            selected_shape = game.shapes[shape_index]
            shape_height, shape_width = selected_shape.shape

            # Shape does not fit
            if x + shape_width > board_size:
                continue

            if y + shape_height > board_size:
                continue

            for color_index in trial_colors:

                trial_board = simulate_shape_placement(g, shape_index, [x, y], color_index)

                if trial_board is None:
                    continue

                
                trial_shapes_list = list(current_shapes)

                trial_shapes_list.append([shape_index,(x, y),color_index])

                trial_cost = obj_function(trial_board,trial_shapes_list)

                if trial_cost < current_cost:

                    return (shape_index,[x, y],color_index)
    return None



MAX_TRIALS = 100 # Try at most 100 neighboring states
MAX_RESTARTS = 50

restart_count = 0


while not done and restart_count < MAX_RESTARTS:

    move_found = False

    current_cost = obj_function(grid,placedShapes)


    for trial in range(MAX_TRIALS):

        next_move = search_next_move(grid, placedShapes)

        if next_move is None:
            continue

        selected_shape = next_move[0]
        selected_position = next_move[1]
        selected_color = next_move[2]


        shapePos = move_brush(shapePos,selected_position)
        currentShapeIndex = switch_shape(currentShapeIndex, selected_shape)
        currentColorIndex = switch_color(currentColorIndex, selected_color)

        game.execute("place")
        (shapePos,currentShapeIndex,currentColorIndex,grid,placedShapes,done) = game.execute("export")

        current_cost = obj_function(grid,placedShapes)

        print(
            "Accepted:",
            "cost =", current_cost,
            "| shapes =", len(placedShapes),
            "| empty =", empty_cells(grid),
            "| conflicts =", conflicts_number(grid),
            "| colors =", colors_number(grid)
        )

        move_found = True
        break

    if done:
        break

    if not move_found:

        restart_count += 1
        print( "Restarting search:", restart_count)

        reset_agent_placements()
        (shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done ) = game.execute("export")

        current_cost = obj_function(
            grid,
            placedShapes
        )

if not done:

    print("Local search stopped before completion.")

    reset_agent_placements()

    (shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done ) = game.execute("export")

    # Find a shape that colors exactly one cell -- restart strategy
    one_cell_shape = None

    for shape_index, shape in enumerate(game.shapes):

        if np.sum(shape) == 1:
            one_cell_shape = shape_index
            break

    if one_cell_shape is not None:

        for row in range(game.gridSize):
            for column in range(game.gridSize):

                if grid[row, column] != -1:
                    continue

                for color_index in range(len(game.colors)):

                    trial_board = simulate_shape_placement(grid, one_cell_shape, [column, row], color_index)

                    if trial_board is None:
                        continue

                    shapePos = move_brush(shapePos, [column, row])

                    currentShapeIndex = switch_shape(currentShapeIndex, one_cell_shape)

                    currentColorIndex = switch_color(currentColorIndex, color_index)

                    game.execute("place")

                    (shapePos,currentShapeIndex,currentColorIndex,grid,placedShapes,done) = game.execute("export")
                    
                    break

                if done:
                    break

            if done:
                break



(shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done) = game.execute("export")


########################################

# Do not modify any of the code below. 

########################################

end = time.time()

print()
print("----- SEARCH SUMMARY -----")

print("Solution found:", done)
print("Total placements:", len(placedShapes))
print("Distinct colors:", colors_number(grid))
print("Remaining empty:", empty_cells(grid))
print("Remaining conflicts:", conflicts_number(grid))
print("Final cost:", obj_function(grid, placedShapes))
print("Restarts used:", restart_count)
print("Elapsed time:", end - start, "seconds")

np.savetxt("grid.txt", grid, fmt="%d" )

with open("shapes.txt", "w") as outfile:
    outfile.write(str(placedShapes))

with open("time.txt", "w") as outfile:
    outfile.write(str(end - start))

print("Runtime:", end - start, "seconds" )

print("Runtime:",(end - start) / 60, "minutes")