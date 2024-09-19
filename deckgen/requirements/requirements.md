# DeckGen

I'm building a Python application to generate a deck of cards. 

I have prototypes of a CLI app and a GUI app. 
- CLI  [imedit-prototype.py](../imedit-prototype.py)
- GUI  [deckgen-prototype.py](../deckgen-prototype.py)

The CLI can generate images providing the parameters are correct
The GUI can collect the parameters, save them as a json, and send input to the CLI. 

See below an example of the json that the GUI app can create, and that the CLI app should use as input:

{
  "input_folder": "assets/input1",
  "output_folder": "out/deck1",
  "prefix_string": "poker_card",
  "app_params": {
    "Design": {
      "Preview index": 42,
      "Outer border": 10,
      "Inner border": 400
    }
  }
}

Now, I would like to create the actual application, using the CLI and the GUI as base.

The Application should have two classes / files:


- DeckGen: python class based on imedit, which can generate a deck of cards.
- DeckGenApp: GUI that can use DeckGen. This App is based on deckgen-prototype.

Below are some details on the implementation of the two classes

DeckGen
- should still work as a command line application using default parameters. See json input file for the default parameters
- shuold also work as a class with a workflow like this.
```python
deckgen = new DeckGen()
deckgen.loadParams(parameters) #loads the parameters into the class
deckgen.generate_deck() # execute generation writing the generated files (based on generate_cards)
deckgen.preview_card(card_number) #executes preview: returns a single card image, as a python object. The image generated is specified by the "preview index" number in the input parameters. If no preview intex is specified, it generates the card at index 0 (based on generate_card_image with card_count as input)
```

DeckGenGui
- shuold keep an instance of deckgen 
- should be able to load parameters to deckGen when the input is changed
- should be able to log generation errors on the log_text 
- should be able to show a preview: when executing preview, it should take the generated image and put it in the preview_window
- should be able to execute the full generation using the input parameters.
DeckGen should still work as a command line application using default parameters
DeckGen should also work as a class:
- instantiated by passing the parameters resulting from loading the above json
- executing the generation by invoking a method generate_cards()


Can you write for me the DeckGen and DeckGenGui, making sure to preserve existing code and comments, and minimize the changes w.r.t. the code present in the protptypes