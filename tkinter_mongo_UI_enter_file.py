import json
import os
import pymongo
from pymongo import MongoClient
import tkinter as tk
from tkinter import filedialog, messagebox


def upload_json():
    # Open file dialog to select JSON file
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            # Load JSON data from file
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Connect to MongoDB
            client = MongoClient("mongodb://localhost:27017/")

            # Create or switch to the database
            db = client["medical_records"]

            # Create or switch to the collection
            collection = db["test_results"]

            # Insert the JSON data into the collection
            collection.insert_many(data)  # OR collection.insert_one(data)

            messagebox.showinfo("Success", "Data inserted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


# Create the main window
root = tk.Tk()
root.title("JSON Uploader")

# Create and place the upload button
upload_button = tk.Button(root, text="Upload JSON", command=upload_json)
upload_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
