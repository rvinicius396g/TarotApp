"""
test_conexao_firebase.py
Script isolado para validar a FIREBASE_WEB_API_KEY e testar o fluxo de
criação/autenticação de conta e recebimento de token com o Firebase Auth.
"""

import os
import sys
from firebase_auth import FirebaseAuthClient


def executar_diagnostico():
    print("=== Teste de Conexao com o Google Firebase Auth ===")
    client = FirebaseAuthClient()

    if not client.possui_chave_valida():
        print("\n[AVISO] A variavel FIREBASE_WEB_API_KEY ainda nao foi configurada!")
        print("Para configurar:")
        print("  1. Crie um arquivo .env na raiz do projeto com:")
        print("     FIREBASE_WEB_API_KEY=AIzaSySuaChaveAqui...")
        print("  OU defina no PowerShell antes de rodar:")
        print('     $env:FIREBASE_WEB_API_KEY="AIzaSySuaChaveAqui..."')
        sys.exit(1)

    email_teste = os.environ.get("FIREBASE_TEST_EMAIL", "vinicius396g@gmail.com")
    senha_teste = os.environ.get("FIREBASE_TEST_PASSWORD", "F2x1dDu$4CEE")
    nome_teste = "Vinicius"

    print(f"Testando autenticacao para: {email_teste} ...")
    resultado = client.sign_in_with_password(email_teste, senha_teste)

    if resultado.get("sucesso"):
        id_token = resultado.get("id_token")
        nome_atual = resultado.get("nome")
        if not nome_atual and id_token:
            upd = client.update_profile(id_token, nome_teste)
            if upd.get("sucesso"):
                nome_atual = upd.get("nome", nome_teste)
        print("[OK] Login realizado com sucesso no Firebase!")
        print(f"     Local ID : {resultado.get('local_id')}")
        print(f"     Nome     : {nome_atual or '(nao definido)'}")
        print(f"     Token    : {str(id_token)[:25]}...")
        return

    codigo = resultado.get("codigo", "")
    print(f"[INFO] Login retornou: {resultado.get('erro')} ({codigo})")

    if codigo in ("EMAIL_NOT_FOUND", "INVALID_LOGIN_CREDENTIALS"):
        print("Tentando criar a conta automaticamente via signUp...")
        cadastro = client.sign_up(email_teste, senha_teste, display_name=nome_teste)
        if cadastro.get("sucesso"):
            print("[OK] Conta criada e autenticada com sucesso no Firebase!")
            print(f"     Local ID : {cadastro.get('local_id')}")
            print(f"     Nome     : {cadastro.get('nome')}")
            print(f"     Token    : {str(cadastro.get('id_token'))[:25]}...")
        else:
            print(f"[ERRO] Falha ao criar conta: {cadastro.get('erro')}")
            sys.exit(1)
    else:
        sys.exit(1)


if __name__ == "__main__":
    executar_diagnostico()
