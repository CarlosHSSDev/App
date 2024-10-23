from flet import SnackBar, Text, colors, padding, Container, alignment, SnackBar, Page, ButtonStyle
from yt_dlp import YoutubeDL
import requests
import os


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
    page.update()

def show_snackbar(page, message, bgcolor=colors.RED_600, color=colors.WHITE):
    snackbar = SnackBar(
        Text(message, color=color,),
        bgcolor=bgcolor,
        
        padding=padding.symmetric(vertical=50, horizontal=20),
    )
    page.overlay.append(snackbar)
    snackbar.open = True
    page.update()


def download(e, page: Page, url, format, ext):
    save = e.control.style
    e.control.style = ButtonStyle(bgcolor=colors.PRIMARY_CONTAINER, color=colors.WHITE, padding=padding.symmetric(5))
    e.control.text = "aguarde"
    e.control.update()
    data = {
        "url": f"{url}",  # Substitua pela URL do vídeo que você deseja testar
        "format": f"{format}",  # Ou outro formato desejado
        "ext": f"{ext}"       # Ou "mp3" para áudio
    }

    try:
        response = requests.post("https://ytdlp-1v9e.onrender.com/download", json=data)

        if response.status_code == 200:
            content = response.headers["Content-Disposition"]
            filenameExt = content.split(";")[1].split("=\"")[1][:-1]
            with open(f"./download/{filenameExt}", 'wb') as f:  # Altere a extensão conforme necessário
                f.write(response.content)
            print("Download concluído com sucesso!")
            show_snackbar(page, "Download concluído com sucesso!", bgcolor=colors.GREEN)
        else:
            print(f"Erro: {response.status_code} - {response.json()}")
    
        e.control.style = save
        e.control.text = "Vídeo" if ext == "mp4" else "Audio"
        e.control.update()
        

        return 200
        
    except Exception as e:
        show_snackbar(page, "Ocorreu um erro ao processar o seu download tente novamente!", bgcolor=colors.RED)
        return 500
    

