# Import necessary libraries
import os
import re               # To renumber each file
import numpy as np      # To calculate statistics
from pathlib import Path

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

class Planner_Structure:
    def __init__(self, output_dir):
        """
        Initializes the Planner_Structure with the specified output directory.
        
        Args:
            output_dir (str): The directory where output files will be stored.
        """
        self.output_dir = output_dir

    def get_structure_more_problems(self):
        """
        Retrieves the structure of directories and files needed for planning.
        
        Returns:
            tuple: Contains paths for domain, problems, logs, plans, progress file, and results directory.
        """
        # Create a Path object for the directory
        dir_path = Path(self.output_dir)

        # Search for files in the directory
        for file in dir_path.iterdir():
            if file.is_file() and file.name.startswith("domain"):
                domain_path = str(file)
            elif file.is_dir() and file.name == "problems":
                problems_dir_path = str(file)
            elif file.is_dir() and file.name == "logs":
                logs_dir_path = str(file)

        # Generate plans folder
        plans_folder_name = 'plans'
        plans_dir_path = os.path.join(self.output_dir, plans_folder_name)
        os.makedirs(plans_dir_path, exist_ok=True)
        
        # Generate results folder
        results_folder_name = 'results'
        results_dir_path = os.path.join(self.output_dir, results_folder_name)
        os.makedirs(results_dir_path, exist_ok=True)

        # Name of the file needed to take the progress value
        progress_file = "progress.txt"
        # Path of the progress ppg file
        planner_progress_path = os.path.join(self.output_dir, progress_file)
        
        # Name of the file needed to record failed problems
        failed_problems_filename = "total_failed_problems.txt"
        # Path of the failed problems file
        failed_problems_after_Ctrl_C = os.path.join(self.output_dir, failed_problems_filename)

        return domain_path, problems_dir_path, logs_dir_path, plans_dir_path, planner_progress_path, results_dir_path, failed_problems_after_Ctrl_C

def read_problems(problems_dir_path):
    """
    Reads problem files from the specified directory.
    
    Args:
        problems_dir_path (str): The path to the directory containing problem files.
        
    Returns:
        tuple: Contains the count of problem files and a list of their paths.
    """
    # Counter for the number of files
    problem_count = 0
    problems_paths = []    # List of paths for each problem file

    # Iterate over files in the folder (without subfolders)
    for problem in os.listdir(problems_dir_path):
        problem_path = os.path.join(problems_dir_path, problem)
        if os.path.isfile(problem_path):  # Check if it is a file
            problems_paths.append(problem_path)
            problem_count += 1

    # Sort the list based on the numeric part of the file name
    problems_paths = sorted(
        problems_paths,
        key=lambda x: int(re.search(r'problem_(\d+)', os.path.basename(x)).group(1))
    )
    return problem_count, problems_paths

def read_plans(plans_dir_path):
    """
    Reads plan files from the '/plans' directory and takes the number of the last generated plan.
    
    Args:
        plans_dir_path (str): The path to the directory containing plan files.
        
    Returns:
        last_plan (int): The number of the last generated plan.
    """
    numbers = []    # Empty list for the numbers of plans
    files = Path(plans_dir_path).glob("*.plan") # Groups the files into "/plans" directory

    for plan in files:
        match = re.search(r'_(\d+)\.plan$', plan.name)  # Regex on numbers of the plans
        if match:
            numbers.append(int(match.group(1)))
    
    if not numbers:
        return None  # No plans found
    
    last_plan = max(numbers)    # Takes the biggest number (is the same number of the last generated plan)
    return last_plan

def rename_plan(output_dir, domain, i):
    """
    Renames a plan file based on the domain name and index.
    
    Args:
        output_dir (str): The output directory where all the files are located.
        domain (object): The domain object containing the name used for the new file.
        i (int): The index to be used in the new file name.
        
    Returns:
        Path: The new path of the renamed plan file.
    """
    # Create a Path object for the directory
    dir_path = Path(output_dir)
    search_string = ".1"

    # Search for files in the directory
    for file in dir_path.iterdir():
        if file.is_file() and (search_string in file.name):
            plan_path = Path(file)
            break
    
    # Set a new name as the original path + the new name for the file
    new_name = plan_path.parent / f"{domain.name}_problem_00000{i+1}.pddl"
    plan_path.rename(new_name)
    return new_name

