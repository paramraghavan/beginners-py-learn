## What happens when pipenv install pkg in run in clean new folder
When you run pipenv install <package> in a clean, new folder (a directory that has no prior configuration or virtual
environment), Pipenv performs the following actions:

### 1. Creation of a Pipfile
- Pipenv generates a Pipfile in the project directory if one doesn't already exist.
- The Pipfile is a declarative file that replaces requirements.txt and serves as the list of dependencies for your
  project.
- The Pipfile contains two sections:
  - [packages]: Lists the standard dependencies your project needs.
  - [dev-packages]: Lists the development dependencies (if specified using pipenv install --dev).

For example, after running **pipenv install requests**, the Pipfile might look like this:

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"

[dev-packages]

[requires]
python_version = "3.12"

```

### 2. Creation of a Virtual Environment
- Pipenv will create an isolated virtual environment (if one doesn't exist) in a directory outside your project folder.
- The location of this virtual environment depends on your system. Pipenv uses `virtualenv` internally to create it. You
  can find the location using:
  ```bash
  pipenv --venv
  ```
This environment is where all the packages you install will be isolated from the global Python environment.

### 3. Installation of the Package
- Pipenv installs the specified package (and its dependencies) into the newly created virtual environment.
- You can specify a package version like this:

  ```bash
  pipenv install requests==2.25.1
  ```

### 4. Creation of a `Pipfile.lock`
- After installing a package, Pipenv generates a `Pipfile.lock` file. This file is used to ensure deterministic builds
  by locking the specific versions of your dependencies and their sub-dependencies.
- This ensures that if someone else installs your project or deploys it to another environment, they will install the
  same versions of all packages.

The `Pipfile.lock` might look like this:

```json
{
  "_meta": {
    "hash": {
      "sha256": "b7f7f9d97b4987b606a5b9d4..."
    },
    "pipfile-spec": 6,
    "requires": {
      "python_version": "3.12"
    }
  },
  "default": {
    "requests": {
      "version": "==2.25.1",
      "hashes": [
        "sha256:..."
      ]
    }
  },
  "develop": {}
}
```

### 5. Virtual Environment Activation Instructions
- If you want to work inside the newly created virtual environment, you will need to activate it using:

  ```bash
  pipenv shell
  ```
### 6.  Specifying a Python Version

If you explicitly create a virtual environment by specifying a Python version with the --python flag, Pipenv will create
the environment immediately:
```bash
pipenv --python 3.x
```
Above command creates a virtual environment with the specified version of Python and generates a Pipfile.


### 7. When to Use the dev Section

The dev section is typically used to install tools that aid development, such as testing frameworks, linters, or
debugging tools. These dependencies are only relevant while you're writing and testing code, but they're not required
when the project is deployed or used in production.

You can install a package as a development dependency by using the --dev flag when running pipenv install. For example:
```bash
// Install pytest (a testing framework) in the virtual environment.
// Add pytest to the [dev-packages] section of the Pipfile.
pipenv install pytest --dev
```
Here's how the pipfile looks like with dev section
- The requests package is a regular dependency (used in both development and production).
- The pytest package is listed under [dev-packages], meaning it's only required during development.
```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"

[dev-packages]
pytest = "*"

[requires]
python_version = "3.8"

```

**Installing Dev Dependencies**
This will install all the packages listed under both [packages] and [dev-packages] into your virtual environment.
```shell
pipenv install --dev

```

**Installing Only Production Dependencies**
```shell
# --ignore-pipfile — Install from the Pipfile.lock and completely ignore Pipfile information.
# --deploy — Verifies the _meta hash of the lock file is up to date with the ``Pipfile``, aborts install if not.
#            makes sure Pipfile and Pipfile.lock are in sync
pipenv install --ignore-pipfile --deploy
# or
pipenv install 
```

**Removing Dev Dependencies from virtualenv**
```shell
# pipenv uninstall <package> --dev
pipenv uninstall pytest --dev
```

## How to Use the `--categories` Option

In Pipenv, the `--categories` option allows you to organize your dependencies into different sections or categories,
besides just "default" (for production) and "dev" (for development). This feature is particularly useful when you need
to further group dependencies beyond these two basic categories, for example, grouping by testing, documentation, or
specific environments.

When installing packages with `pipenv install`, you can assign a package to a custom category by using
the `--categories` flag. For example:

```bash
pipenv install package_name --categories test
```
This command will:
- Install the package.
- Add the package under a `[test]` section in the `Pipfile`.

### Example Usage

#### Install a Package in a Custom Category
Suppose you want to install `pytest` in a custom category for testing tools:

```bash
pipenv install pytest --categories test
```

This will create a new `[test]` section in your `Pipfile`:

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"

[test]
pytest = "*"

[requires]
python_version = "3.12"
```

Here, `pytest` is assigned to a custom `test` category instead of the usual `[dev-packages]`.

### Installing Packages from a Specific Category

Once you have defined categories, you can choose to install only the packages from a specific category by using
the `--categories` flag when running the install command.

For example, if you want to install only the dependencies from the `test` category:

```bash
pipenv install --categories test
```

### Organizing Multiple Categories

You can create as many categories as you need. For instance, you could have categories like `[test]`, `[docs]`, `[ci]`,
and so on. Each category is a section in your `Pipfile`.

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"

[test]
pytest = "*"

[docs]
sphinx = "*"

[ci]
tox = "*"

