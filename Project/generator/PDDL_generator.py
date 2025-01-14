import os
import random
import time
import re
import shutil
from tqdm import tqdm

# Module imports
from Hash_list_manager import generate_hash
from utils import final_output
from Json_setup import PredicateStructure

# PDDL imports
from pddl import parse_domain
from pddl.core import Problem
from pddl.logic import Predicate
from pddl.logic.base import And

__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

class PDDL_Generator:
    """
    Generates PDDL problem files based on a specified domain and configuration.

    Attributes:
    - num_problems (int): The number of problems to generate.
    - progress_manager (object): Manages progress tracking.
    - log_manager (object): Manages logging of operations.
    - hashlist_manager (object): Manages duplicate checking for generated problems.
    - process_controller (object): Controls the processing state (pause, resume, stop).
    """
    def __init__(self, num_problems, progress_manager, log_manager, hashlist_manager, process_controller):
        self.num_problems = num_problems
        self.progress_manager = progress_manager
        self.log_manager = log_manager
        self.hashlist_manager = hashlist_manager
        self.process_controller = process_controller
    
    def generate_problems(self, generator_path, domain_origin, domain, problems_path, output_path, json_schema):
        """
        Generates PDDL problems based on the provided domain and configuration.

        Parameters:
        - generator_path (str): The path for the generator.
        - domain_origin (str): The path for the domain.
        - domain (object): The PDDL domain object.
        - problems_path (str): The path where problem files will be saved.
        - output_path (str): The path for output files.
        - json_schema (object): The JSON schema containing problem configuration.
        """
        if self.num_problems > 1:
            counts_for_init_state = {}           # Dict for init_state to keep track of the number of problems generated for each type
            counts_for_goal_state = {}           # Dict for goal_state to keep track of the number of problems generated for each type

            print("Press one of these keys:\n - 'p' -> Pause the processing\n - 'r' -> Resume the processing\n - 's' -> Stop the processing and Exit")
            
            npg, answer = self.progress_manager.check_progress(problems_path, output_path)
            
            if npg != 0:
                hash_list = self.hashlist_manager.read_hash_list_to_list(answer)  # Needed to update hash list if you want to add more problems
                
                # Add the Progress Bar
                with tqdm(initial=npg, total=self.num_problems, leave=True, desc="Generating problems", unit=" problem") as pbar:
                    
                    # Processing
                    for i in range(npg, self.num_problems):

                        # Check pause, resume and stop
                        if self.process_controller.stop:
                            
                            #print(counts_for_init_state)   # Show how much pools for each type chosen in mutex_pools init
                            #print(counts_for_goal_state)   # Show how much pools for each type chosen in mutex_pools goal
                            
                            t = pbar.format_dict['elapsed']         # Time required for the processing if the process is stopped
                            self.progress_manager.save_progress(i)         # Save progress if stopped processing
                            self.log_manager.generate_log_file(i, problems_path, t)   # Generate log file
                            self.hashlist_manager.generate_hash_list(hash_list)       # Generate hash list file
                            final_output(i, t, problems_path)       # Final output for the user
                            raise SystemExit()
                        while self.process_controller.pause:
                            time.sleep(0.1)  # Wait a moment before checking again the state
                            if self.process_controller.stop:
                                
                                #print(counts_for_init_state)   # Show how much pools for each type chosen in mutex_pools init
                                #print(counts_for_goal_state)   # Show how much pools for each type chosen in mutex_pools goal
                                
                                t = pbar.format_dict['elapsed']         # Time required for the processing if the process is stopped
                                self.progress_manager.save_progress(i)         # Save progress if stopped processing
                                self.log_manager.generate_log_file(i, problems_path, t)   # Generate log file
                                self.hashlist_manager.generate_hash_list(hash_list)       # Generate hash list file
                                final_output(i, t, problems_path)       # Final output for the user
                                raise SystemExit()

                        problem_name = f"{domain.name}_problem_00000{i + 1}"
                        problem, counts_for_init_state, counts_for_goal_state = generate_single_problem(domain, problem_name, json_schema, counts_for_init_state, counts_for_goal_state)
                        
                        hash_16bit = generate_hash(problem)  # Assign the hash to each problem

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

            elif npg == 0:
                hash_list = self.hashlist_manager.read_hash_list_to_list(answer)  # Needed to update hash list if you want to add more problems
                
                # Add the Progress Bar
                with tqdm(total=self.num_problems, leave=True, desc="Generating problems", unit=" problem") as pbar:

                    # Processing
                    for i in range(self.num_problems):

                        # Check pause, resume and stop
                        if self.process_controller.stop:
                            
                            #print(counts_for_init_state)   # show how much pools for each type chosen in mutex_pools init
                            #print(counts_for_goal_state)   # Show how much pools for each type chosen in mutex_pools goal
                            
                            t = pbar.format_dict['elapsed']         # Time required for the processing if the process is stopped
                            self.progress_manager.save_progress(i)         # Save progress if stopped processing
                            self.log_manager.generate_log_file(i, problems_path, t)   # Generate log file
                            self.hashlist_manager.generate_hash_list(hash_list)       # Generate hash list file
                            final_output(i, t, problems_path)       # Final output for the user
                            raise SystemExit()
                        while self.process_controller.pause:
                            time.sleep(0.1)  # Wait a moment before checking again the state
                            if self.process_controller.stop:
                                
                                #print(counts_for_init_state)   # show how much pools for each type chosen in mutex_pools init
                                #print(counts_for_goal_state)   # Show how much pools for each type chosen in mutex_pools goal
                                
                                t = pbar.format_dict['elapsed']         # Time required for the processing if the process is stopped
                                self.progress_manager.save_progress(i)         # Save progress if stopped processing
                                self.log_manager.generate_log_file(i, problems_path, t)   # Generate log file
                                self.hashlist_manager.generate_hash_list(hash_list)       # Generate hash list file
                                final_output(i, t, problems_path)       # Final output for the user
                                raise SystemExit()
                            
                        problem_name = f"{domain.name}_problem_00000{i + 1}"
                        problem, counts_for_init_state, counts_for_goal_state = generate_single_problem(domain, problem_name, json_schema, counts_for_init_state, counts_for_goal_state)

                        hash_16bit = generate_hash(problem)  # Assign the hash to each problem

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

            #print(counts_for_init_state)   # Show how much pools for each type chosen in mutex_pools init
            #print(counts_for_goal_state)   # Show how much pools for each type chosen in mutex_pools goal
            
            t = pbar.format_dict['elapsed']                     # Time required for the processing
            self.progress_manager.save_progress(i+1)                   # Save progress if ended processing
            self.log_manager.generate_log_file(i+1, problems_path, t)   # Generate log file
            self.hashlist_manager.generate_hash_list(hash_list)       # Generate hash list file
            final_output(i+1, t, problems_path)                   # Final output for the user

        elif self.num_problems == 1:
            counts_for_init_state = {}           # Dict for init_state to keep track of the number of problems generated for each type
            counts_for_goal_state = {}           # Dict for goal_state to keep track of the number of problems generated for each type
            
            shutil.copy(domain_origin, generator_path)
            problem_name = f"{domain.name}_problem_000001"
            problem, counts_for_init_state, counts_for_goal_state = generate_single_problem(domain, problem_name, json_schema, counts_for_init_state, counts_for_goal_state)

            # Save the problem file
            problem_file_path = os.path.join(generator_path, f"{problem_name}.pddl")
            with open(problem_file_path, 'w') as file:
                file.write(str(problem))
            print(f"Path of the generated problem file: {problem_file_path}\n")

