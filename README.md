# _Gideon_: PDDL Problem Generator and Planner Framework
A Python-based framework for <b>generating Planning Domain Definition Language (PDDL) problem files</b> and <b>planning solutions</b> using various planners. This tool automates the creation of randomized PDDL problem instances, generates plans, and organizes datasets for AI planning research and development.

## Overview
_<b>Gideon</b>_ is designed to:
- <b>Generate PDDL problem files</b> based on a given domain and a JSON configuration.
- <b>Plan solutions</b> for the generated problems using supported planners (e.g., Probe).
- <b>Organize datasets</b> for training, validation, and testing in AI planning systems.
- <b>Track progress</b> and <b>ensure uniqueness</b> of generated problems and plans.

This framework is ideal for researchers, developers, and educators working with AI planning systems, PDDL-based tools, and dataset generation.

## Key Features

### PDDL Problem Generation
- <b>Customizable Problem Generation</b>: Define problem structures using a JSON configuration file.
- <b>Randomized Initial and Goal States</b>: Generate problems with randomized initial and goal states based on user-defined probabilities.
- <b>Duplicate Detection</b>: Use SHA-256 hashes to ensure unique problem instances.
- <b>Progress Tracking</b>: Resume interrupted generation sessions with progress tracking.
- <b>Logging and Reporting</b>: Automatically generate log files with statistics about the generation process.
- <b>Folder Structure Management</b>: Organize generated problems, logs, and progress files into a structured directory.

### Planning
- <b>Planner Integration</b>: Supports planners like Probe for generating plans.
- <b>Plan Validation</b>: Validate generated plans using the VAL validation tool.
- <b>Progress Tracking</b>: Track planning progress and resume interrupted sessions.
- <b>Logging and Statistics</b>: Generate logs with planning statistics, including execution times and failure rates.

### Dataset Handling
- <b>Dataset Creation</b>: Process PDDL domains, problems, and plans into structured datasets.
- <b>Dataset Splitting</b>: Split datasets into training, validation, and test sets.
- <b>Stopping Sequences</b>: Optionally append stopping sequences to plan files for specific use cases.
- <b>Logging and Reporting</b>: Generate logs summarizing dataset creation and splitting.

## Installation
To use the framework, clone the repository and install the required libraries:
```bash
git clone https://github.com/NichAttGH/Master-Thesis.git
pip install (libraries)
```
- numpy
- tqdm
- pickle
- shutil
- pddl
- re
- tabulate

Check the permissions on Probe and Validate because if they are not executable after downloading, you need to assign executability (Please note: the following commands work when you are inside their respective folders):
```bash
chmod +x probe
```
```bash
chmod +x Validate
```

## Quick Start
### 1. Generate PDDL Problems
1. Prepare your domain file (e.g., domain.pddl) and JSON configuration file (e.g., config.json).
2. Run the problem generator:
```bash
python gpg.py -d domain.pddl -o output_dir -n 10 -j config.json
```
  - `-d`: Path to the PDDL domain file.
  - `-o`: Output directory where you want to generate files.
  - `-n`: Number of problems to generate.
  - `-j`: Path to the JSON configuration file.
3. Generated problems will be saved in the `output_dir/domain_name_folder/problems` directory.

### 2. Generate Plans
1. Use the generated problems to create plans:
```bash
python bp.py -o output_dir -c probe
```
  - `-o`: Output directory containing the generated problems.
  - `-c`: Planner to use (e.g., `probe`).
2. Generated plans will be saved in the `domain_name_folder/plans` directory.

### 3. Create Datasets
1. Process the generated problems and plans into datasets:
```bash
python gd.py -s output_dir -v 20 -t 10
```
  - `-s`: Path to the directory containing the domain, problems, and plans.
  - `-v`: Number of validation set entries.
  - `-t`: Number of test set entries.
2. Datasets will be saved in the `domain_name_folder/dataset` directory.

## Documentation
For detailed documentation on how to configure the JSON file, customize problem generation, use planners, and create datasets, refer to the [Documentation](https://github.com/NichAttGH/Master-Thesis).

## License
This project is licensed under the GNU License. See the [LICENSE](https://github.com/NichAttGH/Master-Thesis/blob/main/LICENSE) file for details.

## Support
If you encounter any issues or have questions, please open an issue on GitHub or contact us at nicholasattolino@gmail.com.

## Acknowledgments
- Special thanks to the developers of the [pddl](https://github.com/AI-Planning/pddl/tree/main) Python library for providing the core functionality for PDDL parsing and manipulation.
- This project was inspired by the need for efficient and scalable PDDL problem generation and planning in AI research.

## Example JSON Configuration
Here’s an example of a JSON configuration file for generating PDDL problems:
```json
{
  "problem_prefix": "joint_bar",
  "domain_name": "joint_bar",
  "objects_pools": {
    "gripper_pool": {
      "object_type": "gripper",
      "mutex": true,
      "sequential": true,
      "count": 2,
      "name_prefix": "g"
    },
    "link_pool": {
      "object_type": "link",
      "sequential": true,
      "count": 4,
      "name_prefix": "link"
    }
  },
  "predicates_pools": {
    "grasped": {
      "in-centre": {
        "count": 1,
        "args": ["center_joint$0"]
      }
    }
  },
  "constant_initial_state": "(link-before link0 link1)",
  "init_state": {
    "predicates": {
      "mutex_pools": [["grasped", "not-grasped"]],
      "mutex_prob": [[0.7, 0.3]],
      "pools": ["angle_joint_init"]
    }
  },
  "constant_goal_state": "",
  "goal_state": {
    "predicates": {
      "mutex_pools": [],
      "mutex_prob": [],
      "pools": ["angle_joint_goal"]
    }
  }
}
```
