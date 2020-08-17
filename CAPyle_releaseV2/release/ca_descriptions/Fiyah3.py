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
import random


def transition_func(grid, neighbourstates, neighbourcounts, burntime):
    
    #Checks how many neighbours are of the states 0-2
    unburnt, burning, burnt = neighbourcounts
    #Checks the state of the directional variable.
    NW, N, NE, W, E, SW, S, SE = neighbourstates
    
    #iterates through the grid igniting and burning out squares
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            wind_value = 0
            terrain = 1 #chapparal
            
            if (i >= 5 and i <= 35 and j >= 33 and j <= 35): #canyon
                terrain = 2
            elif (i >= 30 and i <= 40 and j >= 15 and j <= 25): #forest
                terrain = 3
            elif (i >= 10 and i <= 15 and j >= 5 and j <= 15): #water
                terrain = 4
            
            #if (S[i][j] == 1):
                #wind_value += 1
            
            #if (N[i][j] == 1):
                #wind_value += 1
                
            #if (NE[i][j] == 1):
               # wind_value += 1
            
            #ADD MORE WIND DIRECTIONS IF NEEDED. UNCOMMENT THE DIRECTIONS YOU WANT TO TEST.
            
            chapparal_ignition = ((randomNum(8) - wind_value) < 1) & (burning[i][j] >= 1) & (terrain == 1) & (grid[i][j] == 0)
                                    
            canyon_ignition    = ((randomNum(3)  - wind_value) < 1) & (burning[i][j] >= 1) & (terrain == 2) & (grid[i][j] == 0)
                                 
            forest_ignition    = ((randomNum(15) - wind_value) < 1) & (burning[i][j] >= 1) & (terrain == 3) & (grid[i][j] == 0)
            #PLAY AROUND WITH THE PROBABILITIES TO MAKE IT LOOK REALISTIC.
            
            if (chapparal_ignition or canyon_ignition or forest_ignition):
                grid[i][j] = 1
                #burns for several days (5 assumed here)
                if (chapparal_ignition):
                    burntime[i][j] = 120
                #burns for several hours (20 assumed here)
                if (canyon_ignition):
                    burntime[i][j] = 20
                #burns for a month
                if (forest_ignition):
                    burntime[i][j] = 720 #30 days
            if (burntime[i][j] > 0):
                burntime[i][j] -= 1
                if (burntime[i][j] == 0):
                    grid[i][j] = 2 #burnout
            elif (burntime[i][j] -1 == -1 and grid[i][j] == 1):
                if (terrain == 1):
                    burntime[i][j] = 119
                if (terrain == 2):
                    burntime[i][j] = 19
                if (terrain == 3):
                    burntime[i][j] = 719
                if (terrain == 4):
                    grid[i][j] = 0
            
    return grid

def randomNum(limit): #returns a random number from 0 to the given limit.
    return random.randint(0,limit)

def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "TEAM 19 BOI"
    config.dimensions = 2
    config.states = (0, 1, 2) # we use three states unburnt, burning and burntout.
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0,0,0),(1,1,1),(0.5,0.5,0.5)] #State colours.
    
    # config.num_generations = 150
    if config.grid_dims is None:
        config.grid_dims = (51,51)
    
    if config.initial_grid is None: #Sets all squares to unburnt.
        back_fill = config.states[0] if config.states is not None else 0
        initGrid = np.zeros(config.grid_dims, dtype=type(back_fill))
        config.initial_grid = initGrid
    
    config.wrap = False

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])
    burntime = np.zeros(config.grid_dims) #Creates a new grid with the same dimensions called burntime.
    #colours = np.zeros(config.grid_dims)

    # Create grid object
    grid = Grid2D(config, (transition_func, burntime)) #Pass burntime along with transition function.

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
