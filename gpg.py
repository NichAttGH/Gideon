# Core library imports
import os          # File and directory operations
import random      # Random number generation and selections
import argparse    # Command-line argument parsing
import shutil      # High-level file operations (copy, move)
import hashlib     # For generating unique hashes of problems
import keyboard    # Handling keyboard inputs for control
import time, datetime  # Time tracking and timestamps
from tqdm import tqdm  # Progress bar visualization

# PDDL-specific imports
from pddl import parse_domain          # Parses PDDL domain files
from pddl.core import Problem          # PDDL Problem representation
from pddl.logic import constants, Predicate    # PDDL logical components
from pddl.logic.base import Not, And   # Logical operators for PDDL

__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

# ===== Process Control Functions =====
def paused_p():
    """
    Pauses the problem generation process.
    
    Implementation:
    - Uses global 'pause' variable as a flag
    - Sets pause to True when 'p' key is pressed
    - Prints confirmation message
    
    Usage:
    - Connected to keyboard hotkey 'p'
    - Used in main generation loop to temporarily halt processing
    """
    global pause
    pause = True
    print("\nPaused processing..")

def resume_p():
    """
    Resumes the problem generation process after a pause.
    
    Implementation:
    - Uses global 'pause' variable as control flag
    - Only acts if process is currently paused
    - Connected to keyboard hotkey 'r'
    
    Usage:
    - Called when user presses 'r' key
    - Works in conjunction with paused_p() function
    - Part of the interactive control system
    """
    global pause
    if pause:
        pause = False
        print("\nResume processing..")

def stop_p():
    """
    Stops the problem generation process completely.
    
    Implementation:
    - Uses global 'stop' variable as control flag
    - Connected to keyboard hotkey 's'
    - Triggers cleanup and exit procedures
    
    Usage:
    - Called when user presses 's' key
    - Provides clean termination of process
    - Preserves progress and generates reports
    """
    global stop
    stop = True
    print("\nEnd processing...")

# ===== Other Control Functions =====
def final_output(c, t, problems_path):
    """
    Displays final statistics of the problem generation process.
    
    Args:
        c (int): Count of successfully generated problems
        t (float): Total time taken for generation (in seconds)
        problems_path (str): Directory path where problems were saved
    
    Output Information:
    1. Total number of problems generated
    2. Location of generated problems
    3. Total time taken for generation
    
    Format:
    - Problem count: Simple integer
    - Directory: Full path
    - Time: Formatted to 2 decimal places (seconds)
    
    Usage:
    - Called at normal completion
    - Called after stop_p() termination
    - Provides user with summary statistics
    
    Example Output:
    Number of generated problems: 50
    Directory of generated problems: /path/to/problems
    Time required to generate problems: 23.45 seconds
    """
    print(f"Number of generated problems: {c}")
    print(f"Directory of generated problems: {problems_path}")
    print(f"Time required to generate problems: {t:.2f} seconds")

def folder_structure(output_dir, domain_origin, domain):
    """
    Creates and manages the folder structure for output files.
    
    Args:
        output_dir: Base directory for output
        domain_origin: Path to original domain file
        domain: Parsed domain object
    
    Returns:
        Tuple of (problems_path, logs_path, output_path)
    
    Structure Created:
    output_dir/
    ├── domain_name/
    │   ├── domain.pddl (copied)
    │   ├── problems/
    │   └── logs/
    
    Error Handling:
    - Validates output_path existence
    - Handles file copying errors
    - Creates directories safely with exist_ok
    """
    output_path = os.path.join(output_dir, domain.name)
    os.makedirs(output_path, exist_ok=True)
    
    # Create a copy of the domain file
    if output_path is None:
        raise ValueError(f"The {output_path} argument is None. Please write it or ensure it is set correctly!")
    try:
        shutil.copy(domain_origin, output_path)
    except FileNotFoundError:
        print(f"Error: The file {domain_origin} doesn't exists.")
    except IOError as e:
        print(f"Error when copying the file: {e}")

    # Generate folder for the problem files
    problems_dir = "problems"
    problems_path = os.path.join(output_path, problems_dir)
    os.makedirs(problems_path, exist_ok=True)

    # Generate folder for the log files
    log_dir = "logs"
    logs_path = os.path.join(output_path, log_dir)
    os.makedirs(logs_path, exist_ok=True)

    return problems_path, logs_path, output_path
    
