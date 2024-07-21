# Requirements

Stability.ai official documentation provide a google colab file that I use to generate imaged using their AI apis. The code for their apis is visible in the fours snippets below, which are used a base:

This is to define imports

```
#@title Install requirements
from io import BytesIO
import IPython
import json
import os
from PIL import Image
import requests
import time
from google.colab import output
```

This is to prompt the user to provide his api key, but in my program I will read the api key from a properties file.

```
#@title Connect to the Stability API

import getpass
# @markdown To get your API key visit https://platform.stability.ai/account/keys
STABILITY_KEY = getpass.getpass('Enter your API Key')
```

This snippet provides a set of functions needed to query the APIs

```
#@title Define functions

def send_generation_request(
    host,
    params,
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    # Encode parameters
    files = {}
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = open(image, 'rb')
    if mask is not None and mask != '':
        files["mask"] = open(mask, 'rb')
    if len(files)==0:
        files["none"] = ''

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response

def send_async_generation_request(
    host,
    params,
):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    # Encode parameters
    files = {}
    if "image" in params:
        image = params.pop("image")
        files = {"image": open(image, 'rb')}

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    # Process async response
    response_dict = json.loads(response.text)
    generation_id = response_dict.get("id", None)
    assert generation_id is not None, "Expected id in response"

    # Loop until result or timeout
    timeout = int(os.getenv("WORKER_TIMEOUT", 500))
    start = time.time()
    status_code = 202
    while status_code == 202:
        response = requests.get(
            f"{host}/result/{generation_id}",
            headers={
                **headers,
                "Accept": "image/*"
            },
        )

        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        status_code = response.status_code
        time.sleep(10)
        if time.time() - start > timeout:
            raise Exception(f"Timeout after {timeout} seconds")

    return response
```

This last snippet prompts the user to provide a few parameters for the image generation, and when executed it calls the generation APIs

```
#@title Stable Image Core

prompt = "Four-panel image divided into four sections. Each panel contains a stylized poker card face: Jack. Classic playing card style. High contrast, vibrant colors." #@param {type:"string"}
negative_prompt = "" #@param {type:"string"}
aspect_ratio = "2:3" #@param ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]
seed = 0 #@param {type:"integer"}
output_format = "png" #@param ["webp", "jpeg", "png"]

host = f"https://api.stability.ai/v2beta/stable-image/generate/core"

params = {
    "prompt" : prompt,
    "negative_prompt" : negative_prompt,
    "aspect_ratio" : aspect_ratio,
    "seed" : seed,
    "output_format": output_format
}

response = send_generation_request(
    host,
    params
)

# Decode response
output_image = response.content
finish_reason = response.headers.get("finish-reason")
seed = response.headers.get("seed")

# Check for NSFW classification
if finish_reason == 'CONTENT_FILTERED':
    raise Warning("Generation failed NSFW classifier")

# Save and display result
generated = f"generated_{seed}.{output_format}"
with open(generated, "wb") as f:
    f.write(output_image)
print(f"Saved image {generated}")

output.no_vertical_scroll()
print("Result image:")
IPython.display.display(Image.open(generated))
```

Using the above snippet as an example of how to successfully query the APIs, I want to write a python program with the following specifications: 

The program should start a GUI to enable the user to enter the data needed to query the APIs. 

The program should have the classes below

- GenIO : 
    - a class containing 
        - (mandatory) the image generation parameters: 
            - prompt: a string representing the positive generation input, with default=""
            - negative_prompt: a string representing the negative generation prompt, with default=""
            - aspect_ratio: one of these values ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"], with default="2:3"
            - seed: a number used to seed the generation, with default="0"
            - output_format: one of these values ["webp", "jpeg", "png"], with default="png"
            - gen_result: string response from the server, default = ""
        - (optional) the generation output 
            - gen_image: the image generated if generation was successful.
	- the GenIO can save the data as a set of two files
        - <prefix>_params.json (mandatory) : a json file containing the generation parameters and the gen_result if generation was executed
        - <prefix>_img.<ext> (optional) : the image file generated, where the extension is defined by output_format, if generation was executed successfully
    - the GenIO can be instantiated by loading a set of two files <prefix>_params.json (mandatory) and <prefix>_img.<ext> (optional)
        - <prefix>_params.json : must exist, and from this file we can instantiate a GenIO with all the parameters except for the image
        - <prefix>_img.<ext> : if the <prefix>_params.json exists, we can search for the <prefix>_img.<ext> file. If the file exists, the gen_image can be loaded, stored into the GenIO instance.
	- the GenIO should have a save(folder , prefix) method to save the two files described above based on two parameters
		- folder: the base folder where the output files should be saved 
		- prefix: the common part of the filename between json textual file output and image output
	- the GenIO should have a load (folder, prefix) method which loads two files (where the <prefix>_params.json is mandatory, and <prefix>_image.<ext> is optional) based on parameters and instantiate a new GenIO object, which contains the parameters and the image file (only if the image file is present)
- ImgGenUI: a class that constructs the UI in three rows: 
	- row 1 (header): Panel with a label "Stability.ai generation with Stable Image Core" 
	- row 2 (input): a grid with labels and input fields for the generation parameters 
            - prompt: text representing the positive generation input, with default=""
            - negative_prompt: text representing the negative generation prompt, with default=""
            - aspect_ratio: dropdown with these values ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"], with default="2:3"
            - seed:  number used to seed the generation, with default="0"
            - output_format: dropdown with these values ["webp", "jpeg", "png"], with default="png"
	- row 3 (ui actions): a panel with two buttons "Reset" to reset all the input, "Generate" to request generation, 
	- row 4 (persistence): a panel with two buttons 
		- "Folder" to select the output folder where to save the data. The folder path stored should be relative to the main python script. Default value is `./out` (relative to the python script)
        - "Prefix" to give a prefix to be used to save the GenIO files
		- "Save" : saves the GenIO object using GenIO.save(folder, prefix). If there is a duplication for the file <prefix>_params.json, a popup should appear to ask if you want to overwrite. Yes/No
        - "Load" : loads the GenIO object using GenIO.load(folder, prefix). If the load is successful, the data in the input fields and the image are replaced with the new data loaded
	- row 5 (output): a UI component to display the generated image once the generation is complete
- StabilityAIClient : a class containing all the functions needed to invoke the generation, as provided by the stability.ai snippets
- PropertiesIO : a class that I already wrote, containing a method called get_property( string name ) to get the value of the API key
- StabilityImGen : the main application that does the following: 
	- get the ApiKey as follows `props = PropertiesIO('cardgen.properties')` and then `api_key = props.get_property('stability.ai.api.key')`
	- Load the latest GenIO data using GenIO.load(".imgen", "latest_genio") if exists, or creates a new one with defaults, used as current genIO
	- Open the ImgGenUI, and fills the current genIO parameters with the data in the GenIO instance. Also, if the image exists, the image should be displayed in the row 5 in the UI.
	- when closing, the application automatically saves stores the current genIO files using GenIO.save(".imgen", "latest_genio")

Please, Note: 

The project output structure should be as seen below. Make sure the python files names are matching: 
```
/
├── imgen/ # contains all the classes
│ ├── out/ # Generated images default out folder
│ ├── requirements.txt # Project dependencies
│ ├── properties_io.py # properties utility class
│ ├── gen_io.py # imgen parameters and output to persist
│ ├── img_gen_ui.py # UI for the main application
│ ├── stability_ai_client.py # needed to invoke generation
│ └── stability_imgen.py # Main application
└── venv/ # Virtual environment
```
Make sure the written code is minimal. 



