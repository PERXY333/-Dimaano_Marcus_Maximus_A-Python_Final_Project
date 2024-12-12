#===============================================================================================================================#
#                                        MARCUS MAXIMUS A. DIMAANO, BSIT 2101 PROJECT                                           #
#===============================================================================================================================#                            

import tkinter as tk            #THIS IS ALL THE IMPORTS THAT WILL SUPPORT THE
from tkinter import messagebox    #STRUCTURE OF MY PROJECT
from PIL import Image, ImageTk      #in partnership with Keil Rizher Valida
import pygame
import sqlite3
from tkinter import ttk


#================================================================================================================================#
#                                                  START OF THE PROJECT                                                          #
#================================================================================================================================# 

#THIS WILL INITIALIZE ALL THE SOUND WITHIN THIS PROJECT
pygame.mixer.init()

conn = sqlite3.connect("plants.db") #   <--A WAY TO CONNECT TO THE SQL AND DATABASE
cursor = conn.cursor()

                                      

#=================================================================================================================================#
#                                           TABLE OF DATABASE AND ITS FUNCTIONS                                                   #
#=================================================================================================================================#
cursor.execute('''
CREATE TABLE IF NOT EXISTS plants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner TEXT NOT NULL,                         
    plant_name TEXT NOT NULL,
    plant_type TEXT NOT NULL,
    amount INTEGER NOT NULL,
    bundle TEXT NOT NULL,
    status TEXT NOT NULL
)
''')                          #<----- THE OVERALL TABLE OF MY DATABASE
conn.commit()


def refresh_table(tree):
    for row in tree.get_children():            #<-- THIS IS MY FUNCTION IN ORDER TO REFRESH MY TABLE
        tree.delete(row)
    cursor.execute("SELECT * FROM plants")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, 
                    values=row
                    )


def open_form(tree, action, 
              selected_item=None
              ):
    form_window = tk.Toplevel(root)
    form_window.title(f"{action} Plant")           #<--- MY WINDOW AFTER CLICKING OR EDITING THE PLANT
    form_window.geometry("400x600")
    form_window.configure(bg="black")

    # Dropdown options for "Plant Type" and "Status"
    plant_types = ["Seeds", "Plants", "Trees"]
    statuses = ["Pending", "Sold", "Trade", "Sell"]         #<---- DROPDOWN OPTIONS FOR THE TYPE AND STATUS OF THE PLANT 

    
    plant_type_label = tk.Label(form_window, 
                                text="Plant Type", 
                                font=("Arial", 12),         #<-----LABEL FOR THE PLANT TYPE
                                bg="black", fg="white"
                                )
    plant_type_label.pack(pady=5)
   
    plant_type_combobox = ttk.Combobox(form_window, 
                                       values=plant_types,    #<----- THE DISPLAY OF COMBOBOX FROM THE PLANT TYPE
                                       font=("Arial", 12)
                                       )
    plant_type_combobox.pack(pady=5)

     
    status_label = tk.Label(form_window, 
                            text="Status",                      #<-------LABEL FOR STATUS
                            font=("Arial", 12), 
                            bg="black", 
                            fg="white"
                            )
    status_label.pack(pady=5)
    
    status_combobox = ttk.Combobox(form_window, 
                                   values=statuses,             #<-----STATUS'S COMBOBOX
                                   font=("Arial", 12))
    status_combobox.pack(pady=5)

    
    labels = ["Owner", "Plant Name", "Amount", "Bundle"]
    entries = {}                                               #<----- LABEL OF THE REST, SINCE THEY'RE ALL ENTRIES 
    for i, label in enumerate(labels):                               #SINCE THEY'RE SIMILAR, I JUST COMPILE THEM
        tk.Label(form_window, 
                 text=label, 
                 font=("Arial", 12), 
                 bg="black", 
                 fg="white").pack(pady=5)
        
        entry = tk.Entry(form_window, 
                         font=("Arial", 12)                   #<------THE FUNCTION OF WHITE BOX WHERE YOU'LL WRITE       
                         )
        entry.pack(pady=5)
        entries[label] = entry


    if action == "Update" and selected_item:
        plant = tree.item(selected_item, "values")                   #<----IT POPULATES THE ENTRIES IF GOT UPDATED
        

        entries["Owner"].insert(0, plant[1]) 
        entries["Plant Name"].insert(0, plant[2])  
        plant_type_combobox.set(plant[3])                     #<------- THIS MAKE THE INSERT IN PROPER ORDER, TO AVOID CONFUSION
        entries["Amount"].insert(0, plant[4])                          #          UPON DISPLAYING THE INPUT DATA
        entries["Bundle"].insert(0, plant[5])  
        status_combobox.set(plant[6])  

    # Submit button
    def submit_form():
        owner = entries["Owner"].get()
        plant_name = entries["Plant Name"].get()                 #<------ THE SUBMIT AND ITS FUNCTIONS, THIS WILL ENSURE TO PUT
        plant_type = plant_type_combobox.get()                          #          THE CORRECT DATA THAT WAS WRITTEN
        amount = entries["Amount"].get()
        bundle = entries["Bundle"].get()
        status = status_combobox.get()