# ===== Progress Functions =====
def save_progress(i, progress_path):
    """
    Saves current generation progress to file.
    
    Args:
        i: Current problem number
        progress_path: Path to progress file
    
    Implementation:
    - Writes current problem index to file
    - Used for resuming interrupted generations
    """
    with open(progress_path, 'w') as f:
        f.write(str(i))

def read_progress(progress_path):
    """
    Reads previous generation progress from file.
    
    Args:
        progress_path: Path to progress file
    
    Returns:
        int: Last generated problem number (0 if no progress file)
    
    Implementation:
    - Checks for existing progress file
    - Returns saved progress number or 0
    """
    if os.path.exists(progress_path):
        with open(progress_path, 'r') as f:
            return int(f.read().strip())
    return 0
    
def check_progress(problems_path, output_path, progress_path):
    """
    Interactively checks for previous generation progress.
    
    Args:
        problems_path: Path to problems directory
        output_path: Path to output directory
        progress_path: Path to progress file
    
    Returns:
        int: Number of previously generated problems
    
    User Interaction:
    - Asks user if previous progress exists
    - Validates user input (Y/N)
    - Returns appropriate progress number
    """
    while True:
        print("Is there a stopped processing in advance? (Y for yes, N for no)")
        answer = input().strip().upper()        
        if answer == "Y":
            if os.path.exists(problems_path) and os.path.exists(output_path):
                npg = read_progress(progress_path)
                return npg
        elif answer == "N":
            return 0
        else:
            print("Invalid input, please enter 'Y' for yes or 'N' for no.")

# ===== Log Function =====
def generate_log_file(c, logs_path, problems_path, t):
    """
    Creates log file with generation statistics.
    
    Args:
        c: Count of generated problems
        logs_path: Path to logs directory
        problems_path: Path to problems directory
        t: Time taken for generation
    
    Log Contents:
    - Number of problems generated
    - Directory location
    - Time taken
    - Timestamp in filename
    """
    current_date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f"{current_date}.txt"
    log_file_path = os.path.join(logs_path, log_filename)
    with open(log_file_path, 'w') as log_file:
        log_file.write(f"Number of generated problems: {c}\n")
        log_file.write(f"Directory of generated problems: {problems_path}\n")
        log_file.write(f"Time required to generate problems: {t:.2f} seconds")

# ===== Hash List Functions =====
def generate_hash_list(hash_list_path, hash_list):
    """
    Saves problem hashes to prevent duplicates.
    
    Args:
        hash_list_path: Path to hash list file
        hash_list: List of problem hashes
    
    Purpose:
    - Maintains record of generated problems
    - Used for collision detection
    """
    with open(hash_list_path, 'w') as f:
        for hash in hash_list:
            f.write(f"{hash}\n")
    
def read_hash_list_to_list(hash_list_path):    
    """
    Reads previously saved problem hashes from file into a list.
    
    Args:
        hash_list_path (str): Path to the file containing saved problem hashes
    
    Returns:
        list: List of problem hashes (empty list if file doesn't exist)
    
    Implementation Details:
    1. Initializes empty list for storing hashes
    2. Checks if hash file exists
    3. If exists:
       - Opens file in read mode
       - Reads each line (hash)
       - Strips whitespace/newlines
       - Adds to hash list
    4. If doesn't exist:
       - Returns empty list
    
    Usage:
    - Called when resuming interrupted generation
    - Used for collision detection with previous problems
    - Maintains problem uniqueness across sessions
    
    Error Handling:
    - Safely handles non-existent files
    - Strips any extra whitespace/newlines
    - Returns empty list if file is empty
    """
    hash_list = []
    
    # Check if the file exists and read the hashes
    if os.path.exists(hash_list_path):
        with open(hash_list_path, 'r') as f:
            hash_list = [line.strip() for line in f]

    return hash_list

