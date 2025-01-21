# Import necessary libraries
import random
from pathlib import Path

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

class DatasetHandler:
    """
    Combines dataset processing and splitting functionalities.
    """
    def __init__(self, stopping_seq=None):
        """
        Initialize the DatasetHandler.

        Args:
            stopping_seq (str, optional): A string to append to the end of each plan, if provided.
        """
        self.stopping_seq = stopping_seq

    def process_directory(self, entries, single_entries, domain_dir_path):
        """
        Process a directory containing a domain, problems, and plans, and compiles them into a dataset.

        Args:
            entries (list): List to store processed data.
            single_entries (int): Counter for the number of valid processed entries have a specific domain.
            domain_dir_path (str): Path to the directory containing the domain, problems, and plans.

        Returns:
            tuple: Updated `entries` list and `single_entries` count.
        """
        dir_path = Path(domain_dir_path)    # Convert the directory path to a Path object
        search_domain_file = "domain"       # Expected substring in the domain file name
        search_problems_dir = "problems"    # Expected substring in the problems directory name
        search_plans_dir = "plans"          # Expected substring in the plans directory name

        single_entries = 0                  # Reset the counter for this directory

        # Iterate through the files and directories in the specified path
        for file in dir_path.iterdir():
            if file.is_file() and (search_domain_file in file.name):    # Look for the domain file
                domain_file = Path(file)
            elif file.is_dir() and (search_problems_dir in file.name):  # Look for the problems directory
                problems_dir_path = Path(file)
            elif file.is_dir() and (search_plans_dir in file.name): # Look for the plans directory
                plans_dir_path = Path(file)

        # Ensure all required components (domain, problems, plans) exist
        if domain_file.exists() and problems_dir_path.exists() and plans_dir_path.exists():
            # Process each problem file in the problems directory
            for problem_file in problems_dir_path.glob("*.pddl"):
                plan_file = plans_dir_path / f"{problem_file.stem}.plan"    # Find the corresponding plan file
                if plan_file.exists():  # Ensure the plan file exists
                    # Read the content of the domain, problem, and plan files
                    with open(domain_file, "r") as df, open(problem_file, "r") as pf, open(plan_file, "r") as plf:
                        domain_content = df.read()
                        problem_content = pf.read()
                        plan_content = plf.read()

                        # Optionally append the stopping sequence to the plan
                        if self.stopping_seq:
                            plan_content += f"\n{self.stopping_seq}"

                        # Append the processed entry as a dictionary to the entries list
                        entries.append({
                            "instruction": domain_content,  # Domain file content
                            "input": problem_content,   # Problem file content
                            "output": plan_content  # Plan file content
                        })

                        single_entries += 1     # Increment the counter for valid entries
        return entries, single_entries      # Return the updated list and counter

    def split_dataset(self, entries, val_count, test_count):
        """
        Shuffle and split the dataset into training, validation, and test sets.

        Args:
            entries (list): The complete dataset to be split.
            val_count (int): Number of entries to include in the validation set.
            test_count (int): Number of entries to include in the test set.

        Returns:
            tuple: Training set, validation set, and test set.

        Raises:
            ValueError: If the sum of validation and test counts exceeds the total number of entries.
        """
        random.shuffle(entries)     # Shuffle the entries randomly

        total_entries = len(entries)    # Get the total number of entries
        if val_count + test_count > total_entries:
            # Raise an error if the validation and test sets exceed the total number of entries
            raise ValueError("The sum of validation and test entries exceeds the total number of entries.")
        
        # Print a warning if the validation and test sets exceed 30% of the total entries
        if val_count + test_count > total_entries * 0.3:
            print("Warning: The validation and test entries exceed 30% of the total entries.")

        # Split the dataset into validation, test, and training sets
        val_set = entries[:val_count]
        test_set = entries[val_count:val_count + test_count]
        train_set = entries[val_count + test_count:]

        return train_set, val_set, test_set     # Return the three subsets