# Import necessary libraries
import os
import json
import re
import datetime
from tabulate import tabulate   # To visualize data in tabular format

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

def create_directories(*paths):
    """
    Create directories for the given paths if they do not already exist.
    
    Args:
        *paths: List of paths to create as directories.
    """
    for path in paths:
        os.makedirs(path, exist_ok=True)    # Create the directory if it not exists

def save_to_json(data, output_path):
    """
    Save data to a JSON file.
    
    Args:
        data: Data to be saved (typically a dictionary or list).
        output_path: Path to the output JSON file.
    """
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)        # Writes data in JSON format with indentation

def clean_set(set):
    """
    Clean all elements in a set by removing unnecessary spaces or tabs from the values.
    
    Args:
        set: List of dictionaries to be cleaned.
    
    Returns:
        List: Cleaned set of dictionaries.
    """
    for element in set:                         # It iterates over each element of the set
        for key, value in element.items():      # For each key-value pair
            clean_value = clean_data(value)     # Clean the value
            element[key] = clean_value          # Update the value in the dictionary
    return set      # Returns the clean set

def clean_data(data):
    """
    Clean a string by removing unnecessary spaces and tabs around newlines.
    
    Args:
        data: The string to clean.
    
    Returns:
        str: Cleaned string.
    """
    return re.sub(r'[ \t]*(\n)[ \t]*', r'\1', data)     # Removes spaces/tabs around \n.

def final_output(log_data, train_set, val_set, test_set):
    """
    Print a summary of the dataset generation in a tabular format and show set sizes.
    
    Args:
        log_data: List of dictionaries containing information about the domains processed.
        train_set: Training set entries.
        val_set: Validation set entries.
        test_set: Test set entries.
    """
    # Show the table in tabular format
    print(tabulate(log_data, headers="keys", tablefmt="grid"))
    # Print the number of elements in each set
    print(f"Training set entries: {len(train_set)}")
    print(f"Validation set entries: {len(val_set)}")
    print(f"Test set entries: {len(test_set)}")

def generate_log(logs_dir, log_data, train_set, val_set, test_set):
    """
    Generate a log file summarizing the dataset generation process.
    
    Args:
        logs_dir: Directory where the log file will be saved.
        log_data: List of dictionaries containing information about the domains processed.
        train_set: Training set entries.
        val_set: Validation set entries.
        test_set: Test set entries.
    """
    # Generate timestamp for log filename
    current_date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f"dataset_generation_{current_date}.log"
    log_file_path = os.path.join(logs_dir, log_filename)

    # Write generation statistics to log file
    with open(log_file_path, 'w') as log_file:
        log_file.write(tabulate(log_data, headers="keys", tablefmt="grid"))
        log_file.write("\n")
        log_file.write(f"Training set entries: {len(train_set)}\n")
        log_file.write(f"Validation set entries: {len(val_set)}\n")
        log_file.write(f"Test set entries: {len(test_set)}")