import flet as ft


class Styles:
    def __init__(self, page: ft.Page):
        self.__page = page
        self.color_background_dark = "#2C2E8F"
        self.color_background_light = "#CECEF5"
        self.__color_bg_input_dark = "#D5D5D5"
        self.__color_bg_input_light = "#FFFFFF"
        self.__color_text_input_dark = "#2C2E8F"
        self.__color_text_input_light = "#6063DB"
        self.__primary_bg_btn_dark = "#6063DB"
        self.__secundary_bg_btn_dark = "#CECEF5"
        self.__primary_bg_btn_light = "#2C2E8F"
        self.__secundary_bg_btn_light = "#7273B5"
        self.__terciary_bg_btn = ft.colors.TRANSPARENT
        self.__primary_text_btn_dark = "#FFFFFF"
        self.__secundary_text_btn_dark = "#2C2E8F"
        self.__terciary_text_btn_dark = "#FFFFFF"
        self.__primary_text_btn_light = "#FFFFFF"
        self.__secundary_text_btn_light = "#FFFFFF"
        self.__terciary_text_btn_light = "#2C2E8F"
        self.__title_dark = "#FFFFFF"
        self.__title_light = "#2C2E8F"
        self.__weight_title = ft.FontWeight.BOLD
        self.text_description_dark = "#7273B5" 
        self.text_description_light = "#6063DB"
        self.__placeholder_dark = "#6063DB"
        self.__placeholder_light = "#CECEF5"
        self.__color_bg_card_dark = "#D9D9D9"
        self.__color_bg_card_light = "#FFFFFF"
        self.__text_card_dark = "#1F2061"
        self.__text_card_light = "#1F2061"
        self.__color_icon_green = "#0DA712"
        self.__color_icon_red = "#FF0000"
        self.__size_title_login_signin = 48
        self.__size_title = 24
        self.__weight_primary_btn = ft.FontWeight.BOLD
        self.__weight_secundary_btn = ft.FontWeight.W_500
        self.__weight_terciary_btn = ft.FontWeight.NORMAL
        self.__text_label_dark = "#FFFFFF"
        self.__text_label_light = "#2C2E8F"

    def button_style(self, order: str, dark_mode: bool) -> ft.ButtonStyle:
        if order == "primary":
            bgcolor = self.__primary_bg_btn_dark if dark_mode == True else self.__primary_bg_btn_light
            text_style = ft.TextStyle(
                weight=self.__weight_primary_btn,
            )
            color = self.__primary_text_btn_dark if dark_mode == True else self.__primary_text_btn_light
        elif order == "secundary":
            bgcolor = self.__secundary_bg_btn_dark if dark_mode == True else self.__secundary_bg_btn_light
            text_style = ft.TextStyle(
                weight=self.__weight_secundary_btn,
            )
            color = self.__secundary_text_btn_dark if dark_mode == True else self.__secundary_text_btn_light
        elif order == "terciary":
            bgcolor = self.__terciary_bg_btn
            text_style = ft.TextStyle(
                weight=self.__weight_terciary_btn,
            )
            color = self.__terciary_text_btn_dark if dark_mode == True else self.__terciary_text_btn_light

        else:
            raise ValueError("Order must be 'primary', 'secundary' or 'terciary'")
        return ft.ButtonStyle(bgcolor=bgcolor, text_style=text_style, color=color)
    
    def input_style(self, placeholder: str = "", dark_mode: bool = True, password: bool = False, can_reveal_password: bool = False, col=None, on_submit=None) -> ft.TextField:
        __input_style = ft.TextField(
            col=col,
            bgcolor = self.__color_bg_input_dark if dark_mode == True else self.__color_bg_input_light,
            color=self.__color_text_input_dark if dark_mode == True else self.__color_text_input_light,
            hint_text=placeholder,
            hint_style=ft.TextStyle(color=self.__placeholder_dark if dark_mode == True else self.__placeholder_light),
            password=password,
            can_reveal_password=can_reveal_password,
            on_submit=on_submit
        )
        return __input_style
    
    def title_style(self, dark_mode, login_or_signin: bool = False) -> ft.TextStyle:
        return ft.TextStyle(size=self.__size_title_login_signin if login_or_signin else self.__size_title, color=self.__title_dark if dark_mode else self.__title_light, weight=self.__weight_title)
    
    def label_input(self, dark_mode) -> ft.TextStyle:
        return ft.TextStyle(color=self.__text_label_dark if dark_mode == True else self.__text_label_light)
    
    def icon_button(self,icon, icon_size=30, icon_color = None, col=1, on_click=None, bg=None):
        if icon_color == None:
            icon_color = self.color_background_dark

        return ft.IconButton(
            icon=icon, icon_size=icon_size, icon_color=icon_color,col=col, on_click=on_click, bgcolor=ft.colors.WHITE if bg == None else bg)