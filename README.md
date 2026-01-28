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
**All file paths assume that the python files are run from the directory analysis.**  
**Note:** All generated plots will be saved in the `plots` directory, all videos in the `videos` directory, and all results in the `analysis/results` directory.  
  
To generate new results and compare static vs moving block in rollingstock (this takes 20 minutes) run:
```
python runExperimentsRollingStock.py
```
To generate new results that analyze how the variables influence the outcome (this takes 2 hours) run:
```
python variablesEffect.py 
```
To generate the graph from the rollingstock results run:
```
python graphRollingStock.py
```
to generate the graph that analyzes how the variables influence the outcome run:
```
python graphVariablesEffect.py
```
To generate the graph that compares the capacity per number of trains in moving and static block run:
```
python graphCapacityPerTrain.py
```
To generate results from our Oslo metro simulation and produce a graph comparing them to the reference run:
```
python graphOslo.py
```
To generate a demonstration video of our visualization run:
```
python demonstration.py
```
to generate a video from our Oslo metro simulation run:
```
python OsloDemonstration.py
```

## Known bugs

When creating a model with moving block signalling a single station with a length, the trains wait infinitely long at the station.


