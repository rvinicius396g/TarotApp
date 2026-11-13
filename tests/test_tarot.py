"""
tests/test_tarot.py
Conjunto de testes unitários com pytest para validar dados e mecânicas de sorteio.
"""

import pytest
from cards_data import ARCANOS_MAIORES
import tarot_logic


class TestIntegridadeDados:
    """Testa a consistência e integridade da lista de cartas."""

    def test_total_de_cartas_deve_ser_22(self):
        """Verifica se existem exatamente 22 Arcanos Maiores."""
        assert len(ARCANOS_MAIORES) == 22

    def test_chaves_obrigatorias_em_cada_carta(self):
        """Garante que todas as cartas contêm todas as propriedades essenciais."""
        chaves_esperadas = {"id", "nome", "imagem", "normal", "invertida"}
        for carta in ARCANOS_MAIORES:
            assert chaves_esperadas.issubset(carta.keys()), (
                f"A carta com id {carta.get('id')} não possui todas as chaves obrigatórias."
            )

    def test_ids_devem_ser_unicos(self):
        """Garante que não existem dois Arcanos com o mesmo número de identificação."""
        ids = [carta["id"] for carta in ARCANOS_MAIORES]
        assert len(ids) == len(set(ids)), "Existem IDs duplicados no baralho."

    def test_textos_de_significado_nao_devem_estar_vazios(self):
        """Verifica se nenhuma carta possui significado ou nome em branco."""
        for carta in ARCANOS_MAIORES:
            assert carta["nome"].strip() != ""
            assert carta["normal"].strip() != ""
            assert carta["invertida"].strip() != ""


class TestLogicaSorteio:
    """Testa o comportamento das funções de sorteio e regras do jogo."""

    def test_tirar_uma_carta_retorna_carta_valida(self):
        """Testa o sorteio individual de 1 carta."""
        carta_tirada = tarot_logic.tirar_uma_carta()
        assert "nome" in carta_tirada
        assert carta_tirada["posicao"] in ["Normal", "Invertida"]
        assert isinstance(carta_tirada["is_invertida"], bool)

    def test_tirar_tres_cartas_retorna_exatamente_tres(self):
        """Garante que a tiragem de 3 cartas devolve exatamente 3 elementos."""
        tiragem = tarot_logic.tirar_tres_cartas()
        assert len(tiragem) == 3

    def test_tirar_tres_cartas_sem_repeticao(self):
        """Regra essencial: as cartas na tiragem não se podem repetir."""
        tiragem = tarot_logic.tirar_tres_cartas()
        nomes = [carta["nome"] for carta in tiragem]
        assert len(nomes) == len(set(nomes)), "Houve repetição de cartas na tiragem de 3!"

    def test_posicoes_temporais_corretas(self):
        """Valida a ordem temporal: Passado, Presente e Futuro."""
        tiragem = tarot_logic.tirar_tres_cartas()
        ordem_obtida = [carta["posicao_tiragem"] for carta in tiragem]
        assert ordem_obtida == ["Passado", "Presente", "Futuro"]

    def test_erro_quando_baralho_tem_menos_de_tres_cartas(self):
        """Garante que o código lança exceção caso o baralho seja insuficiente."""
        baralho_insuficiente = [{"id": 0, "nome": "O Louco", "imagem": "", "normal": "", "invertida": ""}]
        with pytest.raises(ValueError):
            tarot_logic.tirar_tres_cartas(baralho_insuficiente)

import database

class TestHistoricoDatabase:
    """Testa a integridade das operações de base de dados SQLite."""

    def test_salvar_e_obter_historico(self, tmp_path):
        # Cria uma base de dados temporária isolada para o teste
        test_db = str(tmp_path / "teste_tarot.db")
        
        database.salvar_tiragem("UtilizadorTeste", "Carta do Dia", "O Louco (Normal)", db_path=test_db)
        historico = database.obter_historico("UtilizadorTeste", db_path=test_db)

        assert len(historico) == 1
        assert historico[0]["tipo"] == "Carta do Dia"
        assert historico[0]["conteudo"] == "O Louco (Normal)"
        assert "data_hora" in historico[0]

    def test_limpar_historico(self, tmp_path):
        test_db = str(tmp_path / "teste_tarot.db")
        
        database.salvar_tiragem("UtilizadorTeste", "Tiragem de 3", "Conteúdo teste", db_path=test_db)
        assert len(database.obter_historico("UtilizadorTeste", db_path=test_db)) == 1

        database.limpar_historico("UtilizadorTeste", db_path=test_db)
        assert len(database.obter_historico("UtilizadorTeste", db_path=test_db)) == 0

from auth_service import AuthService

class TestAuthService:
    """Testa o gerenciamento de sessão de usuário."""

    def test_login_demo_define_usuario_e_nome(self):
        auth = AuthService()
        resposta = auth.login_com_firebase("vinicius396g@gmail.com", "F2x1dDu$4CEE")
        assert resposta["sucesso"] is True
        assert auth.esta_autenticado() is True
        assert auth.usuario_atual["nome"] == "Vinicius"

    def test_logout_limpa_sessao(self):
        auth = AuthService()
        auth.login_google(nome="Júnior")
        assert auth.esta_autenticado() is True
        auth.logout()
        assert auth.esta_autenticado() is False
        assert auth.usuario_atual is None