# ===== Generating PDDL Problem File =====

def load_domain(domain_origin):
    """
    Loads a PDDL domain from a specified file.

    Parameters:
    - domain_origin (str): The path to the PDDL domain file.

    Returns:
    object: The parsed domain object.

    Raises:
    SystemExit: If the domain contains numeric fluents.
    """
    with open(domain_origin, 'r') as file:
        content = file.read()
        if ":functions" in content:
            raise SystemExit("This domain is not valid because it has instances of 'numeric fluents'!")
        else:
            domain = parse_domain(domain_origin)
    return domain

def generate_json_predicates(dict_ordered_by_key, set_predicates):
    """
    Generates a dictionary of predicates based on the ordered keys and set of predicates.

    Parameters:
    - dict_ordered_by_key (dict): A dictionary ordered by keys representing predicates.
    - set_predicates (set): A set of predicates to be used.

    Returns:
    dict: A dictionary of predicates organized by their respective keys.
    """
    predicates_dict = {}    # Dictionary to save predicates

    for outer_key, inner_dict in dict_ordered_by_key.items():
        # Ensure outer_key exists in the dictionary
        if outer_key not in predicates_dict:
            predicates_dict[outer_key] = {}

        for predicate in set_predicates:
            for inner_key, value_list in inner_dict.items():
                # Ensure inner_key exists in the inner dictionary
                if inner_key not in predicates_dict[outer_key]:
                    predicates_dict[outer_key][inner_key] = []

                for value in value_list:
                    if predicate.name == inner_key:
                        if len(predicate.terms) == 2:
                            obj1 = value[0]
                            obj2 = value[1]
                            p = Predicate(predicate.name, obj1, obj2)
                        elif len(predicate.terms) == 1:
                            obj = value[0]
                            p = Predicate(predicate.name, obj)

                        # Add the predicate to the corresponding list
                        predicates_dict[outer_key][inner_key].append(p)

    return predicates_dict
    
