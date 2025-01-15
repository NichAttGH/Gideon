import json
import random
from typing import List, Union, Dict
from pddl.logic import Constant

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

class ObjectPool:
    """
    Represents a pool of objects of a specific type.

    Attributes:
    - object_type (str): The type of objects in the pool.
    - mutex (bool): Indicates if the pool is mutex.
    - sequential (bool): Indicates if the pool is sequential.
    - count (Union[int, List[int]]): The number of objects to create or a range of counts.
    - name_prefix (str): The prefix for naming created objects.
    - name_pattern (List[int]): A pattern for naming objects.
    - created_objects (List[Constant]): The list of created objects.
    """
    def __init__(self, object_type: str, count: Union[int, List[int]], name_prefix: str, mutex: bool = False,
                 sequential: bool = False, name_pattern: List[int] = None, created_objects: List[Constant] = []):
        self.object_type = object_type
        self.mutex = mutex
        self.sequential = sequential
        self.count = count
        self.name_prefix = name_prefix
        self.name_pattern = name_pattern
        self.created_objects = created_objects

    def __str__(self):
        """Returns a string representation of the ObjectPool."""
        return (f"ObjectPool(object_type = {self.object_type}, mutex = {self.mutex}, sequential = {self.sequential}, "
                f"count = {self.count}, name_prefix = {self.name_prefix}, name_pattern = {self.name_pattern},\n"
                f"created_objects = {self.created_objects})")
    
    def __repr__(self):
        """Returns the string representation for the ObjectPool."""
        return self.__str__()

class PredicateStructure:
    """
    Represents a structure for a predicate.

    Attributes:
    - name (str): The name of the predicate.
    - count (int): The number of instances of the predicate.
    - args (list): The arguments of the predicate.
    - probability (float): The probability of the predicate being selected (default 1.0).
    """
    def __init__(self, name: str, count: int, args: list, probability: float = 1.0):
        self.name = name
        self.count = count
        self.args = args
        self.probability = probability  # Default to 1.0 if not provided

    def __str__(self):
        """Returns a string representation of the PredicateStructure."""
        return (f"PredicateStructure(name = {self.name}, count = {self.count}, "
                f"args = {self.args}, probability = {self.probability})")
    
    def __repr__(self):
        """Returns the string representation for the PredicateStructure."""
        return self.__str__()

class PredicatePool:
    """
    Represents a pool of predicates.

    Attributes:
    - name (str): The name of the predicate pool.
    - predicates (dict): A dictionary of predicates in the pool.
    """
    def __init__(self, name: str, predicates: dict):
        self.name = name
        self.predicates = {key: PredicateStructure(key, **value) for key, value in predicates.items()}

    def __str__(self):
        """Returns a string representation of the PredicatePool."""
        predicates_str = "\n    ".join(f"{key}: {pred}" for key, pred in self.predicates.items())
        return (f"PredicatePool(name = {self.name}, predicates = {{\n    {predicates_str}\n  }})")
    
    def __repr__(self):
        """Returns the string representation for the PredicatePool."""
        return self.__str__()

class InitState:
    """
    Represents the initial state of the system.

    Attributes:
    - mutex_pools (list): List of mutex pools in the initial state.
    - mutex_prob (list): List of probabilities for mutex pools.
    - pools (list): List of object pools in the initial state.
    """
    def __init__(self, predicates: dict):
        self.mutex_pools = predicates.get("mutex_pools", [])
        self.mutex_prob = predicates.get("mutex_prob", [])  # Default to empty list if not provided
        self.pools = predicates.get("pools", [])

    def __str__(self):
        """Returns a string representation of the InitState."""
        return (f"InitState(\n  mutex_pools = {self.mutex_pools},\n"
                f"  mutex_prob = {self.mutex_prob},\n"
                f"  pools = {self.pools}\n)")

    def __repr__(self):
        """Returns the string representation for the InitState."""
        return self.__str__()

class GoalState:
    """
    Represents the goal state of the system.

    Attributes:
    - mutex_pools (list): List of mutex pools in the goal state.
    - pools (list): List of object pools in the goal state.
    """
    def __init__(self, predicates: dict):
        self.mutex_pools = predicates.get("mutex_pools", [])
        self.mutex_prob = predicates.get("mutex_prob", [])  # Default to empty list if not provided
        self.pools = predicates.get("pools", [])

    def __str__(self):
        """Returns a string representation of the GoalState."""
        return (f"GoalState(\n  mutex_pools = {self.mutex_pools},\n"
                f"  mutex_prob = {self.mutex_prob},\n"
                f"  pools = {self.pools}\n)")

    def __repr__(self):
        """Returns the string representation for the GoalState."""
        return self.__str__()

