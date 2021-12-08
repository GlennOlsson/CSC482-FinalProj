## Run
First install the packages. If you have `pipenv` installed, this can be done using `pipenv install` inside the `code` directory. Otherwise, simply use `pip` through `pip3 install -r requirements.txt`.

You must also install `en_core_web_sm` and `en_core_web_lg` through `spacy`. This can be done with

```
pipenv run python3 -m spacy download en_core_web_lg
pipenv run python3 -m spacy download en_core_web_sm
```
if you are using `pipenv` or
```
python3 -m spacy download en_core_web_lg
python3 -m spacy download en_core_web_sm
```
if you are not.

To run the program, use the command `pipenv run python3 -m proj2_src` or `python3 -m proj2_src`

### Graphical representation
To be able to generate the graphical representation of the output tree you will need [Graphviz](https://www.graphviz.org/download/) installed. This can for instance be installed on mac through homebrew using `brew install graphviz`. 

If you don't have graphviz installed and in your path, you will simply only generate a GEDCOM file and a .dot (Graphviz file format) file, and these can be used to represent the tree using for instance your favourite website

## Testing
To run the test suit, in root directory run `pipenv run python3 -m unittest tests/*test.py`

## Typing
Typing is somewhat enforced. Run type checking with `pipenv run python3 -m mypy .`

