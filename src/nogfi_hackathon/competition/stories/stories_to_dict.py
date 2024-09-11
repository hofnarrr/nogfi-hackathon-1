import os
import pathlib
from collections import defaultdict


def read_story_to_list(file_path):
    try:
        with open(file_path, "r") as f:
            content = f.read()
            return content.split()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []


# Get the directory of the current script
current_dir = pathlib.Path(__file__).parent.resolve()

all_words = set()
file_words = defaultdict(set)

plots = defaultdict(dict)

# Iterate through all files in the current directory
for filename in os.listdir(current_dir):
    # Check if the file ends with '.txt'
    if filename.endswith(".txt"):
        file_path = os.path.join(current_dir, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            words = read_story_to_list(file_path)
            # print(f"File: {filename}")
            # print(f"{filename.replace(".txt", "")} = {words}")# Empty line for better readability between files
            plots[filename.replace(".txt", "")]["plot"] = words
            # Add words to the file_words dictionary
            file_words[filename] = set(words)
            all_words.update(words)

print("All words across all files:")
print(sorted(all_words))
print()

print("Unique words for each file:")
for filename, words in file_words.items():
    # Calculate words unique to this file
    unique_words = words - set.union(
        *(
            other_words
            for other_file, other_words in file_words.items()
            if other_file != filename
        )
    )
    # print(f"{filename.replace(".txt", "")}_unique = {sorted(unique_words)}")
    plots[filename.replace(".txt", "")]["unique"] = sorted(unique_words)

print(plots)
