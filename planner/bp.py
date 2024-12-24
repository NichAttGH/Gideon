# Import necessary libraries
import argparse                  # For command line argument handling

# Import custom managers and controllers
from Planner_progress_manager import Planner_Progress_Manager
from Planner_log_manager import Planner_Log_Manager
from Planner_generator import Planner_generator, load_domain
from utils_planner import Planner_Structure, read_problems, find_planner_and_validate_paths

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

def main(args):
    """
    Main function to execute the planner generation process.
    
    Args:
        args: Command line arguments parsed from user input.
        
    This function initializes the planner structure, loads the domain and problems, 
    manages progress and logs, get paths of Validate and chosen Planner,
    and generates plans based on the provided parameters.
    """
    # Initialize planner structure
    planner_structure = Planner_Structure(args.output_dir)
    domain_path, problems_dir_path, logs_dir_path, plans_dir_path, planner_progress_path, results_dir_path = planner_structure.get_structure_more_problems()
    domain = load_domain(domain_path)
    num_problems, problems_paths = read_problems(problems_dir_path)

    # Initialize progress and log managers
    planner_progress_manager = Planner_Progress_Manager(planner_progress_path)
    planner_logs_manager = Planner_Log_Manager(logs_dir_path)

    # Get Planner and Validate paths
    planner_path, validate_path = find_planner_and_validate_paths(args.planner)

    # Initialize the planner generator with necessary parameters
    planner_generator = Planner_generator(
        num_problems,
        args.output_dir,
        planner_progress_manager,
        planner_logs_manager,
        args.planner,
        planner_path,
        validate_path
    )
    
    # Generate plans
    planner_generator.generate_plans(problems_paths, domain_path, plans_dir_path, domain, results_dir_path)

    print("All operations completed!")

if __name__ == "__main__":
    # Command line argument parser setup
    parser = argparse.ArgumentParser(description='Generate random instances of PDDL problem files')
    parser.add_argument('-o','--output_dir', type=str, help='Output path of PDDL problem files')
    parser.add_argument('-c', '--planner', choices=['probe'], default='probe', help='Choose which planner to use')
    args = parser.parse_args()

    # Launch main function
    main(args)