def generate_constant_initial_state(all_created_objects, json_schema):
    """
    Generates the constant initial state from the created objects and JSON schema.

    Parameters:
    - all_created_objects (list): List of all created objects.
    - json_schema (object): The JSON schema containing initial state information.

    Returns:
    list: A list of predicates representing the constant initial state.
    """
    # Create a dictionary for quick access to Constant objects
    constant_dict = {const.name: const for const in all_created_objects}

    # Use a regular expression to find all content within parentheses
    matches = re.findall(r"\((.*?)\)", json_schema.constant_initial_state)

    # Transform each found element
    const_init_state = []
    for match in matches:
        # Split the inner string to separate the name and arguments
        parts = match.split()
        predicate_name = parts[0]  # The first element is the name of the predicate
        terms = parts[1:]  # Terms of the predicate

        # Associate terms with Constant objects
        constant_terms = []
        for term in terms:
            if term in constant_dict:
                constant_terms.append(constant_dict[term])
            else:
                print(f"Error: The term '{term}' does not correspond to any defined Constant.")
                break
        else:
            # Create the predicate if all terms are valid
            const_init_state.append(Predicate(predicate_name, *constant_terms))
    return const_init_state

def generate_init_state(predicates_dict, constant_initial_state, json_schema, counts_for_init_state):
    """
    Generates the initial state for the PDDL problem.

    Parameters:
    - predicates_dict (dict): A dictionary of predicates organized by keys.
    - constant_initial_state (list): A list of predicates representing the constant initial state.
    - json_schema (object): The JSON schema containing initial state information.
    - counts_for_init_state (dict): A dictionary that keeps track of the number of pools chosen in mutex_pools to indicate each probability

    Returns:
    set: A set representing the initial state of the problem.
    dict: The updated counts_for_init_state dictionary reflecting the number of predicates chosen from each pool.
    """
    initial_state = set()   # Initialize an empty set to store the initial state predicates

    # Add all constant predicates to the initial state
    for pred in constant_initial_state:
        initial_state.add(pred)

    # Retrieve mutex pools and probabilities from the JSON schema
    mutex_pools = getattr(json_schema.init_state, 'mutex_pools', [])
    mutex_probs = getattr(json_schema.init_state, 'mutex_prob', [])

    if mutex_pools:
        for i, pool in enumerate(mutex_pools):
            # Get the probabilities for the current mutex pool, defaulting to equal probabilities if not provided
            probabilities = mutex_probs[i] if i < len(mutex_probs) else [1 / len(pool)] * len(pool)
            
            # Verify that the probabilities sum to 1
            if not (0.99 <= sum(probabilities) <= 1.01):
                raise ValueError(f"Le probabilità per il gruppo mutex {i} non sommano a 1.")
            
            # Select a predicate from the pool based on the defined probabilities
            selected_pool = random.choices(pool, probabilities)[0]

            # Increment the count for the selected pool
            if selected_pool not in counts_for_init_state:
                counts_for_init_state[selected_pool] = 0  # Initialize the count if it doesn't exist
            counts_for_init_state[selected_pool] += 1

            # Add predicates from the selected pool to the initial state
            for key, value_dict in predicates_dict.items():
                if selected_pool == key:
                    for predicate_list in value_dict.values():
                        for predicate in predicate_list:
                            initial_state.add(predicate)

    # Iterate over additional pools defined in the JSON schema, if they exist
    init_pools = getattr(json_schema.init_state, 'pools', [])

    for pool in init_pools:
        for key, value_dict in predicates_dict.items():
            if pool == key:
                for predicate_list in value_dict.values():
                    for predicate_structure in predicate_list:
                        # Apply probability filtering if the predicate structure has an associated probability
                        if isinstance(predicate_structure, PredicateStructure):
                            if random.random() > predicate_structure.probability:
                                continue  # Skip this predicate based on its probability
                        initial_state.add(predicate_structure)  # Add the predicate to the initial state

    return initial_state, counts_for_init_state
    
