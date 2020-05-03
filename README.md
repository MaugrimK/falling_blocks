# Falling blocks

A python clone of tetris!

![](gameplay.gif)

## Launch the game
1. Clone the project
2. Create conda env
```bash
conda create -n <env_name> -c cogsci --file requirements.txt
conda activate <env_name>
```
3. Navigate to project dir
```bash
cd falling_blocks
```
4. Launch the game
```bash
set PYTHONPATH=.
python falling_blocks\launcher.py
```

## Run the tests
1. Install dev deps
```bash
conda install -c conda-forge --file dev-requirements.txt
```
2. Run tests
```bash
set PYTHONPATH=.
#prevent python from generating __pycache__files
set PYTHONDONTWRITEBYTECODE=1
#run tests
pytest tests
python falling_blocks\launcher.py
```
3. Run tests with coverage
```bash
pytest --cov=falling_blocks  tests
```