#==================================================================================================================================#
#                                          FUNCTIONS OF THE SUBMIT, ADD AND UPDATE BUTTON                                          #
#==================================================================================================================================#
        if not (owner and plant_name and plant_type and amount and bundle and status):
            messagebox.showerror("Error", "All fields must be filled!")
            return

        try:
            amount = int(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        if action == "Add":
            cursor.execute(
                "INSERT INTO plants (owner, plant_name, plant_type, amount, bundle, status) VALUES (?, ?, ?, ?, ?, ?)",
                (owner, 
                 plant_name, 
                 plant_type, 
                 amount, 
                 bundle, 
                 status
                 )
            )
            messagebox.showinfo("Success", "Plant added successfully!")
        elif action == "Update" and selected_item:
            plant_id = tree.item(selected_item, 
                                 "values"
                                 )[0]
            cursor.execute(
                """
                UPDATE plants
                SET owner = ?, plant_name = ?, plant_type = ?, amount = ?, bundle = ?, status = ?
                WHERE id = ?
                """,
                (owner, 
                 plant_name, 
                 plant_type, 
                 amount, 
                 bundle, 
                 status, 
                 plant_id
                 )
            )
            messagebox.showinfo("Success", 
                                "Plant updated successfully!"
                                )

        conn.commit()
        refresh_table(tree)
        form_window.destroy()
#==================================================================================================================================#
#                                                END OF SUBMIT,ADD AND UPDATE FUNCTION                                             #
#==================================================================================================================================#
    tk.Button(form_window, 
              text="Submit", 
              font=("Arial", 14),                           #<--- BUTTON FOR THE SUBMIT
              bg="green", 
              fg="white", 
              command=submit_form).pack(pady=20)

#==================================================================================================================================#
#                                                   START OF THE DELETE FUNCTION                                                   #
#==================================================================================================================================#

def delete_plant(tree): 
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", 
                             "No plant selected!"
                             )
        return

    plant_id = tree.item(selected_item, "values")[0]
    cursor.execute("DELETE FROM plants WHERE id = ?", 
                   (plant_id,)
                   ) 
    conn.commit()
    
    refresh_table(tree)
    messagebox.showinfo("Success",f"Plant with ID {plant_id} is sold successfully."
                        )
#==================================================================================================================================#
#                                                  END OF THE DELETE FUNCTION                                                      #
#==================================================================================================================================#


#==================================================================================================================================#
#                                                    START OF RESET ID FUNCTION                                                    #
#==================================================================================================================================#

def reset_id(tree):
    confirm = messagebox.askyesno("Confirm Reset ID", 
                                  "Are you sure you want to reset the ID? All data will be lost, and IDs will start from 1."
                                  )
    if confirm:
        cursor.execute("DELETE FROM plants")  # Delete all rows
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='plants'")  # Reset the ID sequence
        conn.commit()
        refresh_table(tree)
        messagebox.showinfo("Success", 
                            "ID reset successfully. All data has been cleared, and IDs will start from 1."
                            )
