# conda  -managing dependencies and isolating your project's environment
Creating a Conda environment to run your Python code that interacts with Neptune is a good practice for managing dependencies and isolating your project's environment. Here I am going to setup environment to connect to AWS Neptune and work iwth jupyter notebook. 

> **Purpose**
>> By using a YAML file to define your Conda environment and its dependencies, you can easily create a consistent and reproducible environment for your Neptune project.
>> You can also share the environment.yml file with others, allowing them to create the same environment.

## Step1 - installing miniconda or anaconda
The fastest way to obtain conda is to install Miniconda, a mini version of Anaconda that includes only conda and its dependencies. If you prefer to have conda plus over 7,500 open-source packages, install Anaconda.
[more on this...](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)


## Step2 Create a YAML Environment File - environment.yml
- environment is neptune_graph_viz.yaml
```yaml
name: neptune_graph_viz
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10  # Specify your desired Python version
  - jupyter
  - gremlinpython
  - networkx  # Optional, for graph visualization
  - matplotlib #  Neptune or TinkerPop server, retrieve data, and visualize it using NetworkX and Matplotlib.
  - other_dependency  # Add any other dependencies as needed
  - pip:
    - requests  # A pip package not available in Conda
    - other_pip_dependency
```
- The dependencies section can include both Conda packages and pip packages.
- You would add a line with pip in the dependencies section when you want to include Python packages that are not available in Conda repositories. This is useful when you need to install packages from the Python Package Index (PyPI) or other non-Conda sources.
- channels
  - **Defaults Channel**: The defaults channel is the primary channel that contains the most commonly used packages. It is always included by default, and Conda will search for packages in this channel if no other channels are specified.
  - **Additional Channels**: You can specify additional channels where Conda should look for packages. These channels can be other Conda repositories, including community-managed channels like conda-forge. You might want to use additional channels to access packages that are not available in the default channel.

## Step 3 creating conda env
```shell
conda create -n <environment_name> python=3.x
conda activate <environment_name>
# you can start jupyter notebook
jupyter notebook
# When you're finished working in the environment, deactivate it to return to your global Python environment.
conda deactivate
```

## You can update a Conda environment by adding or removing packages or changing 

```shell
conda activate your_environment_name
# install  the new package not in yaml
conda install new_package_name
# remove package
conda remove package_name_to_remove
```

## delete conda env
```shell
conda env remove --name old_environment_name

```