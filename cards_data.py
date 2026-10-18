"""
cards_data.py
Define os 22 Arcanos Maiores do Tarot com caminhos de imagem
e significados na posição Normal e Invertida.
"""

ARCANOS_MAIORES = [
    {
        "id": 0,
        "nome": "O Louco",
        "imagem": "assets/images/0_o_louco.png",
        "normal": "Novos começos, espontaneidade, liberdade e fé no desconhecido.",
        "invertida": "Imprudência, ingenuidade excessiva, risco desnecessário e hesitação."
    },
    {
        "id": 1,
        "nome": "O Mago",
        "imagem": "assets/images/1_o_mago.png",
        "normal": "Manifestação, recursos próprios, força de vontade e criatividade.",
        "invertida": "Ilusão, manipulação, talentos não aproveitados e planos confusos."
    },
    {
        "id": 2,
        "nome": "A Sacerdotisa",
        "imagem": "assets/images/2_a_sacerdotisa.png",
        "normal": "Intuição, mistério, sabedoria interior e reflexão serena.",
        "invertida": "Segredos revelados, desconexão com a intuição e superficialidade."
    },
    {
        "id": 3,
        "nome": "A Imperatriz",
        "imagem": "assets/images/3_a_imperatriz.png",
        "normal": "Abundância, fertilidade, maternidade, beleza e acolhimento.",
        "invertida": "Dependência, bloqueio criativo, negligência ou excesso de controle."
    },
    {
        "id": 4,
        "nome": "O Imperador",
        "imagem": "assets/images/4_o_imperador.png",
        "normal": "Estrutura, disciplina, liderança, estabilidade e autoridade.",
        "invertida": "Tirania, rigidez mental, falta de disciplina e autoritarismo."
    },
    {
        "id": 5,
        "nome": "O Papa (Hierofante)",
        "imagem": "assets/images/5_o_papa.png",
        "normal": "Tradição, ensinamento espiritual, valores éticos e sabedoria compartilhada.",
        "invertida": "Dogmatismo, quebra de convenções, rigidez de pensamento."
    },
    {
        "id": 6,
        "nome": "Os Enamorados",
        "imagem": "assets/images/6_os_enamorados.png",
        "normal": "Escolhas importantes, harmonia, relacionamentos e alinhamento de valores.",
        "invertida": "Conflito interior, indecisão, desencontro afetivo ou má escolha."
    },
    {
        "id": 7,
        "nome": "O Carro",
        "imagem": "assets/images/7_o_carro.png",
        "normal": "Determinação, superação de obstáculos, foco e progresso veloz.",
        "invertida": "Perda de direção, falta de controle, impulsividade prejudicial."
    },
    {
        "id": 8,
        "nome": "A Justiça",
        "imagem": "assets/images/8_a_justica.png",
        "normal": "Clareza, causa e efeito, integridade, honestidade e imparcialidade.",
        "invertida": "Injustiça, desonestidade, desequilíbrio e fuga de responsabilidades."
    },
    {
        "id": 9,
        "nome": "O Eremita",
        "imagem": "assets/images/9_o_eremita.png",
        "normal": "Busca interior, introspecção, orientação sábia e prudência.",
        "invertida": "Isolamento doloroso, solidão excessiva, rejeição a conselhos."
    },
    {
        "id": 10,
        "nome": "A Roda da Fortuna",
        "imagem": "assets/images/10_a_roda_da_fortuna.png",
        "normal": "Ciclos da vida, destino, mudanças positivas e reviravoltas da sorte.",
        "invertida": "Fase de desafios, resistência a mudanças necessárias, azar temporário."
    },
    {
        "id": 11,
        "nome": "A Força",
        "imagem": "assets/images/11_a_forca.png",
        "normal": "Coragem serena, autocontrole, paciência e compaixão.",
        "invertida": "Dúvida de si mesmo, fraqueza, impulsos agressivos e desânimo."
    },
    {
        "id": 12,
        "nome": "O Enforcado",
        "imagem": "assets/images/12_o_enforcado.png",
        "normal": "Nova perspectiva, pausa voluntária, renúncia e entrega serena.",
        "invertida": "Sacrifício sem sentido, estagnação, resistência ao tempo certo."
    },
    {
        "id": 13,
        "nome": "A Morte",
        "imagem": "assets/images/13_a_morte.png",
        "normal": "Fim de um ciclo, transformação profunda, transição e renascimento.",
        "invertida": "Medo da mudança, apego ao passado e resistência ao inevitável."
    },
    {
        "id": 14,
        "nome": "A Temperança",
        "imagem": "assets/images/14_a_temperanca.png",
        "normal": "Equilíbrio, moderação, harmonia, paciência e cura interior.",
        "invertida": "Excessos, descompasso, impaciência e falta de harmonia."
    },
    {
        "id": 15,
        "nome": "O Diabo",
        "imagem": "assets/images/15_o_diabo.png",
        "normal": "Apego material, paixões cegas, tentação e identificação com sombras.",
        "invertida": "Libertação de vícios, quebra de amarras, consciência dos próprios limites."
    },
    {
        "id": 16,
        "nome": "A Torre",
        "imagem": "assets/images/16_a_torre.png",
        "normal": "Ruptura brusca, queda de ilusões, verdade revelada e transformação súbita.",
        "invertida": "Evitar um colapso iminente, adiamento de crise ou medo do desapego."
    },
    {
        "id": 17,
        "nome": "A Estrela",
        "imagem": "assets/images/17_a_estrela.png",
        "normal": "Esperança, inspiração, renovação espiritual e serenidade diante do futuro.",
        "invertida": "Falta de esperança, pessimismo, desânimo e desconfiança na vida."
    },
    {
        "id": 18,
        "nome": "A Lua",
        "imagem": "assets/images/18_a_lua.png",
        "normal": "Inconsciente, sonhos vívidos, intuição aguda, mas risco de ilusão e medos.",
        "invertida": "Dissipação de dúvidas, alívio de ansiedades e clareza de fatos ocultos."
    },
    {
        "id": 19,
        "nome": "O Sol",
        "imagem": "assets/images/19_o_sol.png",
        "normal": "Alegria, clareza, sucesso, vitalidade, calor humano e celebração.",
        "invertida": "Otimismo exagerado, tristeza momentânea ou dificuldade em ver o lado bom."
    },
    {
        "id": 20,
        "nome": "O Julgamento",
        "imagem": "assets/images/20_o_julgamento.png",
        "normal": "Despertar, chamado vocacional, reflexão sobre o passado e perdão.",
        "invertida": "Autocrítica severa, culpa paralisante e indecisão diante de escolhas."
    },
    {
        "id": 21,
        "nome": "O Mundo",
        "imagem": "assets/images/21_o_mundo.png",
        "normal": "Plenitude, encerramento triunfal de um ciclo, realização e sucesso global.",
        "invertida": "Falta de conclusão, tarefas inacabadas e busca de atalhos vazios."
    }
]