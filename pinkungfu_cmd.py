# Copyright (c) 2023 ot2i7ba
# https://github.com/ot2i7ba/
# This code is licensed under the MIT License (see LICENSE for details).

"""
Generates possible PIN combinations based on user input.
"""

import itertools
import os

os.system('cls' if os.name == 'nt' else 'clear')

# Defining character set
def pinkungfu(length, include_digits, include_lowercase, include_uppercase, include_special, include_zero, allow_double_digits):
    characters = ""
    if include_digits:
        characters += "0123456789"
    if include_lowercase:
        characters += "abcdefghijklmnopqrstuvwxyz"
    if include_uppercase:
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if include_special:
        characters += "!@#$%&*"

    # Definition of exclusion rules
    combinations = itertools.product(characters, repeat=length)
    combinations = filter(lambda x: len(set(x)) == length or allow_double_digits, combinations)
    combinations = filter(lambda x: "0" in x or include_zero, combinations)

    return combinations

# Write possible combinations in text file and split
def write_combinations_to_file(combinations, filename, chunk_size=100000):
    split_file = ""
    while split_file != "y" and split_file != "n":
        split_file = input("Do you want to split the generated text file? (y/n) ").lower()
    if split_file == "n":
        f = open(f"{filename}.txt", "w")
        for combination in list(combinations):
            f.write("".join(combination) + "\n")
        f.close()
    else:
        chunk = 0
        chunk_size = int(input("Enter the chunk size: "))
        for i, combination in enumerate(list(combinations)):
            if i % chunk_size == 0:
                chunk += 1
                f = open(f"{filename}_{chunk}.txt", "w")
            f.write("".join(combination) + "\n")
        f.close()

# PIN-KungFu
def main():
    print("\n" + "PIN-KungFu by ot2i7ba")
    print("-" * 80 + "\n")

    # Set the character length
    try:
        length = int(input("Enter the length of the PIN (3-16): "))
        if length < 3 or length > 16:
            raise ValueError
    except ValueError:
        print("Invalid input. Enter a valid length.")
        return

    if length >= 5:
        print("Warning: The calculation may take a long time.")
        proceed = ""
        while proceed != "y" and proceed != "n":
            proceed = input("Do you want to proceed anyway? (y/n) ").lower()
        if proceed != "y":
            raise Exception("Program was canceled by user.")

    include_digits = ""
    while include_digits != "y" and include_digits != "n":
        include_digits = input("Include digits (0-9)? (y/n) ").lower()
    include_digits = include_digits == "y"

    include_lowercase = ""
    while include_lowercase != "y" and include_lowercase != "n":
        include_lowercase = input("Include lowercase letters (a-z)? (y/n) ").lower()
    include_lowercase = include_lowercase == "y"

    include_uppercase = ""
    while include_uppercase != "y" and include_uppercase != "n":
        include_uppercase = input("Include uppercase letters (A-Z)? (y/n) ").lower()
    include_uppercase = include_uppercase == "y"

    include_special = ""
    while include_special != "y" and include_special != "n":
        include_special = input("Include special characters (!@#$%^&*)? (y/n) ").lower()
    include_special = include_special == "y"

    include_zero = ""
    while include_zero != "y" and include_zero != "n":
        include_zero = input("Allow combinations with zeros (0)? (y/n) ").lower()
    include_zero = include_zero == "y"

    allow_double_digits = ""
    while allow_double_digits != "y" and allow_double_digits != "n":
        allow_double_digits = input("Allow combinations with duplicates? (y/n) ").lower()
    allow_double_digits = allow_double_digits == "y"

    combinations = list(pinkungfu(length, include_digits, include_lowercase, include_uppercase, include_special, include_zero, allow_double_digits))

    # Print sum of possible combinations
    print(f"{len(combinations)} combinations were generated.")

    # Create custom text file
    filename = input("Enter the file name: ")
    #if not filename.endswith(".txt"):
        #filename += ".txt"

    write_combinations_to_file(combinations, filename)
    print(f"File {filename} was created.")

if __name__ == "__main__":
    main()