def convert_to_IPC_format(plans_dir_path):
    """
    Converts plan files to IPC format and removes the original PDDL files.
    
    Args:
        plans_dir_path (str): The path to the directory containing plan files.
    """
    plan_files = sorted([f for f in os.listdir(plans_dir_path) if f.endswith(".pddl")])

    for i, plan in enumerate(plan_files):
        # Open the original file
        file_origin_path = os.path.join(plans_dir_path, plan)
        file_origin = open(file_origin_path, "r")
        
        # Create the new file with the correct name
        new_file_path = os.path.join(plans_dir_path, plan.split(".")[0] + ".plan")
        new_file = open(new_file_path, 'w+')
        
        action_timing = 1
        for line in file_origin:
            line = line.lower()
            line = '%.3f' % (action_timing / 1000) + "00: " + line
            new_file.write(line)
            action_timing += 2

        file_origin.close()
        new_file.close()

        # Check if the file ends with ".pddl" and if it is a file
        if plan.endswith(".pddl") and os.path.isfile(file_origin_path):
            os.remove(file_origin_path)  # Remove the original file

def final_output(i, p_failed, fp_progress, plans_dir_path, hours, minutes, seconds, avg_time, min_time, max_time, median_time, std_dev):
    """
    Prints the final output statistics after planning.
    
    Args:
        i (int): Number of generated problems considered.
        p_failed (int): Number of plans that failed.
        fp_progress (int): Total of plans failed.
        plans_dir_path (str): Directory of generated plans.
        hours (int), minutes (int), seconds (float): Time required to generate plans.
        avg_time (float): Average time taken for planning.
        min_time (float): Minimum time taken for planning.
        max_time (float): Maximum time taken for planning.
        median_time (float): Median time taken for planning.
        std_dev (float): Standard deviation of planning times.
    """
    print(f"Number of generated problems considered: {i}")
    print(f"Number of plans failed in this interaction: {p_failed}")
    print(f"Total of plans failed: {fp_progress}")
    print(f"Directory of generated plans: {plans_dir_path}")
    print(f"Time required to generate plans: {int(hours)}h {int(minutes)}m {seconds:.2f}s")
    print("\n ----- Times for planning -----\n")
    print(f"Average Time: {avg_time:.2f} seconds")
    print(f"Min Time: {min_time:.2f} seconds")
    print(f"Max Time: {max_time:.2f} seconds")
    print(f"Median Time: {median_time:.2f} seconds")
    print(f"Standard Deviation: {std_dev:.2f} seconds")

def calculate_statistics(execution_times):
    """
    Calculates statistical metrics from execution times.
    
    Args:
        execution_times (list): List of execution times.
        
    Returns:
        tuple: Contains average, minimum, maximum, median, and standard deviation of execution times.
    """
    if execution_times:
        avg_time = np.mean(execution_times)
        min_time = np.min(execution_times)
        max_time = np.max(execution_times)
        median_time = np.median(execution_times)
        std_dev = np.std(execution_times)

        return avg_time, min_time, max_time, median_time, std_dev
    else:
        print("No execution times available.")
        return None, None, None, None, None

def delete_and_renumber(output_dir, failed_problems, existing_problems, failed_problems_after_Ctrl_C, progress_path):
    """
    Deletes failed problems and renumbers remaining files.
    
    Args:
        output_dir (str): The output directory containing all the files.
        failed_problems (list): List of failed problem file names to be deleted.
        existing_problems (list): List of all failed problem file names to be deleted.
        failed_problems_after_Ctrl_C (str): Path to the failed problems file.
        progress_path (str): Path to the progress file.
    """
    plans_dir = os.path.join(output_dir, "plans")
    problems_dir = os.path.join(output_dir, "problems")
    hash_list_path = os.path.join(output_dir, "hash_list.txt")

    # Sort the list based on the numeric part of the file name
    failed_problems = sorted(
        failed_problems,
        key=lambda x: int(re.search(r'problem_(\d+)', os.path.basename(x)).group(1))
    )

    if failed_problems:
        print("The following problems have generated wrong plans and are considered failed:")
        # Record failed problems into a file and show them as output
        with open (failed_problems_after_Ctrl_C, 'a') as f:
            for problem in failed_problems:
                f.write(f"{problem}\n")
                print(f"- {problem}")
        existing_problems = read_failed_problems_file(failed_problems_after_Ctrl_C) # Read the failed problems file
                    
        while True:
            # Ask user for a possible choice
            print("There are 3 options:\n"
                  "1) Delete 'failed problems from this interaction', renumber plans and problems and 'update the hash list from this interaction'\n"
                  "2) Delete 'total failed problems', renumber plans and problems and 'update the hash list from total failed problems'\n"
                  "3) No changes! You will have the plans generated by the respective problems, you will also keep the unplannable problems and if you want to see only them\n"
                  "but all together, just open the 'total_failed_problems.txt' file\n")
            choice = input("What do you choose? (1/2/3): ").strip()
            match choice:
                case '1':
                    # Update the hash list
                    update_hash_list(hash_list_path, failed_problems)

                    # Delete the problem
                    for problem in failed_problems:
                        problem_path = os.path.join(problems_dir, problem)
                        if os.path.exists(problem_path):
                            os.remove(problem_path)

                    # Renumber all remaining files to eliminate gaps
                    renumber_files(plans_dir, "plan")
                    renumber_files(problems_dir, "pddl")

                    # Update failed_problems_file
                    update_failed_problems_file(existing_problems, failed_problems_after_Ctrl_C)
                    
                    # Count rows into the hash_list file
                    with open(hash_list_path, 'r') as f:
                        count_rows = sum(1 for _ in f)
                    # Update hash_list_progress
                    update_h_progress(progress_path, count_rows)
                    return choice

                case '2':
                    # Update the hash list
                    update_hash_list(hash_list_path, existing_problems)

                    # Delete the problem
                    for problem in existing_problems:
                        problem_path = os.path.join(problems_dir, problem)
                        if os.path.exists(problem_path):
                            os.remove(problem_path)

                    # Renumber all remaining files to eliminate gaps
                    renumber_files(plans_dir, "plan")
                    renumber_files(problems_dir, "pddl")

                    # Update failed_problems_file
                    update_failed_problems_file(existing_problems, failed_problems_after_Ctrl_C)
                    
                    # Count rows into the hash_list file
                    with open(hash_list_path, 'r') as f:
                        count_rows = sum(1 for _ in f)
                    # Update hash_list_progress
                    update_h_progress(progress_path, count_rows)
                    return choice

                case '3':
                    print("No changes.")
                    # Write problems failed to failed_problems_after_Ctrl_C_file.txt
                    update_failed_problems_file(existing_problems, failed_problems_after_Ctrl_C)
                    return choice

                case _:  # Default case if input is not '1' or '2' or '3'
                    print("Choice not valid. Type '1' or '2' or '3'!")
    else:
        print("No failed problems found.")

