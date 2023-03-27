from flask import Flask, request, render_template, url_for, redirect
import pickle
import string
import random

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load the serialized vectorizer and NLP model
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('model.pkl', 'rb') as f:
    nlp_model = pickle.load(f)


def process_text(text):
    # Convert to lowercase
    text = text.lower()

    # Replace newlines and carriage returns with spaces
    text = text.replace('\n', ' ').replace('\r', ' ')

    # Replace punctuation with spaces
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Split text into tokens
    tokens = text.split()

    # Remove stop words
    stop_words = set(['a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'on', 'at', 'to', 'from', 'by', 'so', 'not'])
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Join filtered tokens into a string
    filtered_text = ' '.join(filtered_tokens)

    return filtered_text


# Define a route to handle incoming requests
# @app.route('/')
# def home():
#     return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the text from the request
        text = request.form.get('headline')
        text = process_text(text)

        # Preprocess the text with the loaded vectorizer
        vectorized_text = vectorizer.transform([text])

        # Use the preprocessed text as input to the NLP model
        prediction = nlp_model.predict(vectorized_text)
        prediction_str = str(prediction[0])

        cache_buster = random.randint(1, 1000000)
        print(type(prediction_str))
        if prediction_str == "1":
            prediction_text = "DON'T TAKE IT SERIOUSLY BECAUSE IT IS A SARCASTIC HEADLINE!"
        else:
            prediction_text = "UPSS ! NO SARCASM HERE."

        # return redirect(url_for('result', prediction=prediction_text, cache_buster=cache_buster, _=random.random()))
        return render_template('res.html', prediction=prediction_text, css_url=url_for('static', filename='style.css'))



    else:
        return render_template('index.html', css_url=url_for('static', filename='style.css'))


# @app.route('/result')
# def result():
#     prediction_text = request.args.get('prediction', '')
#     cache_buster = request.args.get('cache_buster', '')
#     return render_template('res.html', prediction=prediction_text, cache_buster=cache_buster)



if __name__ == '__main__':
    app.run(debug=True)