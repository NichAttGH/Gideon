import os
import shutil
from pathlib import Path    # Handling paths if num_problems == 1

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

class Folder_Structure:
    """
    Manages the creation of a folder structure for organizing generated problems and logs.

    Attributes:
    - num_problems (int): The number of problems to generate.
    - output_dir (str): The base output directory for generated files.
    - domain_origin (str): The path to the original domain file.
    - domain (object): The domain object loaded from the domain file.
    - json_path (str): The path to the JSON configuration file.
    """
    def __init__(self, num_problems, output_dir, domain_origin, domain, json_path):
        self.num_problems = num_problems
        self.output_dir = output_dir
        self.domain_origin = domain_origin
        self.domain = domain
        self.json_path = json_path
    
    def create_structure(self):
        """
        Creates the necessary folder structure based on the number of problems.

        Returns:
        Tuple[str, str, str, str]: Paths for problems, logs, output, and progress files.
        """
        if self.num_problems > 1:
            output_path = os.path.join(self.output_dir, self.domain.name)
            os.makedirs(output_path, exist_ok=True)
            
            # Create a copy of the domain file
            if output_path is None:
                raise ValueError(f"The {output_path} argument is None. Please write it or ensure it is set correctly!")
            try:
                shutil.copy(self.domain_origin, output_path)
            except FileNotFoundError:
                print(f"Error: The file {self.domain_origin} doesn't exists.")
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

            npg_filename = "npg_progress.txt"       # Name of the file needed to take the progress value
            progress_path = os.path.join(output_path, npg_filename)     # Path of the progress npg file
            
            # Create a copy of the JSON file
            if output_path is None:
                raise ValueError(f"The {output_path} argument is None. Please write it or ensure it is set correctly!")
            try:
                shutil.copy(self.json_path, output_path)
            except FileNotFoundError:
                print(f"Error: The file {self.json_path} doesn't exists.")
            except IOError as e:
                print(f"Error when copying the file: {e}")
                
            return problems_path, logs_path, output_path, progress_path
    
        elif self.num_problems == 1:
            # Return empty paths for a single problem
            problems_path = Path()
            logs_path = Path()
            output_path = Path()
            progress_path = Path()

            return problems_path, logs_path, output_path, progress_path
        
def final_output(i, t, problems_path):
    """
    Prints the final output summary after problem generation.

    Parameters:
    - i (int): The number of generated problems.
    - t (float): The time taken to generate the problems.
    - problems_path (str): The directory where the problems are generated.
    """
    print(f"Number of generated problems: {i}")
    print(f"Directory of generated problems: {problems_path}")
    print(f"Time required to generate problems: {t:.2f} seconds")