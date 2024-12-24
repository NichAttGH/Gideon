"""
Process Controller
================

Module for managing the execution state of the PDDL problem generation process.
Provides functionality to pause, resume, and stop the generation process.

Features:
- Process state management (pause/resume/stop)
- User feedback through console messages
- State tracking through boolean flags
"""

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

class Process_Controller:
    """
    Controller class for managing process execution states.
    
    Attributes:
        pause (bool): Flag indicating if process is paused
        resume (bool): Flag indicating if process should resume
        stop (bool): Flag indicating if process should stop
    """
    
    def __init__(self):
        """
        Initialize the process controller with default states.
        All states are initially set to False.
        """
        self.pause = False      # Process pause state
        self.resume = False     # Process resume state
        self.stop = False       # Process stop state

    def paused_p(self):
        """
        Pause the current process execution.
        
        Sets the pause flag to True and provides user feedback
        through console output.
        """
        self.pause = True
        print("\nPaused processing..")
    
    def resume_p(self):
        """
        Resume the process if it was previously paused.
        
        Only resumes if the process was in a paused state.
        Provides user feedback through console output.
        """
        if self.pause:
            self.pause = False
            print("\nResume processing..")
    
    def stop_p(self):
        """
        Stop the process execution.
        
        Sets the stop flag to True and provides user feedback
        through console output. This will trigger process termination.
        """
        self.stop = True
        print("\nEnd processing...")