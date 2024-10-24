from flet import (
    Page,
    app,
    ScrollMode,
    ColorScheme,
    TextSpan,
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
    TextStyle,
    FontWeight,
    WebView,
    Row,
    Stack,
)
import json
import requests
from pages.utils import (
    navigate_to, download, navigation_drawer, _open_drawer
)  


class VideoSearchApp:
    def __init__(self, page: Page):
        """Inicializa a aplicação de busca de vídeos."""
        self.page = page
        self.page.scroll = ScrollMode.AUTO
        self.search_input = None
        self.video_list_column = None
        self.loading_animation = ProgressRing(color=colors.INVERSE_SURFACE)
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
                    color=colors.ON_SURFACE_VARIANT,
                    size=24,
                )
            ],
        )

        self.search_input = TextField(
            hint_text="Pesquisar vídeos",
            bgcolor=colors.INVERSE_SURFACE,
            col=4,
            on_submit=self.handle_search_click,
            text_style=TextStyle(color=colors.PRIMARY),
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
                    IconButton(
                        col=1, icon=icons.MENU, icon_color=colors.INVERSE_SURFACE, on_click=lambda e:  _open_drawer(e, navigation_drawer(self.page, 0))
                    ),
                    Container(
                        height=40,
                        col=5,
                        content=Text(
                            "Bem vindo!",
                            max_lines=1,
                            style=TextStyle(
                                size=24,
                                color=colors.INVERSE_SURFACE,
                                weight=FontWeight.BOLD,
                            ),
                        ),
                    ),
                    self.search_input,
                    IconButton(
                        icon=icons.SEARCH,
                        icon_size=30,
                        col=1,
                        bgcolor=colors.INVERSE_SURFACE,
                        icon_color=colors.PRIMARY,
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
        # self.search_input.value = ""
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
            row_videos.controls.append(self.create_load_more_button())
            row_videos.controls.append(
                Container(bgcolor=colors.TRANSPARENT, width=10, height=70, col=6)
            )

            self.video_list_column.controls.append(row_videos)
        else:
            row_videos.controls.append(
                Container(
                    Text(
                        color=colors.INVERSE_SURFACE,
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
            bgcolor=colors.INVERSE_SURFACE,
            content=Container(
                content=ResponsiveRow(
                    [
                        WebView(url=url, height=200, width=340),
                        Text(
                            title,
                            col=3,
                            weight=FontWeight.BOLD,
                            color=colors.PRIMARY,
                            size=14,
                            overflow=TextOverflow.ELLIPSIS,
                            max_lines=6,
                        ),
                        Container(alignment=alignment.center, col=1, content=Text("Opções de\nDownload: ", color=colors.PRIMARY, expand=True)),
                        FilledTonalButton("Vídeo", expand=True, col=1, on_click=lambda e: download(e, self.page, url, format="best", ext="mp4")),
                        FilledButton(
                            "Audio",
                            expand=True,
                            col=1,
                            style=ButtonStyle(color=colors.INVERSE_SURFACE),
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
                shape=RoundedRectangleBorder(5), bgcolor=colors.INVERSE_SURFACE
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
                            color=colors.PRIMARY,
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
            style=ButtonStyle(shape=RoundedRectangleBorder(5)),
            content=Container(
                padding=5,
                width=150,
                height=200,
                content=Column(
                    [
                        IconButton(icon=icons.ADD, icon_color=colors.INVERSE_SURFACE),
                        Text("Ver mais vídeos", color=colors.INVERSE_SURFACE, size=18),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
            ),
        )


def main(page: Page):
    # page.bgcolor = "#112053"
    VideoSearchApp(page)
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
