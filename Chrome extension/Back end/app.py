from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from transformers import AlbertTokenizerFast
import sys
import tensorflow as tf

app = Flask(__name__)
CORS(app, origins=["chrome-extension://gihbkgdhhghhiigocpdahmfllblebhfg"])

tokenizer = AlbertTokenizerFast.from_pretrained('albert-base-v2')
model = tf.saved_model.load('models/')


def encoder(tokenizer1, text):
    input_ids = []
    attention_mask = []
    inputs = tokenizer1(text,
                        max_length=128,
                        padding='max_length',
                        truncation=True,
                        return_attention_mask=True,
                        return_token_type_ids=False)
    input_ids.extend(inputs['input_ids'])
    attention_mask.extend(inputs['attention_mask'])
    return {
        'input_ids': tf.convert_to_tensor(input_ids),
        'attention_mask': tf.convert_to_tensor(attention_mask)
    }


@app.route('/classify', methods=['POST'])
def classify_text():
    request_data = request.get_json()
    sys.stdout.buffer.write(f"Received data: {request_data}\n".encode('utf-8'))
    data = [request_data['text']]
    inputs = encoder(tokenizer, data)
    tensor_list = [inputs['input_ids'], inputs['attention_mask']]
    output = model(tensor_list, training=False)
    is_spam = 'spam' if output[0][0] > 0.5 else 'not spam'
    return jsonify({'tweet': data, 'result': is_spam})


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
