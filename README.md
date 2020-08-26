[![rworreby](https://img.shields.io/circleci/build/github/rworreby/adato/master?token=b6b05407d76bbca4058ee1ce14674cb0e01e72c3)](https://circleci.com/gh/rworreby/adato)
# adato
Allpurpose Document Annotation Tool for Active Learning

## Usage

### Installation

```bash
# Create your virtual environment and activate it
$ python3 -m venv venv
$ source venv/bin/activate

# Update pip and Install dependencies
$ pip install --upgrade pip
$ pip install -r requirements.txt

# Install the package (adato)
$ pip install -e .
```

### Run the preprocessing and split data

```bash
$ python adato/clean_data.py

# You can provide a split argument to split the training (labeled) data
# from the unlabaled data
$ python adato/clean_data.py -s 500
```

### Train a classifier

```bash
# Run the main program
$ python adato

# Hyperparameter finetuning (hyperopt) can be toggled with a CL argument
$ python adato -ft
```

### Start the labeling webapp

```bash
$ python app/app.py
```
