from pytube import YouTube

def download_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    stream.download(output_path='downloads')  # Salva na pasta 'downloads'

download_video('https://www.youtube.com/watch?v=us1mxpXdsDc')
