- Go to the folder with Pipfile and Pipfile.lock
- pip install pipenv. On MacOS  with M1 chip use brew install pipenv or  arch -x86_64 brew install pipenv
- To update/create the Pipfile.lock file
  - pipenv lock --clear --verbose 
  - pipenv update --clear --verbose or pipenv udapte --clear -vv
- pipenv install -e git+ssh://git@github.com/paramraghavan/test.git@v0.8.0#egg=test ← this will update the Pipfile
- Install whats in pipenv
  - pipenv install --dev --verbose ← this install the dev dependencies like pytest, pytest-mock etc
  - pipenv intall --dev -vv
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
Not sure if my assessment  is correct, here is my observation and what i did
* Upgraded pyspark version from 3.1.1 to 3.1.3
* Ran pipenv install --dev, observed the result, I have python 3.9.x installed in my path. pipenv automatically picked up 3.8.9 from MacOs  path /usr/bin/python3 → Python 3.8.9 and this was giving problem with cryptography library, looked like the Apple M1 chip
* Pipenv checks for the python version dependency in the Pipfile and  in this case dependency is on version 3.8, it looks up for 3.8 version installed in our dev setup.  brew install python@3.8 installed python 3.8.13 which resolved this problem. When i updated it to python version 3.9, this problem was resolved 
* actual error
    > from cryptography import utils       from cryptography.hazmat.bindings._rust import x509 as rust_x509> ImportError: dlopen(/Users/praghavan/.local/share/virtualenvs/data-privacy-Y5bDKn9V/lib/python3.8/site-packages/cryptography/hazmat/bindings/_rust.abi3.so, 0x0002): tried: '/Users/praghavan/.local/share/virtualenvs/data-privacy-Y5bDKn9V/lib/python3.8/site-packages/cryptography/hazmat/bindings/_rust.abi3.so' (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64e')), '/usr/local/lib/_rust.abi3.so' (no such file), '/usr/lib/_rust.abi3.so' (no such file)   
 Installed step → brew install python@3.8. Pipenv is picking using this version of python -/opt/homebrew/bin/python3.8 and this seem to work with any of the errors listed above. Python 3.8.13 got installed.
* following error running - pipenv lock --clear --verbose
    * pipenv.exceptions.ResolutionFailure: ERROR: pip subprocess to install build dependencies exited with 1 ✘ Locking Failed!
    * fix: 
        * pipenv install --skip-lock --dev --verbose
     
**Build server uses “https://github.com" and our dev pc’s  use “ssh://git@github.com”**  
[url "ssh://git@github.com/"]
	insteadOf = https://github.com/
  
