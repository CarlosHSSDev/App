import flet as ft
import os
from pages.utils import (
    navigation_drawer,
    _open_drawer,
    theme_system,
    navigate_to
)
from pages.Styles import Styles

class ConfigurationPage:
    def __init__(self, page):
        self.styles = Styles(page)
        self.page = page
        self.dark_mode = self.page.theme_mode.name == "DARK"
        self.page.bgcolor = self.styles.color_background_dark if self.dark_mode else self.styles.color_background_light
        self.screen()
        self.page.update()

    def screen(self):
        radio = ft.RadioGroup(
            value=self.page.theme_mode.name,
            content=ft.Column(
                [
                    ft.Radio(
                        "DARK",
                        value="DARK",
                        label_position=ft.LabelPosition.RIGHT,
                        toggleable=True,
                    ),
                    ft.Radio(
                        "LIGHT",
                        value="LIGHT",
                        label_position=ft.LabelPosition.RIGHT,
                        toggleable=True,
                    ),
                    ft.Radio(
                        "SYSTEM",
                        value="SYSTEM",
                        label_position=ft.LabelPosition.RIGHT,
                        toggleable=True,
                    ),
                ],
            ),
        )

        radio.on_change = lambda e: self.update_theme(e.control.value)

        container = ft.Container(
            expand=True,
            content=ft.ResponsiveRow(
                columns=6,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
                controls=[
                    ft.IconButton(
                        col=1,
                        icon=ft.icons.MENU,
                        icon_color=ft.colors.INVERSE_SURFACE,
                        on_click=lambda e: _open_drawer(
                            e, navigation_drawer(self.page, 2)
                        ),
                    ),
                    ft.Container(
                        height=40,
                        col=5,
                        padding=ft.padding.only(top=7),
                        content=ft.Text(
                            "Configurações do aplicativo",
                            max_lines=1,
                            style=self.styles.title_style(dark_mode=self.dark_mode, login_or_signin=False),
                        ),
                    ),
                    ft.Container(ft.Text(" "), height=40),
                    ft.Column(
                        [
                            ft.Text("Tema do aplicativo (BETA): "),
                            radio,
                        ],
                        col=5,
                    ),
                ],
            ),
        )
        self.page.add(container)

    def update_theme(self, theme):
        
        # Aplicar os estilos adequados
        if theme == "DARK":
            self.page.theme_mode = ft.ThemeMode.DARK
        elif theme == "LIGHT":
            self.page.theme_mode = ft.ThemeMode.LIGHT
        else:
            self.page.theme_mode = ft.ThemeMode.SYSTEM
        # Aqui você pode aplicar outros estilos nos elementos da página conforme necessário
        
        self.page.update()
        navigate_to(self.page, "configuration")




def main(page: ft.Page):
    ConfigurationPage(page)
    page.padding = ft.padding.only(top=40, bottom=40)
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#112053",
        )
    )
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.PRIMARY
    page.update()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
