## Run
Run with command `pipenv run python3 -m proj2_src` or `python3 -m proj2_src` if you are not using virtual environment

### Graphical representation
To be able to generate the graphical representation of the output tree you will need [Graphviz](https://www.graphviz.org/download/) installed. This can for instance be installed on mac through homebrew using `brew install graphviz`. 

If you don't have graphviz installed and in your path, you will simply only generate a GEDCOM file and a .dot (Graphviz file format) file, and these can be used to represent the tree using for instance your favourite website

## Testing
To run the test suit, in root directory run `pipenv run python3 -m unittest tests/*test.py`
## Typing
Typing is somewhat enforced. Run type checking with `pipenv run python3 -m mypy .`

