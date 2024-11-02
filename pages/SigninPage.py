from flet import (
    Page,
    alignment,
    ResponsiveRow,
    Row,
    Column,
    FilledTonalButton,
    FilledButton,
    MainAxisAlignment,
    CrossAxisAlignment,
    Text,
    Container
)
from pages.security import User
from pages.utils import show_snackbar, create_container, navigate_to
from pages.Styles import Styles


class SigninPage:
    def __init__(self, page: Page):
        self.page = page

    def do_signup(self, nome, email, senha):
        if nome and email and senha:
            User(email, senha, nome).cadastro()
            navigate_to(self.page, "home")
        else:
            show_snackbar(self.page, "Algum dos campos está vazio!")

    def build(self):
        styles = Styles(self.page)
        dark_mode = self.page.theme_mode.name == "DARK"
        nome = styles.input_style(dark_mode=dark_mode)
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
                            "Cadastro",
                            style=styles.title_style(dark_mode, login_or_signin=True),
                        ),
                    ),
                    create_container(
                        self.page,
                        col=5,
                        height=250,
                        content=Column(
                            [
                                Text("Nome", style=styles.label_input(dark_mode)),
                                nome,
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
                        height=100,
                        content=Row(
                            [
                                FilledTonalButton(
                                    "Fazer login",
                                    expand=True,
                                    col=2,
                                    style=styles.button_style("secundary", dark_mode),
                                    height=45,
                                    on_click=lambda e: navigate_to(self.page, "login"),
                                ),
                                FilledButton(
                                    "Me cadastrar",
                                    expand=True,
                                    col=2,
                                    height=45,
                                    style=styles.button_style("primary", dark_mode),
                                    on_click=lambda e: self.do_signup(
                                        nome.value, email.value, senha.value
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
            ),
        )
        self.page.add(container)
