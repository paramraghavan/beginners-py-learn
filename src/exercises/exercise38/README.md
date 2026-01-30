# Package Compatibility Resolver

A Python script to find compatible versions when adding new packages to an existing virtual environment.

## Create installed package list
- We will first create a list of packages currently  installed
- pip freeze > installed_packages.txt

## Then we will create a list of packages to be installed
- new_packages.txt
```text
package1
package2
```

## Create python virtual env
```python
python3 -m venv tempEnv
source tempEnv/bin/activate
```

## First install  the installed packages in the virtual env
```python
pip install -r installed_packages.txt
```
- Make sure above package install goes well

## then install new_packages.txt
```python
pip install -r new_packages.txt
```