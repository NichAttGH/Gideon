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

class Planner_Log_Manager:
    """
    Manager class for handling log file generation and management.
    
    Attributes:
        logs_path (str): Directory path where log files will be stored
    """
    
    def __init__(self, logs_path):
        """
        Initializes the log manager with the specified logs directory.
        
        Args:
            logs_path (str): Directory path where log files will be stored.
        """
        self.logs_path = logs_path
    
    def generate_log_file(self, i, p_failed, fp_progress, plans_dir_path, hours, minutes, seconds, avg_time, min_time, max_time, median_time, std_dev):
        """
        Generates a log file with planning statistics.
        
        This method creates a log file with a timestamped filename and writes
        the provided statistics to it.
        
        Args:
            i (int): Number of generated problems considered.
            p_failed (int): Number of plans that failed.
            fp_progress (int): Total of plans failed.
            plans_dir_path (str): Directory of generated plans.
            hours (int), minutes (int), seconds (float): Time required to generate plans.
            avg_time (float): Average time taken for planning.
            min_time (float): Minimum time taken for planning.
            max_time (float): Maximum time taken for planning.
            median_time (float): Median time taken for planning.
            std_dev (float): Standard deviation of planning times.
        """
        # Generate timestamp for log filename
        current_date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_filename = f"planning_{current_date}.log"
        log_file_path = os.path.join(self.logs_path, log_filename)
        
        # Write generation statistics to log file
        with open(log_file_path, 'w') as log_file:
            log_file.write(f"Number of generated problems considered: {i}\n")
            log_file.write(f"Number of plans failed: {p_failed}\n")
            log_file.write(f"Total of plans failed: {fp_progress}\n")
            log_file.write(f"Directory of generated plans: {plans_dir_path}\n")
            log_file.write(f"Time required to generate plans: {int(hours)}h {int(minutes)}m {seconds:.2f}s\n")
            log_file.write("\n ----- Times for planning -----\n")
            log_file.write(f"Average Time: {avg_time:.2f} seconds\n")
            log_file.write(f"Min Time: {min_time:.2f} seconds\n")
            log_file.write(f"Max Time: {max_time:.2f} seconds\n")
            log_file.write(f"Median Time: {median_time:.2f} seconds\n")
            log_file.write(f"Standard Deviation: {std_dev:.2f} seconds")