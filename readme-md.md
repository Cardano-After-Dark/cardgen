# Stability AI Image Generator

This application uses the Stability AI API to generate images based on text prompts.

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Setup

1. Clone the repository:
   ```
   git clone [your-repo-url]
   cd [your-repo-name]
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
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
   cd imgen
   pip install -r requirements.txt
   ```

## Running the Application

1. Ensure your virtual environment is activated.

2. Run the application:
   ```
   python stability_ai_image_generator.py
   ```

3. Enter your Stability AI API key when prompted.

4. Use the interface to set parameters and generate images.

## Project Structure

```
/
├── imgen/
│   ├── out/                 # Generated images
│   ├── requirements.txt     # Project dependencies
│   └── stability_ai_image_generator.py  # Main application
└── venv/                    # Virtual environment
```

## Note

Make sure to keep your API key confidential and never commit it to version control.