#==================================================================================================================================#
#                                                     END OF RESET ID FUNCTION                                                     #
#==================================================================================================================================#




#==================================================================================================================================#
#                                                 MAIN WINDOW(MENU,LOGO, AND STARTUP)                                              #
#==================================================================================================================================#    



def play_original_background_music():
    pygame.mixer.music.load("jazz2.mp3")                     # <------THE OFFICIAL THEME OF MY PROJECT
    pygame.mixer.music.play(-1, 0.0)


def play_about_us_music():
    pygame.mixer.music.load("Tokyo.mp3")                       # <-------CREDITS THEME
    pygame.mixer.music.play(-1, 0.0)


def play_brazil_sound():
    brazil_sound = pygame.mixer.Sound("BRAZIL.mp3")           # <-------SOUND EEFECT WHEN THE GO TO BRAZIL IS CLICKED
    brazil_sound.play()

def play_special_brazil_sound():
    special_sound = pygame.mixer.Sound("NOOOO.mp3")           # <-------SOUND EEFECT WHEN THE GO TO BRAZIL IS CLICKED
    special_sound.play()
    pygame.mixer.music.stop()



def transition_after_sound():
    play_special_brazil_sound()                              
    play_brazil_sound()                                      # <-------TRANSITION TO THE SECOND WINDOW
    replace_gif_for_brazil()
    root.after(9000, show_new_frame_and_play_music)



def replace_gif_for_brazil(): 
    global gif_label, frames                                         # <-------TRANSITION OF THE GIF WHEN THE BRAZIL IS CLICKED
    brazil_gif_frames = [tk.PhotoImage(file="FA.gif", format=f"gif -index {i}") for i in range(10)]
    frames = brazil_gif_frames


    def update_brazil_gif(frame_index=0):
        frame = frames[frame_index]                        # <------FUNCTION TO ANIMATE replace_gif__for_brazil()
        gif_label.configure(image=frame)
        next_frame_index = (frame_index + 1) % len(frames)
        root.after(100, 
                   update_brazil_gif, 
                   next_frame_index
                   )  

    update_brazil_gif() 
#==================================================================================================================================#
#                                                            CREDITS                                                               #
#==================================================================================================================================#

def show_credits():
    about_us_sound = pygame.mixer.Sound("CJ.mp3")
    about_us_sound.play()                                  # <------SOUND EFFECT FOR CREDITS
    pygame.mixer.music.stop()
   
    sound_duration = about_us_sound.get_length() 
    root.after(int(sound_duration * 1000),
               transition_to_credits
               )                                          # <------DURATION BEFORE TRANSSITIONING TO CREDITS