# ===== Generating PDDL Problem Files =====
def load_domain(domain_origin):
    """
    Loads and validates PDDL domain file.
    
    Args:
        domain_origin: Path to domain file
    
    Returns:
        Parsed domain object
    
    Validation:
    - Checks for numeric fluents (not supported)
    - Parses domain file
    
    Raises:
        SystemExit: If domain contains numeric fluents
    """
    with open(domain_origin, 'r') as file:
        content = file.read()
        if ":functions" in content:
            raise SystemExit("This domain is not valid because it has instances of 'numeric fluents'!")
        else:
            domain = parse_domain(domain_origin)

    return domain

def generate_random_objects(prob_types, set_predicates):
    """
    Creates random objects for the PDDL problem based on domain types.
    
    Args:
        prob_types: List of types defined in the domain (e.g., ['block', 'location'])
        set_predicates: Set of predicates from the domain (e.g., {on(x,y), clear(x)})
    
    Returns:
        List of PDDL constants (objects) with appropriate types
    
    Implementation Details:
    1. Initialize empty list for constants and boolean flag
    2. Check predicates for multi-term requirements:
       - Scans each predicate's terms
       - Sets boolean=True if any predicate needs multiple objects
    
    3. Object Generation Logic:
       a) Multiple Types Case:
          - For each type, creates 1 to n objects
          - Names format: "type_1", "type_2", etc.
          
       b) Single Type with Multi-term Predicates:
          - Creates 2-5 objects (minimum 2 for multi-term predicates)
          - Names format: "obj1_type", "obj2_type", etc.
          
       c) Single Type with Single-term Predicates:
          - Creates 1-5 objects
          - Names format: "obj1_type", "obj2_type", etc.
    """
    vet_constants = []
    boolean = False

    # Checks that among the domain predicates there is one with more than one term
    for predicate in set_predicates:
        if len(predicate.terms) > 1:
            boolean = True

    for type in prob_types:
        if len(prob_types) > 1:
            x = random.randint(1, len(prob_types))          # Random integer number of objects you want to create
            for i in range (x):
                vet_constants += constants(f"{type}_{i+1}", type_=type)
        elif len(prob_types) == 1 & boolean == True:
            y = random.randint(2, 5)                        # Random integer number of objects you want to create.
                                                            # In case the domain has only one type, arbitrarily decide the
                                                            # limit of objects you want to create by changing the number 5
            for i in range (y):
                vet_constants += constants(f"obj{i+1}_{type}", type_=type)
        else:
            z = random.randint(1, 5)                        # Random integer number of objects you want to create.
                                                            # In case the domain has only 1 type and every predicate has
                                                            # only 1 term, arbitrarily decide the limit of objects you want
                                                            # to create by changing the number '5' (like in the 'Y' case)
            for i in range (z):
                vet_constants += constants(f"obj{i+1}_{type}", type_=type)            
    
    prob_objects = vet_constants

    return prob_objects

