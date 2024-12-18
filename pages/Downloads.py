import flet as ft
import os
from pages.utils import get_download_directory, navigation_drawer, _open_drawer, show_snackbar
from pages.Styles import Styles

class DownloadPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.scroll = ft.ScrollMode.AUTO
        self.loading_animation = ft.ProgressRing(color=ft.colors.INVERSE_SURFACE)
        self.video_list_view = ft.ListView(
            expand=True, col=5, padding=ft.padding.only(top=40), spacing=10
        )  # Lista rolável de vídeos
        self.dark_mode = self.page.theme_mode.name == "DARK"
        self.styles = Styles(page)
        page.bgcolor = self.styles.color_background_dark if self.dark_mode else self.styles.color_background_light
        self.screen()

    def extract_thumbnail(self, file_path):
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(file_path):
                print(f"O arquivo {file_path} não foi encontrado.")
                return None, None

            # Extrai o nome do arquivo e o diretório
            file_name = os.path.basename(file_path)
            file_directory = os.path.dirname(file_path)

            return file_name

        except Exception as e:
            print(f"Ocorreu um erro ao processar o vídeo: {e}")
            return None, None

    def add_video_to_list(self, file_path):
        # Extrai a thumbnail e o nome do vídeo
        video_name = self.extract_thumbnail(file_path)
        if file_path.endswith(".mp4"):
            thumbnail_path = file_path.split(".mp4")[0]
            thumbnail_path = f"{thumbnail_path}_thumbnail.jpeg"
        else:
            thumbnail_path = "./assets/Icon_music.img"
        
        if thumbnail_path and video_name:
            # Cria um objeto de imagem e nome para o vídeo
            video_thumbnail = ft.Image(
                src=thumbnail_path,
                height=150,
                fit=ft.ImageFit.COVER,
                col={"xs": 3, "md": 1},
            )
            video_name_text = ft.Text(
                video_name, color=ft.colors.BLACK, expand=True, col={"xs": 2, "md": 1}, weight=ft.FontWeight.W_600
            )

            # Adiciona o vídeo na lista (com botões de download e excluir)
            self.video_list_view.controls.append(
                ft.Container(
                    bgcolor=ft.colors.WHITE,
                    padding=5,
                    border_radius=5,
                    content=ft.ResponsiveRow(
                        [
                            video_thumbnail,
                            video_name_text,
                            ft.Row(
                                col=1,
                                expand=True,
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.PLAY_ARROW,
                                        icon_color=ft.colors.GREEN,
                                        on_click=lambda e: self.play_video(
                                            file_path
                                        ),
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        icon_color=ft.colors.RED,
                                        on_click=lambda e: self.delete_video(
                                            video_name
                                        ),
                                    ),
                                ],
                            ),
                        ],
                        columns=3,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            )
            self.page.update()

    def screen(self):
        container = ft.Container(
            expand=True,
            content=ft.ResponsiveRow(
                columns=6,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
                controls=[
                    ft.IconButton(
                        col=1, icon=ft.icons.MENU, icon_color=ft.colors.INVERSE_SURFACE, on_click=lambda e: _open_drawer(e, navigation_drawer(self.page, 1))
                    ),
                    ft.Container(
                        height=40,
                        col=5,
                        padding=ft.padding.only(top=7),
                        content=ft.Text(
                            "Arquivos baixados",
                            max_lines=1,
                            style=ft.TextStyle(
                                size=24,
                                color=ft.colors.INVERSE_SURFACE,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                    ),
                    self.video_list_view,  # A lista de vídeos agora é um ListView
                ],
            ),
        )
        self.page.add(container)

        # Lista todos os arquivos no diretório
        directory = os.path.join(get_download_directory(), "downloads_app")
        for file_name in os.listdir(directory):
            # Obtém o caminho completo do arquivo
            file_path = os.path.join(directory, file_name)

            # Verifica se é um arquivo e se tem a extensão .mp4
            if os.path.isfile(file_path) and (file_path.endswith(".mp4") or file_path.endswith(".mp3")):
                # Adiciona o vídeo à lista
                self.add_video_to_list(file_path)

    def play_video(self, file_path):
        alert = ft.AlertDialog(content=ft.Video([ft.VideoMedia(file_path)], autoplay=True, show_controls=True, filter_quality=ft.FilterQuality.MEDIUM, playlist_mode=ft.PlaylistMode.LOOP), bgcolor=ft.colors.WHITE)
        self.page.open(alert)
        return
        

    def delete_video(self, file_path):
        show_snackbar(self.page, "Essa funcionalidade ainda está sendo criada!", bgcolor=ft.colors.BLUE)
        return


def main(page: ft.Page):
    DownloadPage(page)
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
