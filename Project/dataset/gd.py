# Import necessary libraries
import argparse
from pathlib import Path

# Import Modules and useful functions
from utils_dataset import create_directories, save_to_json, clean_set, final_output, generate_log
from Dataset_handler import DatasetHandler

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

def main(args):
    """
    Main function to process datasets based on the provided command-line arguments.
    
    Args:
        args: Command-line arguments containing paths and settings for dataset processing.

    This function manages the flow of dataset processing based on the paths provided via command-line arguments.
    It performs operations such as: processing single or multiple directories containing PDDL files,
    generating datasets split into training, validation and test sets, saving results in JSON format
    and creating processing-related logs.
    """
    # Initialize the DatasetHandler with the stopping sequence if provided
    dataset_handler = DatasetHandler(stopping_seq=args.stopping_seq)
    entries = [] # List to hold processed entries
    single_entries = 0 # Counter for single domain entries
    log_data = []  # List to hold log data for output

    # Check if multi-domain directory path is provided
    if args.multi_domains_dir_path:
        # Create a dictionary of domain directories
        domains_dict = {
            file.name: str(file)
            for file in Path(args.multi_domains_dir_path).iterdir() if file.is_dir()
        }
        # Process each domain directory
        for key, value in domains_dict.items():
            entries, single_entries = dataset_handler.process_directory(entries, single_entries, value)
            
            # Append log data for the current domain
            log_data.append({
                "Domain": key,
                "Entries": single_entries,
                "Path": value
            })
            # Check if no valid entries were found
            if not entries:
                print("No valid entries found. Exiting.")
                return

        # Attempt to split the dataset into training, validation, and test sets
        try:
            train_set, val_set, test_set = dataset_handler.split_dataset(entries, args.validation, args.test)
        except ValueError as e:
            print(str(e))
            return
        
        # Define paths for saving datasets and logs
        dataset_path = Path(args.multi_domains_dir_path) / "multi_domains_dataset"
        train_set_dir = dataset_path / "train_set"
        val_set_dir = dataset_path / "val_set"
        test_set_dir = dataset_path / "test_set"
        logs_dir = dataset_path / "logs"
        
        # Clean the datasets
        train_set = clean_set(train_set)
        val_set = clean_set(val_set)
        test_set = clean_set(test_set)

        # Create necessary directories for saving datasets
        create_directories(dataset_path, train_set_dir, val_set_dir, test_set_dir, logs_dir)
        
        # Save datasets to JSON files
        save_to_json(train_set, train_set_dir / "training.json")
        save_to_json(val_set, val_set_dir / "validation.json")
        save_to_json(test_set, test_set_dir / "test.json")
        
        # Generate logs and final output
        generate_log(logs_dir, log_data, train_set, val_set, test_set)
        final_output(log_data, train_set, val_set, test_set)

        print(f"Dataset processing complete. JSON files saved in {dataset_path}.")

    # Check if single domain directory path is provided
    elif args.single_domain_dir_path:
        # Process the single domain directory
        entries, single_entries = dataset_handler.process_directory(entries, single_entries, args.single_domain_dir_path)
        print(f"Entries for {Path(args.single_domain_dir_path).name}: {single_entries}")

        # Append log data for the single domain
        log_data.append({
            "Domain": Path(args.single_domain_dir_path).name,
            "Entries": single_entries,
            "Path": args.single_domain_dir_path
        })
        # Check if no valid entries were found
        if not entries:
            print("No valid entries found. Exiting.")
            return

        # Attempt to split the dataset into training, validation, and test sets
        try:
            train_set, val_set, test_set = dataset_handler.split_dataset(entries, args.validation, args.test)
        except ValueError as e:
            print(str(e))
            return
        
        # Define paths for saving datasets and logs
        dataset_path = Path(args.single_domain_dir_path) / f"{Path(args.single_domain_dir_path).name}_dataset"
        train_set_dir = dataset_path / "train_set"
        val_set_dir = dataset_path / "val_set"
        test_set_dir = dataset_path / "test_set"
        logs_dir = Path(args.single_domain_dir_path) / "logs"

        # Clean the datasets
        train_set = clean_set(train_set)
        val_set = clean_set(val_set)
        test_set = clean_set(test_set)

        # Create necessary directories for saving datasets
        create_directories(dataset_path, train_set_dir, val_set_dir, test_set_dir)

        # Save datasets to JSON files
        save_to_json(train_set, train_set_dir / "training.json")
        save_to_json(val_set, val_set_dir / "validation.json")
        save_to_json(test_set, test_set_dir / "test.json")

        # Generate logs and final output
        generate_log(logs_dir, log_data, train_set, val_set, test_set)
        final_output(log_data, train_set, val_set, test_set)

        print(f"Dataset processing complete. JSON files saved in {dataset_path}.")

if __name__ == "__main__":
    # Command line argument parser setup
    parser = argparse.ArgumentParser(description='Process domains, problems, and plans into JSON datasets')
    parser.add_argument('-s', '--single_domain_dir_path', type=str, help='Single-domain directory for PDDL files')
    parser.add_argument('-m', '--multi_domains_dir_path', type=str, help='Multi-domains directory for PDDL files')
    parser.add_argument('-v', '--validation', type=int, default=0, help='Number of entries for validation set')
    parser.add_argument('-t', '--test', type=int, default=0, help='Number of entries for test set')
    parser.add_argument('--stopping_seq', type=str, default=None, help='Optional stopping sequence to append to plans')
    args = parser.parse_args()

    # Launch main function
    main(args)