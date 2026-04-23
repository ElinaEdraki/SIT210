import tkinter as tk
from gpiozero import LED

living_room = LED(17)
closet = LED(22)
bathroom = LED(27)

def update_leds():
    living_room.off()
    bathroom.off()
    closet.off()
    
    # Turn on the selected light
    selection = room_var.get()
    if selection == 1:
        living_room.on()
    elif selection == 2:
        bathroom.on()
    elif selection == 3:
        closet.on()

def exit_app():
    living_room.off()
    bathroom.off()
    closet.off()
    root.destroy()

# Create the window
root = tk.Tk()
root.title("Linda's Light Controller")
root.geometry("300x200")

# Title label
tk.Label(root, text="Select a room to turn on the light", font=("Arial", 11)).pack(pady=10)

# Radio buttons
room_var = tk.IntVar()
tk.Radiobutton(root, text="Living Room", variable=room_var, value=1, command=update_leds).pack(anchor="w", padx=40)
tk.Radiobutton(root, text="Bathroom",    variable=room_var, value=2, command=update_leds).pack(anchor="w", padx=40)
tk.Radiobutton(root, text="Closet",      variable=room_var, value=3, command=update_leds).pack(anchor="w", padx=40)

# Exit button
tk.Button(root, text="Exit", command=exit_app).pack(pady=20)

root.mainloop()
