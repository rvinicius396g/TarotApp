"""
main.py
Aplicação de Tarot Mobile com UI profissional, autenticação e histórico
de tiragens com persistência em SQLite.
"""

import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import platform

import tarot_logic
import database
from auth_service import AuthService

if platform not in ("android", "ios"):
    Window.size = (390, 800)
auth = AuthService()


class LoginScreen(Screen):
    """Ecrã de Login com layout centralizado e atmosfera mística."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root_layout = FloatLayout()

        with root_layout.canvas.before:
            Color(0.06, 0.05, 0.12, 1)
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)
        root_layout.bind(size=self._atualizar_fundo, pos=self._atualizar_fundo)

        caminho_bg = "assets/images/bg_tarot.png"
        if os.path.exists(caminho_bg):
            bg_imagem = Image(
                source=caminho_bg,
                allow_stretch=True,
                keep_ratio=False,
                opacity=0.35,
                size_hint=(1, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            root_layout.add_widget(bg_imagem)

        content_box = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=[22, 18, 22, 18],
            size_hint=(0.9, 0.88),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        with content_box.canvas.before:
            Color(0.12, 0.10, 0.22, 0.78)
            self.card_bg = RoundedRectangle(
                size=content_box.size,
                pos=content_box.pos,
                radius=[18, 18, 18, 18]
            )
        content_box.bind(size=self._atualizar_card, pos=self._atualizar_card)

        titulo = Label(
            text="[b]TAROT MISTICO[/b]",
            markup=True,
            font_size="23sp",
            size_hint_y=None,
            height=32,
            color=(0.96, 0.82, 0.38, 1)
        )
        subtitulo = Label(
            text="Descubra os segredos do seu destino",
            font_size="12sp",
            size_hint_y=None,
            height=20,
            color=(0.78, 0.75, 0.88, 1)
        )
        content_box.add_widget(titulo)
        content_box.add_widget(subtitulo)

        caminho_icone = "assets/images/0_o_louco.png"
        if os.path.exists(caminho_icone):
            icone_central = Image(
                source=caminho_icone,
                size_hint=(1, None),
                height=125,
                allow_stretch=True,
                keep_ratio=True
            )
            content_box.add_widget(icone_central)

        self.input_email = TextInput(
            hint_text="E-mail (ex: vinicius396g@gmail.com)",
            multiline=False,
            size_hint_y=None,
            height=42,
            font_size="13sp",
            padding=[12, 10, 12, 10],
            background_color=(0.18, 0.16, 0.30, 1),
            foreground_color=(0.96, 0.96, 1, 1),
            hint_text_color=(0.62, 0.60, 0.74, 1),
            cursor_color=(0.96, 0.82, 0.38, 1)
        )
        content_box.add_widget(self.input_email)

        self.input_senha = TextInput(
            hint_text="Senha (minimo 6 caracteres)",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=42,
            font_size="13sp",
            padding=[12, 10, 12, 10],
            background_color=(0.18, 0.16, 0.30, 1),
            foreground_color=(0.96, 0.96, 1, 1),
            hint_text_color=(0.62, 0.60, 0.74, 1),
            cursor_color=(0.96, 0.82, 0.38, 1)
        )
        content_box.add_widget(self.input_senha)

        self.lbl_status = Label(
            text="Entre com sua conta Firebase ou crie uma nova.",
            font_size="11sp",
            halign="center",
            size_hint_y=None,
            height=30,
            color=(0.82, 0.82, 0.88, 1)
        )
        self.lbl_status.bind(width=lambda s, w: s.setter('text_size')(s, (w - 10, None)))
        content_box.add_widget(self.lbl_status)

        btn_entrar = Button(
            text="Entrar com E-mail",
            font_size="14sp",
            size_hint_y=None,
            height=44,
            background_color=(0.24, 0.56, 0.44, 1),
            color=(1, 1, 1, 1)
        )
        btn_entrar.bind(on_press=self.fazer_login_firebase)
        content_box.add_widget(btn_entrar)

        btn_registrar = Button(
            text="Criar Nova Conta",
            font_size="13sp",
            size_hint_y=None,
            height=40,
            background_color=(0.32, 0.28, 0.56, 1),
            color=(0.96, 0.88, 0.55, 1)
        )
        btn_registrar.bind(on_press=self.registrar_conta_firebase)
        content_box.add_widget(btn_registrar)

        social_box = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=40
        )

        btn_google = Button(
            text="Google",
            font_size="13sp",
            background_color=(0.86, 0.27, 0.22, 1),
            color=(1, 1, 1, 1)
        )
        btn_google.bind(on_press=self.fazer_login_google)
        social_box.add_widget(btn_google)

        btn_facebook = Button(
            text="Facebook",
            font_size="13sp",
            background_color=(0.18, 0.40, 0.72, 1),
            color=(1, 1, 1, 1)
        )
        btn_facebook.bind(on_press=self.fazer_login_facebook)
        social_box.add_widget(btn_facebook)

        content_box.add_widget(social_box)

        root_layout.add_widget(content_box)
        self.add_widget(root_layout)

    def _atualizar_fundo(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def _atualizar_card(self, instance, value):
        self.card_bg.size = instance.size
        self.card_bg.pos = instance.pos

    def navegar_para_tarot(self):
        self.input_senha.text = ""
        self.lbl_status.text = "Entre com sua conta Firebase ou crie uma nova."
        self.lbl_status.color = (0.82, 0.82, 0.88, 1)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'tarot_screen'
        self.manager.get_screen('tarot_screen').ao_entrar_na_tela()

    def fazer_login_firebase(self, instance):
        email = self.input_email.text.strip()
        senha = self.input_senha.text.strip()
        resultado = auth.login_com_firebase(email, senha)
        if resultado.get("sucesso"):
            self.navegar_para_tarot()
        else:
            self.lbl_status.text = resultado.get("erro", "Falha ao autenticar.")
            self.lbl_status.color = (0.98, 0.42, 0.42, 1)

    def registrar_conta_firebase(self, instance):
        email = self.input_email.text.strip()
        senha = self.input_senha.text.strip()
        resultado = auth.registrar_com_firebase(email, senha)
        if resultado.get("sucesso"):
            self.navegar_para_tarot()
        else:
            self.lbl_status.text = resultado.get("erro", "Falha ao criar conta.")
            self.lbl_status.color = (0.98, 0.42, 0.42, 1)

    def fazer_login_google(self, instance):
        auth.login_google(nome="Junior")
        self.navegar_para_tarot()

    def fazer_login_facebook(self, instance):
        auth.login_facebook(nome="Junior")
        self.navegar_para_tarot()


class TarotScreen(Screen):
    """Ecrã da Mesa do Oráculo com acesso ao Histórico e gravação em SQLite."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root_layout = FloatLayout()

        with root_layout.canvas.before:
            Color(0.06, 0.05, 0.12, 1)
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)
        root_layout.bind(size=self._atualizar_fundo, pos=self._atualizar_fundo)

        caminho_bg = "assets/images/bg_tarot.png"
        if os.path.exists(caminho_bg):
            bg_imagem = Image(
                source=caminho_bg,
                allow_stretch=True,
                keep_ratio=False,
                opacity=0.30,
                size_hint=(1, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            root_layout.add_widget(bg_imagem)

        main_content = BoxLayout(
            orientation='vertical',
            padding=[16, 12, 16, 16],
            spacing=10,
            size_hint=(1, 1)
        )

        # Barra Superior: Nome do Utilizador, Botão Histórico e Botão Sair
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=42, spacing=8)

        user_badge = BoxLayout(orientation='horizontal', padding=[10, 0, 10, 0])
        with user_badge.canvas.before:
            Color(0.18, 0.16, 0.32, 0.75)
            self.badge_bg = RoundedRectangle(size=user_badge.size, pos=user_badge.pos, radius=[10])
        user_badge.bind(size=self._atualizar_badge, pos=self._atualizar_badge)

        self.lbl_usuario = Label(
            text="Conectado",
            font_size="12sp",
            color=(0.95, 0.85, 0.50, 1),
            halign="left",
            valign="middle"
        )
        self.lbl_usuario.bind(size=self.lbl_usuario.setter('text_size'))
        user_badge.add_widget(self.lbl_usuario)
        top_bar.add_widget(user_badge)

        # Botão para abrir o histórico
        btn_hist = Button(
            text="Histórico",
            size_hint=(None, 1),
            width=76,
            font_size="12sp",
            background_color=(0.28, 0.35, 0.60, 0.95),
            color=(1, 1, 1, 1)
        )
        btn_hist.bind(on_press=self.abrir_historico)
        top_bar.add_widget(btn_hist)

        btn_logout = Button(
            text="Sair",
            size_hint=(None, 1),
            width=58,
            font_size="12sp",
            background_color=(0.60, 0.20, 0.22, 0.9),
            color=(1, 1, 1, 1)
        )
        btn_logout.bind(on_press=self.fazer_logout)
        top_bar.add_widget(btn_logout)
        main_content.add_widget(top_bar)

        # Mesa central da carta
        table_card = BoxLayout(orientation='vertical', padding=[14, 12, 14, 12], spacing=8)
        with table_card.canvas.before:
            Color(0.10, 0.08, 0.20, 0.72)
            self.table_bg = RoundedRectangle(size=table_card.size, pos=table_card.pos, radius=[16])
        table_card.bind(size=self._atualizar_table, pos=self._atualizar_table)

        self.card_image = Image(
            source="",
            size_hint=(1, None),
            height=240,
            allow_stretch=True,
            keep_ratio=True
        )
        table_card.add_widget(self.card_image)

        scroll_view = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text="",
            font_size="14sp",
            halign="center",
            valign="top",
            size_hint_y=None,
            color=(0.92, 0.92, 0.96, 1)
        )
        self.result_label.bind(width=lambda s, w: s.setter('text_size')(s, (w - 10, None)))
        self.result_label.bind(texture_size=lambda s, size: s.setter('height')(s, max(size[1], 110)))
        scroll_view.add_widget(self.result_label)
        table_card.add_widget(scroll_view)

        main_content.add_widget(table_card)

        # Botões de Ação
        buttons_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=52, spacing=12)

        btn_one_card = Button(
            text="Carta do Dia",
            font_size="14sp",
            background_color=(0.26, 0.45, 0.78, 1),
            color=(1, 1, 1, 1)
        )
        btn_one_card.bind(on_press=self.acao_tirar_uma_carta)
        buttons_box.add_widget(btn_one_card)

        btn_three_cards = Button(
            text="Tiragem de 3",
            font_size="14sp",
            background_color=(0.20, 0.58, 0.46, 1),
            color=(1, 1, 1, 1)
        )
        btn_three_cards.bind(on_press=self.acao_tirar_tres_cartas)
        buttons_box.add_widget(btn_three_cards)

        main_content.add_widget(buttons_box)

        root_layout.add_widget(main_content)
        self.add_widget(root_layout)

    def _atualizar_fundo(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def _atualizar_badge(self, instance, value):
        self.badge_bg.size = instance.size
        self.badge_bg.pos = instance.pos

    def _atualizar_table(self, instance, value):
        self.table_bg.size = instance.size
        self.table_bg.pos = instance.pos

    def ao_entrar_na_tela(self):
        if auth.usuario_atual and "nome" in auth.usuario_atual:
            self.lbl_usuario.text = f"{auth.usuario_atual['nome']}, conectado!"
        else:
            self.lbl_usuario.text = "Conectado!"

        caminho_amostra = "assets/images/0_o_louco.png"
        if os.path.exists(caminho_amostra):
            self.card_image.source = caminho_amostra
            self.card_image.opacity = 0.55
        else:
            self.card_image.source = ""

        self.result_label.text = (
            "[b]O Oráculo aguarda sua pergunta[/b]\n\n"
            "Respire fundo, concentre-se na sua intenção e escolha uma das tiragens abaixo."
        )
        self.result_label.markup = True

    def atualizar_imagem(self, caminho_imagem):
        if os.path.exists(caminho_imagem):
            self.card_image.source = caminho_imagem
            self.card_image.opacity = 1.0
            self.card_image.reload()
        else:
            self.card_image.source = ""

    def acao_tirar_uma_carta(self, instance):
        carta = tarot_logic.tirar_uma_carta()
        self.atualizar_imagem(carta["imagem"])
        self.result_label.text = (
            f"[color=f5d160][b]CARTA DO DIA[/b][/color]\n\n"
            f"[size=17sp][b]{carta['nome']}[/b][/size] ({carta['posicao']})\n\n"
            f"{carta['significado']}"
        )
        self.result_label.markup = True

        # Grava no histórico SQLite
        nome_usuario = auth.usuario_atual["nome"] if auth.usuario_atual else "Convidado"
        texto_historico = f"{carta['nome']} ({carta['posicao']}): {carta['significado']}"
        database.salvar_tiragem(nome_usuario, "Carta do Dia", texto_historico)

    def acao_tirar_tres_cartas(self, instance):
        cartas = tarot_logic.tirar_tres_cartas()
        self.atualizar_imagem(cartas[1]["imagem"])

        texto = "[color=f5d160][b]TIRAGEM DE TRÊS CARTAS[/b][/color]\n\n"
        texto_para_banco = ""
        for c in cartas:
            bloco = f"[b]{c['posicao_tiragem']}:[/b] {c['nome']} ({c['posicao']})\n{c['significado']}\n\n"
            texto += bloco
            texto_para_banco += f"{c['posicao_tiragem']}: {c['nome']} ({c['posicao']}) | "

        self.result_label.text = texto.strip()
        self.result_label.markup = True

        # Grava no histórico SQLite
        nome_usuario = auth.usuario_atual["nome"] if auth.usuario_atual else "Convidado"
        database.salvar_tiragem(nome_usuario, "Tiragem de 3", texto_para_banco.rstrip(" | "))

    def abrir_historico(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'history_screen'
        self.manager.get_screen('history_screen').carregar_dados()

    def fazer_logout(self, instance):
        auth.logout()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login_screen'


class HistoryScreen(Screen):
    """Ecrã dedicado a exibir as tiragens anteriores guardadas no SQLite."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root_layout = FloatLayout()

        with root_layout.canvas.before:
            Color(0.06, 0.05, 0.12, 1)
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)
        root_layout.bind(size=self._atualizar_fundo, pos=self._atualizar_fundo)

        caminho_bg = "assets/images/bg_tarot.png"
        if os.path.exists(caminho_bg):
            bg_imagem = Image(
                source=caminho_bg,
                allow_stretch=True,
                keep_ratio=False,
                opacity=0.30,
                size_hint=(1, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            root_layout.add_widget(bg_imagem)

        content = BoxLayout(orientation='vertical', padding=[16, 12, 16, 16], spacing=10)

        # Cabeçalho do Histórico
        header_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=42, spacing=10)
        btn_voltar = Button(
            text="< Voltar",
            size_hint=(None, 1),
            width=80,
            font_size="13sp",
            background_color=(0.28, 0.35, 0.60, 0.95),
            color=(1, 1, 1, 1)
        )
        btn_voltar.bind(on_press=self.voltar)
        header_bar.add_widget(btn_voltar)

        lbl_titulo = Label(
            text="[b]HISTÓRICO DE LEITURAS[/b]",
            markup=True,
            font_size="15sp",
            color=(0.96, 0.82, 0.38, 1),
            halign="center",
            valign="middle"
        )
        lbl_titulo.bind(size=lbl_titulo.setter('text_size'))
        header_bar.add_widget(lbl_titulo)
        content.add_widget(header_bar)

        # Cartão com ScrollView para mostrar a lista de leituras
        card_hist = BoxLayout(orientation='vertical', padding=[12, 12, 12, 12])
        with card_hist.canvas.before:
            Color(0.10, 0.08, 0.20, 0.72)
            self.card_bg = RoundedRectangle(size=card_hist.size, pos=card_hist.pos, radius=[16])
        card_hist.bind(size=self._atualizar_card, pos=self._atualizar_card)

        scroll = ScrollView(size_hint=(1, 1))
        self.lbl_registos = Label(
            text="A carregar histórico...",
            markup=True,
            font_size="13sp",
            halign="left",
            valign="top",
            size_hint_y=None,
            color=(0.92, 0.92, 0.96, 1)
        )
        self.lbl_registos.bind(width=lambda s, w: s.setter('text_size')(s, (w - 10, None)))
        self.lbl_registos.bind(texture_size=lambda s, size: s.setter('height')(s, max(size[1], 150)))
        scroll.add_widget(self.lbl_registos)
        card_hist.add_widget(scroll)

        content.add_widget(card_hist)

        # Botão para limpar histórico
        btn_limpar = Button(
            text="Limpar Todo o Histórico",
            size_hint_y=None,
            height=46,
            font_size="13sp",
            background_color=(0.60, 0.20, 0.22, 0.9),
            color=(1, 1, 1, 1)
        )
        btn_limpar.bind(on_press=self.limpar_historico)
        content.add_widget(btn_limpar)

        root_layout.add_widget(content)
        self.add_widget(root_layout)

    def _atualizar_fundo(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def _atualizar_card(self, instance, value):
        self.card_bg.size = instance.size
        self.card_bg.pos = instance.pos

    def carregar_dados(self):
        """Lê os dados da base de dados e formata o texto para apresentação."""
        nome_usuario = auth.usuario_atual["nome"] if auth.usuario_atual else "Convidado"
        registos = database.obter_historico(nome_usuario)

        if not registos:
            self.lbl_registos.text = (
                "[color=aaaaaa]Ainda não realizou nenhuma tiragem.\n\n"
                "Volte à mesa do Tarot e consulte a Carta do Dia ou a Tiragem de 3![/color]"
            )
            return

        texto = ""
        for item in registos:
            texto += (
                f"[color=f5d160][b]{item['tipo']} - {item['data_hora']}[/b][/color]\n"
                f"{item['conteudo']}\n"
                f"[color=444455]----------------------------------------[/color]\n\n"
            )
        self.lbl_registos.text = texto.strip()

    def limpar_historico(self, instance):
        nome_usuario = auth.usuario_atual["nome"] if auth.usuario_atual else "Convidado"
        database.limpar_historico(nome_usuario)
        self.carregar_dados()

    def voltar(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'tarot_screen'


class TarotApp(App):
    def build(self):
        self.title = "Tarot Mobile"
        try:
            database.inicializar_banco()
            sm = ScreenManager()
            sm.add_widget(LoginScreen(name='login_screen'))
            sm.add_widget(TarotScreen(name='tarot_screen'))
            sm.add_widget(HistoryScreen(name='history_screen'))
            return sm
        except Exception:
            import traceback
            erro_txt = traceback.format_exc()
            return Label(
                text=f"Erro ao iniciar:\n{erro_txt}",
                font_size="11sp",
                halign="left",
                valign="middle"
            )


if __name__ == '__main__':
    TarotApp().run()