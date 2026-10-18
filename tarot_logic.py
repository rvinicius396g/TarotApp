"""
tarot_logic.py
Regras de negócio e lógica de sorteio para o jogo de Tarot.
"""

import random
from cards_data import ARCANOS_MAIORES


def sortear_posicao():
    """
    Sorteia aleatoriamente se a carta sairá na posição Normal ou Invertida.
    Retorna True se for invertida, False caso contrário.
    """
    return random.choice([True, False])


def formatar_carta(carta, invertida=None):
    """
    Recebe um dicionário de carta e define a posição (sorteada se invertida for None).
    Retorna um dicionário com os dados processados para a exibição.
    """
    if invertida is None:
        invertida = sortear_posicao()

    posicao_str = "Invertida" if invertida else "Normal"
    significado = carta["invertida"] if invertida else carta["normal"]

    return {
        "id": carta["id"],
        "nome": carta["nome"],
        "imagem": carta["imagem"],
        "posicao": posicao_str,
        "is_invertida": invertida,
        "significado": significado
    }


def tirar_uma_carta(baralho=ARCANOS_MAIORES):
    """
    Sorteia uma única carta do baralho fornecido.
    """
    carta_escolhida = random.choice(baralho)
    return formatar_carta(carta_escolhida)


def tirar_tres_cartas(baralho=ARCANOS_MAIORES):
    """
    Sorteia 3 cartas distintas (sem repetição) para Passado, Presente e Futuro.
    """
    if len(baralho) < 3:
        raise ValueError("O baralho precisa conter pelo menos 3 cartas.")

    cartas_sorteadas = random.sample(baralho, 3)
    posicoes_tempo = ["Passado", "Presente", "Futuro"]

    resultado = []
    for i in range(3):
        carta_formatada = formatar_carta(cartas_sorteadas[i])
        carta_formatada["posicao_tiragem"] = posicoes_tempo[i]
        resultado.append(carta_formatada)

    return resultado