class JsonSchema:
    """
    Represents the JSON schema for the planning problem.

    Attributes:
    - problem_prefix (str): The prefix for the problem.
    - domain_name (str): The name of the domain.
    - objects_pools (Dict[str, ObjectPool]): A dictionary of object pools.
    - predicate_pools (Dict[str, PredicatePool]): A dictionary of predicate pools.
    - constant_initial_state (str): The initial state in constant form.
    - init_state (InitState): The initial state object.
    - constant_goal_state (str): The goal state in constant form.
    - goal_state (GoalState): The goal state object.
    """
    def __init__(self, problem_prefix: str, domain_name: str, objects_pools: Dict[str, ObjectPool], predicate_pools: Dict[str, PredicatePool] = None,
                 constant_initial_state: str = "", init_state: InitState = None, constant_goal_state: str = "", goal_state: GoalState = None):
        self.problem_prefix = problem_prefix
        self.domain_name = domain_name
        self.objects_pools = objects_pools
        self.predicate_pools = predicate_pools
        self.constant_initial_state = constant_initial_state
        self.init_state = init_state
        self.constant_goal_state = constant_goal_state
        self.goal_state = goal_state
    
    def __str__(self):
        """Returns a string representation of the JsonSchema."""
        objects_pools_str = "\n  ".join(f"{key}: {pool}" for key, pool in self.objects_pools.items())
        predicate_pools_str = "\n  ".join(f"{key}: {pool}" for key, pool in self.predicate_pools.items()) if self.predicate_pools else "None"
        return (f"JsonSchema(\n  problem_prefix = {self.problem_prefix},\n  domain_name = {self.domain_name},\n"
                f"  objects_pools = {{\n  {objects_pools_str}\n  }},\n"
                f"  predicate_pools = {{\n  {predicate_pools_str}\n  }},\n"
                f"  constant_initial_state = {self.constant_initial_state},\n"
                f"  init_state = {self.init_state},\n"
                f"  constant_goal_state = {self.constant_goal_state},\n"
                f"  goal_state = {self.goal_state}\n)")
    
    def __repr__(self):
        """Returns the string representation for the JsonSchema."""
        return self.__str__()

    def generate_objects(self):
        """
        Generates objects based on the defined object pools.

        This method populates the created_objects attribute of each ObjectPool
        with instances of the Constant class, based on the specified count and naming conventions.
        
        Returns:
        List[Constant]: A list of created objects for the last processed pool.
        """
        for pool in self.objects_pools.values():
            pool.created_objects = []

            # Determines the number of objects to be created
            count = pool.count
            if isinstance(count, list):  # If count is a list, choose a random value
                count = random.randint(count[0], count[1])
            for i in range(count):
                if pool.name_pattern:
                    step = pool.name_pattern[1]
                    name_pattern_value = i * step
                    constant_name = f"{pool.name_prefix}{name_pattern_value}"
                else:
                    constant_name = f"{pool.name_prefix}{i}"
                constant = Constant(constant_name, pool.object_type)
                pool.created_objects.append(constant)
        return pool.created_objects
        
    def gen_dict_ordered(self):
        """
        Generates a dictionary of predicates ordered by their keys.

        This method iterates through the predicate pools and constructs a dictionary
        that organizes predicates by their associated pools and structures.

        Returns:
        dict: A dictionary ordered by keys containing predicates and their arguments.
        """
        dict_ordered_by_key = dict()  # Initialize an empty dictionary

        for key, pool in self.predicate_pools.items():
            # Initialize a dictionary to store the predicates associated with this pool
            if key not in dict_ordered_by_key:
                dict_ordered_by_key[key] = {}

            for pred_name, pred_structure in pool.predicates.items():
                # Dictionary for storing already selected objects
                selected_objects = {}
                # Dictionary for tracking indexes used, separated by pool
                used_indices_per_pool = {}

                for i in range(pred_structure.count):

                    # Evaluate the probability to include the predicate.
                    if random.random() > pred_structure.probability:  # Skip the predicate based on probability
                        continue

                    pred_args = []  # List of terms of the current predicate

                    for arg in pred_structure.args:
                        if "$" in arg:  # Contains a reference to the pool with suffix
                            base_name = arg.split("$")[0]

                            # Get the corresponding pool
                            if base_name in self.objects_pools:
                                pool = self.objects_pools[base_name]

                                # Initialize the indexes used for the pool, if not already done
                                if base_name not in used_indices_per_pool:
                                    used_indices_per_pool[base_name] = set()

                                used_indices = used_indices_per_pool[base_name]

                                # Check if you have already selected an object for this pool
                                if base_name not in selected_objects:
                                    selected_objects[base_name] = None  # Initialize as None

                                # If the pool is sequential
                                if pool.sequential:
                                    current_index = len(used_indices) % len(pool.created_objects)
                                    obj = pool.created_objects[current_index]
                                    used_indices.add(current_index)
                                    selected_objects[base_name] = current_index
                                else:
                                    # If the pool is not sequential, choose a unique random value
                                    available_indices = list(set(range(len(pool.created_objects))) - used_indices)
                                    if available_indices:
                                        selected_index = random.choice(available_indices)
                                        used_indices.add(selected_index)
                                        obj = pool.created_objects[selected_index]
                                        selected_objects[base_name] = selected_index
                                    else:
                                        print(f"All objects for the {base_name} pool have already been used in this iteration.")
                                        continue
                        else:
                            base_name = arg

                            # Get the corresponding pool
                            if base_name in self.objects_pools:
                                pool = self.objects_pools[base_name]

                                # Initialize the indexes used for the pool, if not already done
                                if base_name not in used_indices_per_pool:
                                    used_indices_per_pool[base_name] = set()

                                used_indices = used_indices_per_pool[base_name]

                                # Check if you have already selected an object for this pool
                                if base_name not in selected_objects:
                                    selected_objects[base_name] = None  # Initialize as None

                                # If the pool is sequential
                                if pool.sequential:
                                    current_index = len(used_indices) % len(pool.created_objects)
                                    obj = pool.created_objects[current_index]
                                    used_indices.add(current_index)
                                    selected_objects[base_name] = current_index
                                else:
                                    # If the pool is not sequential, choose a unique random value
                                    available_indices = list(set(range(len(pool.created_objects))) - used_indices)
                                    if available_indices:
                                        selected_index = random.choice(available_indices)
                                        used_indices.add(selected_index)
                                        obj = pool.created_objects[selected_index]
                                        selected_objects[base_name] = selected_index
                                    else:
                                        print(f"All objects for the {base_name} pool have already been used in this iteration.")
                                        continue
                        
                        # Add the object to the list of terms in the current predicate
                        if obj:
                            pred_args.append(obj)

                    # Initialize the key in the pool dictionary if necessary
                    if pred_structure.name not in dict_ordered_by_key[key]:
                        dict_ordered_by_key[key][pred_structure.name] = []

                    # Add the created predicate
                    dict_ordered_by_key[key][pred_structure.name].append(pred_args)

        return dict_ordered_by_key

