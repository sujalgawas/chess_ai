from flask import Flask, render_template,request,jsonify
import numpy as np 

app = Flask(__name__)

def min_max(current_stats):
    PST_white = {
    'opening': np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],        # Rank 8
        [5, 5, 5, 5, 5, 5, 5, 5],        # Rank 7
        [1, 1, 2, 3, 3, 2, 1, 1],        # Rank 6
        [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],  # Rank 5
        [0, 0, 0, 2, 2, 0, 0, 0],        # Rank 4
        [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],  # Rank 3
        [0.5, 1, 1, -2, -2, 1, 1, 0.5],  # Rank 2
        [0, 0, 0, 0, 0, 0, 0, 0]         # Rank 1
    ]),
    'middlegame': np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],        # Rank 8
        [5, 5, 5, 5, 5, 5, 5, 5],        # Rank 7
        [1, 1, 2, 3, 3, 2, 1, 1],        # Rank 6
        [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],  # Rank 5
        [0, 0, 0, 3, 3, 0, 0, 0],        # Rank 4
        [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],  # Rank 3
        [0.5, 1, 1, -2, -2, 1, 1, 0.5],  # Rank 2
        [0, 0, 0, 0, 0, 0, 0, 0]         # Rank 1
    ]),
    'endgame': np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],        # Rank 8
        [10, 10, 10, 10, 10, 10, 10, 10],  # Rank 7
        [10, 10, 10, 10, 10, 10, 10, 10],  # Rank 6
        [10, 10, 10, 10, 10, 10, 10, 10],  # Rank 5
        [10, 10, 10, 10, 10, 10, 10, 10],  # Rank 4
        [10, 10, 10, 10, 10, 10, 10, 10],  # Rank 3
        [10, 10, 10, 10, 10, 10, 10, 10],  # Rank 2
        [0, 0, 0, 0, 0, 0, 0, 0]         # Rank 1
    ])
    }
    PST_black = {}
    # Loop over each game phase and reverse the ranks
    for phase, table in PST_white.items():
        PST_white[phase] = table[::-1]
    
    white_co,black_co = current_stats
    white_co = np.array(white_co)  # White coefficient matrix
    black_co = np.array(black_co)  # Black coefficient matrix
    
    def adjust_pst(pst, white_co, black_co):
        result = pst.copy()
        for i in range(len(pst)):
            if i % 2 == 0:  # Even rank
                result[i] = pst[i] - white_co[i]
            else:  # Odd rank
                result[i] = pst[i] - black_co[i]
        return result

    # Adjust all phases
    PST_white['opening'] = adjust_pst(PST_white['opening'], white_co, black_co)
    PST_white['middlegame'] = adjust_pst(PST_white['middlegame'], white_co, black_co)
    PST_white['endgame'] = adjust_pst(PST_white['endgame'], white_co, black_co)
    
    return PST_white['opening']

def pre_process(data):
    # Initialize two 8x8 matrices for white and black scores
    score_w_matrix = [[0 for _ in range(8)] for _ in range(8)]
    score_b_matrix = [[0 for _ in range(8)] for _ in range(8)]

    # Function to process the data and fill the matrices
    for item in data:
        # Extract the coordinate and split it into row and column
        coord = item['cordinate']
        row, col = map(int, coord.split(','))

        # Place the scores in the respective matrices
        score_w_matrix[row][col] = item['score_w']
        score_b_matrix[row][col] = item['score_b']
    
    return score_w_matrix,score_b_matrix

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()  # Get the JSON data from the POST request
    results = data.get('results')
    #print(f"results: {results}")
    current_stats = pre_process(results)
    after_min_max = min_max(current_stats)
    print(after_min_max)
    return jsonify({'status': 'success', 'message': f"results: {results}"})

if __name__ == '__main__':
    app.run(debug=True)