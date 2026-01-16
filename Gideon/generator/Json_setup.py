# Import necessary libraries
import json
import random
from typing import List, Union, Dict
from pddl.logic import Constant

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2026, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.1.0"
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
    - unique (int): Number of unique objects in the pool.
    - name_prefix (str): The prefix for naming created objects.
    - name_pattern (List[int]): A pattern for naming objects.
    - is_grid (bool): If True and count is [rows, cols], creates grid layout.
    - created_objects (List[Constant]): The list of created objects.
    """
    def __init__(self, object_type: str, count: Union[int, List[int]], name_prefix: str, mutex: bool = False,
                 sequential: bool = False, unique: int = None, name_pattern: List[int] = None, is_grid: bool = False, created_objects: List[Constant] = []):
        """Initializes an ObjectPool instance."""
        self.object_type = object_type
        self.mutex = mutex
        self.sequential = sequential
        self.count = count
        self.unique = unique
        self.name_prefix = name_prefix
        self.name_pattern = name_pattern
        self.is_grid = is_grid
        self.created_objects = created_objects

    def __str__(self):
        """Returns a string representation of the ObjectPool."""
        return (f"ObjectPool(object_type = {self.object_type}, mutex = {self.mutex}, sequential = {self.sequential}, "
                f"count = {self.count}, unique = {self.unique}, name_prefix = {self.name_prefix}, \n"
                f" name_pattern = {self.name_pattern}, is_grid = {self.is_grid}, created_objects = {self.created_objects})")
    
    def __repr__(self):
        """Returns the string representation for the ObjectPool."""
        return self.__str__()

class PredicateStructure:
    """
    Represents a structure for a predicate.

    Attributes:
    - name (str): The name of the predicate.
    - count (Union[int, List[int]]): The number of instances of the predicate, or a range [min, max].
    - args (list): The arguments of the predicate.
    - probability (float): The probability of the predicate being selected (default 1.0).
    """
    def __init__(self, name: str, count: Union[int, List[int]], args: list, probability: float = 1.0):
        """Initializes a PredicateStructure instance."""
        self.name = name
        self.count = count
        self.args = args
        self.probability = probability  # Default to 1.0 if not provided
    
    def get_actual_count(self):
        """
        Returns the actual count, resolving random range if needed.
        If count is a list [min, max], selects a random integer in that range.
        Otherwise returns the fixed count value.
        
        Returns:
            int: The resolved count value for this predicate instance.
        """
        if isinstance(self.count, list):
            return random.randint(self.count[0], self.count[1])
        else:
            return self.count
    
    def get_max_possible_count(self):
        """
        Returns the maximum possible count (for pre-planning purposes).
        
        Returns:
            int: The maximum count that could be generated.
        """
        if isinstance(self.count, list):
            return self.count[1]  # Return max value
        else:
            return self.count

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
        """
        Initializes a PredicatePool instance.
        Converts raw predicate dictionaries into PredicateStructure objects.
        """
        self.name = name
        self.predicates = {key: PredicateStructure(key, **value) for key, value in predicates.items()}

    def __str__(self):
        """Returns a string representation of the PredicatePool."""
        predicates_str = "\n    ".join(f"{key}: {pred}" for key, pred in self.predicates.items())
        return (f"PredicatePool(name = {self.name}, predicates = {{\n    {predicates_str}\n  }})")
    
    def __repr__(self):
        """Returns the string representation for the PredicatePool."""
        return self.__str__()

class FunctionStructure:
    """
    Represents the structure of a function.

    Attributes:
    - name (str): The name of the function.
    - value (float): The value of the function.
    """
    def __init__(self, function_name: str, function_value: float):
        """
        Initializes a FunctionStructure instance.
        Used to represent numeric functions in PDDL (e.g., for metrics or costs).
        """
        self.name = function_name
        self.value = function_value
    
    def __str__(self):
        """Returns a string representation of the Function."""
        return (f"Function(name = {self.name}, value = {self.value})")
    
    def __repr__(self):
        """Returns the string representation of the Function."""
        return self.__str__()
    
class InitState:
    """
    Represents the initial state of the system.

    Attributes:
    - mutex_pools (list): List of mutex pools in the initial state.
    - mutex_prob (list): List of probabilities for mutex pools.
    - pools (list): List of object pools in the initial state.
    - functions (list): List of functions in the initial state.
    """
    def __init__(self, init_state: dict):
        """
        Initializes an InitState instance from a configuration dictionary.
        Extracts predicate pools and functions to define the initial problem state.
        """
        # Extract predicates from the field 'predicates'
        predicates = init_state.get("predicates", {})
        self.mutex_pools = predicates.get("mutex_pools", [])
        self.mutex_prob = predicates.get("mutex_prob", [])  # Default to empty list if not provided
        self.pools = predicates.get("pools", [])
        # Extract functions from the field 'functions'
        self.functions = init_state.get("functions", {})

    def __str__(self):
        """Returns a string representation of the InitState."""
        return (f"InitState(\n  mutex_pools = {self.mutex_pools},\n"
                f"  mutex_prob = {self.mutex_prob},\n"
                f"  pools = {self.pools}\n),\n"
                f"  functions = {self.functions}\n")

    def __repr__(self):
        """Returns the string representation for the InitState."""
        return self.__str__()

class GoalState:
    """
    Represents the goal state of the system.

    Attributes:
    - mutex_pools (list): List of mutex pools in the goal state.
    - mutex_prob (list): List of probabilities for mutex pools.
    - pools (list): List of object pools in the goal state.
    - functions (list): List of functions in the goal state.
    """
    def __init__(self, g_state: dict):
        """
        Initializes a GoalState instance from a configuration dictionary.
        Defines the target state that the planner should achieve.
        """
        # Extract predicates from the field 'predicates'
        predicates = g_state.get("predicates", {})
        self.mutex_pools = predicates.get("mutex_pools", [])
        self.mutex_prob = predicates.get("mutex_prob", [])  # Default to empty list if not provided
        self.pools = predicates.get("pools", [])
        # Extract functions from the field 'functions'
        self.functions = g_state.get("functions", {})

    def __str__(self):
        """Returns a string representation of the GoalState."""
        return (f"GoalState(\n  mutex_pools = {self.mutex_pools},\n"
                f"  mutex_prob = {self.mutex_prob},\n"
                f"  pools = {self.pools}\n),\n"
                f"  functions = {self.functions}\n")
    
    def __repr__(self):
        """Returns the string representation for the GoalState."""
        return self.__str__()

class MetricStructure:
    """
    Represents the structure of the metric.

    Attributes:
    - optimization (str): The choice of the optimization (minimize or maximize).
    - function (str): The name of the function to be optimized.
    """
    def __init__(self, optimize: str, function_name: str):
        """
        Initializes a MetricStructure instance.
        Defines the optimization objective for the PDDL problem.
        """
        self.optimization = optimize
        self.function = function_name
    
    def __str__(self):
        """Returns a string representation of the MetricStructure."""
        return (f"MetricStructure(optimization = {self.optimization}, function = {self.function})")
    
    def __repr__(self):
        """Returns the string representation of the MetricStructure."""
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
    - metric (MetricStructure): The metric applied on a specific function.
    """
    def __init__(self, problem_prefix: str, domain_name: str, objects_pools: Dict[str, ObjectPool], predicate_pools: Dict[str, PredicatePool] = None,
                 constant_initial_state: str = "", init_state: InitState = None, constant_goal_state: str = "", g_state: GoalState = None, metric: MetricStructure = None):
        """Initializes a JsonSchema instance representing a complete PDDL problem."""
        self.problem_prefix = problem_prefix
        self.domain_name = domain_name
        self.objects_pools = objects_pools
        self.predicate_pools = predicate_pools
        self.constant_initial_state = constant_initial_state
        self.init_state = init_state
        self.constant_goal_state = constant_goal_state
        self.goal_state = g_state
        self.metric = metric
    
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
                f"  goal_state = {self.goal_state},\n"
                f"  metric = {self.metric}\n)")
    
    def __repr__(self):
        """Returns the string representation for the JsonSchema."""
        return self.__str__()

    def generate_objects(self):
        """
        Generates objects based on the defined object pools.
        This method populates the created_objects attribute of each ObjectPool
        with instances of the Constant class, based on the specified count and naming conventions.
        
        Returns:
            created_objects (List[Constant]): A list of created objects for the last processed pool.
        """
        for pool in self.objects_pools.values():
            pool.created_objects = []

            # Determines the number of objects to be created
            count = pool.count
            # Take bool flag from JSON if a grid pattern is needed
            isgrid = pool.is_grid
            # Get unique value if specified
            unique = pool.unique

            # Condition for grid pattern
            if isinstance(count, list) and isgrid == True:
                rows = count[0]
                columns = count[1]
                for i in range(rows):
                    for j in range(columns):
                        if pool.name_pattern:
                            step = pool.name_pattern[1]
                            name_pattern_value = j * step
                            constant_name = f"{pool.name_prefix}{name_pattern_value}"
                        else:
                            constant_name = f"{pool.name_prefix}_{i}-{j}"
                        constant = Constant(constant_name, pool.object_type)
                        pool.created_objects.append(constant)

            # Condition if count is a list with a minimum and maximum value to choose from
            elif isinstance(count, list):
                count = random.randint(count[0], count[1])
                # Handle unique constraint
                if unique is not None and unique < count:
                    # Generate unique objects first
                    unique_objects = []
                    for i in range(unique):
                        if pool.name_pattern:
                            step = pool.name_pattern[1]
                            name_pattern_value = i * step
                            constant_name = f"{pool.name_prefix}{name_pattern_value}"
                        else:
                            constant_name = f"{pool.name_prefix}{i}"
                        constant = Constant(constant_name, pool.object_type)
                        unique_objects.append(constant)
                    
                    # Distribute copies as evenly as possible
                    base_copies = count // unique
                    extra_copies = count % unique
                    
                    for i, obj in enumerate(unique_objects):
                        # Add base number of copies
                        copies_to_add = base_copies
                        # Add one extra copy for the first 'extra_copies' objects
                        if i < extra_copies:
                            copies_to_add += 1
                        
                        for _ in range(copies_to_add):
                            pool.created_objects.append(obj)
                else:
                    # Normal generation without unique constraint
                    for i in range(count):
                        if pool.name_pattern:
                            step = pool.name_pattern[1]
                            name_pattern_value = i * step
                            constant_name = f"{pool.name_prefix}{name_pattern_value}"
                        else:
                            constant_name = f"{pool.name_prefix}{i}"
                        constant = Constant(constant_name, pool.object_type)
                        pool.created_objects.append(constant)
            
            # Condition if count is a simple int value
            elif isinstance(count, int):
                # Handle unique constraint
                if unique is not None and unique < count:
                    # Generate unique objects first
                    unique_objects = []
                    for i in range(unique):
                        if pool.name_pattern:
                            step = pool.name_pattern[1]
                            name_pattern_value = i * step
                            constant_name = f"{pool.name_prefix}{name_pattern_value}"
                        else:
                            constant_name = f"{pool.name_prefix}{i}"
                        constant = Constant(constant_name, pool.object_type)
                        unique_objects.append(constant)
                    
                    # Distribute copies as evenly as possible
                    base_copies = count // unique
                    extra_copies = count % unique
                    
                    for i, obj in enumerate(unique_objects):
                        # Add base number of copies
                        copies_to_add = base_copies
                        # Add one extra copy for the first 'extra_copies' objects
                        if i < extra_copies:
                            copies_to_add += 1
                        
                        for _ in range(copies_to_add):
                            pool.created_objects.append(obj)
                else:
                    # Normal generation without unique constraint
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
        Generates a dictionary of predicates ordered by their keys with proper object assignment.
        Implements advanced object selection logic including:
        - Variable predicate count: when count is [min, max], randomly selects within range
        - Synchronization tags ($): ensures same objects used across related predicates
        - Offset expressions ($tag+n, $tag-n): selects objects relative to synchronized base
        - Mutex constraints: prevents object reuse within predicates (local and global)
        - Sequential selection: picks objects in order with optional wrapping
        - Probability filtering: only generates predicates based on their probability value
        
        The method performs two passes:
        1. Pre-allocates synchronized object selections for all $tags
        2. Generates actual predicate instances using allocated objects
        
        Returns:
            dict: Nested dictionary structure:
                  {pool_name: {predicate_name: [[obj1, obj2, ...], ...]}}
                  where each inner list represents arguments for one predicate instance.
        """
        dict_ordered_by_key = dict()
        global_sync_selections = {}
        next_index_per_pool = {}
        used_indices_per_pool = {}

        # FIRST PASS: Collect all sync tags (using MAX possible count for planning)
        tag_max_counts = {}
        tag_pools = {}
        
        for key, pool in self.predicate_pools.items():
            for predicate_name, pred_structure in pool.predicates.items():
                for arg in pred_structure.args:
                    if "$" in arg:
                        base_name, expression = arg.split("$", 1)
                        
                        tag = expression
                        if "+" in expression:
                            tag = expression.split("+")[0]
                        elif "-" in expression:
                            tag = expression.split("-")[0]
                        
                        unique_tag = f"{base_name}${tag}"
                        
                        if unique_tag not in tag_max_counts:
                            tag_max_counts[unique_tag] = 0
                            tag_pools[unique_tag] = base_name
                        
                        max_count = pred_structure.get_max_possible_count()
                        tag_max_counts[unique_tag] = max(tag_max_counts[unique_tag], max_count)

        # Pre-generate selections for each synchronization tag
        for unique_tag, max_count in tag_max_counts.items():
            pool_name = tag_pools[unique_tag]
            if pool_name in self.objects_pools:
                pool_obj = self.objects_pools[pool_name]
                effective_pool = get_effective_pool(pool_obj)
                
                track_key = f"{unique_tag}_track"
                if track_key not in used_indices_per_pool:
                    used_indices_per_pool[track_key] = []
                if track_key not in next_index_per_pool:
                    next_index_per_pool[track_key] = 0
                
                selected_objects = []
                for i in range(max_count):
                    available_indices = list(range(len(effective_pool)))
                    
                    if pool_obj.sequential:
                        if i == 0:
                            selected_index = random.choice(available_indices)
                            next_index_per_pool[track_key] = selected_index
                        else:
                            selected_index = (next_index_per_pool[track_key] + 1) % len(effective_pool)
                        next_index_per_pool[track_key] = selected_index
                    else:
                        if pool_obj.mutex:
                            available_indices = [idx for idx in available_indices if idx not in used_indices_per_pool[track_key]]
                            if not available_indices:
                                used_indices_per_pool[track_key] = []
                                available_indices = list(range(len(effective_pool)))
                        
                        selected_index = random.choice(available_indices)
                    
                    selected_objects.append(effective_pool[selected_index])
                    
                    if pool_obj.mutex:
                        used_indices_per_pool[track_key].append(selected_index)
                
                global_sync_selections[unique_tag] = selected_objects

        # SECOND PASS: Generate predicates with VARIABLE COUNT support
        for key, pool in self.predicate_pools.items():
            if key not in dict_ordered_by_key:
                dict_ordered_by_key[key] = {}

            for predicate_name, pred_structure in pool.predicates.items():
                if predicate_name not in dict_ordered_by_key[key]:
                    dict_ordered_by_key[key][predicate_name] = []

                # Solve the actual count for this predicate
                actual_count = pred_structure.get_actual_count()
                
                # Optional: Debug print to see the resolved count
                #if isinstance(pred_structure.count, list):
                #    print(f"Predicate {predicate_name}: count range {pred_structure.count} → resolved to {actual_count}")

                # Extended mutex tracking
                global_predicate_mutex_usage = {}

                for predicate_instance in range(actual_count):
                    if pred_structure.probability < 1.0 and random.random() > pred_structure.probability:
                        continue

                    pred_args = []
                    predicate_mutex_usage = {}
                    predicate_sequential_state = {}

                    for arg_index, arg in enumerate(pred_structure.args):
                        obj = None
                        
                        if "$" in arg:  # Synchronized argument
                            base_name, expression = arg.split("$", 1)
                            
                            tag = expression
                            step = 0
                            
                            if "+" in expression:
                                tag, step_str = expression.split("+", 1)
                                step = int(step_str)
                            elif "-" in expression:
                                tag, step_str = expression.split("-", 1)
                                step = -int(step_str)

                            unique_tag = f"{base_name}${tag}"

                            if (unique_tag in global_sync_selections and 
                                predicate_instance < len(global_sync_selections[unique_tag])):
                                
                                base_obj = global_sync_selections[unique_tag][predicate_instance]
                                
                                if step != 0:
                                    pool_obj = self.objects_pools[base_name]
                                    effective_pool = get_effective_pool(pool_obj)
                                    
                                    base_obj_index = -1
                                    for idx, obj_in_pool in enumerate(effective_pool):
                                        if obj_in_pool.name == base_obj.name:
                                            base_obj_index = idx
                                            break
                                    
                                    if base_obj_index != -1:
                                        actual_index = (base_obj_index + step) % len(effective_pool)
                                        obj = effective_pool[actual_index]
                                    else:
                                        obj = base_obj
                                else:
                                    obj = base_obj

                        else:
                            # Non-synchronized argument with extended mutex
                            base_name = arg
                            if base_name in self.objects_pools:
                                pool_obj = self.objects_pools[base_name]
                                effective_pool = get_effective_pool(pool_obj)
                                
                                if base_name not in predicate_mutex_usage:
                                    predicate_mutex_usage[base_name] = []
                                if base_name not in predicate_sequential_state:
                                    predicate_sequential_state[base_name] = None
                                
                                global_key = (base_name, arg_index)
                                if global_key not in global_predicate_mutex_usage:
                                    global_predicate_mutex_usage[global_key] = []

                                available_indices = list(range(len(effective_pool)))

                                if pool_obj.mutex:
                                    # Apply global mutex (across instances)
                                    available_indices = [i for i in available_indices 
                                                    if i not in global_predicate_mutex_usage[global_key]]
                                    
                                    # Apply local mutex (within instance)
                                    available_indices = [i for i in available_indices 
                                                    if i not in predicate_mutex_usage[base_name]]
                                    
                                    if not available_indices:
                                        if pool_obj.sequential:
                                            raise ValueError(f"Pool {base_name}: no objects available "
                                                        f"with extended mutex and sequential=True")
                                        else:
                                            predicate_mutex_usage[base_name] = []
                                            available_indices = list(range(len(effective_pool)))
                                            available_indices = [i for i in available_indices 
                                                            if i not in global_predicate_mutex_usage[global_key]]
                                            
                                            if not available_indices:
                                                raise ValueError(f"Pool {base_name}: no objects available "
                                                            f"with global mutex. Pool too small.")

                                # Object selection logic
                                if pool_obj.sequential:
                                    if predicate_sequential_state[base_name] is None:
                                        current_index = random.choice(available_indices)
                                        predicate_sequential_state[base_name] = current_index
                                    else:
                                        if pool_obj.mutex:
                                            current = predicate_sequential_state[base_name]
                                            next_candidates = []
                                            for offset in range(1, len(effective_pool)):
                                                candidate = (current + offset) % len(effective_pool)
                                                if candidate in available_indices:
                                                    next_candidates.append(candidate)
                                            
                                            if not next_candidates:
                                                raise ValueError(f"Pool {base_name}: no sequential objects available")
                                            
                                            current_index = min(next_candidates)
                                        else:
                                            current_index = (predicate_sequential_state[base_name] + 1) % len(effective_pool)
                                        
                                        predicate_sequential_state[base_name] = current_index
                                else:
                                    current_index = random.choice(available_indices)
                                
                                # Update mutex tracking
                                if pool_obj.mutex:
                                    predicate_mutex_usage[base_name].append(current_index)
                                    global_predicate_mutex_usage[global_key].append(current_index)

                                obj = effective_pool[current_index]
                        
                        if obj:
                            pred_args.append(obj)

                    if pred_args:
                        dict_ordered_by_key[key][predicate_name].append(pred_args)

        return dict_ordered_by_key

# Helper function to get effective pool (unique objects if unique is set)
def get_effective_pool(pool_obj):
    """
    Returns the effective pool of objects, considering the unique constraint.
    
    If a pool has a 'unique' attribute set and it's less than the total count,
    this function returns only the unique objects (no duplicates).
    Otherwise, it returns the full pool of created objects.
    
    Args:
        pool_obj: An ObjectPool instance
        
    Returns:
        list: A list of Constant objects (either unique or all objects)
    """
    if pool_obj.unique is not None and pool_obj.unique < len(pool_obj.created_objects):
        # Create a list of unique objects
        unique_objects = []
        seen_names = set()
        for obj in pool_obj.created_objects:
            if obj.name not in seen_names:
                unique_objects.append(obj)
                seen_names.add(obj.name)
        return unique_objects
    else:
        return pool_obj.created_objects

def load_json(filepath: str):
    """
    Loads a JSON file and creates instances of the relevant classes.
    This function parses a JSON configuration file and instantiates all necessary
    objects for a PDDL problem schema, including object pools, predicate pools,
    initial state, and goal state.
    
    Parameters:
        - filepath (str): The path to the JSON file to be loaded.

    Returns:
        json_schema (JsonSchema): An instance of the JsonSchema class populated with data from the JSON file.
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
    init_state = InitState(data["init_state"])
    g_state = GoalState(data["goal_state"])

    # Creation of JsonSchema instance
    json_schema = JsonSchema(
        problem_prefix=data["problem_prefix"],
        domain_name=data["domain_name"],
        objects_pools=objects_pools,
        predicate_pools=predicate_pools,
        constant_initial_state=data["constant_initial_state"],
        init_state=init_state,
        constant_goal_state=data["constant_goal_state"],
        g_state=g_state,
        metric=data["metric"]
    )

    return json_schema

