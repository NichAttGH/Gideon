"""
Hash List Manager
===============

Module for managing hash-based duplicate detection of PDDL problems.
Provides functionality to generate, store, and verify SHA-256 hashes
of generated problems to ensure uniqueness.

Features:
- SHA-256 hash generation for PDDL problems
- Persistent storage of hashes in text file
- Hash list management for duplicate detection
- Support for resuming previous generation sessions
"""

import os
import hashlib

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

class Hash_list_Manager:
    """
    Manager class for handling problem hashes and duplicate detection.
    
    Attributes:
        hash_list (list): Class-level list storing all previously used hashes
        hash_list_filename (str): Name of file storing the hash list
        hash_list_path (str): Full path to the hash list file
    """
    
    hash_list = []      # Class-level list to store all previously used hashes

    def __init__(self, output_path):
        """
        Initialize the hash list manager.
        
        Args:
            output_path (str): Directory path where the hash list file will be stored
        """
        self.hash_list_filename = "hash_list.txt"       # Name of the hash list file
        self.hash_list_path = os.path.join(output_path, self.hash_list_filename)  # Full path to hash list file

    def generate_hash_list(self, hash_list):
        """
        Save the current hash list to file.
        
        Writes each hash on a new line in the hash list file.
        
        Args:
            hash_list (list): List of hashes to save
        """
        with open(self.hash_list_path, 'w') as f:
            for hash in hash_list:
                f.write(f"{hash}\n")
        
    def read_hash_list_to_list(self, answer):
        """
        Read previously stored hashes from file.
        
        Loads existing hashes if continuing a previous session (answer='Y'),
        or returns empty list for new session (answer='N').
        
        Args:
            answer (str): 'Y' to load existing hashes, 'N' for fresh start
            
        Returns:
            list: List of loaded hashes or empty list
        """
        hash_list = []
        
        # Check if the file exists and read the hashes based on user choice
        if os.path.exists(self.hash_list_path):
            if answer == 'Y':
                with open(self.hash_list_path, 'r') as f:
                    hash_list = [line.strip() for line in f]
            elif answer == 'N':
                hash_list = []
        return hash_list
    
def generate_hash(problem):
    """
    Generate SHA-256 hash for a PDDL problem.
    
    Converts the problem to string and generates a unique hash
    to identify duplicate problems.
    
    Args:
        problem: PDDL problem object to hash
        
    Returns:
        str: Hexadecimal representation of the SHA-256 hash
    """
    hash_16bit = hashlib.sha256(str(problem).encode()).hexdigest()
    return hash_16bit