from flet import (
    Page,
    colors,
    TextField,
    Container,
    alignment,
    ResponsiveRow,
    ButtonStyle,
    FilledButton,
    #    padding,
    Text,
    TextStyle,
    #    SnackBar,
    Row,
    Column,
    FilledTonalButton,
    FontWeight,
    MainAxisAlignment,
    CrossAxisAlignment,
)
from pages.security import User
from pages.utils import show_snackbar, create_container, navigate_to


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
        nome = TextField(bgcolor=colors.WHITE, color=colors.PRIMARY)
        email = TextField(bgcolor=colors.WHITE, color=colors.PRIMARY)
        senha = TextField(bgcolor=colors.WHITE, color=colors.PRIMARY, password=True, can_reveal_password=True)

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
                            color=colors.WHITE,
                            style=TextStyle(48, weight=FontWeight.BOLD),
                        ),
                    ),
                    create_container(
                        self.page,
                        col=5,
                        height=250,
                        content=Column(
                            [
                                Text("Nome", color=colors.WHITE),
                                nome,
                                Text("Email", color=colors.WHITE),
                                email,
                                Text("Senha", color=colors.WHITE),
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
                                    style=ButtonStyle(color=colors.PRIMARY, bgcolor=colors.ON_SURFACE),
                                    height=45,
                                    on_click=lambda e: navigate_to(self.page, "login"),
                                ),
                                FilledButton(
                                    "Me cadastrar",
                                    expand=True,
                                    col=2,
                                    height=45,
                                    style=ButtonStyle(color=colors.INVERSE_SURFACE, bgcolor=colors.PRIMARY_CONTAINER),
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
