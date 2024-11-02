from flet import (
    Page,
    app,
    ScrollMode,
    ColorScheme,
    ThemeMode,
    Theme,
    ProgressRing,
    colors,
    Column,
    MainAxisAlignment,
    CrossAxisAlignment,
    Text,
    TextAlign,
    IconButton,
    icons,
    TextField,
    Container,
    margin,
    alignment,
    ResponsiveRow,
    AlertDialog,
    FilledButton,
    FilledTonalButton,
    ButtonStyle,
    RoundedRectangleBorder,
    Image,
    ImageFit,
    TextOverflow,
    padding,
    WebView,
    Row,
    Stack,
    FontWeight,
)
import json
import requests
from pages.utils import (
    navigate_to, download, navigation_drawer, _open_drawer
)
from pages.Styles import Styles 


class VideoSearchApp:
    def __init__(self, page: Page):
        """Inicializa a aplicação de busca de vídeos."""
        self.page = page
        self.dark_mode = self.page.theme_mode.name == "DARK"
        self.page.scroll = ScrollMode.AUTO
        self.search_input = None
        self.video_list_column = None
        self.styles = Styles(page)
        page.bgcolor = self.styles.color_background_dark if self.dark_mode else self.styles.color_background_light
        self.loading_animation = ProgressRing(color= self.styles.color_background_light if self.dark_mode else self.styles.color_background_dark)

        self.initialize_ui()

    def initialize_ui(self):
        """Configura a interface inicial da aplicação."""
        self.video_list_column = Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                Text(
                    "Para aparecer os vídeos, faça a pesquisa acima e clique no ícone de pesquisa.",
                    text_align=TextAlign.CENTER,
                    color=self.styles.text_description_dark if self.dark_mode else self.styles.text_description_light,
                    #style=self.styles.label_input(dark_mode=self.dark_mode),
                    size=24,
                )
            ],
        )

        self.search_input = self.styles.input_style(
            placeholder="Pesquisar vídeos",
            dark_mode=self.dark_mode,
            col=4,
            on_submit=self.handle_search_click,
        )

        container = self.create_main_container()
        self.page.add(container)

    def create_main_container(self) -> Container:
        """Cria o container principal que contém a barra de pesquisa e a lista de vídeos."""
        return Container(
            expand=True,
            content=ResponsiveRow(
                columns=6,
                alignment=MainAxisAlignment.CENTER,
                expand=True,
                controls=[
                    self.styles.icon_button(icon=icons.MENU, col=1, bg=colors.TRANSPARENT, on_click=lambda e:  _open_drawer(e, navigation_drawer(self.page, 0))),
                    Container(
                        height=40,
                        col=5,
                        padding=padding.only(top=10),
                        content=Text(
                            "Bem vindo!",
                            max_lines=1,
                            style=self.styles.title_style(dark_mode=self.dark_mode, login_or_signin=False)
                        ),
                    ),
                    self.search_input,
                    self.styles.icon_button(
                        icon=icons.SEARCH,
                        on_click=self.handle_search_click,
                    ),
                    Container(
                        margin=margin.only(top=40),
                        col=5,
                        alignment=alignment.center,
                        content=self.video_list_column,
                    ),
                ],
            ),
        )

    def handle_search_click(self, e):
        """Função chamada quando o usuário clica no botão de pesquisa."""
        search_term = self.search_input.value
        self.search_input.update()
        if search_term:
            self.search_videos(search_term)

    def search_videos(self, query: str):
        """Realiza a pesquisa de vídeos com base no termo fornecido."""
        self.display_loading_animation()
        video_data = self.fetch_videos(query)
        self.display_videos(video_data)

    def display_loading_animation(self):
        """Exibe a animação de carregamento enquanto os vídeos são carregados."""
        self.video_list_column.controls.clear()
        self.video_list_column.controls.append(
            Container(width=70, height=70, content=self.loading_animation)
        )
        self.video_list_column.update()

    def fetch_videos(self, query: str) -> list:
        """Busca vídeos a partir de uma API externa e retorna os dados em formato de lista."""
        try:
            response = requests.get(
                f"https://test123124.pythonanywhere.com/fetch_videos?q={query}"
            )
            return json.loads(response.text)
        except requests.RequestException as e:
            print(f"Erro ao buscar vídeos: {e}")
            return []

    def display_videos(self, video_data: list):
        """Remove a animação de carregamento e exibe os vídeos na tela."""
        self.video_list_column.controls.clear()

        row_videos = ResponsiveRow(columns={"xs": 2, "md": 4, "xl": 7}, expand=True)

        for video in video_data:
            row_videos.controls.append(
                self.create_video_container(
                    video["Title"], video["Image URL"], video["Link"]
                )
            )

        # Adiciona o botão "Ver mais vídeos"
        if len(row_videos.controls) != 0:
            #row_videos.controls.append(self.create_load_more_button())
            row_videos.controls.append(
                Container(bgcolor=colors.TRANSPARENT, width=10, height=70, col=6)
            )

            self.video_list_column.controls.append(row_videos)
        else:
            
            row_videos.controls.append(
                Container(
                    Text(
                        color=colors.WHITE,
                        value="Ocorreu um erro ao pesquisar os vídeos, verifique sua conexão com a internet e tente novamente",
                    ),
                    padding=5,
                    bgcolor=colors.ERROR_CONTAINER,
                )
            )
            self.video_list_column.controls.append(row_videos)
        self.video_list_column.update()

    def custom_dialog(self, title, url):
        dlg = AlertDialog(
            content_padding=0,
            bgcolor=colors.TRANSPARENT,
            content=Stack(
                [
                    Container(
                        width=70,
                        height=70,
                        content=self.loading_animation,
                        expand=True,
                        alignment=alignment.center,
                    )
                ],
                alignment=alignment.center,
            ),
        )

        self.page.open(dlg)

        url_ = requests.get(
            f"https://test123124.pythonanywhere.com/selected_video?q={url}"
        )
        url = json.loads(url_.text)
        url = url["Link YouTube"]
        dlg.content = Container(
            border_radius=5,
            width=320,
            padding=padding.all(5),
            bgcolor=colors.WHITE,
            content=Container(
                content=ResponsiveRow(
                    [
                        WebView(url=url, height=200, width=340),
                        Text(
                            title,
                            col=3,
                            weight=FontWeight.BOLD,
                            color=self.styles.color_background_dark,
                            size=14,
                            overflow=TextOverflow.ELLIPSIS,
                            max_lines=6,
                        ),
                        Container(alignment=alignment.center, col=1, content=Text("Opções de\nDownload: ", color=self.styles.color_background_dark, expand=True)),
                        FilledTonalButton("Vídeo", expand=True, col=1,style=self.styles.button_style("secundary", self.dark_mode), on_click=lambda e: download(e, self.page, url, format="best", ext="mp4")),
                        FilledButton(
                            "Audio",
                            expand=True,
                            col=1,
                            style=self.styles.button_style("primary", self.dark_mode),
                            on_click=lambda e: download(e, self.page, url, format="bestaudio/best", ext="mp3")
                        ),
                    ],
                    columns=3,
                    spacing=10,
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER
                ),
            ),
        )

        dlg.update()

    def create_video_container(
        self, title: str, image_url: str, url: str
    ) -> FilledButton:
        """Cria o container para exibir cada vídeo individualmente."""
        return FilledButton(
            col=1,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(5), bgcolor=colors.WHITE
            ),
            content=Container(
                width=150,
                height=200,
                padding=5,
                content=Column(
                    [
                        Image(src=image_url, fit=ImageFit.COVER),
                        Text(
                            title,
                            color=self.styles.color_background_dark,
                            size=14,
                            overflow=TextOverflow.ELLIPSIS,
                            max_lines=4,
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    expand=True,
                    auto_scroll=True,
                ),
                on_click=lambda e: self.custom_dialog(title, url),
            ),
        )

    def create_load_more_button(self) -> FilledButton:
        """Cria um botão para carregar mais vídeos."""
        return FilledButton(
            col=1,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(5), bgcolor=colors.WHITE
            ),
            content=Container(
                padding=5,
                width=150,
                height=200,
                content=Column(
                    [
                        IconButton(icon=icons.ADD, icon_color=colors.WHITE),
                        Text("Ver mais vídeos", color=colors.WHITE, size=18),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
            ),
        )


def main(page: Page):
    VideoSearchApp(page)
    page.padding = padding.only(top=40)
    page.theme = Theme(color_scheme=ColorScheme(primary="#112053"))
    page.theme_mode = ThemeMode.DARK
    page.bgcolor = colors.PRIMARY
    page.update()



if __name__ == "__main__":
    app(target=main, assets_dir="assets")
