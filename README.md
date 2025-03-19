# WOM Clan Player Updater

1. Install Git
2. Install Python 3.5+ (`py -V` to check installed version)
3. **Optional** (Use `py -m venv .venv` to create a virtual environment **after** cloning down the repository and moving to it.)


`git clone https://github.com/SaltisRS/ironclad.git "target_folder"` (Fetch Code, from github)

`cd "target_folder` (Move to target directory)

`pip install -r requirements.exe` (Install dependencies)

(**Optional** if using venv first run `.venv/Scripts/activate`)

`py src/main.py` (Run Script)

(**Optional** if using venv, must be in active environment `.venv/Scripts/activate`)

**Running** `setup.bat` enables the script as a headless background service on startup. Alongside creating a python VENV.