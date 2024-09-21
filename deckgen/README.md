# Deckgen

## Project set up

- Clone and enter the project. 
```bash
git clone git@github.com:Cardano-After-Dark/cardgen.git 
cd cardgen
```
- Create/Activate venv
```bash
python -m venv venv # only the first time 
source venv/bin/activate # every with a new shell
```
- install requirements
```
pip install -r deckgen/requirements.txt
```
- run the application
```
python deckgen/deckgen_gui.py
```
- Deactivate venv
```bash
deactivate # when closing your session
```