# Import necessary libraries
import os
import json
import random
import argparse
from pathlib import Path

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

def process_directory(entries, domain_dir_path, stopping_seq):
    """
    Process the given directory to compile domains, problems, and plans into a list.
    
    Parameters:
        - entries: List to store the compiled entries.
        - domain_dir_path: Path to the directory containing domain, problems, and plans.
        - stopping_seq: Optional sequence to append to the plan content.
        
    Returns:
        - Updated entries list containing dictionaries of domain, problem, and plan content.
    """

    # Create a Path object for the directory
    dir_path = Path(domain_dir_path)
    search_domain_file = "domain"
    search_problems_dir = "problems"
    search_plans_dir = "plans"

    # Search for files in the directory
    for file in dir_path.iterdir():
        if file.is_file() and (search_domain_file in file.name):
            domain_file = Path(file)
        elif file.is_dir() and (search_problems_dir in file.name):
            problems_dir_path = Path(file)
        elif file.is_dir() and (search_plans_dir in file.name):
            plans_dir_path = Path(file)

    if domain_file.exists() and problems_dir_path.exists() and plans_dir_path.exists():
        for problem_file in problems_dir_path.glob("*.pddl"):
            plan_file = plans_dir_path / f"{problem_file.stem}.plan"
            if plan_file.exists():
                with open(domain_file, "r") as df, open(problem_file, "r") as pf, open(plan_file, "r") as plf:
                    domain_content = df.read()
                    problem_content = pf.read()
                    plan_content = plf.read()

                    if stopping_seq:
                        plan_content += f"\n{stopping_seq}"

                    entries.append({
                        "domain": domain_content,
                        "problem": problem_content,
                        "plan": plan_content
                    })
    return entries

def split_dataset(entries, val_count, test_count):
    """
    Shuffle and split the dataset into training, validation, and test sets.
    
    Parameters:
        - entries: List of entries to be split.
        - val_count: Number of entries for the validation set.
        - test_count: Number of entries for the test set.
        
    Returns:
        - train_set: List of training entries.
        - val_set: List of validation entries.
        - test_set: List of test entries.
    """
    random.shuffle(entries)

    total_entries = len(entries)
    print(total_entries)
    if val_count + test_count > total_entries:
        raise ValueError("The sum of validation and test entries exceeds the total number of entries.")

    if val_count + test_count > total_entries * 0.3:
        print("Warning: The validation and test entries exceed 30% of the total entries.")

    val_set = entries[:val_count]
    test_set = entries[val_count:val_count + test_count]
    train_set = entries[val_count + test_count:]

    return train_set, val_set, test_set

def save_to_json(data, output_path):
    """
    Save the given data to a JSON file.
    
    Parameters:
        - data: Data to be saved in JSON format.
        - output_path: Path where the JSON file will be saved.
    """
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

def main(args):
    '''
    Main function to process command line arguments and execute the dataset processing.
    
    Parameters:
        - args: Command line arguments containing output directory and counts for validation and test sets.
    '''
    output_dir = Path(args.output_dir)
    domains_dict = dict()
    for file in output_dir.iterdir():
        if file.is_dir():
            domains_dict[file.name] = str(file)

    entries = []

    for value in domains_dict.values():
        # Process the input directory
        entries = process_directory(entries, value, args.stopping_seq)

        if not entries:
            print("No valid entries found. Exiting.")
            return

    # Split the dataset
    try:
        train_set, val_set, test_set = split_dataset(entries, args.validation, args.test)
    except ValueError as e:
        print(str(e))
        return
    
    # Structure of the Dataset folder
    dataset_dir_name = "dataset"
    train_set_dir_name = "train_set"
    val_set_dir_name = "val_set"
    test_set_dir_name = "test_set"
    dataset_path = os.path.join(args.output_dir, dataset_dir_name)
    train_set_dir_path = os.path.join(dataset_path, train_set_dir_name)
    val_set_dir_path = os.path.join(dataset_path, val_set_dir_name)
    test_set_dir_path = os.path.join(dataset_path, test_set_dir_name)
    os.makedirs(dataset_path, exist_ok=True)
    os.makedirs(train_set_dir_path, exist_ok=True)
    os.makedirs(val_set_dir_path, exist_ok=True)
    os.makedirs(test_set_dir_path, exist_ok=True)

    # Paths of the json files
    train_set_name = "training.json"
    val_set_name = "validation.json"
    test_set_name = "test.json"
    train_set_path = os.path.join(train_set_dir_path, train_set_name)
    val_set_path = os.path.join(val_set_dir_path, val_set_name)
    test_set_path = os.path.join(test_set_dir_path, test_set_name)

    # Save the datasets to JSON files
    save_to_json(train_set, train_set_path)
    save_to_json(val_set, val_set_path)
    save_to_json(test_set, test_set_path)

    print(f"Dataset processing complete. JSON files saved in {dataset_path}.")

if __name__ == "__main__":
    # Command line argument parsing
    parser = argparse.ArgumentParser(description='Process domains, problems, and plans into JSON datasets')
    parser.add_argument('-o', '--output_dir', type=str, help='Output directory for PDDL files')
    parser.add_argument('-v', '--validation', type=int, default=0, help='Number of entries for validation set')
    parser.add_argument('-t', '--test', type=int, default=0, help='Number of entries for test set')
    parser.add_argument('--stopping_seq', type=str, default=None, help='Optional stopping sequence to append to plans')
    args = parser.parse_args()

    main(args)