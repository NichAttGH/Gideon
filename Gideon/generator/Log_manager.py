"""
Log Manager
==========

Module for managing log file generation during PDDL problem generation.
Creates timestamped log files containing generation statistics and details.

Features:
- Timestamped log file creation
- Generation statistics tracking
- Path and timing information logging
"""

# Import necessary libraries
import datetime
import os

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

class Log_Manager:
    """
    Manager class for handling log file generation and management.
    
    Attributes:
        logs_path (str): Directory path where log files will be stored
    """
    
    def __init__(self, logs_path):
        """
        Initialize the log manager.
        
        Args:
            logs_path (str): Directory path where log files will be stored
        """
        self.logs_path = logs_path
    
    def generate_log_file(self, i, problems_path, t):
        """
        Generate a timestamped log file with generation statistics.
        
        Creates a log file containing:
        - Number of problems generated
        - Directory path of generated problems
        - Total generation time in seconds
        
        Args:
            i (int): Number of problems generated
            problems_path (str): Directory path containing generated problems
            t (float): Time taken for generation in seconds
            
        File Format:
            problem_generation_YYYY-MM-DD_HH-MM-SS.log
        """
        # Generate timestamp for log filename
        current_date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_filename = f"problem_generation_{current_date}.log"
        log_file_path = os.path.join(self.logs_path, log_filename)
        
        # Write generation statistics to log file
        with open(log_file_path, 'w') as log_file:
            log_file.write(f"Number of generated problems: {i}\n")
            log_file.write(f"Directory of generated problems: {problems_path}\n")
            log_file.write(f"Time required to generate problems: {t:.2f} seconds")