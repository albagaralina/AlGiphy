from django.shortcuts import render
from giphy_emails.forms import EmailForm
import requests

API_KEY = 'tsAk2y5Pi44mtiGXVFVUxRPP4dzjhPxv'

def fetch_gifs(lang='en'):
    url = f'https://api.giphy.com/v1/gifs/trending?api_key={API_KEY}&limit=5&lang={lang}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        gifs = data.get('data', [])
        gif_urls = [gif.get('images', {}).get('fixed_height', {}).get('url') for gif in gifs]
        return gif_urls
    else:
        print("Failed to fetch trending GIFs.")
        return []

def base(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            selected_language = form.cleaned_data['language']
            print(f"Selected Language: {selected_language}")  # Print selected language to console
            gif_urls = fetch_gifs(selected_language)
            print("Trending GIF URLS: ")
            for url in gif_urls:
                print(url)
            return render(request, 'base.html', {'form': form, 'gif_urls': gif_urls})
    else:
        form = EmailForm()
    return render(request, 'base.html', {'form': form})