def generate_random_init_state(prob_objects, set_predicates):
    """
    Generates random initial state by creating ground predicates.
    
    Args:
        prob_objects: List of available PDDL objects (e.g., [block1, block2])
        set_predicates: Set of predicates from domain (e.g., {on(x,y), clear(x)})
    
    Returns:
        Set of ground predicates forming initial state
    
    Implementation Details:
    1. Initialize empty set for initial state
    2. For each predicate in domain:
       a) Extract predicate name and parameters
       b) Handle based on parameter count:
          - 2 parameters: Select two distinct objects
          - 1 parameter: Select one object
          - 0 parameters: Use predicate directly
       c) Randomly decide to negate predicate
       d) Add to initial state
    """
    initial_state = set()
    
    for predicate in set_predicates:
        predicate_name = predicate.name
        params = predicate.terms

        if len(params) == 2:
            obj1, obj2 = random.sample(prob_objects, 2)
            p = Predicate(predicate_name, obj1, obj2)
            k = random.choice([p, Not(p)])
            initial_state.add(k)
        elif len(params) == 1:
            obj = random.choice(prob_objects)
            p = Predicate(predicate_name, obj)
            k = random.choice([p, Not(p)])
            initial_state.add(k)
        else:
            p = Predicate(predicate_name)
            k = random.choice([p, Not(p)])
            initial_state.add(k)

    return initial_state

def generate_random_goal_state(prob_objects, set_predicates):
    """
    Generates random goal state for the PDDL problem.
    
    Args:
        prob_objects: List of available PDDL objects
        set_predicates: Set of predicates from domain
    
    Returns:
        Set of ground predicates forming goal state
    
    Implementation Details:
    1. Initialize empty goal state set
    2. Randomly select subset of predicates to use in goal
    3. For each selected predicate:
       - Handle different arities (0,1,2 parameters)
       - Randomly assign objects and negation
    
    Key Difference from init_state:
    - Only uses a subset of predicates (makes goals more achievable)
    """
    goal_state = set()
    selected_predicates = random.sample(list(set_predicates), 
                                      k=random.randint(1, len(set_predicates)))

    for predicate in selected_predicates:
        predicate_name = predicate.name
        params = predicate.terms

        if len(params) == 2:
            obj1, obj2 = random.sample(prob_objects, 2)
            p = Predicate(predicate_name, obj1, obj2)
            k = random.choice([p, Not(p)])
            goal_state.add(k)

        elif len(params) == 1:
            obj = random.choice(prob_objects)
            p = Predicate(predicate_name, obj)
            k = random.choice([p, Not(p)])
            goal_state.add(k)

        else:
            p = Predicate(predicate_name)
            k = random.choice([p, Not(p)])
            goal_state.add(k)

    return goal_state

def generate_single_problem(domain, problem_name):
    """
    Generates single PDDL problem instance.
    
    Args:
        domain: Parsed domain object
        problem_name: Name for new problem
    
    Returns:
        Problem: Complete PDDL problem instance
    
    Process:
    1. Extract domain components (types, predicates)
    2. Generate random objects
    3. Create initial state
    4. Create goal state
    5. Construct complete problem
    """
    prob_types = domain.types
    prob_predicates = domain.predicates
    set_predicates = set(prob_predicates)           # Needed to use predicates into the functions
    prob_objects = generate_random_objects(prob_types, set_predicates)
    init_state = generate_random_init_state(prob_objects, set_predicates)
    goal_state = generate_random_goal_state(prob_objects, set_predicates)

    # Instance of the problem
    problem = Problem(
        name=problem_name,
        domain=domain,
        domain_name=domain.name,
        requirements=domain.requirements,
        objects=prob_objects,
        init=init_state,
        goal=And(*goal_state)   # '*' unpacks the data structure to obtain the goal state
                                # You can change the logic port And() with others like Or() ecc..
    )

    return problem

