# Import necessary libraries
import os                   # For control commands
import subprocess           # To execute Planner and Validate
import shutil               # To copy or remove files
import time                 # To calculate statistics
import pickle               # To easily make figures using pandas
from tqdm import tqdm       # To put a bar that increases
from pathlib import Path    # To iterate over the paths

# Modules import
from pddl import parse_domain
from utils_planner import (
    rename_plan,
    convert_to_IPC_format,
    final_output,
    calculate_statistics,
    find_failed_problems,
    delete_and_renumber,
    read_plans,
    update_npg_progress
)

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

class Planner_generator:
    def __init__(self, num_problems, output_dir, planner_progress_manager, planner_logs_manager,
                 planner, planner_path, validate_path):
        """
        Initializes the Planner_generator with the specified parameters.
        
        Args:
            num_problems (int): Number of problems to generate.
            output_dir (str): Directory where output files will be stored.
            planner_progress_manager (Planner_Progress_Manager): Manager for tracking progress.
            planner_logs_manager (Planner_Log_Manager): Manager for handling logs.
            planner (str): The planner to be used for generation.
            planner_path (str): Path to the planner executable.
            validate_path (str): Path to the validation tool.
        """
        self.num_problems = num_problems
        self.output_dir = output_dir
        self.planner_progress_manager = planner_progress_manager
        self.planner_logs_manager = planner_logs_manager
        self.planner = planner
        self.planner_path = planner_path
        self.validate_path = validate_path

    def generate_plans(self, problems_paths, domain_path, plans_dir_path, domain, results_dir_path):
        """
        Generates plans for the specified problems using the configured planner.
        
        Args:
            problems_paths (list): List of paths to problem files.
            domain_path (str): Path to the domain file.
            plans_dir_path (str): Directory where generated plans will be stored.
            domain: The domain object used for planning.
            results_dir_path (str): Directory where results will be saved.
            
        This method manages the planning process, including progress tracking, 
        execution time measurement, and result storage.
        Furthermore, By pressing 'Ctrl + C' is possible to stop the processing
        and choose to save the progress or not (like folders, plans, ecc..)
        """
        try:
            if self.num_problems > 1:
                ppg = self.planner_progress_manager.check_progress(plans_dir_path, self.output_dir)

                execution_times = []    # List to collect execution times

                if ppg != 0:
                    # Add the Progress Bar
                    with tqdm(initial=ppg, total=self.num_problems, leave=True, desc="Generating plans", unit=" plan") as pbar:
                        # Processing
                        for i, problem in enumerate(problems_paths[ppg:], start=ppg):
                            new_name, execution_times = choose_planner(
                                self.planner, self.planner_path, domain_path, problem, plans_dir_path,
                                self.output_dir, domain, i, execution_times)
                            check_val_and_move(self.validate_path, domain_path, problem, new_name, plans_dir_path)
                            pbar.update(1) # Update the Progress Bar
                
                elif ppg == 0:
                    # Add the Progress Bar
                    with tqdm(initial=ppg, total=self.num_problems, leave=True, desc="Generating plans", unit=" plan") as pbar:
                        # Processing
                        for i, problem in enumerate(problems_paths[ppg:], start=ppg):
                            new_name, execution_times = choose_planner(
                                self.planner, self.planner_path, domain_path, problem, plans_dir_path,
                                self.output_dir, domain, i, execution_times)
                            check_val_and_move(self.validate_path, domain_path, problem, new_name, plans_dir_path)
                            pbar.update(1) # Update the Progress Bar

                # Convert each plan to IPC format
                convert_to_IPC_format(plans_dir_path)

                # Check deleted problems and renumber
                failed_problems = find_failed_problems(self.output_dir)
                answer = delete_and_renumber(self.output_dir, failed_problems)

                # Calculate statistics
                avg_time, min_time, max_time, median_time, std_dev = calculate_statistics(execution_times)

                # Save data in /results with pickle
                pickle_file_path = os.path.join(results_dir_path,"execution_times.pkl")
                with open(pickle_file_path, "wb") as file:  # "wb" = write binary
                    pickle.dump(execution_times, file)
                print(f"Times saved in: {pickle_file_path}")

                # Time required for the processing
                t = pbar.format_dict['elapsed']

                # Count generated plans to save progress
                plan_count = read_plans(plans_dir_path)
                self.planner_progress_manager.save_progress(plan_count)

                # Update the progress of generated problems
                if answer == 'y':
                    npg_path = os.path.join(self.output_dir, "npg_progress.txt")
                    update_npg_progress(plan_count, npg_path)

                # Generate log file
                self.planner_logs_manager.generate_log_file(
                    i+1, len(failed_problems), plans_dir_path, t, avg_time, min_time, max_time, median_time, std_dev)
                
                # Final output for the user
                final_output(i+1, len(failed_problems), plans_dir_path, t, avg_time, min_time, max_time, median_time, std_dev)
        
        except KeyboardInterrupt:
            # Intercepts Ctrl+C and offer a choice to the User
            print("\nProcessing interrupted by the user")
            while True:
                user_input = input("Do you want to delete generated files until now? (y/n): ").strip().lower()
                if user_input == 'y':
                    print("Deleting in progress...")
                    shutil.rmtree(plans_dir_path)
                    shutil.rmtree(results_dir_path)
                    log_dir_path = Path(os.path.join(self.output_dir, "logs"))
                    search_string = "planning"
                    for file in log_dir_path.iterdir():
                        if file.is_file() and (search_string in file.name):
                            os.remove(file)
                    print("All the generated files have been deleted")
                    break
                elif user_input == 'n':
                    # Convert each plan to IPC format
                    convert_to_IPC_format(plans_dir_path)

                    # Check deleted problems and renumber
                    failed_problems = find_failed_problems(self.output_dir)
                    answer = delete_and_renumber(self.output_dir, failed_problems)

                    # Calculate statistics
                    avg_time, min_time, max_time, median_time, std_dev = calculate_statistics(execution_times)

                    # Save data in /results with pickle
                    pickle_file_path = os.path.join(results_dir_path,"execution_times.pkl")
                    with open(pickle_file_path, "wb") as file:  # "wb" = write binary
                        pickle.dump(execution_times, file)
                    print(f"Times saved in: {pickle_file_path}")

                    # Time required for the processing
                    t = pbar.format_dict['elapsed']

                    # Count generated plans to save progress
                    plan_count = read_plans(plans_dir_path)
                    self.planner_progress_manager.save_progress(plan_count)

                    # Update the progress of generated problems
                    if answer == 'y':
                        npg_path = os.path.join(self.output_dir, "npg_progress.txt")
                        update_npg_progress(plan_count, npg_path)

                    # Generate log file
                    self.planner_logs_manager.generate_log_file(
                        i, len(failed_problems), plans_dir_path, t, avg_time, min_time, max_time, median_time, std_dev)
                    
                    # Final output for the user
                    final_output(i, len(failed_problems), plans_dir_path, t, avg_time, min_time, max_time, median_time, std_dev)
                    break
                else:
                    print("Choice not valid. Type 'y' or 'n' !")

