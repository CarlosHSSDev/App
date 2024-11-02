from flet import (
    Page,
    padding,
    app,
    ThemeMode
)
from pages.LoginPage import LoginPage
from pages.Styles import Styles

def main(page: Page):
    styles = Styles(page)
    page.theme_mode = ThemeMode.SYSTEM
    dark_mode = page.theme_mode.name == "DARK"
    page.bgcolor = styles.color_background_dark if dark_mode else styles.color_background_light
    page.padding = padding.only(top=40)
    
    LoginPage(page).build()

 
if __name__ == "__main__":
    app(target=main, assets_dir="assets")