def generate_problems(generator_path, num_problems, domain, problems_path, logs_path, output_path):
    """
    Main problem generation orchestration function.
    
    Args:
        generator_path: Path to generator
        num_problems: Number of problems to generate
        domain: Parsed domain
        problems_path: Output path for problems
        logs_path: Path for log files
        output_path: Base output directory
    
    Features:
    - Progress bar display
    - Pause/Resume/Stop functionality
    - Duplicate detection
    - Progress saving
    - Log generation
    
    Implementation:
    1. Initialize tracking variables
    2. Set up progress and hash tracking
    3. Generate problems with user control
    4. Handle interruptions and completion
    """
    if num_problems > 1:
        hash_list = []      # Hash list that will contain all the hash already used
        c = 0       # Counter for generated problems
        npg = 0     # Initialized to 0 because at the beginning there isn't a progress
        npg_filename = "npg_progress.txt"       # Name of the file needed to take the progress value
        progress_path = os.path.join(output_path, npg_filename)     # Path of the progress npg file
        hash_list_filename = "hash_list.txt"      # Name of the file needed to take progress of the hash list
        hash_list_path = os.path.join(output_path, hash_list_filename)    # Path of the progress hash list file

        print("Press one of these keys:\n - 'p' -> Pause the processing\n - 'r' -> Resume the processing\n - 's' -> Stop the processing and Exit")
        
        npg = check_progress(problems_path, output_path, progress_path)
        
        if npg != 0:
            hash_list = read_hash_list_to_list(hash_list_path)  # Needed to update hash list if you want to add more problems
            
            # Add the Progress Bar
            with tqdm(initial=npg, total=num_problems, leave=True, desc="Generating problems", unit=" problem") as pbar:
                
                # Processing
                for i in range(npg, num_problems):

                    # Check pause, resume and stop
                    if stop:
                        t = pbar.format_dict['elapsed']         # Time required for the processing if the process is stopped
                        save_progress(i, progress_path)         # Save progress if stopped processing
                        generate_log_file(c, logs_path, problems_path, t)   # Generate log file
                        generate_hash_list(hash_list_path, hash_list)       # Generate hash list file
                        final_output(c, t, problems_path)       # Final output for the user
                        raise SystemExit()
                    while pause:
                        time.sleep(0.1)  # Wait a moment before checking again the state
                        if stop:
                            t = pbar.format_dict['elapsed']         # Time required for the processing if the process is stopped
                            save_progress(i, progress_path)         # Save progress if stopped processing
                            generate_log_file(c, logs_path, problems_path, t)   # Generate log file
                            generate_hash_list(hash_list_path, hash_list)       # Generate hash list file
                            final_output(c, t, problems_path)       # Final output for the user
                            raise SystemExit()

                    problem_name = f"{domain.name}_problem_00000{i + 1}"
                    problem = generate_single_problem(domain, problem_name)

                    hash_16bit = hashlib.sha256(str(problem).encode()).hexdigest()  # Assign the hash to each problem

                    # Check Collision
                    if hash_16bit in hash_list:
                        print(f"Collision revealed: the problem '{problem.name}' is duplicated.\n")
                        print(f"The hash '{hash_16bit}' is already present.\n")
                    else:
                        hash_list.append(hash_16bit)
                        problem_file_path = os.path.join(problems_path, f"{problem_name}.pddl")
                        with open(problem_file_path, 'w') as file:
                            file.write(str(problem))

                    pbar.update(1)                  # Update the Progress Bar
                    c += 1                          # Increases each time a problem is generated

        elif npg == 0:
            hash_list = read_hash_list_to_list(hash_list_path)  # Needed to update hash list if you want to add more problems
            
            # Add the Progress Bar
            with tqdm(total=num_problems, leave=True, desc="Generating problems", unit=" problem") as pbar:

                # Processing
                for i in range(num_problems):

                    # Check pause, resume and stop
                    if stop:
                        t = pbar.format_dict['elapsed']         # Time required for the processing if the process is stopped
                        save_progress(i, progress_path)         # Save progress if stopped processing
                        generate_log_file(c, logs_path, problems_path, t)   # Generate log file
                        generate_hash_list(hash_list_path, hash_list)       # Generate hash list file
                        final_output(c, t, problems_path)       # Final output for the user
                        raise SystemExit()
                    while pause:
                        time.sleep(0.1)  # Wait a moment before checking again the state
                        if stop:
                            t = pbar.format_dict['elapsed']         # Time required for the processing if the process is stopped
                            save_progress(i, progress_path)         # Save progress if stopped processing
                            generate_log_file(c, logs_path, problems_path, t)   # Generate log file
                            generate_hash_list(hash_list_path, hash_list)       # Generate hash list file
                            final_output(c, t, problems_path)       # Final output for the user
                            raise SystemExit()
                        
                    problem_name = f"{domain.name}_problem_00000{i + 1}"
                    problem = generate_single_problem(domain, problem_name)

                    hash_16bit = hashlib.sha256(str(problem).encode()).hexdigest()  # Assign the hash to each problem

                    # Check Collision
                    if hash_16bit in hash_list:
                        print(f"Collision revealed: the problem '{problem.name}' is duplicated.\n")
                        print(f"The hash '{hash_16bit}' is already present.\n")
                    else:
                        hash_list.append(hash_16bit)
                        problem_file_path = os.path.join(problems_path, f"{problem_name}.pddl")
                        with open(problem_file_path, 'w') as file:
                            file.write(str(problem))

                    pbar.update(1)                          # Update the Progress Bar
                    c += 1                                  # Increases each time a problem is generated

        t = pbar.format_dict['elapsed']                     # Time required for the processing
        save_progress(i+1, progress_path)                   # Save progress if ended processing
        generate_log_file(c, logs_path, problems_path, t)   # Generate log file
        generate_hash_list(hash_list_path, hash_list)       # Generate hash list file
        final_output(c, t, problems_path)                   # Final output for the user

    elif num_problems == 1:
        problem_name = f"{domain.name}_problem_000001"
        problem = generate_single_problem(domain, problem_name)

        # Save the problem file
        problem_file_path = os.path.join(generator_path, f"{problem_name}.pddl")
        with open(problem_file_path, 'w') as file:
            file.write(str(problem))
        print(f"Path of the generated problem file: {problem_file_path}\n")        