def transition_to_credits():                              # <------FUNCTION FOR CHANGING THE THEME FOR THE CREDITS
    play_about_us_music()  

    main_menu_frame.pack_forget()  
    credits_frame = tk.Frame(root, 
                             bg="black"
                             )                            # <------CREDITS FRAME
    play_about_us_music()  
    credits_frame.pack(fill="both", 
                       expand=True
                       )

    # Create a Frame for the Credits
    credits_text_frame = tk.Frame(credits_frame,          # <------ALSO CREDITS FRAME
                                  bg="black", 
                                  width=600, 
                                  height=800, 
                                  relief="solid"
                                  )
   
    credits_text_frame.pack(side="left", 
                            padx=20, 
                            fill="both", 
                            expand=True
                            )


    gif_frame = tk.Frame(credits_frame, 
                         bg="black",                       # <------THE GIF USED IN THE CREDITS AT THE OPPOSITE SIDE
                         width=600, 
                         height=800, 
                         relief="solid"
                         )
    
    gif_frame.pack(side="right", 
                   padx=20, 
                   fill="both", 
                   expand=True
                   )

   
    canvas = tk.Canvas(credits_text_frame, 
                       bg="black",                         # <------CANVAS ON THE CREDITS
                       highlightthickness=0
                       )
    canvas.pack(fill="both",
                expand=True
                )

    back_button = tk.Button(credits_frame,
                            text="Back to Menu",
                            font=("Arial", 14),
                            command=lambda: back_to_menu(credits_frame),      # <------BUTTON FOR GOING BACK TO THE MAIN MENU
                            bg="black",
                            fg="white"
                            )
    
    back_button.place(relx=0.5, 
                      rely=0.1, 
                      anchor="center"
                      )

    text_frame = tk.Frame(canvas, 
                          bg="black"
                          )
    
    canvas.create_window(0, 
                         0, 
                         anchor="nw", 
                         window=text_frame
                         )

    credits = [
        "PROJECT TERRESTRIAL",
        "Developed by MARCUS POGI.INC",
        "",
        "EDITOR:",
        "MARCUS MAXIMUS A. DIMAANO",
        "",                                                               # <------THE CREDITS
        "TECHNICIAN:",
        "MARCUS MAXIMUS A DIMAANO",
        "",
        "Background Music:",
        "PLANTS VS ZOMBIE ORG THEME",
        "",
        "I HOPE YOU ENJOY MY PROJECT!",
        "",
        "Copyright © 2024"
    ]

    for line in credits:
        tk.Label(text_frame, 
                 text=line, 
                 font=("Arial", 18), 
                 fg="white", bg="black").pack(pady=5)

    text_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    
    frames = [tk.PhotoImage(file="LOL.gif", format=f"gif -index {i}") for i in range(10)]    # <------THE GIF USED IN CREDITS
    gif_label = tk.Label(gif_frame, bg="black")
    gif_label.pack(pady=300)

   
    def update_gif(frame_index=0):
        frame = frames[frame_index]
        gif_label.configure(image=frame)
        next_frame_index = (frame_index + 1) % len(frames)                        # <------GIF ANNIMATION AREA
        root.after(100, 
                   update_gif, 
                   next_frame_index
                   )  
    update_gif()  

    def roll():
        canvas.yview_scroll(-1, "units")
        if canvas.bbox("all")[3] > 0:
            root.after(50, roll)

    roll()

def back_to_menu(frame_to_destroy):
    frame_to_destroy.pack_forget()                                               # <------BACK TO MENU MENU FUNCTION
    main_menu_frame.pack(fill="both", 
                         expand=True
                         )
    play_original_background_music()  # Revert to the original background music
#==================================================================================================================================#
#                                                         END OF CREDITS                                                           #
#==================================================================================================================================#


#==================================================================================================================================#
#                                                           MAIN MENU                                                              #
#==================================================================================================================================#
def exit_app():
    pygame.mixer.music.stop()                                    # <------EXICUTES END TASK OF MY PROJECT
    root.destroy()


def show_second_intro():
    intro_label.configure(text="PROJECT TERRESTRIAL!")           # <------SECOND INTRO LABELS
    root.after(8000, 
               show_main_menu
               )


def show_main_menu():
    intro_frame.pack_forget()                                   # <------MAIN MENU
    main_menu_frame.pack(fill="both", 
                         expand=True
                         )


def display_second_photo():
    global second_image, photo_label
    second_image = Image.open("NIP.png").convert("RGBA")       # <------FUNCTIONS AFTER THE FIRST PHOTO HAS FADED
    second_tk_image = ImageTk.PhotoImage(second_image)
    photo_label.config(image=second_tk_image)
    photo_label.image = second_tk_image
    photo_label.pack(pady=20)
    root.after(8000, 
               show_second_intro
               )

def fade_out_photo(alpha=255):
    if alpha > 0:
        faded_image = intro_image.copy()
        faded_image.putalpha(alpha)
        faded_tk_image = ImageTk.PhotoImage(faded_image)      # <------FUNCTION TO FADE THE PHOTO
        photo_label.config(image=faded_tk_image)
        photo_label.image = faded_tk_image
        root.after(50, 
                   fade_out_photo,
                   alpha - 15
                   )
    else:
        display_second_photo()


def display_intro_photo():
    global intro_image, photo_label
    intro_image = Image.open("DAD.png").convert("RGBA")
    intro_tk_image = ImageTk.PhotoImage(intro_image)
    photo_label = tk.Label(intro_frame,                     # <------FUNCTIONS FOR DISPLAYING THE FIRST PHOTO IN THE INTRO
                           image=intro_tk_image, 
                           bg="black"
                           )
    photo_label.image = intro_tk_image
    photo_label.pack(pady=20)
    root.after(9000, 
               fade_out_photo
               )


