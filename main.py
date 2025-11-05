# from pprint import pp as log # Used for logging purpose especially dealing with dictionary. Not really used.
import random
def main():
    def en_dict(s):
        """
        Will turn a set or multi-dimensional set into a dict. I figure out that it's much more convenient to assume that each key of the y_axis, and each x inside the set of y_axis, to have a key representing their own coordinate.
        {
            0: {0: "A", 1: "B", 2: "C"}
            1: {0: "1", 1: "2", 2: "3"} (assuming each key is str already)
        }

        Therefore, (1,0) = "B"
        """
        # Initialize dictionary
        init_dict = {}
        if type(s[0]) == list:
            # When @s is a multi-dimensional array. If its multdi-dimensional, or has a set inside a set.
            for y_i, y_v in zip(range(len(s)+1), s):
                # Traverse through each array with respect of Y-Axis. Where: @y_i is the index of Y-Axis, @y_v is the value with respect to index of Y-Axis
                #NOTE: y_i represents each index of a set (return 0,1,2,3). y_v represent each value of a set(return "A", "B")
                y_dict = {} # Temporary storage for the any y dictionary
                for x_i, x_v in zip(range(len(y_v)+1), y_v):
                    # Traverse through each index, and value, within each y set.
                    y_dict.update({f"{x_i}": x_v}) # For any complete traverse, we want to turn them into dict-version. So, [2,3,5] => {0: 2, 1: 3, 2:5}
                # If any given x value has been appended within y_dict, add y_dict to init_dict as y=0, y=1, and so on.
                init_dict[f"{y_i}"] = y_dict # When traverse of X-Axis complete, we turn them into dict_version.
            return init_dict
        else:
            #NOTE: This part isn't much used btw.
            # When @s is a single-dimensional array
            for x_i, x_v in zip(range(len(s)+1), s):
                # Access each value of the each array
                init_dict.update({f"{x_i}": x_v})
            return init_dict
    
    # Read / Modify coordi(nate)
    def coord(s, x, y, proc=None, mod_v=None):
        """
        s = The set to be accessed. [Dict]
        x = The x-axis of the set. [Int]
        y = The y-axis of the set. [Int]
        proc = None | "modify" # If None, it will simply read the key. If "modify" it will read and replace the key with @mod_v
        mod_v # modified value = None | Any # If None, it will send an Error, since assuming you did "modify" as process, but does not give any value, is incomplete! If exist, then it will run a function _modify()
        """
        def _modify(x, y, t, v):
            """
            It is short. The only reason for me to make this function, is for the name to be much more intuitive.
            """
            y[f"{x}"] = v
        try:
            x_axis = f"{x}" # Eg. "1" will access (1,y)
            y_axis = s[f"{y}"] # Eg. "3" will access (x,3)
            target = y_axis[x_axis] # s["3"]["1"] will access (1,3)
            if proc == "modify" and mod_v:
                # If proc exist, and mod_v also exist. 
                return _modify(x_axis, y_axis, target, mod_v)   
            elif proc:
                # Sometimes, user may forgot to provide mod_v if proc is not given.
                raise Exception("[ERR] Value for param:mod_v is not given.")
            else:
                # Return the value itself.
                return target
        except:
            # Sometimes there are error such as, accessing coordinate beyond providede bound of @set. It should be ignored.
            pass

    # Create the map 
    def create_map(x, y, value):
        map_size = [] # This is map_size_y btw. 
        for size_y in range(prompt_size_y):
            # For every nth of y_axis, we're gonna add another array acting as map_size_x (of map_size_y[nth])
            map_size_x = []
            for any_x in range(prompt_size_x):
                # For each x of a nth of y_axis, we're gonna assert a value.
                map_size_x.append(value)
            # If the map_size_x is done, then add that to map_size/map_size_y
            map_size.append(map_size_x)
        return map_size
    # ---------------------- TEST PROGRAM ------------------------
    # dset = [["x","y","z","w","t","q"],
    #         ["a", "b", "c", "d", "e", "f"],
    #         [1, 2, 3, 4, 5, 6]]
    #
    # dict_dset = en_dict(dset) # Turn into dictionary
    #
    # log(dict_dset) # Print this
    #
    # # Go to (x,y)=(5,2), modify the value to "zaki gae"
    # coord(dict_dset, 2, 2, "modify", "wow!")
    #
    # log(dict_dset) # Print the modified result

    # -------------------- MINE SWEEPER --------------------
    prompt_size_x = int(input("Set map X-size : "))+1 # +1 because, _map will return the value of the prompt_size_x but minus 1.
    prompt_size_y = int(input("Set map Y-size : "))+1 # Same as well like above, but y.
    bombs_total = int(input("How many bombs exist in the map : ")) # A total of prompt_size_x * prompt_size_y is a good amount.
    _map = en_dict(create_map(prompt_size_x, prompt_size_y, ["#", "-"])) # For each value of each cell in the map. We want to ensure it has two value. [APPERANCE_VAL, ACTUAL_VAL]. @APPEARANCE_VAL is the value when you did not step into the cell. @ACTUAL_VAL is the value when you DID STEP into the cell, giving you the actual cell value.
    #NOTE: If you're wondering, why "#". Because to me, "#" appaers like a grass.
    
    # Generate Bombs
    bombs_coords = [] # self-explanatory
    for _ in range(bombs_total):
        # For any random (x between bound_x, y between bound_y), add BOMB_VALUE coords, ONLY WITHIN THAT MAP.
        random_x = int(random.randrange(0, prompt_size_x))
        random_y = int(random.randrange(0, prompt_size_y))
        bombs_coords.append([random_x, random_y])
        coord(_map, random_x, random_y, "modify", ["#","X"]) # For the bomb value. We set it as "X", giving the appearance of "#".
    
    # Track for any cells around bomb
    count_coords = {}
    for _bomb in bombs_coords:
        pos_x = _bomb[0]
        pos_y = _bomb[1]
        # The LMR defines the (x-1), (x), (x+1)
        # The TMB defines the (y-1), (y), (y+1)
        # Giving us 3^2 - 1 = 8 possible combination coords! The reason it is minus by 1, because MM is the coordinate of the bomb itself. So it does not count.
        """
        |  |  |  |    |LT|MT|RT|    |(x-1,y-1)|(x,y-1)|(x+1,y-1)|
        |  |XX|  | => |LM|XX|RM| => | (x-1,y) | (x,y) | (x+1,y) |
        |  |  |  |    |LB|MB|RB|    |(x-1,y+1)|(x,y+1)|(x+1,y+1)|
        """
        for dx in [-1, 0, 1]: # For any x-1, x, x+1
            for dy in [-1, 0, 1]: # For any y-1, y, y+1
                if dx == 0 and dy == 0: continue # If it's (x,y) or MM or the BOMB itself. Ignore.
                xy = f"{pos_x + dx}|{pos_y + dy}" # template (x,y)
                if not ([pos_x+dx, pos_y+dy] in bombs_coords): # We want to make sure that the pixel can be modified IF, there is also no bomb around around the radius. We do not want it to replace the BOMB_coordinate, with the COUNT later.
                    count_coords[xy] = count_coords.get(xy, 0) + 1 # This method says. Access count_coords[xy], if it has no value, then set it to 0. But if it does has a value, add +1. Credit: ChatGPT, no idea why this works lol.
        # LT = f"{pos_x-1}|{pos_y-1}"
        # LM = f"{pos_x-1}|{pos_y}"
        # LB = f"{pos_x-1}|{pos_y+1}"
        # MT = f"{pos_x}|{pos_y-1}"
        # MB = f"{pos_x}|{pos_y+1}"
        # RT = f"{pos_x+1}|{pos_y-1}"
        # RM = f"{pos_x+1}|{pos_y}"
        # RB = f"{pos_x+1}|{pos_y+1}"
        # Below code do this:
        # If there is no any bomb radius coordinate created before, then add 1 for that coordinate. 
        # But if there is bomb radius coordinate that conjoint withe coordinate to be added, then DO NOT ADD or SET.    
    
    # Positioning the 'count' with respect to its coordinate
    for count_coord in count_coords:
        # the pos_x and pos_y returns value template like "X|Y".
        pos_x = int(count_coord.split("|")[0])
        pos_y = int(count_coord.split("|")[1])
        value_count = count_coords.get(count_coord)
        coord(_map, pos_x, pos_y, "modify", ["#", int(value_count)]) # Modify the coordinate of any bomd radius, so it has an actual COUNT inside.
    
    # Displaying
    def display(Hint=None):
        index = 0 # Index X. the x is omitted btw.
        indexy = 0 # Index Y 
        show = 0 
        if Hint == "show": 
            show = 1
        else: 
            show = 0
        for y in range(prompt_size_y):
            if indexy>=10: # Incase the indexy, is more than or equal to 10, we remove one of the space. So in the terminal, it looks fit.
                sep = "| "
            else:
                sep = " | "
            print(f"{y}", end=sep)
            indexy+=1 # For each printed index, we add +1, so if hits 10 later in indexy, it will appear fit.
            for x in range(prompt_size_x): # Within Y, for each x 
                if index == 0: # Also like indexy, but for x pos 
                    if x>=10:
                        sep = "| "
                    else:
                        sep = " | "
                    print(f"{x}", end=sep)
                else:
                    # Handling the cell when COUNT is >= 10. So the separator look fit.
                    cell = coord(_map, x, y) 
                    if type(cell[show]) is int and cell[show] >= 10:
                        sep = "| "
                    elif type(cell[0]) is str:
                        sep = " | "
                    print(coord(_map, x, y)[show],end=sep)
            index+=1
            print()
    # Display Map:
    
    fail_detect = 0 # It can also act as a chance detection, by changing "fail_detect == <1>" -> <2> or any.
    score = 0 # Determined via the total of radis_count of any bomb you hit. 
    while True: # Repeating the UI. 
        if fail_detect == 1:
            display("show")
            break
        display()
        move = list(input("Go where (x,y): ").split(',')) # 3,2 will work. 3, 2 will not work. Be careful with spaces.
        step = coord(_map, int(move[0]), int(move[1])) # The step or pixel that we stepped unto
        if step[1] == "X": # Bomb
            print(f"You failed! You stepped on a landmine!\nScore: {score}")
            fail_detect = 1 # loser.
        elif step[1] == "-" or type(step[1]) is int: # Non-Bomb Element
            coord(_map, int(move[0]), int(move[1]), "modify", [step[1], step[1]]) # Now @APPEARANCE_VAL is either - or N, and so is @ACTUAL_VAL
            if type(step[1]) is int: score += step[1] # If the pixel/step has count step, add it to the score


if __name__ == "__main__":
        main()
