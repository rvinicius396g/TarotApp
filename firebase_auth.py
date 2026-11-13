"""
firebase_auth.py
Cliente HTTP para autenticação via Google Firebase Identity Toolkit v1 (REST API).
Suporta criação de conta (signUp), login com e-mail/senha (signInWithPassword)
e atualização de perfil (update).
"""

import os
import requests


def _carregar_env_local(caminho_env=".env"):
    """Lê variáveis simples do arquivo .env local, caso exista."""
    if not os.path.exists(caminho_env):
        return
    try:
        with open(caminho_env, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue
                chave, valor = linha.split("=", 1)
                chave = chave.strip()
                valor = valor.strip().strip('"').strip("'")
                if chave and chave not in os.environ:
                    os.environ[chave] = valor
    except OSError:
        pass


_carregar_env_local()


class FirebaseAuthClient:
    BASE_URL = "https://identitytoolkit.googleapis.com/v1/accounts"

    # Tradução amigáveis dos códigos de erro comuns do Firebase
    MENSAGENS_ERRO = {
        "EMAIL_EXISTS": "Este e-mail já está cadastrado.",
        "INVALID_EMAIL": "Formato de e-mail inválido.",
        "WEAK_PASSWORD : Password should be at least 6 characters": "A senha deve ter pelo menos 6 caracteres.",
        "EMAIL_NOT_FOUND": "E-mail não encontrado.",
        "INVALID_PASSWORD": "Senha incorreta.",
        "INVALID_LOGIN_CREDENTIALS": "E-mail ou senha inválidos.",
        "USER_DISABLED": "Esta conta de usuário foi desativada.",
        "TOO_MANY_ATTEMPTS_TRY_LATER": "Muitas tentativas. Tente novamente mais tarde.",
    }

    def __init__(self, api_key=None, timeout=10):
        self.api_key = api_key or os.environ.get("FIREBASE_WEB_API_KEY", "")
        self.timeout = timeout

    def possui_chave_valida(self):
        """Verifica se há uma Web API Key real configurada."""
        placeholders = {"", "SUA_API_KEY_AQUI", "COLE_SUA_WEB_API_KEY_AQUI"}
        return bool(self.api_key and self.api_key.strip() not in placeholders)

    def _endpoint(self, operacao):
        return f"{self.BASE_URL}:{operacao}?key={self.api_key}"

    def _traduzir_erro(self, codigo_erro):
        if codigo_erro in self.MENSAGENS_ERRO:
            return self.MENSAGENS_ERRO[codigo_erro]
        for chave, msg in self.MENSAGENS_ERRO.items():
            if codigo_erro.startswith(chave.split(" ")[0]):
                return msg
        return f"Erro na autenticação ({codigo_erro})."

    def sign_up(self, email, password, display_name=None):
        """Cria um novo usuário no Firebase Auth com e-mail e senha."""
        if not self.possui_chave_valida():
            return {"sucesso": False, "erro": "FIREBASE_WEB_API_KEY não configurada."}

        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True,
        }
        try:
            resp = requests.post(self._endpoint("signUp"), json=payload, timeout=self.timeout)
            dados = resp.json()
            if resp.status_code == 200:
                id_token = dados.get("idToken")
                if display_name and id_token:
                    self.update_profile(id_token, display_name)
                return {
                    "sucesso": True,
                    "id_token": id_token,
                    "refresh_token": dados.get("refreshToken"),
                    "local_id": dados.get("localId"),
                    "email": dados.get("email", email),
                    "nome": display_name or "",
                }
            codigo = dados.get("error", {}).get("message", "ERRO_DESCONHECIDO")
            return {"sucesso": False, "erro": self._traduzir_erro(codigo), "codigo": codigo}
        except requests.RequestException as exc:
            return {"sucesso": False, "erro": f"Falha de conexão com o Firebase: {exc}"}

    def sign_in_with_password(self, email, password):
        """Autentica um usuário existente com e-mail e senha."""
        if not self.possui_chave_valida():
            return {"sucesso": False, "erro": "FIREBASE_WEB_API_KEY não configurada."}

        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True,
        }
        try:
            resp = requests.post(
                self._endpoint("signInWithPassword"), json=payload, timeout=self.timeout
            )
            dados = resp.json()
            if resp.status_code == 200:
                return {
                    "sucesso": True,
                    "id_token": dados.get("idToken"),
                    "refresh_token": dados.get("refreshToken"),
                    "local_id": dados.get("localId"),
                    "email": dados.get("email", email),
                    "nome": dados.get("displayName", ""),
                }
            codigo = dados.get("error", {}).get("message", "ERRO_DESCONHECIDO")
            return {"sucesso": False, "erro": self._traduzir_erro(codigo), "codigo": codigo}
        except requests.RequestException as exc:
            return {"sucesso": False, "erro": f"Falha de conexão com o Firebase: {exc}"}

    def update_profile(self, id_token, display_name):
        """Atualiza o displayName do usuário autenticado no Firebase."""
        if not self.possui_chave_valida():
            return {"sucesso": False, "erro": "FIREBASE_WEB_API_KEY não configurada."}

        payload = {
            "idToken": id_token,
            "displayName": display_name,
            "returnSecureToken": True,
        }
        try:
            resp = requests.post(self._endpoint("update"), json=payload, timeout=self.timeout)
            dados = resp.json()
            if resp.status_code == 200:
                return {
                    "sucesso": True,
                    "nome": dados.get("displayName", display_name),
                    "email": dados.get("email", ""),
                }
            codigo = dados.get("error", {}).get("message", "ERRO_DESCONHECIDO")
            return {"sucesso": False, "erro": self._traduzir_erro(codigo), "codigo": codigo}
        except requests.RequestException as exc:
            return {"sucesso": False, "erro": f"Falha de conexão com o Firebase: {exc}"}
