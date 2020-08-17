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
    
    #neighbourcounts check how many of the neighbouring squares are of the 
    #listed states and stores them as the following variables. 
    unburnt_chaparral, unburnt_canyon, unburnt_forest, water, burning, burntout_chaparral, burntout_canyon, burntout_forest, town = neighbourcounts
    
    #neighbourstates returns the current value of the selected directional 
    #variable as one of the 9 states
    NW, N, NE, W, E, SW, S, SE = neighbourstates
    
    #iterate through the state grid changing squares to their appropriate states.
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            wind_value = 0 #Initialise to 0.
            wind_strength = 1 #this will remain as 1.
            terrain = 0 #All squares are initially given the terrain chapparal.
            
            #wind_value increases based on how the user wants the wind to be set up.
            #if (NW[i][j] == 1):
                #wind_value += wind_strength
            
            #if (N[i][j] == 1):
                #wind_value += wind_strength
                
            #if (NE[i][j] == 1):
               # wind_value += wind_strength
               
            #if (E[i][j] == 1):
                #wind_value += wind_strength
            
            #if (SE[i][j] == 1):
                #wind_value += wind_strength
                
            #if (S[i][j] == 1):
               # wind_value += wind_strength
            
            #if (SW[i][j] == 1):
                #wind_value += wind_strength
            
            #if (W[i][j] == 1):
                #wind_value += wind_strength
                
            #ADD MORE WIND DIRECTIONS IF NEEDED. UNCOMMENT THE DIRECTIONS YOU WANT TO TEST.
			
    		  #Assigns squares their correct terrains.
            if (i >= 5 and i <= 35 and j >= 33 and j <= 35 and grid[i][j] != 6): #canyon
               terrain = 1
            elif (i >= 30 and i <= 40 and j >= 15 and j <= 25 and grid[i][j] != 7): #forest
               terrain = 2
            elif (i >= 10 and i <= 15 and j >= 5 and j <= 15): #water
               terrain = 3
            elif (i >= 49 and i <= 50 and j >= 0 and j <= 3): #town
               terrain = 4
            
            #ignition likelihoods for each burnable terrain. Returns a boolean value.
            chapparal_ignition = ((randomNum(8) - wind_value) < 1) & (burning[i][j] >= 1) & (grid[i][j] == 0)
                                    
            canyon_ignition    = ((randomNum(3)  - wind_value) < 1) & (burning[i][j] >= 1) & (grid[i][j] == 1)
                                 
            forest_ignition    = ((randomNum(15) - wind_value) < 1) & (burning[i][j] >= 1) & (grid[i][j] == 2)
            #PLAY AROUND WITH THE PROBABILITIES TO MAKE IT LOOK REALISTIC.
            
            # Assigns burntimes to squares based on if they are to be ignited or not.
            if (chapparal_ignition or canyon_ignition or forest_ignition):
                grid[i][j] = 4
                if (chapparal_ignition):
                    
                    burntime[i][j] = 120 #5 days.
                    
                if (canyon_ignition):
                    
                    burntime[i][j] = 20 #20 hours
                    
                if (forest_ignition):
                    
                    burntime[i][j] = 720 #30 days
            
            #decays the squares burntime to 0.
            if (burntime[i][j] > 0):
                burntime[i][j] -= 1
                
                if (burntime[i][j] == 0):
                    
                    if (terrain == 0):#burntout chapparal
                        grid[i][j] = 5
                        
                    if (terrain == 1):#burntout canyon
                        grid[i][j] = 6
                        
                    if (terrain == 2):#burntout forest
                        grid[i][j] = 7
                        
            elif (burntime[i][j] -1 == -1 and grid[i][j] == 4): #sets the intial user selected burning squares their actual burntime.
                if (terrain == 0):
                    burntime[i][j] = 119
                elif (terrain == 1):
                    burntime[i][j] = 19
                elif (terrain == 2):
                    burntime[i][j] = 719
                elif (terrain == 3): #if terrain is water, leave it as water.
                    grid[i][j] = 3
                elif (terrain == 4): #if terrain is town, leave it as town.
                    grid[i][j] = 8
            
    return grid

def randomNum(limit): #returns a random number from 0 to the paramater limit.
    return random.randint(0,limit)

def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "TEAM 19 BOI"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5, 6, 7, 8) #We use 9 states in total.
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    #colors for each state.
    config.state_colors = [(0.88,1,0.27),(0.45,0.5,0.54),(0,0.29,0),(0,0.16,1),(1,0,0),(0.32,0.32,0),(0,0,0),(0.04,0.13,0.04),(0,0,0)]
    
    # config.num_generations = 150
    if config.grid_dims is None:
        config.grid_dims = (51,51)
    
    #initialises the required map layout.
    if config.initial_grid is None:
        back_fill = config.states[0] if config.states is not None else 0
        initGrid = np.zeros(config.grid_dims, dtype=type(back_fill))
        for i in range(len(initGrid)):#iterates through the initial grid, setting squares to their initial states.
            for j in range(len(initGrid[0])):
                
                
                if (i >= 5 and i <= 35 and j >= 33 and j <= 35): #canyon
                    initGrid[i][j] = 1
                elif (i >= 30 and i <= 40 and j >= 15 and j <= 25): #forest
                    initGrid[i][j] = 2
                elif (i >= 10 and i <= 15 and j >= 5 and j <= 15): #water
                    initGrid[i][j] = 3
                elif (i >= 49 and i <= 50 and j >= 0 and j <= 3):
                    initGrid[i][j] = 8 #Town.
        config.initial_grid = initGrid
    
    config.wrap = False #Disable grid wrap.

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])
    burntime = np.zeros(config.grid_dims) #Create a new grid with the same dimensions as our 2d grid.

    # Create grid object
    grid = Grid2D(config, (transition_func, burntime)) #Pass the transition function and the burntime.

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