[requires]
python_version = "3.12"
```

### When to Use `--categories`

This feature is useful in larger projects or when managing dependencies for different environments, such as:
- **Testing environments:** You might want to have testing tools like `pytest` or `tox` in their own category.
- **Documentation dependencies:** You might keep documentation-related tools like `Sphinx` in a `[docs]` category.
- **Continuous integration (CI):** You might need specific tools for CI that you only want installed when working in
  that environment.

  
## My project already has Pipfile and Pipfile.lock
- Go to the folder with Pipfile and Pipfile.lock
- Installing pipenv
  - On windows --> pip install pipenv. 
  - On MacOS  with M1 chip/Arch -x86_64 use 
    - brew install pipenv or  a brew install pipenv
- To update/create the Pipfile.lock file
  - pipenv lock --clear --verbose 
  - pipenv update --clear --verbose or pipenv udapte --clear -vv
- pipenv install -e git+ssh://git@github.com/paramraghavan/test.git@v0.8.0#egg=test ← this will update the Pipfile
- Install what's in pipenv
  - pipenv install --dev --verbose ← this install the dev dependencies like pytest, pytest-mock etc
  - pipenv install --dev -vv
  - Note: On macbook with M1 chip , if above is giving trouble try
  - arch -x86_64 pipenv install --dev
  - ARCHFLAGS="-arch arm64" pipenv install xgboost="==0.80"
- pipenv --venv ← this gives you the virtual env folder location, for example /Users/praghavan/.local/share/virtualenvs/glue-a9kAnMxy
- pipenv install <package> This will create a Pipfile if one doesn't exist
- pipenv run pipenv_to_requirements -f , It will generate requirements.txt and, if applicable, requirements-dev.txt, in the current directory. ref: pipenv-to-requirements . Note you need to isntall pipenv_to_requirements package - pip install pipenv-to-requiremen
- **Macbook M1 problem try**: arch -x86_64 pip install pandas ← run pip command under x86_emulation but the terminal stays in the native arm environment.

**To update/create the Pipfile.lock file**
- pipenv lock --clear --verbose 
- pipenv update --clear --verbose or pipenv udapte --clear -vv

**Install whats in pipenv**
- pipenv install --dev --verbose ← this install the dev dependencies like pytest, pytest-mock etc
- pipenv intall --dev -vv

**To see the installed packages**
- pipenv graph

**generate requirements.txt**
- pip install pipenv-to-requirements # one time 
- pipenv run pipenv_to_requirements -f # create 2 files
  - requirements-dev.txt 
  - requirements.txt 
**pipenv use requirements.txt**
 - pipenv install -r requirements.txt

** activate/remove venv**
- pipenv shell  ← activates  virtualenv; This will create a virtual environment if one doesn’t already exist.
- pipenv --rm - removes virtual environment
- pipenv install <package> This will create a Pipfile if one doesn't exist
- 
**pipenv and pytest**
* pipenv run pytest -vv test/ or pipenv run pytest --trace -vv test/ 
* pipenv run list freeze
* pipenv graph
* pipenv lock -r > requirements.txt
* pipenv install --dev --verbose

**Error's related to mac-book M1 chip**
* pipenv lock hangs
    * On mac, do something like 'find ~/Library/Caches/pipenv/http | grep lock, and delete this *.lock  file, this may help or try deleting the cache folder under pipenv
    * arch -x86_64 pipenv install --dev
    * another option to try is to  install with arch -x86_64 pip install pipenv, we gave this a try it did not help with running pipenv install
 
**Note the Python version picked up by Pipenv file and Apple M1**
Not sure if my assessment is correct, here is my observation and what i did

* Upgraded pyspark version from 3.1.1 to 3.1.3
* Ran pipenv install --dev, observed the result, I have python 3.9.x installed in my path. pipenv automatically picked
  up 3.8.9 from MacOs path /usr/bin/python3 → Python 3.8.9 and this was giving problem with cryptography library, looked
  like the Apple M1 chip
* Pipenv checks for the python version dependency in the Pipfile and in this case dependency is on version 3.8, it looks
  up for 3.8 version installed in our dev setup. brew install python@3.8 installed python 3.8.13 which resolved this
  problem. When i updated it to python version 3.9, this problem was resolved
* actual error
  > from cryptography import utils from cryptography.hazmat.bindings._rust import x509 as rust_x509> ImportError:
  dlopen(
  /Users/praghavan/.local/share/virtualenvs/data-privacy-Y5bDKn9V/lib/python3.8/site-packages/cryptography/hazmat/bindings/_
  rust.abi3.so, 0x0002): tried: '
  /Users/praghavan/.local/share/virtualenvs/data-privacy-Y5bDKn9V/lib/python3.8/site-packages/cryptography/hazmat/bindings/_
  rust.abi3.so' (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64e')), '/usr/local/lib/_
  rust.abi3.so' (no such file), '/usr/lib/_rust.abi3.so' (no such file)   Installed step → brew install python@3.8.
  Pipenv is picking using this version of python -/opt/homebrew/bin/python3.8 and this seem to work with any of the
  errors listed above. Python 3.8.13 got installed.
* following error running - pipenv lock --clear --verbose
    * pipenv.exceptions.ResolutionFailure: ERROR: pip subprocess to install build dependencies exited with 1 ✘ Locking
      Failed!
    * fix:
        * pipenv install --skip-lock --dev --verbose

**Build server uses “https://github.com" and our dev pc’s use “ssh://git@github.com”**  
[url "ssh://git@github.com/"]
insteadOf = https://github.com/
  
