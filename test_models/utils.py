import json
import re
import os
import datetime
import numpy as np
from pathlib import Path

class Folders_Structure:
    def __init__(self, dataset_dir_path, model_name):
        self.dataset_dir_path = dataset_dir_path
        self.model_name = model_name
    
    def create_structure(self):
        # Create models_result folder
        models_result_dir_name = "models_result"
        m_r_dir_path = Path(self.dataset_dir_path) / models_result_dir_name
        os.makedirs(m_r_dir_path, exist_ok=True)

        # Create model folder
        model_dir_path = Path(m_r_dir_path) / self.model_name
        os.makedirs(model_dir_path, exist_ok=True)

        # Create domains, problems and plans folders
        domains_dir = "domains"
        domains_dir_path = Path(model_dir_path) / domains_dir
        os.makedirs(domains_dir_path, exist_ok=True)

        # Create the JSON file path
        test_set_json = Path(self.dataset_dir_path) / "test_set" / "test_copy.json"

        return test_set_json, domains_dir_path

def open_json_file(test_set_json):
    # Check if the file exists
    if test_set_json.exists() and test_set_json.suffix == '.json':
        with open(test_set_json, 'r') as file:
            # Load data from JSON file
            json_data = json.load(file)
            return json_data
    else:
        raise FileNotFoundError(f"The {test_set_json} file  doesn't exist or is not a valid JSON file.")
    
def find_domain_name(domain):
    # Use a regex to find "domain" and the word that comes immediately after
    match = re.search(r'\(define\s*\(domain\s+(\w+)', domain)
    if match:
        return match.group(1)  # Return the found word
    else:
        return None  # No words found after "domain"
    
def find_domain_name_in_problem(problem):
    # Use a regex to find "domain" and the word that comes immediately after
    match = re.search(r'\(:domain\s+(\w+)', problem)
    if match:
        return match.group(1)  # Return the found word
    else:
        return None  # No words found after "domain"

def find_problem_name(problem):
    # Use a regex to find "problem" and the word that comes immediately after
    match = re.search(r'\(define\s*\(problem\s+(\w+)', problem)
    if match:
        return match.group(1)  # Return the found word
    else:
        return None  # No words found after "problem"
    
def write_domain(domains_dir_path, domain):
    domain_name = find_domain_name(domain)
    domain_dir_path = Path(domains_dir_path) / domain_name
    os.makedirs(domain_dir_path, exist_ok=True)
    domain_file_name = f"{domain_name}.pddl"
    domain_file_path = Path(domain_dir_path) / domain_file_name
    if domain_file_path.exists() and domain_file_path.is_file():
        pass
    else:
        with open(domain_file_path, "w") as f:
            f.writelines(domain)

    # Create the logs folder path
    logs_dir = "logs"
    logs_dir_path = Path(domain_dir_path) / logs_dir
    os.makedirs(logs_dir_path, exist_ok=True)
    return domain_dir_path, domain_name, domain_file_path, logs_dir_path

def write_problem(problem, domain_name, domain_dir_path):
    domain_name_in_problem = find_domain_name_in_problem(problem)
    if domain_name_in_problem == domain_name:
        problems_dir_path = Path(domain_dir_path) / "problems"
        os.makedirs(problems_dir_path, exist_ok=True)
        problem_name = find_problem_name(problem)
        problem_file_name = f"{problem_name}.pddl"
        problem_file_path = Path(problems_dir_path) / problem_file_name
        with open(problem_file_path, "w") as file:
            file.writelines(problem)
    return problem_name, problem_file_path

def write_plan(domain_dir_path, problem_name, assistant_message):
    plans_dir_path = Path(domain_dir_path) / "plans"
    os.makedirs(plans_dir_path, exist_ok=True)
    plan_name = f"{problem_name}.plan"
    plan_file_path = Path(plans_dir_path) / plan_name
    with open(plan_file_path, "w") as pfile:
        pfile.writelines(assistant_message)
    return plan_file_path, plans_dir_path

def write_log(logs_dir_path, plans_failed, plans_dir_path, avg_time, min_time, max_time, median_time, std_dev):
    # Generate timestamp for log filename
    current_date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f"times_planning_{current_date}.log"
    log_file_path = Path(logs_dir_path) / log_filename
    # Write generation statistics to log file
    with open(log_file_path, 'w') as log_file:
        log_file.write(f"Total of plans failed: {plans_failed}\n")
        log_file.write(f"Directory of generated plans: {plans_dir_path}\n")
        log_file.write("\n ----- Times for planning -----\n")
        log_file.write(f"Average Time: {avg_time:.2f} seconds\n")
        log_file.write(f"Min Time: {min_time:.2f} seconds\n")
        log_file.write(f"Max Time: {max_time:.2f} seconds\n")
        log_file.write(f"Median Time: {median_time:.2f} seconds\n")
        log_file.write(f"Standard Deviation: {std_dev:.2f} seconds")

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

def final_output(plans_failed, plans_dir_path, avg_time, min_time, max_time, median_time, std_dev):
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
    print(f"Total of plans failed: {plans_failed}")
    print(f"Directory of generated plans: {plans_dir_path}")
    print("\n ----- Times for planning -----\n")
    print(f"Average Time: {avg_time:.2f} seconds")
    print(f"Min Time: {min_time:.2f} seconds")
    print(f"Max Time: {max_time:.2f} seconds")
    print(f"Median Time: {median_time:.2f} seconds")
    print(f"Standard Deviation: {std_dev:.2f} seconds")