def renumber_files(directory, extension):
    """
    Renumbers files in the specified directory to eliminate gaps in numbering.
    
    Args:
        directory (str): The directory containing files to be renumbered.
        extension (str): The file extension of the files to be renumbered.
    """
    # Find files in the directory
    files = sorted(
        [f for f in os.listdir(directory) if f.endswith(f".{extension}")],
        key=lambda x: int(re.search(r"_(\d+)\.", x).group(1))  # Extracts the number
    )

    for idx, file in enumerate(files, start=1):
        # Extract the prefix before the number
        prefix = re.match(r"^(.*_)\d+\.", file).group(1)
        old_path = os.path.join(directory, file)

        # Create the index with leading zeros
        padded_index = f"00000{str(idx)}"

        # New file name
        new_name = f"{prefix}{padded_index}.{extension}"
        new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)  # Rename the file

        if extension == "pddl":
            # Update the content of the file
            with open(new_path, 'r') as f:
                content = f.read()
            
            # Look up the problem definition and substitute the name
            new_problem_name = new_name.rsplit('.', 1)[0]  # Name without extension
            updated_content = re.sub(
                r"\(define \(problem [^\)]+\)",  # Regex to find the problem name
                f"(define (problem {new_problem_name})",  # Change with the new name
                content
            )

            # Write the updated content into the file
            with open(new_path, 'w') as f:
                f.write(updated_content)

def update_hash_list(hash_list_path, failed_problems):
    """
    Removes failed problems from the hash list.
    
    Args:
        hash_list_path (str): The path to the hash list file.
        failed_problems (list): List of failed problem file names to be removed from the hash list.
    """
    # Read all hashes from the list
    with open(hash_list_path, 'r') as f:
        hash_list = f.readlines()

    # Remove hashes of failed problems
    failed_indices = [int(re.search(r"_(\d+)\.(pddl|plan)", problem).group(1)) - 1 for problem in failed_problems]

    # Filter out non-failed lines
    hash_list = [hash_list[i] for i in range(len(hash_list)) if i not in failed_indices]

    # Write the new hash list
    with open(hash_list_path, 'w') as f:
        f.writelines(hash_list)

    print("hash_list.txt updated.")

def update_npg_progress(last_plan, progress_path):
    """
    Updates the progress file with the number of problems that correspond to the plans generated.
    
    Args:
        last_plan (int): The number of the last generated plan.
        progress_path (str): The path to the progress file to be updated.
    """
    # Read the content of the file
    with open(progress_path, 'r') as f:
        lines = f.readlines()

    # Search the row that contains 'hash_list_progress = '
    for l, line in enumerate(lines):
        if line.startswith("npg_progress = "):
            # Overwrite the value with the new value
            lines[l] = f"npg_progress = {last_plan}\n"
            break
    
    # Rewrite the file with the new value
    with open(progress_path, 'w') as file:
        file.writelines(lines)

