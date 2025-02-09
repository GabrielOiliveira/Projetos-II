import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

ARQUIVO_USUARIOS = "usuarios.json"

if not os.path.exists(ARQUIVO_USUARIOS):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump([], f)

class Servidor(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """ Habilita o CORS para permitir requisições do navegador """
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        """ Lida com requisições POST (Cadastro e Login) """
        if self.path == "/cadastrar":
            self.cadastrar_usuario()
        elif self.path == "/login":
            self.fazer_login()
        else:
            self.send_error(404, "Rota não encontrada.")

    def carregar_usuarios(self):
        """ Carrega os usuários do arquivo JSON """
        try:
            with open(ARQUIVO_USUARIOS, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def salvar_usuarios(self, usuarios):
        """ Salva os usuários no arquivo JSON """
        with open(ARQUIVO_USUARIOS, "w") as f:
            json.dump(usuarios, f, indent=4)

    def cadastrar_usuario(self):
        """ Cadastra um novo usuário """
        content_length = int(self.headers["Content-Length"])
        dados = json.loads(self.rfile.read(content_length).decode("utf-8"))

        nome = dados.get("nome").strip()
        senha = dados.get("senha").strip()

        if not nome or not senha:
            self.responder_json({"mensagem": "Nome e senha não podem estar vazios!"})
            return

        usuarios = self.carregar_usuarios()

        for usuario in usuarios:
            if usuario["nome"] == nome:
                self.responder_json({"mensagem": "Nome já cadastrado!"})
                return

        usuarios.append({"nome": nome, "senha": senha})
        self.salvar_usuarios(usuarios)

        self.responder_json({"mensagem": "Cadastro realizado com sucesso!"})

    def fazer_login(self):
        """ Verifica se o usuário e senha estão corretos """
        content_length = int(self.headers["Content-Length"])
        dados = json.loads(self.rfile.read(content_length).decode("utf-8"))

        nome = dados.get("nome").strip()
        senha = dados.get("senha").strip()

        usuarios = self.carregar_usuarios()

        for usuario in usuarios:
            if usuario["nome"] == nome and usuario["senha"] == senha:
                self.responder_json({"sucesso": True, "mensagem": f"Bem-vindo, {nome}!"})
                return

        self.responder_json({"sucesso": False, "mensagem": "Nome ou senha incorretos!"})

    def responder_json(self, resposta):
        """ Envia uma resposta JSON para o navegador """
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(resposta).encode("utf-8"))

if __name__ == "__main__":
    servidor = HTTPServer(("localhost", 8080), Servidor)
    print("Servidor rodando em http://localhost:8080")
    servidor.serve_forever()
