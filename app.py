from flask import Flask, render_template, url_for, jsonify, request
# import translate, sentiment, synthesize
#import final
import test

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def translate_text():
    data = request.get_json()
    file_url = data['url']
    num_fields = data['field']
    num_neigbour = data['neigbour']
    print(file_url, num_fields, num_neigbour)
    response = test.KNN(file_url, int(num_fields), int(num_neigbour))
    print(response)
    return jsonify(response)


if __name__ == '__main__':
	app.run(host='0.0.0.0')