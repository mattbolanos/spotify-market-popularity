
<img src="assets/spotify_icon.png" width="75" height="75" align="right">

# Spotify Track Popularity by Market Analysis


Predicting popularity of a given track in a given Spotify market from its audio features in the Spotify API.

*Student Milestone II project for the Applied Data Science Master's program at the University of Michigan.*

## Developer Notes
#### Poetry
This project uses [Poetry](https://python-poetry.org/) for dependency management. To install Poetry, run the following command in your terminal:
```
pip install poetry
```
To install the project dependencies, run the following command in the project root directory:
```
poetry install
```
To open a shell with the project dependencies installed, run the following command in the project root directory:
```
poetry shell
```
Once the above steps are followed, you should be able to select the poetry shell as the kernel in a Jupyter Notebook.

#### Organization
- Develop in the `src/proto` directory
    - We can move around files later
- The raw JSON data is in `data`
    - see `src/proto/dev_feature_eng.ipynb` for an example of how to load the data as pandas dataframes
#### Pushing Code w/ Pre-Commit
To install pre-commit, run the following command in your terminal:
```
pip install pre-commit
```
To install the pre-commit hooks, run the following command in the project root directory:
**Note: You must be in the poetry shell to install the pre-commit hooks**
```
pre-commit install
```
If you are ready to commit/push code, stage the changes and run the following command in the project root directory:
```
pre-commit run --all-files
```
This will run the pre-commit hooks on all files that have been staged. If any of the hooks fail, further changes will be applied and will need to be recomitted.
