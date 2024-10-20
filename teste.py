import requests

json = {"url": r"https://www.youtube.com/watch?v=us1mxpXdsDc&embeds_referring_euri=https%3A%2F%2Frandomyoutube.net%2F&source_ve_path=Mjg2NjY&autoplay=1&controls=1&fs=1"}
response = requests.get(f"https://flet-360-carloshssdevs-projects.vercel.app/selected_video?q={json}")
print(response.content)