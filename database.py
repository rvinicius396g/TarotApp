"""
database.py
Módulo responsável por gerir a base de dados SQLite local
para armazenar o histórico de tiragens de cada utilizador.
"""

import os
import sqlite3
from datetime import datetime

# Nome do ficheiro da base de dados local
DB_NAME = "tarot_history.db"


def _resolver_caminho_db(db_path=DB_NAME):
    """Garante caminho gravável tanto no Desktop quanto no Android."""
    if db_path != DB_NAME:
        return db_path
    try:
        from kivy.app import App
        from kivy.utils import platform
        if platform == "android":
            app = App.get_running_app()
            if app and getattr(app, "user_data_dir", None):
                os.makedirs(app.user_data_dir, exist_ok=True)
                return os.path.join(app.user_data_dir, DB_NAME)
    except Exception:
        pass
    if "ANDROID_PRIVATE" in os.environ:
        return os.path.join(os.environ["ANDROID_PRIVATE"], DB_NAME)
    return db_path


def obter_conexao(db_path=DB_NAME):
    """Cria e devolve uma ligação à base de dados SQLite."""
    caminho_real = _resolver_caminho_db(db_path)
    conn = sqlite3.connect(caminho_real)
    # Permite aceder aos campos por nome de coluna
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_banco(db_path=DB_NAME):
    """Cria a tabela de histórico se ainda não existir."""
    with obter_conexao(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historico_tiragens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                tipo_tiragem TEXT NOT NULL,
                conteudo TEXT NOT NULL,
                data_hora TEXT NOT NULL
            )
            """
        )
        conn.commit()


def salvar_tiragem(usuario, tipo_tiragem, conteudo, db_path=DB_NAME):
    """
    Regista uma nova leitura de cartas para o utilizador indicado.
    Formata a data/hora atual no padrão legível DD/MM/AAAA HH:MM.
    """
    inicializar_banco(db_path)
    data_formatada = datetime.now().strftime("%d/%m/%Y %H:%M")

    with obter_conexao(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO historico_tiragens (usuario, tipo_tiragem, conteudo, data_hora)
            VALUES (?, ?, ?, ?)
            """,
            (usuario, tipo_tiragem, conteudo, data_formatada)
        )
        conn.commit()


def obter_historico(usuario, db_path=DB_NAME):
    """
    Devolve a lista de todas as leituras do utilizador,
    ordenadas da mais recente para a mais antiga.
    """
    inicializar_banco(db_path)
    with obter_conexao(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT tipo_tiragem, conteudo, data_hora
            FROM historico_tiragens
            WHERE usuario = ?
            ORDER BY id DESC
            """,
            (usuario,)
        )
        linhas = cursor.fetchall()

    return [
        {
            "tipo": linha["tipo_tiragem"],
            "conteudo": linha["conteudo"],
            "data_hora": linha["data_hora"]
        }
        for linha in linhas
    ]


def limpar_historico(usuario, db_path=DB_NAME):
    """Remove todos os registos do utilizador especificado."""
    inicializar_banco(db_path)
    with obter_conexao(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM historico_tiragens WHERE usuario = ?",
            (usuario,)
        )
        conn.commit()