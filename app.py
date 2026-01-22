from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Untuk session

# Data soal quiz (5 soal sederhana)
questions = [
    {
        "question": "Apa ibu kota Indonesia?",
        "options": ["Jakarta", "Surabaya", "Bandung", "Medan"],
        "answer": "Jakarta"
    },
    {
        "question": "Berapa hasil dari 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    },
    {
        "question": "Planet apa yang terdekat dengan Matahari?",
        "options": ["Venus", "Mars", "Merkurius", "Bumi"],
        "answer": "Merkurius"
    },
    {
        "question": "Siapa penemu lampu pijar?",
        "options": ["Albert Einstein", "Thomas Edison", "Nikola Tesla", "Isaac Newton"],
        "answer": "Thomas Edison"
    },
    {
        "question": "Apa warna langit pada siang hari?",
        "options": ["Merah", "Biru", "Hijau", "Kuning"],
        "answer": "Biru"
    }
]

@app.route('/')
def index():
    # Inisialisasi session jika belum ada
    if 'current_question' not in session:
        session['current_question'] = 0
        session['score'] = 0
        session['answers'] = []
    return render_template('index.html', questions=questions)

@app.route('/get_question', methods=['GET'])
def get_question():
    current_q = session['current_question']
    if current_q < len(questions):
        return jsonify(questions[current_q])
    else:
        return jsonify({'finished': True, 'score': session['score'], 'total': len(questions)})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    selected_answer = data['selected_answer']
    current_q = session['current_question']
    correct_answer = questions[current_q]['answer']
    is_correct = selected_answer == correct_answer
    if is_correct:
        session['score'] += 1
    session['answers'].append({'question': current_q, 'selected': selected_answer, 'correct': is_correct})
    return jsonify({'is_correct': is_correct, 'correct_answer': correct_answer})

@app.route('/next_question', methods=['POST'])
def next_question():
    session['current_question'] += 1
    return jsonify({'success': True})

@app.route('/restart', methods=['POST'])
def restart():
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)