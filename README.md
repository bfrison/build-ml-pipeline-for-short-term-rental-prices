# Weights and Biases link:
[nyc\_airbnb](https://wandb.ai/bfrison/nyc_airbnb)
# Instructions:  
## Environment:
To run the scripts in this repository, you will need to use the `mlflow` Python library. Version 2.9.2 was used during development.  
For the steps within the pipeline, all Python libraries are specified in the steps' respective `conda.yml` and will automatically be installed by `mlflow`.
## Execution:
To execute the pipeline, execute the following line in a bash console:
```bash
mlflow run <path_to_git_root>
```
To execute only some of the steps, execute the following line:
```bash
mlflow run . -P steps=<comma_separated_list_of_steps>
```
Be sure to not insert any whitespace between the steps, only a comma. The name of the steps are as follows:
- download
- basic\_cleaning
- data\_check
- data\_split
- train\_random\_forest
- test\_regression\_model
