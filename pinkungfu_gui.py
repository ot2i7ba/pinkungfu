# Copyright (c) 2023 ot2i7ba
# https://github.com/ot2i7ba/
# This code is licensed under the MIT License (see LICENSE for details).

"""
Generates possible PIN combinations based on user input.
"""

import itertools
import os
import tkinter as tk
from tkinter import messagebox

def pinkungfu(length, include_digits, include_lowercase, include_uppercase, include_special, include_zero, allow_double_digits):
    characters = ""
    if include_digits:
        characters += "0123456789"
    if include_lowercase:
        characters += "abcdefghijklmnopqrstuvwxyz"
    if include_uppercase:
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if include_special:
        characters += "!@#$%&*" # Modify as needed

    # Definition of exclusion rules
    combinations = itertools.product(characters, repeat=length)
    combinations = filter(lambda x: len(set(x)) == length or allow_double_digits, combinations)
    combinations = filter(lambda x: "0" in x or include_zero, combinations)

    return combinations

# Write possible combinations in text file and split
def write_combinations_to_file(combinations, filename, chunk_size=None):
    if chunk_size:
        chunk = 0
        for i, combination in enumerate(list(combinations)):
            if i % chunk_size == 0:
                chunk += 1
                f = open(f"{filename}_{chunk}.txt", "w")
            f.write("".join(combination) + "\n")
        f.close()
        messagebox.showinfo("Success", f"Files {filename}_1.txt to {filename}_{chunk}.txt were created.")
    else:
        f = open(f"{filename}.txt", "w")
        for combination in list(combinations):
            f.write("".join(combination) + "\n")
        f.close()
        messagebox.showinfo("Success", f"File {filename}.txt was created.")

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.header_label = tk.Label(self, text="PIN-KungFu", font=("TkDefaultFont", 14))
        self.header_label.pack()

        self.header_label = tk.Label(self, text="Generate PIN Combinations", font=("TkDefaultFont", 12))
        self.header_label.pack()

        self.line = tk.Frame(self, height=2, width=300, bd=300, relief="solid")
        self.line.pack(pady=10)

        self.length_label = tk.Label(self, text="Enter the length of the PIN (3-16):")
        self.length_label.pack()
        self.length_entry = tk.Entry(self)
        self.length_entry.pack()
        
        self.empty_line = tk.Label(self, text="")
        self.empty_line.pack()

        self.include_digits_var = tk.BooleanVar()
        self.include_digits_var.set(True)
        self.include_digits_check = tk.Checkbutton(self, text="Include digits (0-9)?", variable=self.include_digits_var)
        self.include_digits_check.pack()
        
        self.include_lowercase_var = tk.BooleanVar()
        self.include_lowercase_check = tk.Checkbutton(self, text="Include lowercase letters (a-z)?", variable=self.include_lowercase_var)
        self.include_lowercase_check.pack()
        
        self.include_uppercase_var = tk.BooleanVar()
        self.include_uppercase_check = tk.Checkbutton(self, text="Include uppercase letters (A-Z)?", variable=self.include_uppercase_var)
        self.include_uppercase_check.pack()
        
        self.include_special_var = tk.BooleanVar()
        self.include_special_check = tk.Checkbutton(self, text="Include special characters (!@#$%^&*)?", variable=self.include_special_var)
        self.include_special_check.pack()
        
        self.include_zero_var = tk.BooleanVar()
        self.include_zero_check = tk.Checkbutton(self, text="Allow combinations with zeros (0)?", variable=self.include_zero_var)
        self.include_zero_check.pack()
        
        self.allow_double_digits_var = tk.BooleanVar()
        self.allow_double_digits_check = tk.Checkbutton(self, text="Allow combinations with duplicates?", variable=self.allow_double_digits_var)
        self.allow_double_digits_check.pack()

        self.empty_line = tk.Label(self, text="")
        self.empty_line.pack()
        
        self.split_label = tk.Label(self, text="Split the file into chunks of size (optional):")
        self.split_label.pack()
        self.split_entry = tk.Entry(self)
        self.split_entry.pack()
        
        self.filename_label = tk.Label(self, text="Enter the file name:")
        self.filename_label.pack()
        self.filename_entry = tk.Entry(self)
        self.filename_entry.pack()

        self.empty_line = tk.Label(self, text="")
        self.empty_line.pack()

        self.line = tk.Frame(self, height=2, width=300, bd=300, relief="solid")
        self.line.pack(pady=10)

        self.empty_line = tk.Label(self, text="")
        self.empty_line.pack()
        
        self.generate_button = tk.Button(self, text="Generate", command=self.generate)
        self.generate_button.pack()

        self.empty_line = tk.Label(self, text="")
        self.empty_line.pack()

        self.footer_label = tk.Label(self, text="Copyright 2023 by ot2i7ba", font=("TkDefaultFont", 10), anchor="w", foreground="gray")
        self.footer_label.pack(side="bottom")

    # Check length of PIN
    def generate(self):
        try:
            length = int(self.length_entry.get())
            if length < 3 or length > 16:
                raise ValueError
            elif length >= 4:
                result = messagebox.askyesno("Warning", "Generating combinations for a length of 4 or higher may take a long, long time. Do you want to continue?")
                if not result:
                    return
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Enter a valid length.")
            return

        include_digits = self.include_digits_var.get()
        include_lowercase = self.include_lowercase_var.get()
        include_uppercase = self.include_uppercase_var.get()
        include_special = self.include_special_var.get()
        include_zero = self.include_zero_var.get()
        allow_double_digits = self.allow_double_digits_var.get()

        # Check for empty checkboxes
        if not (include_digits or include_lowercase or include_uppercase or include_special):
            messagebox.showerror("Error", "At least one character set must be selected.")
            return

        combinations = list(pinkungfu(length, include_digits, include_lowercase, include_uppercase, include_special, include_zero, allow_double_digits))
        print(f"{len(combinations)} combinations were generated.")

        chunk_size = None
        try:
            chunk_size = int(self.split_entry.get())
        except:
            pass

        # Check for empty filename
        filename = self.filename_entry.get()
        if not filename:
            messagebox.showerror("Error", "Please enter a file name.")
            return

        write_combinations_to_file(combinations, filename, chunk_size)

root = tk.Tk()
root.geometry("365x565")
root.title("PIN-KungFu v0.6 (20230213)")
app = Application(master=root)
app.mainloop()
