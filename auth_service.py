"""
auth_service.py
Módulo responsável por gerenciar a sessão do utilizador (Google / Facebook / Firebase).
"""

import re
from firebase_auth import FirebaseAuthClient


class AuthService:
    def __init__(self, firebase_client=None):
        self.usuario_atual = None
        self.provedor = None
        self.id_token = None
        self.firebase = firebase_client or FirebaseAuthClient()

    @staticmethod
    def _extrair_nome_do_email(email):
        """Extrai e formata um nome legível a partir do prefixo do e-mail."""
        prefixo = email.split("@")[0] if "@" in email else email
        match = re.match(r"([a-zA-ZÀ-ÿ]+)", prefixo)
        if match:
            return match.group(1).capitalize()
        return prefixo.capitalize() or "Utilizador"

    def login_com_firebase(self, email, senha):
        """
        Autentica o utilizador via Firebase Auth (ou em modo demo local caso
        a FIREBASE_WEB_API_KEY ainda não esteja configurada no ambiente).
        """
        email = (email or "").strip()
        senha = (senha or "").strip()

        if not email or "@" not in email:
            return {"sucesso": False, "erro": "Informe um e-mail válido."}
        if len(senha) < 6:
            return {"sucesso": False, "erro": "A senha deve ter pelo menos 6 caracteres."}

        if self.firebase.possui_chave_valida():
            resposta = self.firebase.sign_in_with_password(email, senha)
            if not resposta.get("sucesso"):
                return resposta
            nome = resposta.get("nome") or self._extrair_nome_do_email(email)
            self.id_token = resposta.get("id_token")
        else:
            # Modo Demo / Local quando a chave Web API ainda não foi definida
            nome = self._extrair_nome_do_email(email)
            self.id_token = "demo_token_local"

        self.usuario_atual = {
            "nome": nome,
            "email": email,
            "provedor": "Firebase",
        }
        self.provedor = "firebase"
        return {"sucesso": True, "usuario": self.usuario_atual}

    def registrar_com_firebase(self, email, senha, nome=None):
        """
        Regista um novo utilizador no Firebase Auth (ou em modo demo local).
        """
        email = (email or "").strip()
        senha = (senha or "").strip()
        nome_final = (nome or "").strip() or self._extrair_nome_do_email(email)

        if not email or "@" not in email:
            return {"sucesso": False, "erro": "Informe um e-mail válido."}
        if len(senha) < 6:
            return {"sucesso": False, "erro": "A senha deve ter pelo menos 6 caracteres."}

        if self.firebase.possui_chave_valida():
            resposta = self.firebase.sign_up(email, senha, display_name=nome_final)
            if not resposta.get("sucesso"):
                return resposta
            self.id_token = resposta.get("id_token")
        else:
            self.id_token = "demo_token_local"

        self.usuario_atual = {
            "nome": nome_final,
            "email": email,
            "provedor": "Firebase",
        }
        self.provedor = "firebase"
        return {"sucesso": True, "usuario": self.usuario_atual}

    def login_google(self, nome="Júnior"):
        """
        Simula a autenticação via Google OAuth.
        Recebe o nome do perfil do utilizador.
        """
        self.usuario_atual = {
            "nome": nome,
            "email": f"{nome.lower().replace(' ', '')}@gmail.com",
            "provedor": "Google"
        }
        self.provedor = "google"
        return self.usuario_atual

    def login_facebook(self, nome="Júnior"):
        """
        Simula a autenticação via Facebook OAuth.
        Recebe o nome do perfil do utilizador.
        """
        self.usuario_atual = {
            "nome": nome,
            "email": f"{nome.lower().replace(' ', '')}@facebook.com",
            "provedor": "Facebook"
        }
        self.provedor = "facebook"
        return self.usuario_atual

    def logout(self):
        """Encerra a sessão ativa do utilizador."""
        self.usuario_atual = None
        self.provedor = None
        self.id_token = None

    def esta_autenticado(self):
        """Verifica se há uma sessão ativa."""
        return self.usuario_atual is not None
