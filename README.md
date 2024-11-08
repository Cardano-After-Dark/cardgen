# cardgen

## Prerequisites

- Python 3.7+ with pip

## Applications

This repository contains two main applications: 

### deckgen
Python application to generate a deck of cards. You can run it as follows:
```bash
cd deckgen
python deckgen_gui.py
```
### imgen
Python application to generate and save images using stability.ai apis
```bash
cd imgen
python stability_imgen.py
```
To use imgen, you need to rename the stability.ai.properties.example by adding your apy key and removing the example prefix

## Setup

 - Clone the repository and enter the repo
   ```
   git clone git@github.com:Cardano-After-Dark/cardgen.git
   cd cardgen
   ```

 - Create a virtual environment:
   After cloning, you need create the venv at least once
   ```bash
   python -m venv venv
   ```

 - Activate the virtual environment:
   Every time you want to run the app, you first need to activate the venv
   - Windows:
     ```
     .\venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

 - Install dependencies:
   In a new, activated venv, you migh want to install the needed dependencies
   ```
   pip install -r requirements.txt
   ```

## Configure VSCode

1. Open the project in VSCode
2. Use the command Palette (Ctrl+Shift+P or Cmd+Shift+P on macOS)
3. Select "Python: Select Interpreter"
4. Choose the interpreter from the local `venv` folder

## Run the Application

1. Ensure your virtual environment is activated.

2. Run the application:
   ```
   python stability-ai-image-generator.py
   ```

3. Enter your Stability AI API key when prompted.

4. Use the interface to set parameters and generate images.

## Project Structure

```
/
├── imgen/
│   ├── out/                 # Generated images default out folder
│   ├── requirements.txt     # Project dependencies
│   └── stability_ai_image_generator.py  # Main application
└── venv/                    # Virtual environment
```

## Note

You can find your API key at: https://platform.stability.ai/account/keys
Make sure to keep your API key confidential and never commit it to version control.


## Additional VSCode Setup tips

1. Select the correct python interpreter: 
    - Open the command Palette (Ctrl+Shift+P or Cmd+Shift+P on macOS)
    - Type "Python: Select Interpreter" and choose this option
    - Select the interpreter from your 'venv' folder
2. Use the provided launch configuration
    - That was created Via Run and Debug view (Ctrl+Shift+D or Cmd+Shift+D on macOS)
    - A "launch.json" file was created for Python
    - A Python debug configuration was added
    - The application can be run using F5 or via Run and Debug view, clicking on the green Play button

## Project setup

If you have nixos, you need to : 
```
nix-env -iA nixpkgs.python312
nix-env -iA nixpkgs.python312Packages.virtualenv
```

For macOS, Windows, and Linux, just install Python 3.12

When python is installed execute these three commands from the root directory

``` bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```



