"""
auth_service.py
Módulo responsável por gerenciar a sessão do usuário (Google / Facebook / Convidado).
Mais adiante, conectaremos este serviço às chamadas de API do Firebase Auth.
"""

class AuthService:
    def __init__(self):
        self.usuario_atual = None
        self.provedor = None  # 'google', 'facebook' ou 'convidado'

    def login_google(self):
        """
        Simula a autenticação via Google OAuth.
        Retorna um dicionário com os dados do usuário.
        """
        self.usuario_atual = {
            "nome": "Usuário Google",
            "email": "usuario@gmail.com",
            "provedor": "Google"
        }
        self.provedor = "google"
        return self.usuario_atual

    def login_facebook(self):
        """
        Simula a autenticação via Facebook OAuth.
        Retorna um dicionário com os dados do usuário.
        """
        self.usuario_atual = {
            "nome": "Usuário Facebook",
            "email": "usuario@facebook.com",
            "provedor": "Facebook"
        }
        self.provedor = "facebook"
        return self.usuario_atual

    def logout(self):
        """Encerra a sessão atual do usuário."""
        self.usuario_atual = None
        self.provedor = None

    def esta_autenticado(self):
        """Verifica se há um usuário com sessão ativa."""
        return self.usuario_atual is not None