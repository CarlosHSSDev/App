from flet import (
    Page,
    padding,
    app,
    Theme,
    ThemeMode,
    ColorScheme,
    colors
)
from pages.LoginPage import LoginPage

def main(page: Page):
    page.bgcolor = "#112053"
    LoginPage(page).build()
    page.padding = padding.only(top=40)
    page.theme = Theme(
        color_scheme=ColorScheme(
            primary="#112053",
        )
    )

    page.theme_mode = ThemeMode.DARK
    page.bgcolor = colors.PRIMARY
    page.update()


if __name__ == "__main__":
    app(target=main, assets_dir="assets")