def load_json(filepath: str):
    """
    Loads a JSON file and creates instances of the relevant classes.

    Parameters:
    - filepath (str): The path to the JSON file to be loaded.

    Returns:
    JsonSchema: An instance of the JsonSchema class populated with data from the JSON file.
    """
    with open(filepath, 'r') as file:
        data = json.load(file)  # Load the JSON data

    # Reading object pools
    objects_pools = {
        name: ObjectPool(**pool_data)
        for name, pool_data in data["objects_pools"].items()
    }

    # Creating PredicatePool instances
    predicate_pools = {
        pool_name: PredicatePool(
            pool_name,
            {pred_name: {**pred_data, "probability": pred_data.get("probability", 1.0)} 
             for pred_name, pred_data in predicates.items()}
        )
        for pool_name, predicates in data["predicates_pools"].items()
    }

    # Creation of InitState and GoalState instances
    init_state = InitState(data["init_state"]["predicates"])
    goal_state = GoalState(data["goal_state"]["predicates"])

    # Creation of JsonSchema instance
    json_schema = JsonSchema(
        problem_prefix=data["problem_prefix"],
        domain_name=data["domain_name"],
        objects_pools=objects_pools,
        predicate_pools=predicate_pools,
        constant_initial_state=data["constant_initial_state"],
        init_state=init_state,
        constant_goal_state=data["constant_goal_state"],
        goal_state=goal_state
    )
    return json_schema