def load_domain(domain_path):
    """
    Loads a PDDL domain from a specified file.

    Args:
        domain_path (str): The path to the PDDL domain file.

    Returns:
        object: The parsed domain object.

    Raises:
        SystemExit: If the domain contains numeric fluents.
    """
    with open(domain_path, 'r') as file:
        content = file.read()
        if ":functions" in content:
            raise SystemExit("This domain is not valid because it has instances of 'numeric fluents'!")
        else:
            domain = parse_domain(domain_path)
    return domain

def choose_planner(planner, planner_path, domain_path, problem_path, plans_dir_path, output_dir, domain, i, execution_times):
    """
    Chooses the planner to execute based on the specified planner type.
    
    Args:
        planner (str): The planner to use (e.g., "probe").
        planner_path (str): Path to the planner executable.
        domain_path (str): Path to the domain file.
        problem_path (str): Path to the problem file.
        plans_dir_path (str): Directory where plans will be stored.
        output_dir (str): Directory for output files.
        domain: The domain object used for planning.
        i (int): Index of the current problem.
        execution_times (list): List to collect execution times.
    """

    if planner == "probe":
        try:
            start_time = time.time()  # Start measuring time

            # Start the external process in non-blocking mode
            probe_process = subprocess.Popen(
                [planner_path, "-d", domain_path, "-i", problem_path, "-o", plans_dir_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            # Retrieve output upon process completion
            stdout, stderr = probe_process.communicate()

            # Calculate execution time and add it to the list
            end_time = time.time()
            execution_time = end_time - start_time
            execution_times.append(execution_time)

            if "SOLUTION" in stdout:
                new_name = rename_plan(output_dir, domain, i)
            else:
                new_name = None

            return new_name, execution_times
        except Exception as e:
            print(f"Error while executing planner: {e}")
            return None, execution_times

    #elif planner == "altro_planner":
        # Logic for others planners
    else:
        print(f"Planner {planner} not recognized")

def check_val_and_move(validate_path, domain_path, problem_path, new_name, plans_dir_path):
    """
    Validates the generated plan and moves it to the plans directory if valid.
    
    Args:
        validate_path (str): Path to the validation tool.
        domain_path (str): Path to the domain file.
        problem_path (str): Path to the problem file.
        new_name (str): Name of the newly generated plan.
        plans_dir_path (str): Directory where plans will be stored.
        
    Returns:
        int: Updated number of failed plans.
    """
    if new_name is not None:
        try:
            # Start the external process in non-blocking mode
            process = subprocess.Popen(
                [validate_path, domain_path, problem_path, new_name],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            # Retrieve output upon process completion
            stdout, stderr = process.communicate()

            # Check if "success" is in the command output
            if "Successful" in stdout:
                shutil.move(new_name, plans_dir_path)
            else:
                os.remove(new_name)
        except Exception as e:
            print(f"Error during validation: {e}")