import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pymongo import MongoClient

# Connect to MongoDB
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['health_records_jt']
    bmi_collection = db['bmi']
    bp_collection = db['blood_pressure']
except Exception as e:
    messagebox.showerror("Connection Error", f"Failed to connect to MongoDB: {e}")


# Function to save BMI data to MongoDB
def save_bmi_data():
    print("Save BMI Data function called")
    name = name_entry.get()
    age = age_entry.get()
    date_1 = date_1_entry.get()
    height = height_entry.get()
    weight = weight_entry.get()

    if not name or not age or not date_1 or not height or not weight:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        age = int(age)
        height = float(height)
        weight = float(weight)
    except ValueError:
        messagebox.showwarning("Input Error", "Age must be an integer, and height and weight must be numbers.")
        return

    # Save data to MongoDB
    try:
        bmi_record = {
            "name": name,
            "age": age,
            "date": date_1,
            "height": height,
            "weight": weight,
            "bmi": (weight*703) / (height*height*0.0254*0.0254)
        }
        bmi_collection.insert_one(bmi_record)
        save_button.config(text="Data Saved")
        messagebox.showinfo("Success", "Data saved successfully!")
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to save data: {e}")

    # Clear the entry fields
    # name_entry.delete(0, tk.END)
    # age_entry.delete(0, tk.END)
    date_1_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)


# Function to save blood pressure data to MongoDB
def save_bp_data():
    name = name_entry_bp.get()
    age = int(age_entry_bp.get())
    day_1 = day_1_entry.get()
    date_1 = date_1_entry_bp.get()
    time_1 = time_1_entry.get()
    systolic = int(systolic_entry.get())
    diastolic = int(diastolic_entry.get())
    arm = arm_entry.get()
    if systolic and diastolic:
        data = {
            "name": name,
            "age": age,
            "day": day_1,
            "date": date_1,
            "time": time_1,
            "systolic_bp": systolic,
            "diastolic_bp": diastolic,
            "arm": arm
        }
        bp_collection.insert_one(data)
        save_button_bp.config(text="Data Saved")  # use when submitting forms
        messagebox.showinfo("Success", "Data saved successfully!")
        # Clear the entry fields
        systolic_entry.delete(0, tk.END)
        diastolic_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter both systolic and diastolic values.")


# Create the main window
root = tk.Tk()
root.title("Health Data Collection")

# Create a style object
style = ttk.Style()

# Customize the tabs
style.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'), padding=[10, 10], background='lightblue')
style.map('TNotebook.Tab', background=[('selected', 'black')], foreground=[('selected', 'blue')])

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root, style='TNotebook')
notebook.grid(row=0, column=0, padx=10, pady=10)

# Create frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(tab1, text="BMI Form")
notebook.add(tab2, text="Blood Pressure Form")

# Create and place labels and entry widgets in tab1
tk.Label(tab1, text="Name:").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(tab1)
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(tab1, text="Age:").grid(row=1, column=0, padx=10, pady=10)
age_entry = tk.Entry(tab1)
age_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(tab1, text="Date:").grid(row=2, column=0, padx=10, pady=10)
date_1_entry = tk.Entry(tab1)
date_1_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(tab1, text="Height (cm):").grid(row=3, column=0, padx=10, pady=10)
height_entry = tk.Entry(tab1)
height_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(tab1, text="Weight (lbs):").grid(row=4, column=0, padx=10, pady=10)
weight_entry = tk.Entry(tab1)
weight_entry.grid(row=4, column=1, padx=10, pady=10)

# Create and place the save button in tab1
save_button = tk.Button(tab1, text="Save Data", command=save_bmi_data)
save_button.grid(row=5, column=0, columnspan=2, pady=10)

# Create and place labels and entry widgets in tab2
tk.Label(tab2, text="Name:").grid(row=0, column=0, padx=10, pady=10)
name_entry_bp = tk.Entry(tab2)
name_entry_bp.grid(row=0, column=1, padx=10, pady=10)

tk.Label(tab2, text="Age:").grid(row=1, column=0, padx=10, pady=10)
age_entry_bp = tk.Entry(tab2)
age_entry_bp.grid(row=1, column=1, padx=10, pady=10)

tk.Label(tab2, text="Day:").grid(row=2, column=0, padx=10, pady=10)
day_1_entry = tk.Entry(tab2)
day_1_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(tab2, text="Date:").grid(row=3, column=0, padx=10, pady=10)
date_1_entry_bp = tk.Entry(tab2)
date_1_entry_bp.grid(row=3, column=1, padx=10, pady=10)

tk.Label(tab2, text="Time:").grid(row=4, column=0, padx=10, pady=10)
time_1_entry = tk.Entry(tab2)
time_1_entry.grid(row=4, column=1, padx=10, pady=10)

tk.Label(tab2, text="Systolic:").grid(row=5, column=0, padx=10, pady=10)
systolic_entry = tk.Entry(tab2)
systolic_entry.grid(row=5, column=1, padx=10, pady=10)

tk.Label(tab2, text="Diastolic:").grid(row=6, column=0, padx=10, pady=10)
diastolic_entry = tk.Entry(tab2)
diastolic_entry.grid(row=6, column=1, padx=10, pady=10)

tk.Label(tab2, text="Arm (Left or Right):").grid(row=7, column=0, padx=10, pady=10)
arm_entry = tk.Entry(tab2)
arm_entry.grid(row=7, column=1, padx=10, pady=10)

# Create and place the save button in tab2
save_button_bp = tk.Button(tab2, text="Save Data", command=save_bp_data)
save_button_bp.grid(row=8, column=0, columnspan=2, pady=20)

# print(save_button.config().keys())
# Run the main event loop
root.mainloop()