def update_gif(frame_index=0):
    global frames
    frame = frames[frame_index]
    gif_label.configure(image=frame)
    next_frame_index = (frame_index + 1) % len(frames)      # <------FUNCTIONS FOR ANITMATING THE GIF
    root.after(100, 
               update_gif, 
               next_frame_index
               )
#==================================================================================================================================#
#                                                   END OF THE PARTS OF  MAIN MENU                                                 #
#==================================================================================================================================#



#==================================================================================================================================#
#                                                           SECOND WINDOW                                                          #
#==================================================================================================================================#


def back_to_main_menu(second_frame):
    second_frame.pack_forget()                              # <------BACK TO THE MENU AND FUNCTIONS FOR REVERTING THE BG          
    main_menu_frame.pack(fill="both",                                #            AFTER CLICKING THE BUTTON
                         expand=True
                         ) 
    play_original_background_music()  


def play_new_music():
    pygame.mixer.music.load("FAHAA.mp3")
    pygame.mixer.music.play(-1, 0.0)

def toggle_fullscreen(event=None):
    is_fullscreen = root.attributes('-fullscreen')         #<------FUCNTION FOR FULLSCREEN(ABANDONED, I CANNOT WORK THIS OUT)  
    root.attributes('-fullscreen',
                    not is_fullscreen
                    )

def show_second_frame():
    main_menu_frame.pack_forget()

    
    second_frame = tk.Frame(root,  
                            bg="black"
                            )                              #<------SECOND FRAME BACKGROND AND SOME STUFF   
    second_frame.pack(fill="both", 
                      expand=True
                      )


    ongoing_label = tk.Label(second_frame,
                             text="Terrestrial Management is Ongoing",   #<------THE SECOND WINDOW TITLE 
                             font=("Arial", 24, "bold"),
                             fg="white",
                             bg="black"
                            )
    ongoing_label.pack(pady=50)


    columns = ("ID", 
               "Owner", 
               "Plant Name",                                             #<------THE TABLE CONTENTS
               "Plant Type", 
               "Amount", 
               "Bundle", 
               "Status"
               )
    
    tree = ttk.Treeview(second_frame,
                        columns=columns, 
                        show="headings", 
                        height=15
                        )                                                #<------THE SECOND FRAME HEADING
   
    tree.pack(fill="both", 
              expand=True, 
              padx=20, 
              pady=20
              )


    for col in columns:
        tree.heading(col,
                     text=col
                     )                                                   #<------COLUMN FUNCTIONS
        tree.column(col, width=100,                                       
                    anchor="center"
                    )

    # Fetch data from the database and display it
    refresh_table(tree)
#==================================================================================================================================#
#                                                       SECOND WINDOW(TABLE) BUTTONS                                               #
#==================================================================================================================================#
 

    tk.Button(second_frame, 
              text="Add Plant",
              font=("Arial", 14), 
              bg="green", 
              fg="white",
              command=lambda: open_form(tree, 
                                        "Add"
                                        )).pack(side="left", 
                                                           padx=10
                                                           )
    tk.Button(second_frame, 
              text="Update Plant", 
              font=("Arial", 14), 
              bg="blue",
              fg="white",
              command=lambda: open_form(tree,
                                        "Update",
                                        tree.selection()
                                        )).pack(side="left", 
                                                            padx=10
                                                            )
    tk.Button(second_frame, 
              text="BUY",
              font=("Arial", 14), 
              bg="red", 
              fg="white", 
              command=lambda: delete_plant(tree
                                           )).pack(side="left", 
                                                       padx=10
                                                       )
    tk.Button(second_frame, 
              text="Reset ID", 
              font=("Arial", 14), 
              bg="orange", 
              fg="white", 
              command=lambda: reset_id(tree
                                       )).pack(side="left", 
                                                   padx=10
                                                   )
    bottom_button_frame = tk.Frame(second_frame, bg="black")
    bottom_button_frame.pack(side="bottom", fill="x", pady=20)

    
    
    
    # "Back to Main Menu" button
    back_button = tk.Button(
        bottom_button_frame,
        text="Back to Main Menu",
        font=("Arial", 
              14
              ),
        command=lambda: back_to_main_menu(second_frame
                                         ),
        bg="black",
        fg="white"
    )
    back_button.pack(pady=10)
