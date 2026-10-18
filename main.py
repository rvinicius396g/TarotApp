"""
main.py
Interface do usuário e lógica de tiragem de cartas usando Kivy.
"""

import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Importa a nossa lista com os 22 Arcanos Maiores
from cards_data import ARCANOS_MAIORES

# Define o tamanho inicial da janela simulando um smartphone moderno (ex: 390x844)
Window.size = (390, 800)


class TarotApp(App):
    def build(self):
        self.title = "Tarot Mobile - Protótipo"

        # Layout raiz vertical com espaçamento
        root = BoxLayout(orientation='vertical', padding=18, spacing=14)

        # Cabeçalho da aplicação
        header = Label(
            text="[b]TAROT DOS ARCANOS[/b]",
            markup=True,
            font_size="22sp",
            size_hint_y=None,
            height=40,
            color=(0.95, 0.85, 0.5, 1)  # Tom dourado suave
        )
        root.add_widget(header)

        # Área de rolagem para o texto do resultado (garante que caiba no celular)
        scroll_view = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text="Bem-vindo ao Tarot!\nEscolha uma das tiragens abaixo para iniciar sua leitura.",
            font_size="15sp",
            halign="center",
            valign="middle",
            size_hint_y=None,
            color=(0.9, 0.9, 0.9, 1)
        )
        # Permite que o texto se ajuste automaticamente à largura e altura da tela
        self.result_label.bind(width=lambda s, w: s.setter('text_size')(s, (w - 20, None)))
        self.result_label.bind(texture_size=lambda s, size: s.setter('height')(s, max(size[1], 300)))
        scroll_view.add_widget(self.result_label)
        root.add_widget(scroll_view)

        # Container para os botões de ação
        buttons_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=52, spacing=10)

        # Botão 1: Carta do Dia
        btn_one_card = Button(
            text="Carta do Dia",
            font_size="15sp",
            background_color=(0.3, 0.5, 0.8, 1)
        )
        btn_one_card.bind(on_press=self.tirar_uma_carta)
        buttons_box.add_widget(btn_one_card)

        # Botão 2: Três Cartas (Passado, Presente e Futuro)
        btn_three_cards = Button(
            text="3 Cartas",
            font_size="15sp",
            background_color=(0.2, 0.6, 0.5, 1)
        )
        btn_three_cards.bind(on_press=self.tirar_tres_cartas)
        buttons_box.add_widget(btn_three_cards)

        root.add_widget(buttons_box)
        return root

    def sortear_carta(self, carta_dict):
        """
        Recebe o dicionário da carta e decide aleatoriamente
        se ela saiu na posição normal ou invertida.
        """
        invertida = random.choice([True, False])
        posicao = "Invertida" if invertida else "Normal"
        significado = carta_dict["invertida"] if invertida else carta_dict["normal"]
        return f"{carta_dict['nome']} ({posicao})\n{significado}"

    def tirar_uma_carta(self, instance):
        """Sorteia uma única carta do baralho."""
        carta = random.choice(ARCANOS_MAIORES)
        resultado = self.sortear_carta(carta)
        self.result_label.text = f"[b]--- CARTA DO DIA ---[/b]\n\n{resultado}"
        self.result_label.markup = True

    def tirar_tres_cartas(self, instance):
        """Sorteia três cartas sem repetição para Passado, Presente e Futuro."""
        cartas_sorteadas = random.sample(ARCANOS_MAIORES, 3)
        posicoes = ["Passado", "Presente", "Futuro"]
        
        texto_final = "[b]--- TIRAGEM DE 3 CARTAS ---[/b]\n\n"
        for i in range(3):
            detalhe = self.sortear_carta(cartas_sorteadas[i])
            texto_final += f"[b]{posicoes[i]}:[/b]\n{detalhe}\n\n"

        self.result_label.text = texto_final.strip()
        self.result_label.markup = True


if __name__ == '__main__':
    TarotApp().run()