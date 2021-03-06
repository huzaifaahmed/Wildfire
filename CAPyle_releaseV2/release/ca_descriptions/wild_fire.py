# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np


def transition_func(grid, neighbourstates, neighbourcounts):
    # dead = state == 0, live = state == 1
    # unpack state counts for state 0 and state 1
    dead_neighbours, burning_neighbours, healthy_neighbours = neighbourcounts
    # create boolean arrays for the birth & survival rules
    # if 3 live neighbours and is dead -> cell born
    #birth = (live_neighbours == 3) & (grid == 0)
    # if 2 or 3 live neighbours and is alive -> survives
    #survive = ((live_neighbours == 2) | (live_neighbours == 3)) & (grid == 1)
    # Set all cells to 0 (dead)
    grid[:, :] = 0
    # Set cells to 1 where either cell is born or survives
    #grid[birth | survive] = 1
    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    config.grid_dims = (51,51)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Conway's game of life"
    config.dimensions = 2
	#0 = burnt, 1 = burning, 2 = healthy (chaparral by default)
    config.states = (0, 1, 2)

    if config.terrain is None:
        fillstate = 2
        config.terrain = np.zeros(config.grid_dims, dtype=type(fillstate))
        config.terrain.fill(fillstate)

    for x in range(5, 15):
        for y in range (35, 40):
            config.terrain[50-y, x] = 3

    for x in range(32, 35):
        for y in range (15, 45):
            fillstate3 = 4
            config.terrain[50-y, x] = fillstate3

    for x in range(15, 25):
        for y in range (9, 20):
            fillstate4 = 5
            config.terrain[50-y, x] = fillstate4

    #0 = lake, 1 = canyon, 2 = dense forest, 3 = burning chaparral, 4 = burning canyon, 5 = burning dense forest
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0,0,0), (1,0,0), (0.6,0.6,0)]
    config.num_generations = 100

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
