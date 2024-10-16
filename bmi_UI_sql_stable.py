import sqlite3
from tkinter import *
from tkinter import messagebox

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('bmi_database.db')
c = conn.cursor()

# Create table to store user information
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             age INTEGER,
             weight REAL,
             weight_unit TEXT,
             height REAL,
             height_unit TEXT,
             bmi REAL)''')

def calculate_bmi(weight, height, weight_unit, height_unit):
    # Convert weight to kg if necessary
    if weight_unit == "lbs":
        weight = weight * 0.453592
    elif weight_unit != "kg":
        raise ValueError("Invalid weight unit. Use 'kg' or 'lbs'.")

    # Convert height to meters if necessary
    if height_unit == "inches":
        height = height * 0.0254
    elif height_unit == "feet":
        height = height * 0.3048
    elif height_unit == "cm":
        height = height / 100
    elif height_unit != "meters":
        raise ValueError("Invalid height unit. Use 'meters', 'feet', 'cm', or 'inches'.")

    # Calculate BMI
    bmi = weight / (height ** 2)
    return bmi

def submit_info():
    name = entry_name.get()
    age = int(entry_age.get())
    weight = float(entry_weight.get())
    weight_unit = weight_unit_var.get()
    height = float(entry_height.get())
    height_unit = height_unit_var.get()

    try:
        bmi = calculate_bmi(weight, height, weight_unit, height_unit)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    # Insert user data into the database
    c.execute('''INSERT INTO users (name, age, weight, weight_unit, height, height_unit, bmi)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (name, age, weight, weight_unit, height, height_unit, bmi))
    conn.commit()

    bmi_result_label.config(text=f"{name}, your BMI is {bmi:.2f}")

# Create the main window
root = Tk()
root.title("BMI Calculator")

# Create and place the labels and entry widgets
Label(root, text="Name:").grid(row=0, column=0)
entry_name = Entry(root)
entry_name.grid(row=0, column=1)

Label(root, text="Age:").grid(row=1, column=0)
entry_age = Entry(root)
entry_age.grid(row=1, column=1)

Label(root, text="Weight:").grid(row=2, column=0)
entry_weight = Entry(root)
entry_weight.grid(row=2, column=1)

Label(root, text="Weight Unit:").grid(row=3, column=0)
weight_unit_var = StringVar(value="kg")
weight_unit_menu = OptionMenu(root, weight_unit_var, "kg", "lbs")
weight_unit_menu.grid(row=3, column=1)

Label(root, text="Height:").grid(row=4, column=0)
entry_height = Entry(root)
entry_height.grid(row=4, column=1)

Label(root, text="Height Unit:").grid(row=5, column=0)
height_unit_var = StringVar(value="meters")
height_unit_menu = OptionMenu(root, height_unit_var, "meters", "feet", "cm", "inches")
height_unit_menu.grid(row=5, column=1)

# Create and place the submit button
Button(root, text="Submit", command=submit_info).grid(row=6, column=0, columnspan=2)

# Label to display BMI result
bmi_result_label = Label(root, text="")
bmi_result_label.grid(row=7, column=0, columnspan=2)

# Run the main loop
root.mainloop()

# Close the database connection when done
conn.close()