# ===== Main Function =====
def main(args):
    """
    Main execution function coordinating the problem generation process.
    
    Args:
        args: Parsed command line arguments containing:
            - domain_origin: Path to source domain file
            - output_dir: Directory for output files
            - num_problems: Number of problems to generate
            - generator_path: Path to generator script
    
    Process Flow:
    1. Load and validate domain file
    2. Create folder structure
    3. Generate requested problems
    4. Handle completion and cleanup
    
    Error Handling:
    - Domain loading errors
    - Directory creation issues
    - Generation interruptions
    """
    domain = load_domain(args.domain_origin)    # Load the domain file

    # Define the folder structure
    problems_path, logs_path, output_path = folder_structure(args.output_dir, args.domain_origin, domain)

    # Generate the problem files
    generate_problems(args.generator_path, args.num_problems, domain, problems_path, logs_path, output_path)
    print("All operations completed. Happy planning!")

if __name__ == "__main__":
    """
    Script entry point and command-line interface setup.
    
    Command Line Arguments:
    -g, --generator_path: Path to generator (required for single problem)
    -d, --domain_origin: Path to PDDL domain file
    -o, --output_dir: Output directory for generated files
    -n, --num_problems: Number of problems to generate
    
    Global Controls:
    - pause: Flag for pausing generation
    - stop: Flag for stopping generation
    
    Keyboard Shortcuts:
    - 'p': Pause generation
    - 'r': Resume generation
    - 's': Stop generation
    """
    parser = argparse.ArgumentParser(description='Generate random istances of PDDL problem files')   
    parser.add_argument('-g', '--generator_path', type=str, help='Origin path of the generator, only needed for 1 PDDL problem file')
    parser.add_argument('-d','--domain_origin', type=str, help='Origin path of PDDL domain file')
    parser.add_argument('-o','--output_dir', type=str, help='Output path of PDDL problem files')
    parser.add_argument('-n', '--num_problems', type=int, help='Number of problems that you want to create')
    args = parser.parse_args()

    # Control variables
    pause = False
    stop = False

    # Assign keys to the functions
    keyboard.add_hotkey('p', paused_p)
    keyboard.add_hotkey('r', resume_p)
    keyboard.add_hotkey('s', stop_p)

    main(args)