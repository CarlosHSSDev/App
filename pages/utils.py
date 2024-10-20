from flet import SnackBar, Text, colors, padding, Container, alignment, SnackBar, Page, ButtonStyle
from yt_dlp import YoutubeDL
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
    ydl_opts = {
        "format": f"{format}",
        "outtmpl": "download/%(title)s.%(ext)s",
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get("title", None)
            video_ext = info_dict.get("ext", None)
            video_path = f"./download/{video_title}.{video_ext}"
            os.rename(video_path, f"./download/{video_title}.{ext}")
            e.control.style = save
            e.control.text = "Vídeo" if ext == "mp4" else "Audio"
            e.control.update()
            show_snackbar(page, "Download concluído com sucesso!", bgcolor=colors.GREEN)

            return 200
        
    except Exception as e:
        show_snackbar(page, "Download concluído com sucesso!", bgcolor=colors.GREEN)
        return 500
    

