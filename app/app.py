import pandas as pd
from flask import Flask, render_template, redirect, url_for
from flair.data import Sentence
from flair.models import TextClassifier

app = Flask(__name__)

labeling_counter = 0
LABEL_CLASSES = {'1': 'World', '2': 'Sports', '3': 'Business', '4': 'Sci/Tech'}

path = './adato/data/'
train_df = pd.read_csv(
    path + 'cleaned_train.csv',
    header=0,
    names=['classid', 'title', 'description'],
)

classifier = TextClassifier.load('adato/model/classifiers/flair/best-model.pt')


@app.route('/')
def index():
    return redirect(url_for('label', number=labeling_counter))


@app.route('/label/')
@app.route('/label/<number>')
def label(number=0):
    labeling_counter = int(number)

    sentence = Sentence(train_df.iloc[labeling_counter]['description'])
    classifier.predict(sentence)

    return render_template('label.html',
                           data=train_df.iloc[labeling_counter]['description'],
                           data_counter=labeling_counter,
                           label=LABEL_CLASSES[str(sentence.labels[0])[0]],
                           labels=LABEL_CLASSES,
                           )


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/config')
def config():
    return render_template('config.html')


if __name__ == '__main__':
    app.run(debug=True)
