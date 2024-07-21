from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    
    if text:
        data = {
            'text': text
        }
        # Aqui você pode chamar uma função Python com os dados
        process_data(data)
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Texto é necessário'}), 400

def process_data(data):
    # Função de exemplo que processa os dados
    print(f"Processando dados: {data}")
    

if __name__ == '__main__':
    port = 5000
    print(f"Servidor rodando na porta {port}...")
    app.run(debug=True, port=port)
