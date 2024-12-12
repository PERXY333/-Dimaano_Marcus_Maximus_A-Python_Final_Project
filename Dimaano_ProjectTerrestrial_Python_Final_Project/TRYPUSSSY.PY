import tkinter as tk
from PIL import Image, ImageTk

# Function to update the GIF when the button is clicked
def change_gif():
    # Load the new GIF (You can load different GIFs)
    new_gif = Image.open("DAD.gif")
    new_gif_tk = ImageTk.PhotoImage(new_gif)

    # Update the image in the label
    gif_label.config(image=new_gif_tk)
    gif_label.image = new_gif_tk  # Keep a reference to avoid garbage collection

# Set up the main window
root = tk.Tk()
root.title("GIF Change Example")
root.geometry("400x400")

# Load the initial GIF (You can load any GIF you like)
initial_gif = Image.open("LOL.gif")
initial_gif_tk = ImageTk.PhotoImage(initial_gif)

# Create a Label to display the GIF
gif_label = tk.Label(root, image=initial_gif_tk)
gif_label.pack(pady=20)

# Create a Button to trigger the GIF change
change_button = tk.Button(root, text="Change GIF", command=change_gif)
change_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
