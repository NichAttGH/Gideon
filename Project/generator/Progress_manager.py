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

import os

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
        npg (int): Class-level counter for number of problems generated
        progress_path (str): Path to the progress file
    """
    
    npg = 0    # Class-level counter for number of problems generated

    def __init__(self, progress_path):
        """
        Initialize the progress manager.
        
        Args:
            progress_path (str): Path where progress file will be stored
        """
        self.progress_path = progress_path
    
    def save_progress(self, i):
        """
        Save current progress to file.
        
        Writes the current number of generated problems to the progress file.
        
        Args:
            i (int): Current number of problems generated
        """
        with open(self.progress_path, 'w') as f:
            f.write(str(i))

    def read_progress(self):
        """
        Read previously saved progress from file.
        
        Returns:
            int: Number of problems previously generated, or 0 if no progress file exists
        """
        if os.path.exists(self.progress_path):
            with open(self.progress_path, 'r') as f:
                return int(f.read().strip())
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
                  First element is progress count (int)
                  Second element is user's choice ('Y' or 'N')
        """
        while True:
            print("Is there a stopped processing in advance? (Y for yes, N for no)")
            answer = input().strip().upper()        
            if answer == "Y":
                if os.path.exists(problems_path) and os.path.exists(output_path):
                    npg = self.read_progress()
                    return npg, answer
            elif answer == "N":
                return 0, answer
            else:
                print("Invalid input, please enter 'Y' for yes or 'N' for no.")