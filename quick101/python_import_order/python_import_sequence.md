# Python Import Sequence Tracking & Analysis Tools

This guide compares the three tools I've developed for tracking and analyzing Python import sequences. Each has specific
advantages depending on your needs.

## Quick Comparison

| Feature                | Import Tracker | Import Path Analyzer | Static Module Mapper |
|------------------------|----------------|----------------------|----------------------|
| Simplicity             | ★★★★★          | ★★★☆☆                | ★★☆☆☆                |
| User-defined filtering | ✓              | ✓                    | ✓                    |
| Runtime analysis       | ✓              | ✓                    | ✓                    |
| Static analysis        | ✗              | ✓                    | ✓✓✓                  |
| Code path tracking     | ✗              | ✓✓✓                  | ✓                    |
| Visual output          | ✗              | ✓                    | ✓✓✓                  |
| Best for               | Quick analysis | Path execution       | Codebase mapping     |

## 1. Import Tracker

**Best for:** Quick import sequence analysis of a single script

A lightweight tool that shows all imports in order of execution with detailed timing information. This is a direct
replacement for `python -v` with cleaner output and filtering options.

### Example Usage:

```bash
python import_tracker.py your_script.py --user-only
python import_tracker.py your_script.py arg1 arg2 --detail
```

### Key Features:

- Simple to use with minimal setup
- Shows imports in execution order
- Provides timing information
- Can filter standard library imports
- Works with any Python script without modification

## 2. Import Path Analyzer

**Best for:** Understanding which imports are used in different execution paths

Combines runtime analysis with code coverage to show which modules are imported and which execution paths are taken
based on arguments or environment variables.

### Example Usage:

```bash
python import_path_analyzer.py your_script.py --user-only
python import_path_analyzer.py your_script.py arg1 arg2 --export=html
```

### Key Features:

- Analyzes execution paths with code coverage
- Shows which imports are actually used during execution
- Exports data in JSON, CSV, or HTML format
- Creates visual reports of code paths and imports
- Perfect for conditional import analysis

## 3. Static Module Mapper

**Best for:** Comprehensive analysis of large codebases and their dependencies

The most advanced tool that combines static analysis with optional runtime tracking to create a complete map of module
dependencies and import relationships.

### Example Usage:

```bash
python module_mapper.py /path/to/project --user-only
python module_mapper.py /path/to/project --run main.py --args "arg1 arg2" --graph
```

### Key Features:

- Maps entire project dependencies
- Generates visual dependency graphs (requires graphviz)
- Combines static analysis with runtime data
- Identifies entry points and most-imported modules
- Can exclude specified patterns
- Shows import relationships between modules

## Usage Recommendations

1. **For quick script analysis:** Use the Import Tracker for a simple, clean alternative to `python -v`
2. **For execution path analysis:** Use the Import Path Analyzer to understand which imports are activated based on
   runtime conditions
3. **For codebase mapping:** Use the Static Module Mapper to analyze entire projects and visualize module dependencies

## Installation

All tools require only Python's standard library, except:

- Import Path Analyzer requires the `coverage` package (`pip install coverage`)
- Static Module Mapper's graph feature requires `graphviz` (`pip install graphviz`)

## Tips for Best Results

1. **Use `--user-only` for cleaner output** - Filter out standard library modules to focus on your own code
2. **Combine with different arguments** - Run the same script with different arguments to see how import paths change
3. **Generate HTML reports** - For complex analysis, export to HTML for easier visualization
4. **Use the graph feature** - For large codebases, visual dependency graphs make understanding relationships much
   easier
5. **Exclude test directories** - Use `--exclude` patterns to skip test folders or virtual environments