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
                            "Login",
                            color=colors.WHITE,
                            style=TextStyle(48, weight=FontWeight.BOLD),
                        ),
                    ),
                    create_container(
                        self.page,
                        col=5,
                        height=200,
                        content=Column(
                            [
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
                        height=50,
                        content=Row(
                            [
                                FilledTonalButton(
                                    "Me cadastrar",
                                    col=2,
                                    expand=True,
                                    style=ButtonStyle(color=colors.PRIMARY, bgcolor=colors.ON_SURFACE),
                                    height=45,
                                    on_click=lambda e: navigate_to(self.page, "signin"),
                                ),
                                FilledButton(
                                    "Fazer login",
                                    col=2,
                                    expand=True,
                                    height=45,
                                    style=ButtonStyle(color=colors.INVERSE_SURFACE, bgcolor=colors.PRIMARY_CONTAINER),
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
                        content=Text("Esqueci minha senha!", color=colors.WHITE),
                    ),
                ],
            ),
        )
        self.page.add(container)
