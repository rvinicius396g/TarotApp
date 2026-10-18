"""
main.py
Interface gráfica do Tarot com suporte à exibição de imagens das cartas.
"""

import os
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from cards_data import ARCANOS_MAIORES

# Dimensões da janela simulando um telemóvel
Window.size = (390, 800)


class TarotApp(App):
    def build(self):
        self.title = "Tarot Mobile - Protótipo com Imagens"

        # Layout vertical principal
        root = BoxLayout(orientation='vertical', padding=16, spacing=12)

        # Cabeçalho
        header = Label(
            text="[b]TAROT DOS ARCANOS[/b]",
            markup=True,
            font_size="22sp",
            size_hint_y=None,
            height=36,
            color=(0.95, 0.85, 0.5, 1)
        )
        root.add_widget(header)

        # Widget de Imagem da Carta (proporção mantida)
        self.card_image = Image(
            source="",  # Inicia vazio até o primeiro sorteio
            size_hint_y=None,
            height=260,
            allow_stretch=True,
            keep_ratio=True
        )
        root.add_widget(self.card_image)

        # Área de texto com barra de rolagem para explicações
        scroll_view = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text="Selecione uma tiragem abaixo para começar.",
            font_size="15sp",
            halign="center",
            valign="top",
            size_hint_y=None,
            color=(0.9, 0.9, 0.9, 1)
        )
        # Permite que o texto se auto-ajuste à largura da janela
        self.result_label.bind(width=lambda s, w: s.setter('text_size')(s, (w - 20, None)))
        self.result_label.bind(texture_size=lambda s, size: s.setter('height')(s, max(size[1], 150)))
        scroll_view.add_widget(self.result_label)
        root.add_widget(scroll_view)

        # Linha inferior de botões
        buttons_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=52, spacing=10)

        btn_one_card = Button(
            text="Carta do Dia",
            font_size="15sp",
            background_color=(0.3, 0.5, 0.8, 1)
        )
        btn_one_card.bind(on_press=self.tirar_uma_carta)
        buttons_box.add_widget(btn_one_card)

        btn_three_cards = Button(
            text="3 Cartas",
            font_size="15sp",
            background_color=(0.2, 0.6, 0.5, 1)
        )
        btn_three_cards.bind(on_press=self.tirar_tres_cartas)
        buttons_box.add_widget(btn_three_cards)

        root.add_widget(buttons_box)
        return root

    def atualizar_imagem(self, caminho_imagem):
        """Verifica se o ficheiro de imagem existe antes de tentar carregar."""
        if os.path.exists(caminho_imagem):
            self.card_image.source = caminho_imagem
            self.card_image.reload()
        else:
            # Se o ficheiro ainda não foi adicionado na pasta, limpa o widget sem dar erro
            self.card_image.source = ""

    def tirar_uma_carta(self, instance):
        """Sorteia uma única carta e atualiza a imagem e o texto."""
        carta = random.choice(ARCANOS_MAIORES)
        invertida = random.choice([True, False])
        posicao = "Invertida" if invertida else "Normal"
        significado = carta["invertida"] if invertida else carta["normal"]

        # Atualiza a imagem na tela
        self.atualizar_imagem(carta["imagem"])

        # Atualiza a descrição
        self.result_label.text = (
            f"[b]--- CARTA DO DIA ---[/b]\n\n"
            f"[size=18sp]{carta['nome']}[/size] ({posicao})\n\n"
            f"{significado}"
        )
        self.result_label.markup = True

    def tirar_tres_cartas(self, instance):
        """Sorteia três cartas para Passado, Presente e Futuro."""
        cartas = random.sample(ARCANOS_MAIORES, 3)
        posicoes = ["Passado", "Presente", "Futuro"]

        # Mostra a imagem da carta central (Presente) como destaque principal
        self.atualizar_imagem(cartas[1]["imagem"])

        texto = "[b]--- TIRAGEM DE 3 CARTAS ---[/b]\n\n"
        for i in range(3):
            invertida = random.choice([True, False])
            pos = "Invertida" if invertida else "Normal"
            sig = cartas[i]["invertida"] if invertida else cartas[i]["normal"]
            texto += f"[b]{posicoes[i]}:[/b] {cartas[i]['nome']} ({pos})\n{sig}\n\n"

        self.result_label.text = texto.strip()
        self.result_label.markup = True


if __name__ == '__main__':
    TarotApp().run()