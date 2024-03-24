# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import psycopg2
import os
import webbrowser
from flask import send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configuração do banco de dados
DB_HOST = 'localhost'
 # O PostgreSQL.app geralmente roda no localhost
DB_PORT = '5001'  # Porta em que o PostgreSQL.app está configurado para escutar
DB_NAME = 'produtos'  # Nome do banco de dados
DB_USER = 'postgres'  # Nome do usuário do banco de dados
DB_PASSWORD = '27241618Lc@'  # Senha do banco de dados

app = Flask(__name__, template_folder='/Users/LuizCastagno/Desktop/castore/FLASK/Template')

# Função para conectar ao banco de dados
def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

# Rota para página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para adicionar produto
@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto():
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            tipo = request.form['tipo']
            preco = request.form['preco']
            descricao = request.form['descricao']
            imagem = request.files['imagem']
            # Salvar a imagem e obter o caminho
            imagem.save(os.path.join('caminho/para/salvar', imagem.filename))
            caminho_imagem = os.path.join('caminho/para/salvar', imagem.filename)
            # Inserir no banco de dados
            cur.execute("INSERT INTO produtos (tipo, preco, descricao, imagem) VALUES (%s, %s, %s, %s)", (tipo, preco, descricao, caminho_imagem))
            conn.commit()
            return jsonify({'message': 'Produto adicionado com sucesso!'})
        except psycopg2.Error as e:
            print("Erro ao adicionar produto:", e)
            return jsonify({'message': 'Erro ao adicionar produto.'}), 500
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({'message': 'Erro ao conectar ao banco de dados.'}), 500

# Rota para obter histórico de postagens# Rota para obter histórico de postagens e gerar PDF
@app.route('/historico_postagens_pdf')
def historico_postagens_pdf():
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM produtos")
            historico = cur.fetchall()
            # Criar PDF
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            y = 750  # Posição inicial na página
            for row in historico:
                tipo, preco, descricao, imagem = row
                c.drawString(100, y, f"Tipo: {tipo}")
                c.drawString(100, y - 20, f"Preço: {preco}")
                c.drawString(100, y - 40, f"Descrição: {descricao}")
                y -= 60  # Espaçamento entre os registros
            c.save()
            pdf_buffer.seek(0)
            # Disponibilizar o PDF para download
            return send_file(pdf_buffer, attachment_filename='historico_produtos.pdf', as_attachment=True)
        except psycopg2.Error as e:
            print("Erro ao obter histórico de postagens:", e)
            return jsonify({'message': 'Erro ao obter histórico de postagens.'}), 500
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({'message': 'Erro ao conectar ao banco de dados.'}), 500

if __name__ == '__main__':
    # Abrir a página do gerenciador no navegador padrão ao iniciar o app Python
    webbrowser.open('http://127.0.0.1:5001')
    app.run(debug=True)