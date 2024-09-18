from flask import Flask, render_template,request,jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()  # Get the JSON data from the POST request
    score_w = data.get('score_w')
    score_b = data.get('score_b')

    if score_w and score_b:
        # Do something with the color and piece, for example, print them
        print(f"score:{score_w},score:{score_b}")
        return jsonify({'status': 'success', 'message': f"score_b:{score_b} score_w:{score_w}"})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid data'})

if __name__ == '__main__':
    app.run(debug=True)