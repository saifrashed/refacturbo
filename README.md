```   ___      ___         __           __      
  / _ \___ / _/__ _____/ /___ ______/ /  ___ 
 / , _/ -_) _/ _ `/ __/ __/ // / __/ _ \/ _ \
/_/|_|\__/_/ \_,_/\__/\__/\_,_/_/ /_.__/\___/
```    


# Installation steps


1. Install Python 3.12
```bash
brew update
brew install python@3.12
```

2. Verify the installation
```bash
python3.12 --version
```

3. Create a virtual environment
```bash
python3.12 -m venv venv
```

4. Activate the virtual environment
```bash
source ./venv/bin/activate
```

# Execution

1. See version
```bash
./src/main.py --version
```

2. Install the required dependencies
```bash
./src/main.py --install
```

3. Run the following command
```bash
./src/main.py --refactor <absolute path to the project directory>
```

4. Run the Unit and Integration tests
```bash
./src/main.py --test
```