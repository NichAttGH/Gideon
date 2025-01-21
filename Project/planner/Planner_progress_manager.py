# Import necessary libraries
import os
import re

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

class Planner_Progress_Manager:
    """
    Manager class for handling generation progress tracking.
    
    Attributes:
        progress_path (str): Path to the progress file
    """

    def __init__(self, progress_path):
        """
        Initialize the Planner_Progress_Manager with the specified progress file path.
        
        Args:
            planner_progress_path (str): Path where progress file will be stored
        """
        self.progress_path = progress_path
    
    def save_progress(self, plan_count):
        """
        Saves the current progress to the specified file.
        Writes the current number of generated plans to the progress file.
        
        Args:
            plan_count (int): Current number of plans generated.
        """
        # Read the content of the file
        with open(self.progress_path, 'r') as file:
            lines = file.readlines()

        # Search the row that contains 'ppg_progress ='
        for l, line in enumerate(lines):
            if line.startswith("ppg_progress = "):
                # Rewrite the value with the new one
                lines[l] = f"ppg_progress = {plan_count}\n"
                break
        
        # Rewrite the file with the new value
        with open(self.progress_path, 'w') as file:
            file.writelines(lines)

    def read_progress(self):
        """
        Reads previously saved progress from the progress file.
        
        Returns:
            Value (int): Number of plans previously generated, or 0 if no progress file exists.
        """
        # Define a regex pattern to match the line containing 'ppg_progress'
        pattern = r"ppg_progress\s*=\s*(\d+)"
        
        # Check if the progress file exists
        if os.path.exists(self.progress_path):
            with open(self.progress_path, 'r') as f:
                content = f.read()
                
                # Search for the pattern in the file content
                match = re.search(pattern, content)
                if match:
                    # If a match is found, return the captured number (group 1)
                    return int(match.group(1))
        # Return 0 if no progress file exists or no match is found
        return 0
        
    def check_progress(self, plans_path, output_dir):
        """
        Checks for existing progress and handles user interaction.
        
        Prompts the user to decide whether to resume from previous progress
        or start fresh generation.
        
        Args:
            plans_path (str): Path to the generated plans directory.
            output_dir (str): Path to the output directory.
            
        Returns:
            ppg (int): Number of plans generated (a progress counter).
        """
        while True:
            print("Is there a stopped processing in advance? (Y for yes, N for no)")
            answer = input().strip().upper()        
            if answer == "Y":
                if os.path.exists(plans_path) and os.path.exists(output_dir):
                    ppg = self.read_progress()
                    return ppg
            elif answer == "N":
                return 0
            else:
                print("Invalid input, please enter 'Y' for yes or 'N' for no.")