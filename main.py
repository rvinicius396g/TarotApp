"""
main.py
Aplicação principal de Tarot com gerenciamento de telas (Login e Mesa de Tarot).
"""

import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

import tarot_logic
from auth_service import AuthService

# Simulação do tamanho de tela de smartphone
Window.size = (390, 800)

# Instância global do serviço de autenticação
auth = AuthService()


class LoginScreen(Screen):
    """Tela inicial de autenticação do usuário."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=24, spacing=16)

        # Título de Boas-vindas
        titulo = Label(
            text="[b]TAROT MÍSTICO[/b]\n[size=16sp]Descubra o seu caminho[/size]",
            markup=True,
            font_size="24sp",
            halign="center",
            size_hint_y=None,
            height=80,
            color=(0.95, 0.85, 0.5, 1)
        )
        layout.add_widget(titulo)

        # Espaço reservado para ilustração ou ícone central
        espaco_central = Label(
            text="Faça login para salvar suas leituras\ne acessar o oráculo diariamente.",
            font_size="15sp",
            halign="center",
            color=(0.8, 0.8, 0.8, 1)
        )
        espaco_central.bind(width=lambda s, w: s.setter('text_size')(s, (w - 20, None)))
        layout.add_widget(espaco_central)

        # Botão: Entrar com Google
        btn_google = Button(
            text="Entrar com Google",
            font_size="16sp",
            size_hint_y=None,
            height=54,
            background_color=(0.85, 0.25, 0.2, 1)  # Vermelho Google
        )
        btn_google.bind(on_press=self.fazer_login_google)
        layout.add_widget(btn_google)

        # Botão: Entrar com Facebook
        btn_facebook = Button(
            text="Entrar com Facebook",
            font_size="16sp",
            size_hint_y=None,
            height=54,
            background_color=(0.23, 0.35, 0.6, 1)  # Azul Facebook
        )
        btn_facebook.bind(on_press=self.fazer_login_facebook)
        layout.add_widget(btn_facebook)

        self.add_widget(layout)

    def navegar_para_tarot(self):
        """Realiza a transição suave para a tela principal de Tarot."""
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'tarot_screen'
        # Atualiza a mensagem de boas-vindas com o usuário logado
        tarot_screen = self.manager.get_screen('tarot_screen')
        tarot_screen.atualizar_saudacao()

    def fazer_login_google(self, instance):
        auth.login_google()
        self.navegar_para_tarot()

    def fazer_login_facebook(self, instance):
        auth.login_facebook()
        self.navegar_para_tarot()


class TarotScreen(Screen):
    """Tela principal do jogo de Tarot onde as tiragens acontecem."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=16, spacing=10)

        # Barra de topo com identificação do usuário e botão Logout
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=36)
        self.lbl_usuario = Label(
            text="Olá, Viajante",
            font_size="13sp",
            halign="left",
            color=(0.7, 0.9, 0.7, 1)
        )
        self.lbl_usuario.bind(size=self.lbl_usuario.setter('text_size'))
        top_bar.add_widget(self.lbl_usuario)

        btn_logout = Button(
            text="Sair",
            size_hint=(None, 1),
            width=70,
            font_size="12sp",
            background_color=(0.5, 0.2, 0.2, 1)
        )
        btn_logout.bind(on_press=self.fazer_logout)
        top_bar.add_widget(btn_logout)
        layout.add_widget(top_bar)

        # Imagem da Carta Sorteada
        self.card_image = Image(
            source="",
            size_hint_y=None,
            height=250,
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(self.card_image)

        # Área de Leitura com Scroll
        scroll_view = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text="Selecione uma tiragem abaixo para iniciar.",
            font_size="15sp",
            halign="center",
            valign="top",
            size_hint_y=None,
            color=(0.9, 0.9, 0.9, 1)
        )
        self.result_label.bind(width=lambda s, w: s.setter('text_size')(s, (w - 20, None)))
        self.result_label.bind(texture_size=lambda s, size: s.setter('height')(s, max(size[1], 140)))
        scroll_view.add_widget(self.result_label)
        layout.add_widget(scroll_view)

        # Botões de Ação
        buttons_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=52, spacing=10)

        btn_one_card = Button(
            text="Carta do Dia",
            font_size="15sp",
            background_color=(0.3, 0.5, 0.8, 1)
        )
        btn_one_card.bind(on_press=self.acao_tirar_uma_carta)
        buttons_box.add_widget(btn_one_card)

        btn_three_cards = Button(
            text="3 Cartas",
            font_size="15sp",
            background_color=(0.2, 0.6, 0.5, 1)
        )
        btn_three_cards.bind(on_press=self.acao_tirar_tres_cartas)
        buttons_box.add_widget(btn_three_cards)

        layout.add_widget(buttons_box)
        self.add_widget(layout)

    def atualizar_saudacao(self):
        """Atualiza a mensagem superior com o nome do usuário autenticado."""
        if auth.usuario_atual:
            self.lbl_usuario.text = f"Conectado via {auth.usuario_atual['provedor']}"

    def atualizar_imagem(self, caminho_imagem):
        if os.path.exists(caminho_imagem):
            self.card_image.source = caminho_imagem
            self.card_image.reload()
        else:
            self.card_image.source = ""

    def acao_tirar_uma_carta(self, instance):
        carta = tarot_logic.tirar_uma_carta()
        self.atualizar_imagem(carta["imagem"])
        self.result_label.text = (
            f"[b]--- CARTA DO DIA ---[/b]\n\n"
            f"[size=18sp]{carta['nome']}[/size] ({carta['posicao']})\n\n"
            f"{carta['significado']}"
        )
        self.result_label.markup = True

    def acao_tirar_tres_cartas(self, instance):
        cartas = tarot_logic.tirar_tres_cartas()
        self.atualizar_imagem(cartas[1]["imagem"])

        texto = "[b]--- TIRAGEM DE 3 CARTAS ---[/b]\n\n"
        for c in cartas:
            texto += f"[b]{c['posicao_tiragem']}:[/b] {c['nome']} ({c['posicao']})\n{c['significado']}\n\n"

        self.result_label.text = texto.strip()
        self.result_label.markup = True

    def fazer_logout(self, instance):
        auth.logout()
        self.card_image.source = ""
        self.result_label.text = "Selecione uma tiragem abaixo para iniciar."
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login_screen'


class TarotApp(App):
    def build(self):
        self.title = "Tarot Mobile - com Login"
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(TarotScreen(name='tarot_screen'))
        return sm


if __name__ == '__main__':
    TarotApp().run()