"""
Progress Manager
==============

Module for managing and tracking the progress of PDDL problem generation.
Handles saving, reading, and checking generation progress to support
resumption of interrupted generations.

Features:
- Progress state persistence
- Progress recovery after interruption
- User interaction for progress handling
"""

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

class Progress_Manager:
    """
    Manager class for handling generation progress tracking.
    
    Attributes:
        progress_path (str): Path to the progress file
    """

    def __init__(self, progress_path):
        """
        Initialize the progress manager.
        
        Args:
            progress_path (str): Path where progress file will be stored
        """
        self.progress_path = progress_path
    
    def save_progress(self, i):
        """
        Save current progress into the 'progress.txt' file.
        
        Writes the current number of generated problems to the progress file.
        
        Args:
            i (int): Current number of problems generated
        """
        # Read the content of the file
        with open(self.progress_path, 'r') as file:
            lines = file.readlines()

        # Search the row that contains 'npg_progress ='
        for l, line in enumerate(lines):
            if line.startswith("npg_progress = "):
                # Rewrite the value with the new one
                lines[l] = f"npg_progress = {i}\n"
                break
        
        # Rewrite the file with the new value
        with open(self.progress_path, 'w') as file:
            file.writelines(lines)

    def read_progress(self):
        """
        Read previously saved progress from the file.
        
        This function reads the progress from a specified file and returns the number of problems generated.
        
        Returns:
            Value (int): Number of problems previously generated, or 0 if no progress file exists
        """
        # Define a regex pattern to match the line containing 'npg_progress'
        pattern = r"npg_progress\s*=\s*(\d+)"
        
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
        
    def check_progress(self, problems_path, output_path):
        """
        Check for existing progress and handle user interaction.
        
        Prompts user to decide whether to resume from previous progress
        or start fresh generation.
        
        Args:
            problems_path (str): Path to generated problems directory
            output_path (str): Path to output directory
            
        Returns:
            tuple: (number of problems generated, user's answer)
                    - First element is progress count (int)
                    - Second element is user's choice ('Y' or 'N')
        """
        while True:
            print("Is there a stopped processing in advance? (Y/N)")
            answer = input().strip().upper()        
            if answer == "Y":
                if os.path.exists(problems_path) and os.path.exists(output_path):
                    npg = self.read_progress()
                    return npg, answer
            elif answer == "N":
                # Creation of the 'progress.txt' file
                template_progress = {
                    "npg_progress": 0,
                    "ppg_progress": 0,
                    "hash_list_progress": 0,
                    "failed_problems_progress": 0,
                }
                with open(self.progress_path, "w") as f:
                    for key, value in template_progress.items():
                        f.write(f"{key} = {value}\n")
                return 0, answer
            else:
                print("Invalid input, please enter 'Y' for yes or 'N' for no.")