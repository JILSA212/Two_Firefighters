import tkinter as tk

# Global Variables
t = 1
buttons_dict = {}
upper_range_row = 26
upper_range_column = 61
fire_color = "#ff0000"
fighter_color = "#000000"
initial_color = "#82e0aa"
font_color = "#ffffff"
fire_vertices = []
fighter_vertices = []
previous_fire = []
previous_fighters = []
current_fighters = []
row = 0
column = 0

def has_a_path(x1, y1, x2, y2):
    if(x1 == x2 and (x1, (y1 + y2)//2) not in fire_vertices):
        return True
    if(y1 == y2 and (y1, (x1 + x2)//2) not in fire_vertices):
        return True
    if((x1, y2) not in fire_vertices or (x2, y1) not in fire_vertices):
        return True
    else:
        return False



def button_clicked(row, column):
    print("Button clicked!")
    if((row, column) in fire_vertices):
        print("Fire block clicked")
        status_label.config(text="Firefighter can not walk on fire")
        return
    if((row, column) in fighter_vertices):
        print("Firefighter block clicked")
        status_label.config(text="Firefighter is already there")
        return
    if((row, column) in current_fighters):
        print("Firefighter from this round clicked")
        status_label.config(text="Already occupied by another fighter")
        return
    if(len(fighter_vertices) != 0):
        print("Valid block detected")
        # Only one fighter replaced
        if(len(current_fighters) == 0):
            print("First fighter placed")
            dist1 = abs(previous_fighters[0][0] - row) + abs(previous_fighters[0][1] - column)
            dist2 = abs(previous_fighters[1][0] - row) + abs(previous_fighters[1][1] - column)
            if(dist1 <= 2):
                if(dist1 < 2 or dist1 == 2 and has_a_path(previous_fighters[0][0], previous_fighters[0][1], row, column)):
                    print("Distance from first firefighter is valid")
                    button = buttons_dict[(row, column)]
                    button.config(bg=fighter_color)
                    button.config(fg=font_color)
                    button.config(text=str(t))
                    current_fighters.append((row, column))
                else:
                    print("Distance from first firefighter valid but path is not found")
                    status_label.config(text="No path available for firefighter")
                    return
            elif(dist2 <= 2):
                if(dist2 < 2 or dist2 == 2 and has_a_path(previous_fighters[1][0], previous_fighters[1][1], row, column)):
                    print("Distance from second firefighter is valid")
                    button = buttons_dict[(row, column)]
                    button.config(bg=fighter_color)
                    button.config(fg=font_color)
                    button.config(text=str(t))
                    current_fighters.append((row, column))
                else:
                    print("Distance from second firefighter valid but path is not found")
                    status_label.config(text="No path available for firefighter")
                    return
            else:
                print("Distance from both firefighter invalid")
                status_label.config(text="Firefighter can only travel 2 blocks")
                return
        # Two firefighters placed
        else:
            print("Second firefighter placed")
            current_fighters.append((row, column))

            # Checking if we have more than 2 firefighters
            if(len(current_fighters) > 2):
                (wrong_x, wrong_y) = current_fighters.pop(0)
                button = buttons_dict[(wrong_x, wrong_y)]
                button.config(bg=initial_color)
                button.config(fg="black")
                button.config(text="")

            # Pair 1
            dist1 = abs(previous_fighters[0][0] - current_fighters[0][0]) + abs(previous_fighters[0][1] - current_fighters[0][1])
            dist2 = abs(previous_fighters[1][0] - current_fighters[1][0]) + abs(previous_fighters[1][1] - current_fighters[1][1])
            print("Checking pair 1-1, 2-2")
            if(dist1 <= 2 and dist2 <= 2):
                if(dist1 < 2 or dist1 == 2 and has_a_path(previous_fighters[0][0], previous_fighters[0][1], current_fighters[0][0], current_fighters[0][1])):
                    if(dist2 < 2 or dist2 == 2 and has_a_path(previous_fighters[1][0], previous_fighters[1][1], current_fighters[1][0], current_fighters[1][1])):
                        print("All conditions fulfilled, placing firefighter")
                        button = buttons_dict[((row, column))]
                        button.config(bg=fighter_color)
                        button.config(fg=font_color)
                        button.config(text=str(t))
                        return
            # Pair 2
            dist1 = abs(previous_fighters[1][0] - current_fighters[0][0]) + abs(previous_fighters[1][1] - current_fighters[0][1])
            dist2 = abs(previous_fighters[0][0] - current_fighters[1][0]) + abs(previous_fighters[0][1] - current_fighters[1][1])
            print("Checking pair 1-2, 2-1")
            if(dist1 <= 2 and dist2 <= 2):
                if(dist1 < 2 or dist1 == 2 and has_a_path(previous_fighters[1][0], previous_fighters[1][1], current_fighters[0][0], current_fighters[0][1])):
                    if(dist2 < 2 or dist2 == 2 and has_a_path(previous_fighters[0][0], previous_fighters[0][1], current_fighters[1][0], current_fighters[1][1])):
                        print("All conditions fulfilled, placing firefighter")
                        button = buttons_dict[((row, column))]
                        button.config(bg=fighter_color)
                        button.config(fg=font_color)
                        button.config(text=str(t))
                        return

            current_fighters.pop()        
            print("No valid distance from any firefighter")
            status_label.config(text="Firefighter can only travel 2 blocks")
            return
    else:
        print("No firefighter to measure distance")
        print("Row: ", row)
        print("Column: ", column)
        button = buttons_dict[((row, column))]
        button.config(bg=fighter_color)
        button.config(fg=font_color)
        button.config(text=str(t))
        current_fighters.append((row, column))
        if(len(current_fighters) > 2):
            (x, y) = current_fighters.pop(0)
            button = buttons_dict[(x, y)]
            button.config(bg=initial_color)
            button.config(fg="black")
            button.config(text="")
            



def next_turn():
    print("Next Turn")

    global fire_vertices
    global fighter_vertices
    global current_fighters
    global previous_fire
    global previous_fighters
    global t

    if(len(current_fighters) < 2):
        status_label.config(text="Pick two firefighter positions")
    else:
        new_fire = []
        for (fire_x, fire_y) in previous_fire:
            if(fire_x - 1 < 0 or fire_y - 1 < 0 or fire_x + 1 > upper_range_row or fire_y + 1 > upper_range_column):
                print("Fire has reach the boundary")
                status_label.config(text="Fire is out of control now")
                return
            if((fire_x - 1, fire_y) not in (fire_vertices + fighter_vertices + current_fighters)):
                new_fire.append((fire_x - 1, fire_y))
            if((fire_x, fire_y - 1) not in (fire_vertices + fighter_vertices + current_fighters)):
                new_fire.append((fire_x, fire_y - 1))
            if((fire_x + 1, fire_y) not in (fire_vertices + fighter_vertices + current_fighters)):
                new_fire.append((fire_x + 1, fire_y))
            if((fire_x, fire_y + 1) not in (fire_vertices + fighter_vertices + current_fighters)):
                new_fire.append((fire_x, fire_y + 1))
        if(len(new_fire) == 0):
            status_label.config(text="Fire is contained, You won!")
            return
        else:
            for (fire_x, fire_y) in new_fire:
                button = buttons_dict[(fire_x, fire_y)]
                button.config(text=t)
                button.config(bg=fire_color)
            fire_vertices = fire_vertices + new_fire
            for (fighter_x, fighter_y) in current_fighters:
                button = buttons_dict[(fighter_x, fighter_y)]
                button.config(text=t)
                button.config(bg=fighter_color)
                button.config(fg=font_color)
                fighter_vertices.append((fighter_x, fighter_y))
            previous_fire = new_fire.copy()
            previous_fighters = current_fighters.copy()
            current_fighters = []
        t += 1


root = tk.Tk()
root.title("Distance Restricted Firefighting Problem - 2 Firefighters, 2 distance")

# Create a square grid of buttons
for i in range(upper_range_row):
    for j in range(upper_range_column):
        # button = tk.Button(root, text=f"Button {i},{j}", width=5, height=2, command=lambda i=i, j=j: button_clicked(i, j))
        button = tk.Button(root, text="", width=1, height=1, command=lambda i=i, j=j: button_clicked(i, j))
        button.grid(row=i, column=j, padx=1, pady=1)
        button.config(bg=initial_color)
        buttons_dict[(i, j)] = button

# Create a frame for the bottom row
bottom_frame = tk.Frame(root)
bottom_frame.grid(row=upper_range_row, column=0, columnspan=upper_range_column, sticky="ew")

# Create a label in the bottom row
status_label = tk.Label(bottom_frame, text="You are doing great", borderwidth=1, relief="solid")
status_label.pack(side="left", fill="x", expand=True)

# Create a button in the bottom row
button = tk.Button(bottom_frame, text="Submit", command=next_turn)
button.pack(side="right", padx=5, pady=5)


mid_point_x = upper_range_row // 2
mid_point_y = upper_range_column // 2
fire_source = buttons_dict[(mid_point_x, mid_point_y)]
fire_source.config(bg=fire_color)
# fire_source.config(state="disabled")
fire_vertices.append((mid_point_x, mid_point_y))
previous_fire.append((mid_point_x, mid_point_y))

root.mainloop()