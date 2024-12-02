# Import necessary libraries
import argparse                 # For command line argument handling
from pynput import keyboard     # For keyboard shortcut management

# Import custom managers and controllers
from Process_controller import Process_Controller
from utils import Folder_Structure
from Progress_manager import Progress_Manager
from Log_manager import Log_Manager
from Hash_list_manager import Hash_list_Manager
from PDDL_generator import PDDL_Generator, load_domain
from Json_setup import load_json

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

def on_press(key):
    """
    Handles keyboard press events to control the process execution.

    Parameters:
    key (Key): The key that was pressed.

    Functionality:
    - Listens for specific key presses to control the process:
        - 'p': Pauses the process.
        - 'r': Resumes the process.
        - 's': Stops the process and exits the listener.
    """
    try:
        # Check if the pressed key has a character attribute (i.e., it's a regular key)
        if key.char == 'p':  # Pause
            process_controller.paused_p()
        elif key.char == 'r':  # Resume
            process_controller.resume_p()
        elif key.char == 's':  # Stop
            process_controller.stop_p()
            return False  # Stop listener to exit the program
    except AttributeError:
        # If the pressed key does not have a character (e.g., special keys), ignore the error
        pass

def main(args):
    """
    Main function to orchestrate the generation of PDDL problem files.
    
    Parameters:
    args (Namespace): Parsed command line arguments containing paths and settings.
    
    Steps:
    1. Load the PDDL domain from the specified file.
    2. Initialize the folder structure manager with the provided parameters.
    3. Create the necessary folder structure and retrieve paths for problems, logs, output, and progress.
    4. Initialize managers for progress tracking, logging, and duplicate checking.
    5. Load the JSON schema and generate objects from it.
    6. Initialize the PDDL generator with the necessary managers and parameters.
    7. Start the problem generation process.
    8. Print a completion message.
    """
    # Load PDDL domain from specified file
    domain = load_domain(args.domain_origin)
    
    # Initialize folder structure manager
    folder_structure = Folder_Structure(args.num_problems, args.output_dir, args.domain_origin, domain, args.json_path)

    # Create folder structure and get paths
    problems_path, logs_path, output_path, progress_path = folder_structure.create_structure()

    # Initialize required managers for generation
    progress_manager = Progress_Manager(progress_path)   # Handles generation progress
    log_manager = Log_Manager(logs_path)                 # Handles log files
    hashlist_manager = Hash_list_Manager(output_path)    # Handles duplicate checking

    # Read JSON file and generate objects
    json_schema = load_json(args.json_path)
    json_schema.generate_objects()

    # Initialize PDDL generator with all necessary managers
    pddl_generator = PDDL_Generator(
        args.num_problems, 
        progress_manager, 
        log_manager, 
        hashlist_manager, 
        process_controller,
    )

    # Start problem generation
    pddl_generator.generate_problems(args.generator_path, domain, problems_path, output_path, json_schema)

    print("All operations completed. Happy planning!")

if __name__ == "__main__":
    """
    Entry point of the script. Sets up command line argument parsing and initializes the process controller.
    
    Steps:
    1. Set up command line argument parser with descriptions and expected parameters.
    2. Parse the command line arguments.
    3. Initialize the process controller for managing execution flow.
    4. Start the listener for keys (pause, resume, stop).
    5. Call the main function with the parsed arguments.
    """
    # Command line argument parser setup
    parser = argparse.ArgumentParser(description='Generate random instances of PDDL problem files')   
    parser.add_argument('-g', '--generator_path', type=str, help='Origin path of the generator, only needed for 1 PDDL problem file')
    parser.add_argument('-d','--domain_origin', type=str, help='Origin path of PDDL domain file')
    parser.add_argument('-o','--output_dir', type=str, help='Output path of PDDL problem files')
    parser.add_argument('-n', '--num_problems', type=int, help='Number of problems that you want to create')
    parser.add_argument('-j', '--json_path', type=str, help='Origin path of the JSON file')
    args = parser.parse_args()

    # Process controller initialization
    process_controller = Process_Controller()

    # Start the listener for keys (pause, resume, stop)
    listener = keyboard.Listener(on_press=on_press) # Set up the keyboard listener for key press events
    listener.start()    # Start the listener

    # Launch main function
    main(args)