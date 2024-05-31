from django.shortcuts import render
from giphy_emails.forms import EmailForm
import requests
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse


API_KEY = 'tsAk2y5Pi44mtiGXVFVUxRPP4dzjhPxv'

def fetch_gifs(keyword, lang='en'):
    url = f'https://api.giphy.com/v1/gifs/search?api_key={API_KEY}&q={keyword}&lang={lang}&limit=5'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        gifs = data.get('data', [])
        gif_urls = [gif.get('images', {}).get('fixed_height', {}).get('url') for gif in gifs]
        return gif_urls
    else:
        print("Failed to fetch GIFs.")
        return []

def base(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            selected_language = form.cleaned_data['language']
            print(f"Selected Language: {selected_language}")  # Print selected language to console
            gif_urls = fetch_gifs(keyword, selected_language)
            print("GIF URLS: ")
            for url in gif_urls:
                print(url)
            return render(request, 'preview.html', {'form': form, 'gif_urls': gif_urls})
    else:
        form = EmailForm()
    return render(request, 'base.html', {'form': form})


def send_email(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        message = request.POST.get('message')
        gif_url = request.POST.get('gif_url')

        # Send email using send_mail function
        try:
            send_mail(
                'Subject of the email',  # Subject of the email
                message,  # Message content
                'sender@example.com',  # Sender's email address
                [recipient],  # List of recipient email addresses
                html_message=f'<p>{message}</p><img src="{gif_url}" alt="GIF">'  # HTML content of the email
            )
            return HttpResponse('Email sent successfully!')
        except Exception as e:
            return HttpResponse(f'Failed to send email: {str(e)}')
    else:
        return HttpResponse('Invalid request method!')