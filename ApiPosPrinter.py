import threading
import sys
import time
import signal
from flask import Flask, render_template, request, jsonify, json
from libACBr import limpar_tela, configModelo, configPorta, imprimir

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
        imprimir(text.encode('utf-8'))
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Texto é necessário'}), 400

def run_server():
    port = 5000
    print(f"Servidor rodando na porta {port}...")
    app.run(debug=True, port=port, use_reloader=False)

def print_menu():
    limpar_tela()
    menu_text = """
    1. Configura Modelo
    2. Configura Porta 
    3. Iniciar Servidor
    Pressione ESC para parar o servidor
    """
    print(menu_text)

def main():
    
    server_thread = None

    while True:
        limpar_tela()
        print_menu()
        choice = input("Escolha uma opção: ")
        if choice == '1':
            # Adicione aqui as opções de configuração
            configModelo()
        if choice == '2':
            # Adicione aqui as opções de configuração
            configPorta()
        elif choice == '3':
            if server_thread is None or not server_thread.is_alive():
                server_thread = threading.Thread(target=run_server)
                server_thread.daemon = True
                server_thread.start()
                print("Servidor iniciado...")
            else:
                print("Servidor já está em execução.")
        elif choice.lower() == 'esc':
            print("Parando o servidor...")
            if server_thread and server_thread.is_alive():
                # Sinalizar o servidor para parar
                request.environ.get('werkzeug.server.shutdown')()
                server_thread.join()
            print("Servidor parado. Saindo...")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
