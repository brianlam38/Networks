# networks_ass2
## Implementation
- 2017 UNSW COMP3331 Assignment 2 Implementation by Alex Nguyen and Brian Lam
## Structure
- helpers contains data structures used as part of routing performance
- docs contains data used to create report/program e.g. excel sheet (plots), project architecture
- ``report.pdf``` and main program, ```routing_performance.py```
- run tests in ```tests/``` by running the following in root dir: ```pip install -r requirements.txt && pytest```


## Run base assignment
- Use packet rate of 1
- SHP:
```
python -m routing_performance CIRCUIT SHP topology.txt workload.txt 1
```
- SDP:
```
python -m routing_performance CIRCUIT SDP topology.txt workload.txt 1
```
- LLP (broken atm):
```
python -m routing_performance CIRCUIT LLP topology.txt workload.txt 1
```
- Debug:
```
python -m pdb routing_performance.py CIRCUIT SDP topology.txt workload.txt 1
```

## How to add pathing algorithm
- add new function to ```pathing_algorithms.py```
- import new function in ```routing_performance.py``` line 3
- change line 36 of ```routing_performance.py``` to use new function instead of ```shortest_path```
- in ```VirtualConnection.fill_path``` check arguments are being used correctly in new function (```path_algorithm``` is your new algorithm function and is currently set to those of ```shortest_path``` - modify as needed)

## Git commands 
- Clone specific branch
```
git clone -b master (git url)
```
- Create new branch and push it on server side
```
git branch new_branch_name
git checkout new_branch_name
git push --set-upstream origin new_branch_name
```
- Merge changes from branch with another branch 
```
git checkout master
git pull origin other_branch_name
# alternatively, can use merge instead i think?
git push

```
- Oh-no, need to go back in time
```
git log
# pick commit hash number
git checkout hash_number
# you're now in detached head state, do below when you want to go back
git checkout ^HEAD
```
