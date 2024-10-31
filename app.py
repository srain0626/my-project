import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
CORS(app)  # CORS 설정 추가

# Sentence-Transformers 모델 로드
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/correct', methods=['POST'])
def correct():
    input_text = request.json['text']
    corrected_text = correct_text(input_text)
    return jsonify({'corrected_text': corrected_text})

def correct_text(text):
    url = "https://api.languagetool.org/v2/check"
    params = {
        "text": text,
        "language": "en-US"  # 영어 (미국)
    }
    response = requests.post(url, data=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return text
    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError:
        print("JSONDecodeError: 응답을 디코딩할 수 없습니다.")
        return text
    
    corrections = []
    for match in result['matches']:
        corrections.append({
            'offset': match['offset'],
            'length': match['length'],
            'replacement': match['replacements'][0]['value'] if match['replacements'] else ''
        })
    
    # 원문에 반영
    corrected_text = list(text)
    for correction in reversed(corrections):
        start = correction['offset']
        end = start + correction['length']
        corrected_text[start:end] = correction['replacement']
    
    return ''.join(corrected_text)

if __name__ == '__main__':
    app.run(debug=True)
