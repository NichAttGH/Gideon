# Import necessary libraries
import os

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

class Planner_Progress_Manager:
    
    ppg = 0    # Class-level counter for number of plans generated

    def __init__(self, planner_progress_path):
        """
        Initialize the Planner_Progress_Manager with the specified progress file path.
        
        Args:
            planner_progress_path (str): Path where progress file will be stored
        """
        self.planner_progress_path = planner_progress_path
    
    def save_progress(self, plan_count):
        """
        Saves the current progress to the specified file.
        
        Args:
            plan_count (int): Current number of plans generated.
            
        This method writes the number of generated plans to the progress file.
        """
        with open(self.planner_progress_path, 'w') as f:
            f.write(str(plan_count))

    def read_progress(self):
        """
        Reads previously saved progress from the progress file.
        
        Returns:
            int: Number of plans previously generated, or 0 if no progress file exists.
        """
        if os.path.exists(self.planner_progress_path):
            with open(self.planner_progress_path, 'r') as f:
                return int(f.read().strip())
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
            ppg (int): Number of plans generated (a progress count).
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