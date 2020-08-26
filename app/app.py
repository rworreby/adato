import pandas as pd
from flask import Flask, render_template, redirect, url_for, request
from flair.data import Sentence
from flair.models import TextClassifier

app = Flask(__name__)

labeling_counter = 0
LABEL_CLASSES = {'1': 'World', '2': 'Sports', '3': 'Business', '4': 'Sci/Tech'}

path = './adato/data/'
train_df = pd.read_csv(
    path + 'remaining_cleaned_train.csv',
    header=0,
)

classifier = TextClassifier.load('adato/model/classifiers/flair/best-model.pt')


def save_label(index, label):
    train_df.loc[index, 'label'] = label
    train_df.to_csv(path + 'remaining_cleaned_train.csv', index=False)


@app.route('/')
def index():
    return redirect(url_for('label', number=labeling_counter))


@app.route('/label/')
@app.route('/label/<int:number>', methods=['POST', 'GET'])
def label(number=0):
    labeling_counter = int(number)

    sentence = Sentence(train_df.iloc[labeling_counter]['description'])
    classifier.predict(sentence)

    # Take the first element of the label/prediction of form "[3 0.9124]"
    # TODO: Fix to work with more than max 10 classes
    predicted_class = str(sentence.labels[0])[0]

    if request.method == 'POST':
        if request.form.get("accept_user"):
            print(f"Saving user input for document {labeling_counter} ...")
            print("Predicted: ", LABEL_CLASSES[predicted_class])

            if request.form.get("World"):
                print("Label World getting saved ...")

            return redirect(url_for('label', number=labeling_counter))
        elif request.form.get("accept_predicted"):
            print(f"Saving predicted input for document {labeling_counter} ...")
            print("Predicted: ", LABEL_CLASSES[predicted_class])

            save_label(labeling_counter, predicted_class)

            return redirect(url_for('label', number=labeling_counter))
        else:
            print("Neither pred nor user")
            return redirect(url_for('label', number=labeling_counter))

    elif request.method == 'GET':
        return render_template('label.html',
                               data=train_df.iloc[labeling_counter]['description'],
                               data_counter=labeling_counter,
                               label=LABEL_CLASSES[predicted_class],
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
