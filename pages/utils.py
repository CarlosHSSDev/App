from flet import (
    SnackBar,
    Text,
    colors,
    padding,
    Container,
    alignment,
    Page,
    ButtonStyle,
    NavigationDrawer,
    NavigationDrawerDestination,
    Divider,
    icons,
)
import requests
import os
import platform


# Função para criar Containers reutilizáveis
def create_container(page, col, color=colors.TRANSPARENT, height=200, content=None):
    return Container(
        bgcolor=color,
        col=col,
        height=height,
        content=content,
        alignment=alignment.center,
    )


# Função para navegar entre as páginas
def navigate_to(page, destination):
    page.clean()
    if destination == "home":
        from pages.HomePage import VideoSearchApp

        VideoSearchApp(page)
    elif destination == "signin":
        from pages.SigninPage import SigninPage

        SigninPage(page).build()
    elif destination == "login":
        from pages.LoginPage import LoginPage

        LoginPage(page).build()
    elif destination == "arquivos_baixados":
        from pages.Downloads import DownloadPage

        DownloadPage(page)
    page.update()


def show_snackbar(page, message, bgcolor=colors.RED_600, color=colors.WHITE):
    snackBar = SnackBar(
        Text(message, color=color),
        bgcolor=bgcolor,
        padding=padding.symmetric(vertical=50, horizontal=20),
    )
    page.overlay.append(snackBar)
    snackBar.open = True
    page.update()


# Função para obter o diretório apropriado conforme o sistema operacional
def get_download_directory():
    system = platform.system()
    if system == "Linux":  # Android roda em cima de Linux
        return "/storage/emulated/0/Download/"
    elif system == "Darwin":  # iOS é baseado em Darwin
        return os.path.expanduser("~/Documents/")
    else:
        # No caso de outros sistemas operacionais ou fallback
        return "./"


# Função para fazer download
def download(e, page: Page, url, format, ext):
    # Mudança de estilo do botão
    save = e.control.style
    e.control.style = ButtonStyle(
        bgcolor=colors.PRIMARY_CONTAINER,
        color=colors.WHITE,
        padding=padding.symmetric(5),
    )
    e.control.text = "aguarde"
    e.control.update()

    data = {
        "url": f"{url}",  # URL do vídeo a ser baixado
        "format": f"{format}",  # Formato do vídeo
        "ext": f"{ext}",  # Extensão do arquivo (mp4 ou mp3)
    }

    try:
        
        # Requisição para o servidor de download
        response = requests.post("https://ytdlp-1v9e.onrender.com/download", json=data)

        if response.status_code == 200:
            content = response.headers["Content-Disposition"]
            filenameExt = content.split(";")[1].split('="')[1][:-1]

            # Obter o diretório apropriado dinamicamente
            download_dir = get_download_directory()
            app_download_dir = os.path.join(download_dir, "downloads_app")

            # Verificar se o diretório 'downloads_app' existe, senão criar
            if not os.path.exists(app_download_dir):
                os.makedirs(app_download_dir)

            file_path = os.path.join(app_download_dir, filenameExt)
            
            # Escrever o arquivo no diretório de download
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            if ext == "mp4":
                #pegar e salvar a thumbnail
                response = requests.post("https://ytdlp-1v9e.onrender.com/thumbnail", json={"url": f"{url}"})
                print(response.headers)
                with open(f"{file_path.split(".mp4")[0]}_thumbnail.jpeg", "wb") as file:
                    file.write(response.content)

            show_snackbar(
                page, "Download concluído com sucesso!", bgcolor=colors.GREEN
            )
            
        else:
            show_snackbar(
                page,
                f"Ocorreu um erro tente novamente, caso não resolva reinicie o aplicativo!",
                bgcolor=colors.RED,
            )

        # Restaurar o estilo do botão
        e.control.style = save
        e.control.text = "Vídeo" if ext == "mp4" else "Áudio"
        e.control.update()

        return 200

    except Exception as e:
        show_snackbar(
            page,
            f"Ocorreu um erro ao processar o seu download, tente novamente! {str(e)}",
            bgcolor=colors.RED,
        )
        return 500


def navigation_drawer(page: Page, selected_index):
    drawer = NavigationDrawer(
        [
            Container(Text("Menu", size=30), padding=padding.only(left=20)),
            Divider(2),
            Container(height=10),
            NavigationDrawerDestination("Home", icon=icons.HOME),
            Container(height=10),
            NavigationDrawerDestination(
                "Arquivos Baixados", icon=icons.FILE_DOWNLOAD_DONE
            ),
            Container(height=10),
            Divider(2),
            Container(height=5),
            NavigationDrawerDestination("Configurações", icon=icons.ENGINEERING),
        ],
        selected_index=selected_index,
        on_change=lambda e: navigate_to(
            page, "home" if e.control.selected_index == 0 else "arquivos_baixados"
        ),
    )
    
    return drawer



def _open_drawer(e, drawer):
    e.control.page.drawer = drawer
    drawer.open = True
    e.control.page.update()
