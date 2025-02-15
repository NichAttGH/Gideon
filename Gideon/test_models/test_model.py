# Import necessary libraries
import argparse
import os
import re
import json
import time
import sseclient
import requests
import subprocess
from pathlib import Path

# Import necessary functions
from utils import (
    Folders_Structure,
    open_json_file,
    write_domain_and_create_logs_dir,
    write_problem,
    write_plan,
    calculate_statistics,
    final_output,
    write_log
)

# Project metadata
__author__ = "Nicholas Attolino"
__copyright__ = "Copyright 2024, Nicholas Attolino"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Attolino"
__email__ = "nicholasattolino@gmail.com"
__status__ = "Development"

def load_model(model_name):
    """
    Load a machine learning model from a specified URL.

    Args:
        model_name (str): The name of the model to be loaded.

    Sends a POST request to the model loading endpoint and prints the response.
    """
    url = "http://127.0.0.1:5000/v1/internal/model/load"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer yourPassword123"
    }

    data = {
        "model_name": model_name
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Response:", response.json())
        print("Model loaded successfully!")
    else:
        print(f"Error loading model. Code: {response.status_code}")
        print("Details:", response.text)
    
def request_plan_to_the_model(domain_problem, execution_times):
    """
    Request a planning response from the model based on the provided domain&problem prompt.

    Args:
        domain_problem (str): The combined domain and problem prompt.
        execution_times (list): A list to record execution times for each request.

    Returns:
        tuple: The assistant's message and updated execution times.
    """
    url = "http://127.0.0.1:5000/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer yourPassword123"
    }

    prompt = []
    prompt.append({"role": "user", "content": domain_problem})

    data = {
        "mode": "chat-instruct",
        "stream": True,
        "character": "Example",
        "messages": prompt,
        "temperature": 0.01,
        #"max_tokens": 2048
    }

    stream_response = requests.post(url, headers=headers, json=data, verify=False, stream=True)
    client = sseclient.SSEClient(stream_response)

    start_request = time.time()
    assistant_message = ''
    for event in client.events():
        payload = json.loads(event.data)
        chunk = payload['choices'][0]['delta']['content']
        assistant_message += chunk
        print(chunk, end='')
    full_time = time.time() - start_request

    print()
    print(f"Time required for the request: {full_time:.2f}")

    execution_times.append(full_time)
    
    return assistant_message, execution_times

def check_val(validate_path, domain_file_path, problem_file_path, plan_file_path, plans_failed, failed_problems):
    """
    Validate the generated plan using an external validation tool (VALIDATE).

    Args:
        validate_path (str): The path to the validation tool (VALIDATE).
        domain_file_path (str): The path to the domain file.
        problem_file_path (str): The path to the problem file.
        plan_file_path (str): The path to the generated plan file.
        plans_failed (int): The current count of failed plans.
        failed_problems (list): A list of problems whose plans were found to be invalid.

    Returns:
        tuple: Updated counts of failed plans and the list of failed problems.
    """
    try:
        # Start the external process in blocking mode
        process = subprocess.run(
            [validate_path, domain_file_path, problem_file_path, plan_file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Check if "success" is in the command output
        if "Successful" in process.stdout:
            print("Plan valid!")
        else:
            # Delete the plan, increase plans_failed counter and add the failed problem to the list
            os.remove(plan_file_path)
            plans_failed += 1
            failed_problems.append(Path(problem_file_path).name)
            
        return plans_failed, failed_problems
    except Exception as e:
        print(f"Error during validation: {e}")
        return plans_failed, failed_problems

def main(args):
    """
    Main function to orchestrate the loading of the model, processing of domains and problems,
    and validation of generated plans.

    Args:
        args (Namespace): Command line arguments containing dataset directory path,
                          validation tool path, and model name.
    """
    # Create folders structure
    folders_structure =  Folders_Structure(args.dataset_dir_path, args.model_name)
    test_set_json, domains_dir_path = folders_structure.create_structure()

    # Read JSON file and split domains and problems
    json_data = open_json_file(test_set_json)
    domains = [item['instruction'] for item in json_data]
    problems = [item['input'] for item in json_data]

    # Change into Str for api requests
    domains = list(map(str, domains))
    problems = list(map(str, problems))
    
    # Initialize the history of the chat
    history = []

    # Initialize the counter of plans failed and the list of the problems failed
    plans_failed = 0
    failed_problems = []

    # Initialize execution_times list
    execution_times = []

    # Load the model
    load_model(args.model_name)

    for i in range (len(problems)):
        # Write each domain and problem as a file
        domain = domains[i]
        domain_dir_path, domain_name, domain_file_path, logs_dir_path = write_domain_and_create_logs_dir(domains_dir_path, domain)
        
        problem = problems[i]
        problem_name, problem_file_path = write_problem(problem, domain_name, domain_dir_path)
        
        # Request to the model
        domain_problem = "\n".join([domain, problem])
        assistant_message, execution_times = request_plan_to_the_model(domain_problem, execution_times)

        # Write each plan as a file
        plan_file_path, plans_dir_path = write_plan(domain_dir_path, problem_name, assistant_message)

        # Check plans with VALIDATE
        plans_failed, failed_problems = check_val(args.validate_path, domain_file_path, problem_file_path, plan_file_path, plans_failed, failed_problems)

        # Update the history
        history.append({"role": "system", "content": domain})
        history.append({"role": "user", "content": problem})
        history.append({"role": "assistant", "content": assistant_message})

    # Compute statistics
    avg_time, min_time, max_time, median_time, std_dev = calculate_statistics(execution_times)

    # Sort the list based on the numeric part of the file name
    failed_problems = sorted(
        failed_problems,
        key=lambda x: int(re.search(r'problem_(\d+)', os.path.basename(x)).group(1))
    )
    # Print failed problems for invalid plans
    print("\nThe following problems did not result in viable plans:")
    for problem in failed_problems:
        print(problem)

    # Save a log file
    write_log(logs_dir_path, plans_failed, plans_dir_path, avg_time, min_time, max_time, median_time, std_dev)

    # Print the output with several informations
    final_output(plans_failed, plans_dir_path, avg_time, min_time, max_time, median_time, std_dev)

if __name__ == "__main__":
    # Command line argument parser setup
    parser = argparse.ArgumentParser(description='Process plans from the model')
    parser.add_argument('-d', '--dataset_dir_path', type=str, help='Dataset directory path')
    parser.add_argument('-v', '--validate_path', type=str, help='Validate tool path')
    parser.add_argument('-m', '--model_name', type=str, help='Name of the model used')
    args = parser.parse_args()

    # Launch main function
    main(args)