#==================================================================================================================================#
#                                                 END OF THE SECOND WINDOW(TABLE) BUTTION                                          #
#==================================================================================================================================#    
    

def show_new_frame_and_play_music():
    play_new_music()                                                    #<------COLUMN FUNCTIONS
    show_second_frame()  
    
    
def toggle_fullscreen(event=None):
    is_fullscreen = root.attributes('-fullscreen')                       #<------FULLSCREEN FUNCTION(ABANDONED, DIDNT WORK)
    root.attributes('-fullscreen', 
                    not is_fullscreen
                    )
    root.bind("<F11>",
              toggle_fullscreen
              )  


#==================================================================================================================================#
#                                                    CONTINUANCE OF THE MAIN MENU                                                  #
#==================================================================================================================================#
root = tk.Tk()
root.title("Project Terrestrial")
root.configure(bg="black")
root.geometry("1200x1800")                                         #<------TITLE OF THE PROJECT


intro_frame = tk.Frame(root, 
                       bg="black"
                       )                                           #<------FRAME OF THE MAIN MENU
intro_frame.pack(fill="both",
                 expand=True
                 )
play_original_background_music()
display_intro_photo()


intro_label = tk.Label(
    intro_frame,
    text="MARCUS POGI PRESENTS",                                     #<------FIRST LABEL INTRO 
    font=("Arial", 
          24, "bold"
          ),
    fg="white",
    bg="black"
)
intro_label.pack(pady=50)


root.after(9000, 
           show_second_intro                                      #<-----DURATION OF THE LABEL BEFORE TRANSITIONING
           )


main_menu_frame = tk.Frame(root,
                           bg="black"
                           )

title_label = tk.Label(
    main_menu_frame,
    text="PROJECT TERRESTRIAL",                                    #<------TITLE INTRO ON THE MAIN MENU
    font=("Arial", 
          24, "bold"
          ),
    fg="pink",
    bg="black"

)
title_label.pack(pady=20)

frames = [tk.PhotoImage(file="DEEZ.gif",
                        format=f"gif -index {i}") for i in range(10)]        #<------GIF IN THE MAIN MENU

gif_label = tk.Label(main_menu_frame, 
                     bg="black"
                     )
gif_label.pack(pady=10)

update_gif()

frame = tk.Frame(main_menu_frame, 
                 bg="black"                                                  #<------MAIN MENU FRAME
                 )
frame.pack(pady=10)
#==================================================================================================================================#
#                                                          MAIN MENU BUTTONS                                                       #
#==================================================================================================================================#
display_button = tk.Button(frame, 
                           text="GO TO BRAZIL!", 
                           font=("Arial", 14),                          
                           command = transition_after_sound,
                           bg="black", 
                           fg="white"
                           )
display_button.pack(pady=20)


credits_button = tk.Button(frame, 
                           text="CREDITS!", 
                           font=("Arial", 14),
                           command=show_credits,
                           bg="black",
                           fg="white"
                           )
credits_button.pack(side="top",
                    padx=20, 
                    pady=10
                    )


exit_button = tk.Button(frame, 
                        text="EXIT!", 
                        font=("Arial", 14), 
                        command=exit_app,
                        bg="black", 
                        fg="white"
                        )

exit_button.pack(side="top", 
                 padx=20, 
                 pady=10
                 )
#==================================================================================================================================#
#                                                     END OF THE MAIN MENU BUTTONS                                                 #
#==================================================================================================================================#
    
root.mainloop()
#==================================================================================================================================#
#                                                END OF THE PROGRAM, END OF THE PROJECT                                            #
#==================================================================================================================================#

#in partnership with Keil Rizher Valida