def find_parent_before_directory(start_path, target_directory):
    """
    Traverses the directory hierarchy to find the parent path
    immediately before the target directory.

    Args:
        start_path: Starting path.
        target_directory: Name of the target directory.
        
    Returns:
        Parent path before the target directory, or None if not found.
    """
    current_path = Path(start_path).resolve()

    # Ascend to the root directory
    while current_path != current_path.parent:
        if current_path.name == target_directory:
            return current_path.parent  # Return the parent path before the target directory
        current_path = current_path.parent

    return None  # Not found

def find_planner_and_validate_paths(planner):
    """
    Finds the paths for the planner and validation tool based on the project structure.

    Parameters:
        planner: Name of the planner to be used.
        
    Returns:
        planner_path (str), validate_path (str): The paths for the planner and validation tool.
    """
    # Starting path (e.g., the path of the executed script)
    start_path = __file__

    # Name of the target directory
    target_directory = "Project"

    # Find the parent path before the target directory
    parent_path = find_parent_before_directory(start_path, target_directory)

    if parent_path:
        origin_planners = "Project/planner/planners_and_val"
        origin_validate = "Project/planner/planners_and_val/VAL/build/linux64/Release/bin/Validate"
        planner_path = os.path.join(parent_path, origin_planners, planner)
        validate_path = os.path.join(parent_path, origin_validate)       
    
    return planner_path, validate_path

def read_failed_problems_file(failed_problems_after_Ctrl_C):
    """
    Reads the list of previously failed problems from a specified file.
    
    Args:
        failed_problems_after_Ctrl_C (str): The path to the file containing failed problems.
        
    Returns:
        existing_problems (set): A set of problem names that have previously failed.
    """
    existing_problems = set()

    # Read existing problems from the file
    if os.path.exists(failed_problems_after_Ctrl_C):
        with open(failed_problems_after_Ctrl_C, 'r') as f:
            existing_problems = set(line.strip() for line in f)
    return existing_problems

def update_failed_problems_file(existing_problems, failed_problems_after_Ctrl_C):
    """
    Updates the file containing failed problems by adding new entries.
    
    Args:
        existing_problems (set): A set of problem names that have previously failed.
        failed_problems_after_Ctrl_C (str): The path to the file where failed problems are recorded.
    """
    # Filter out problems not yet in the file
    new_problems = [problem for problem in existing_problems if problem not in existing_problems]

    # Add only new problems
    with open(failed_problems_after_Ctrl_C, 'a') as f:
        for problem in new_problems:
            f.write(f"{problem}\n")

def update_fp_progress(progress_path, fp_progress):
    """
    Updates the progress file with the number of failed problems encountered.
    
    Args:
        progress_path (str): The path to the progress file to be updated.
        fp_progress (int): The number of failed problems to record in the progress file.
    """
    # Read the content of the file
    with open(progress_path, 'r') as file:
        lines = file.readlines()

    # Search the row that contains 'npg_progress ='
    for l, line in enumerate(lines):
        if line.startswith("failed_problems_progress = "):
            # Sovrascrivi il valore con il nuovo valore
            lines[l] = f"failed_problems_progress = {fp_progress}\n"
            break
    
    # Rewrite the file with the new value
    with open(progress_path, 'w') as file:
        file.writelines(lines)

def read_fp_progress(progress_path):
    """
    Reads the number of failed problems from the progress file.
    
    Args:
        progress_path (str): The path to the progress file to read from.
        
    Returns:
        Value (int): The number of failed problems recorded in the progress file, or 0 if not found.
    """
    # Define a regex pattern to match the line containing 'failed_problems_progress'
    pattern = r"failed_problems_progress\s*=\s*(\d+)"
    
    # Check if the progress file exists
    if os.path.exists(progress_path):
        with open(progress_path, 'r') as f:
            content = f.read()
            
            # Search for the pattern in the file content
            match = re.search(pattern, content)
            if match:
                # If a match is found, return the captured number (group 1)
                return int(match.group(1))
    # Return 0 if no progress file exists or no match is found
    return 0

def update_h_progress(progress_path, count_rows):
    """
    Updates the progress file with the number of rows in the hash list.
    
    Args:
        progress_path (str): The path to the progress file to be updated.
        count_rows (int): The number of rows to record in the progress file.
    """
    # Read the content of the file
    with open(progress_path, 'r') as f:
        lines = f.readlines()

    # Search the row that contains 'hash_list_progress = '
    for l, line in enumerate(lines):
        if line.startswith("hash_list_progress = "):
            # Overwrite the value with the new value
            lines[l] = f"hash_list_progress = {count_rows}\n"
            break
    
    # Rewrite the file with the new value
    with open(progress_path, 'w') as file:
        file.writelines(lines)