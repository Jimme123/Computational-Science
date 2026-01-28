## Usage

Create and enter a virtual environment
```
python -m venv venv
source venv/bin/activate
```
Then install the packages
```
pip install -r requirements.txt
```

## Files
To generate new results and compare static- vs moving block (this takes 20 minutes) run:
```
python analysis/runExperimentsRollingStock.py
```

## Known bugs

When creating a model with moving block signalling a single station with a length, the trains wait infinitely long at the station.

