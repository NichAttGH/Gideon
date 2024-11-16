# Master-Thesis
Here will be present the work done for my Master Thesis

## PDDL problem generator:

### 1. Purpose

This script automatically generates random PDDL problem files from a given PDDL domain file.<br>
It's particularly useful for testing planning algorithms and generating diverse problem instances.

### 2. Main Components

#### A. Command Line Interface

```python
parser.add_argument('-g', '--generator_path', type=str)
parser.add_argument('-d', '--domain_origin', type=str)
parser.add_argument('-o', '--output_dir', type=str)
parser.add_argument('-n', '--num_problems', type=int)
```
- Takes inputs for generator path, domain file, output directory, and number of problems to generate

#### B. Process Control

- Implements three control functions:
  - `paused_p()`: Pauses generation (triggered by 'p' key)
  - `resume_p()`: Resumes generation (triggered by 'r' key)
  - `stop_p()`: Stops generation (triggered by 's' key)

#### C. File Structure Management

```python
output_dir/
├── domain_name/
│   ├── domain.pddl (copied)
│   ├── problems/
│   └── logs/
```
- Creates organized directory structure
- Copies domain file
- Creates separate directories for problems and logs

#### D. Progress Tracking

- Saves generation progress to allow resumption if interrupted
- Maintains hash list to prevent duplicate problems
- Generates log files with statistics

### 3. Problem Generation Process

#### A. Domain Loading

1. Reads PDDL domain file
2. Validates domain (checks for unsupported features like numeric fluents)
3. Parses domain structure (types, predicates, etc.)

#### B. Object Generation

```python
def generate_random_objects(prob_types, set_predicates):
```
- Creates random objects based on domain types
- Handles both single and multiple type domains
- Ensures sufficient objects for multi-term predicates

#### C. State Generation

1. Initial State (`generate_random_init_state`):
   - Creates random ground predicates
   - Assigns random truth values
   - Handles predicates with different arities
2. Goal State (`generate_random_goal_state`):
   - Similar to initial state but uses subset of predicates
   - Makes goals potentially achievable

#### D. Problem Construction

```python
problem = Problem(
    name=problem_name,
    domain=domain,
    domain_name=domain.name,
    requirements=domain.requirements,
    objects=prob_objects,
    init=init_state,
    goal=And(*goal_state)
)
```
- Combines all components into PDDL problem instance
- Uses logical AND for goal conditions

### 4. Features

#### A. Duplicate Detection

- Generates SHA-256 hash for each problem
- Maintains list of existing hashes
- Prevents duplicate problem generation

#### B. Progress Monitoring

- Displays progress bar using tqdm
- Shows generation status and time elapsed
- Allows pause/resume/stop operations

#### C. Error Handling

- Validates input files and directories
- Handles interruptions gracefully
- Preserves progress on interruption

### 5. How to install

#### On Windows:

1) Install [Python](https://www.python.org/downloads/) -> Tick "Add python.exe to PATH" and Select "Install Now"
2) Install these packages:

```bash
pip3 install pddl, keyboard, tqdm
```

3) Download this repository in your Workspace, or with git:

```bash
git clone https://github.com/NichAttGH/Master-Thesis.git
```

#### On Ubuntu (used Ubuntu 20.04 for testing):

1) Install last version of Python
2) Install these packages:

```bash
pip3 install pddl, keyboard, tqdm
```

3) Download this repository in your Workspace, or with git:

```bash
git clone https://github.com/NichAttGH/Master-Thesis.git
```

### 6. Usage and Example

- On Windows:

To see how many args are available, just use the command below:

```bash
python <path/to/gpg.py> -h
```

Example of usage:

```bash
python <path/to/gpg.py> -d <path/to/domain.pddl> -o <path/to/output_directory> -n 10
```

- On Ubuntu (used Ubuntu 20.04 for testing):

To see how many args are available, just use the command below:

```bash
sudo python3 <path/to/gpg.py> -h
```

Example of usage:

```bash
sudo python3 <path/to/gpg.py> -d <path/to/domain.pddl> -o <path/to/output_directory> -n 10
```

**NOTICE**: for security reasons, Unix-like OS make the parent folder owned by root so you cannot delete the final output folder from CLI. Because of this I recommend using the command below to unlock the parent folder whenever you are done with the generator:

```bash
sudo chown -R $USER:$USER <path/to/father's_folder>
```

#### For both OS

This example would:
1. Load domain.pddl
2. Create output directory structure
3. Generate 10 unique problems
4. Save problems and logs
5. Allow interactive control during generation

**NOTICE**: to generate only 1 PDDL problem file, use along with the rest of the command also:

```bash
-g <path/to/gpg.py>
```

The script is particularly useful for automated testing and benchmarking of PDDL planners, providing a way to generate several problem instances while maintaining control over the generation process.
