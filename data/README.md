# Instruction to read the sample JSON file:
e.g https://github.com/ExtraYukawa/Script_ForMVA/blob/main/data/sample_2017UL.json

- The first line:
```
"DYnlo":   [6077.22,  1, "DY",        632,  0],
```
| DYnlo         | 6077.22            | 1      | DY               | 632                        | 0                                             |   
| ------------- | -------------      | ---    | -------------    | -------------------------- | -------------------------------------------   |
| Process       | cross-section (pb) | 0: MC  | Category for bkg | NO to plot(not useful here)|  0: not used for training(but for application)|
|               | 1 for data         | 1: data|                  |                            |  1: used for training and application         |
|               |                    |        |                  |                            | -1: NOT used for training and application     |


