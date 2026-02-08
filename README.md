<figure style="margin: 2rem 0; text-align: center;">
  <img src="https://www.saifrashed.com/assets/refacturbo/cover.jpg" alt="Refacturbo banner" style="max-width: 100%; height: auto; border-radius: 8px;" />
</figure>


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
