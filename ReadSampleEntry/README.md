To run parallel production, use
```
python run_parallel_production.py [--era=ERA]
```
Do not run all of the ERA because the tmp memory will be full.

After run all of them, use following to produce final json file
```
python combine_json.py[--era=ERA]
```
