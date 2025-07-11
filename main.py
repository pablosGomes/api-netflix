from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
ARQUIVO_JSON = 'filmes.json'

def carregar_filmes():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, 'r') as f:
            return json.load(f)
    return []

def salvar_filmes(filmes):
    with open(ARQUIVO_JSON, 'w') as f:
        json.dump(filmes, f, indent=4)

@app.route('/filmes', methods=['GET'])
def listar_filmes():
    return jsonify(carregar_filmes())

@app.route('/filmes/<int:id>', methods=['GET'])
def visualizar_filme(id):
    filmes = carregar_filmes()
    filme = next((f for f in filmes if f['id'] == id), None)
    if filme:
        return jsonify(filme)
    return jsonify({"erro": "Filme não encontrado"}), 404

@app.route('/filmes', methods=['POST'])
def cadastrar_filme():
    filmes = carregar_filmes()
    dados = request.json
    novo_id = max([f['id'] for f in filmes] + [0]) + 1
    filme = {
        "id": novo_id,
        "titulo": dados.get("titulo"),
        "ano": dados.get("ano"),
        "descricao": dados.get("descricao")
    }
    filmes.append(filme)
    salvar_filmes(filmes)
    return jsonify(filme), 201

@app.route('/filmes/<int:id>', methods=['PUT'])
def editar_filme(id):
    filmes = carregar_filmes()
    dados = request.json
    for filme in filmes:
        if filme['id'] == id:
            filme['titulo'] = dados.get("titulo", filme['titulo'])
            filme['ano'] = dados.get("ano", filme['ano'])
            filme['descricao'] = dados.get("descricao", filme['descricao'])
            salvar_filmes(filmes)
            return jsonify(filme)
    return jsonify({"erro": "Filme não encontrado"}), 404

@app.route('/filmes/<int:id>', methods=['DELETE'])
def excluir_filme(id):
    filmes = carregar_filmes()
    filmes_novos = [f for f in filmes if f['id'] != id]
    if len(filmes_novos) == len(filmes):
        return jsonify({"erro": "Filme não encontrado"}), 404
    salvar_filmes(filmes_novos)
    return jsonify({"mensagem": "Filme removido com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)
