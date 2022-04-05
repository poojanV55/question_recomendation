from flask import Flask,request,jsonify
from flask_cors import CORS
import recommendation

app = Flask(__name__)
CORS(app)

@app.route('/',methods = ['GET'])
def sayhello():
    return 'App running'

@app.route('/question', methods=['GET'])
def recommend_question():
    res = recommendation.results(request.args.get('question_name'))
    return jsonify(res)


if __name__ == '__main__':
    app.run(port=5000, debug=True)