def generate_constant_goal_state(all_created_objects, json_schema):
    """
    Generates the constant goal state from the created objects and JSON schema.

    Parameters:
    - all_created_objects (list): List of all created objects.
    - json_schema (object): The JSON schema containing goal state information.

    Returns:
    list: A list of predicates representing the constant goal state.
    """
    # Create a dictionary for quick access to Constant objects
    constant_dict = {const.name: const for const in all_created_objects}

    # Use a regular expression to find all content within parentheses
    matches = re.findall(r"\((.*?)\)", json_schema.constant_goal_state)

    # Transform each found element
    const_goal_state = []
    for match in matches:
        # Split the inner string to separate the name and arguments
        parts = match.split()
        predicate_name = parts[0]  # The first element is the name of the predicate
        terms = parts[1:]  # Terms of the predicate

        # Associate terms with Constant objects
        constant_terms = []
        for term in terms:
            if term in constant_dict:
                constant_terms.append(constant_dict[term])
            else:
                print(f"Errore: Il termine '{term}' non corrisponde a nessun Constant definito.")
                break
        else:
            # Create the predicate if all terms are valid
            const_goal_state.append(Predicate(predicate_name, *constant_terms))
    return const_goal_state

def generate_goal_state(predicates_dict, constant_goal_state, json_schema, counts_for_goal_state):
    """
    Generates the goal state for the PDDL problem.

    Parameters:
    - predicates_dict (dict): A dictionary of predicates organized by keys.
    - constant_goal_state (list): A list of predicates representing the constant goal state.
    - json_schema (object): The JSON schema containing goal state information.
    - counts_for_goal_state (dict): A dictionary that keeps track of the number of pools chosen in mutex_pools to indicate each probability

    Returns:
    set: A set representing the goal state of the problem.
    dict: The updated counts_for_goal_state dictionary reflecting the number of predicates chosen from each pool.
    """
    goal_state = set()   # Initialize an empty set to store the goal state predicates

    # Add all constant predicates to the goal state
    for pred in constant_goal_state:
        goal_state.add(pred)

    # Retrieve mutex pools and probabilities from the JSON schema
    mutex_pools = getattr(json_schema.goal_state, 'mutex_pools', [])
    mutex_probs = getattr(json_schema.goal_state, 'mutex_prob', [])

    if mutex_pools:
        for i, pool in enumerate(mutex_pools):
            # Get the probabilities for the current mutex pool, defaulting to equal probabilities if not provided
            probabilities = mutex_probs[i] if i < len(mutex_probs) else [1 / len(pool)] * len(pool)
            
            # Verify that the probabilities sum to 1
            if not (0.99 <= sum(probabilities) <= 1.01):
                raise ValueError(f"Le probabilità per il gruppo mutex {i} non sommano a 1.")
            
            # Select a predicate from the pool based on the defined probabilities
            selected_pool = random.choices(pool, probabilities)[0]

            # Increment the count for the selected pool
            if selected_pool not in counts_for_goal_state:
                counts_for_goal_state[selected_pool] = 0  # Initialize the count if it doesn't exist
            counts_for_goal_state[selected_pool] += 1

            # Add predicates from the selected pool to the initial state
            for key, value_dict in predicates_dict.items():
                if selected_pool == key:
                    for predicate_list in value_dict.values():
                        for predicate in predicate_list:
                            goal_state.add(predicate)

    # Iterate over additional pools defined in the JSON schema, if they exist
    goal_pools = getattr(json_schema.goal_state, 'pools', [])

    for pool in goal_pools:
        for key, value_dict in predicates_dict.items():
            if pool == key:
                for predicate_list in value_dict.values():
                    for predicate_structure in predicate_list:
                        # Apply probability filtering if the predicate structure has an associated probability
                        if isinstance(predicate_structure, PredicateStructure):
                            if random.random() > predicate_structure.probability:
                                continue  # Skip this predicate based on its probability
                        goal_state.add(predicate_structure)  # Add the predicate to the initial state

    return goal_state, counts_for_goal_state

