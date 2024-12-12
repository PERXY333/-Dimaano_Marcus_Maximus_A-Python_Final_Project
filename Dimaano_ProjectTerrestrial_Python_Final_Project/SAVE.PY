import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import pygame
import sqlite3

# Initialize Pygame mixer
pygame.mixer.init()

# SQLite Database setup
conn = sqlite3.connect("plants.db")
cursor = conn.cursor()
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
''')
conn.commit()

# Function to refresh table data
def refresh_table(tree):
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM plants")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

# Function to manage plant form
def open_form(tree, action, selected_item=None):
    form_window = tk.Toplevel(root)
    form_window.title(f"{action} Plant")
    form_window.geometry("400x400")
    form_window.configure(bg="black")

    plant_types = ["Seeds", "Plants", "Trees"]
    statuses = ["Pending", "Sold", "Trade", "Sell"]

    # Form fields
    tk.Label(form_window, text="Plant Type", font=("Arial", 12), bg="black", fg="white").pack(pady=5)
    plant_type_combobox = ttk.Combobox(form_window, values=plant_types, font=("Arial", 12))
    plant_type_combobox.pack(pady=5)

    tk.Label(form_window, text="Status", font=("Arial", 12), bg="black", fg="white").pack(pady=5)
    status_combobox = ttk.Combobox(form_window, values=statuses, font=("Arial", 12))
    status_combobox.pack(pady=5)

    labels = ["Owner", "Plant Name", "Amount", "Bundle"]
    entries = {}
    for label in labels:
        tk.Label(form_window, text=label, font=("Arial", 12), bg="black", fg="white").pack(pady=5)
        entry = tk.Entry(form_window, font=("Arial", 12))
        entry.pack(pady=5)
        entries[label] = entry

    if action == "Update" and selected_item:
        plant = tree.item(selected_item, "values")
        entries["Owner"].insert(0, plant[1])
        entries["Plant Name"].insert(0, plant[2])
        plant_type_combobox.set(plant[3])
        entries["Amount"].insert(0, plant[4])
        entries["Bundle"].insert(0, plant[5])
        status_combobox.set(plant[6])

    def submit_form():
        owner = entries["Owner"].get()
        plant_name = entries["Plant Name"].get()
        plant_type = plant_type_combobox.get()
        amount = entries["Amount"].get()
        bundle = entries["Bundle"].get()
        status = status_combobox.get()

        if not all([owner, plant_name, plant_type, amount, bundle, status]):
            messagebox.showerror("Error", "All fields must be filled!")
            return

        try:
            amount = int(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        if action == "Add":
            cursor.execute("""
                INSERT INTO plants (owner, plant_name, plant_type, amount, bundle, status)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (owner, plant_name, plant_type, amount, bundle, status))
            messagebox.showinfo("Success", "Plant added successfully!")
        elif action == "Update" and selected_item:
            plant_id = tree.item(selected_item, "values")[0]
            cursor.execute("""
                UPDATE plants
                SET owner = ?, plant_name = ?, plant_type = ?, amount = ?, bundle = ?, status = ?
                WHERE id = ?""",
                (owner, plant_name, plant_type, amount, bundle, status, plant_id))
            messagebox.showinfo("Success", "Plant updated successfully!")

        conn.commit()
        refresh_table(tree)
        form_window.destroy()

    tk.Button(form_window, text="Submit", font=("Arial", 14), bg="green", fg="white", command=submit_form).pack(pady=20)

# Other CRUD functions
def delete_plant(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No plant selected!")
        return
    plant_id = tree.item(selected_item, "values")[0]
    cursor.execute("DELETE FROM plants WHERE id = ?", (plant_id,))
    conn.commit()
    refresh_table(tree)
    messagebox.showinfo("Success", "Plant deleted successfully!")

def reset_id(tree):
    confirm = messagebox.askyesno("Confirm Reset ID", "Are you sure you want to reset the ID? All data will be lost!")
    if confirm:
        cursor.execute("DELETE FROM plants")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='plants'")
        conn.commit()
        refresh_table(tree)
        messagebox.showinfo("Success", "ID reset successfully. All data cleared.")

# Audio Functions
def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1, 0.0)

def play_sound(file_path):
    sound = pygame.mixer.Sound(file_path)
    sound.play()

# Main Application Structure
def main_menu():
    root.title("Project Terrestrial")
    root.geometry("1200x800")
    root.configure(bg="black")

    intro_frame = tk.Frame(root, bg="black")
    intro_frame.pack(fill="both", expand=True)

    main_menu_frame = tk.Frame(root, bg="black")
    title_label = tk.Label(main_menu_frame, text="PROJECT TERRESTRIAL", font=("Arial", 24, "bold"), fg="pink", bg="black")
    title_label.pack(pady=20)
    main_menu_frame.pack(fill="both", expand=True)

    # Buttons for navigation
    tk.Button(main_menu_frame, text="Go to Brazil!", font=("Arial", 14), command=lambda: None, bg="black", fg="white").pack(pady=20)
    tk.Button(main_menu_frame, text="Credits", font=("Arial", 14), command=lambda: None, bg="black", fg="white").pack(pady=10)
    tk.Button(main_menu_frame, text="Exit", font=("Arial", 14), command=root.quit, bg="black", fg="white").pack(pady=10)

# Application Execution
root = tk.Tk()
main_menu()
root.mainloop()
