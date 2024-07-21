# cardgen

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Setup CLI

Do the following on the command line only, before opening VSCode

1. Clone the repository:
   ```
   git clone git@github.com:Cardano-After-Dark/cardgen.git
   cd cardgen
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:``
   - Windows:
     ```
     .\venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
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

``` bash
python -m venv venv
source venv/bin/activate
pip install requirements.txt
```