def generate_single_problem(domain, problem_name, json_schema, counts_for_init_state, counts_for_goal_state):
    """
    Generates a single PDDL problem instance.

    Parameters:
    - domain (object): The PDDL domain object.
    - problem_name (str): The name of the problem to be generated.
    - json_schema (object): The JSON schema containing problem configuration.
    - counts_for_init_state (dict): A dictionary that keeps track of the number of pools chosen in mutex_pools to indicate each probability
    - counts_for_goal_state (dict): A dictionary that keeps track of the number of pools chosen in mutex_pools to indicate each probability


    Returns:
    object: The generated PDDL problem instance.
    dict: The updated counts_for_init_state dictionary reflecting the number of predicates chosen from each pool.
    dict: The updated counts_for_goal_state dictionary reflecting the number of predicates chosen from each pool.
    """
    # Generate all objects
    all_created_objects = [obj for pool in json_schema.objects_pools.values() for obj in pool.created_objects]

    prob_predicates = domain.predicates
    set_predicates = set(prob_predicates)           # Needed to use predicates into the functions
    dict_ordered_by_key = json_schema.gen_dict_ordered()   # Dictionary ordered to represent predicates from JSON
    predicates_dict = generate_json_predicates(dict_ordered_by_key, set_predicates) # Predicates formatted

    constant_initial_state = generate_constant_initial_state(all_created_objects, json_schema)
    init_state, counts_for_init_state = generate_init_state(predicates_dict, constant_initial_state, json_schema, counts_for_init_state)
    constant_goal_state = generate_constant_goal_state(all_created_objects, json_schema)
    goal_state, counts_for_goal_state = generate_goal_state(predicates_dict, constant_goal_state, json_schema, counts_for_goal_state)

    # Instance of the problem
    problem = Problem(
        name=problem_name,
        domain=domain,
        domain_name=domain.name,
        requirements=domain.requirements,
        objects=all_created_objects,
        init=init_state,
        goal=And(*goal_state)   # '*' unpacks the data structure to obtain the goal state
                                # You can change the logic port And() with others like Or() ecc..
    )

    return problem, counts_for_init_state, counts_for_goal_state