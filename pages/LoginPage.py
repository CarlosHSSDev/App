from flet import (
    Page,
    colors,
    TextField,
    Container,
    alignment,
    ResponsiveRow,
    FilledButton,
    BorderSide,
    # padding,
    Text,
    ButtonStyle,
    TextStyle,
    # SnackBar,
    Row,
    Column,
    FilledTonalButton,
    FontWeight,
    MainAxisAlignment,
    CrossAxisAlignment,
)
from pages.security import User
from pages.utils import show_snackbar, create_container, navigate_to
from pages.Styles import Styles
import requests


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def do_login(self, email, senha):
        if email and senha:
            if User(email, senha).login() == 200:
                navigate_to(self.page, "home")
            else:
                show_snackbar(
                    self.page,
                    "Seu login está incorreto, verifique seu email e sua senha!",
                )
        else:
            show_snackbar(self.page, "Algum dos campos está vazio!")

    def build(self):
        styles = Styles(self.page)
        dark_mode = self.page.theme_mode.name == "DARK"
        email = styles.input_style(dark_mode=dark_mode)
        senha = styles.input_style(dark_mode=dark_mode, password=True, can_reveal_password=True)

        container = Container(
            expand=True,
            alignment=alignment.center,
            content=ResponsiveRow(
                columns=6,
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    create_container(
                        self.page,
                        col=5,
                        height=70,
                        content=Text(
                            "Login",
                            style=styles.title_style(dark_mode, login_or_signin=True),
                        ),
                    ),
                    create_container(
                        self.page,
                        col=5,
                        height=200,
                        content=Column(
                            [
                                Text("Email", style=styles.label_input(dark_mode)),
                                email,
                                Text("Senha", style=styles.label_input(dark_mode)),
                                senha,
                            ],
                            alignment=MainAxisAlignment.SPACE_EVENLY,
                        ),
                    ),
                    create_container(
                        self.page,
                        col=5,
                        height=50,
                        content=Row(
                            [
                                FilledTonalButton(
                                    "Me cadastrar",
                                    col=2,
                                    expand=True,
                                    style=styles.button_style("secundary", dark_mode),
                                    height=45,
                                    on_click=lambda e: navigate_to(self.page, "signin"),
                                ),
                                FilledButton(
                                    "Fazer login",
                                    col=2,
                                    expand=True,
                                    height=45,
                                    style=styles.button_style("primary", dark_mode),
                                    on_click=lambda e: self.do_login(
                                        email.value, senha.value
                                    ),
                                ),
                            ]
                        ),
                    ),
                    create_container(
                        self.page,
                        col=3,
                        height=30,
                        content=FilledButton("Esqueci minha senha!", style=styles.button_style("terciary", dark_mode),),
                    ),
                ],
            ),
        )
        self.page.add(container)
        try:
            requests.get("https://ytdlp-1v9e.onrender.com/")
        except:
            pass
