from django.shortcuts import render, redirect
from giphy_emails.forms import EmailForm
import requests
from django.core.mail import send_mail
from django.http import HttpResponse

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from io import BytesIO

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
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            subject = form.cleaned_data.get('subject', 'Subject of the email')  # Default subject if not provided
            message = form.cleaned_data['message']
            gif_url = request.POST.get('gif_url')

            # Download the GIF from the URL
            response = requests.get(gif_url)
            if response.status_code == 200:
                gif_data = response.content
                gif_filename = 'image.gif'  # You can set a custom filename here
                print('gif_url', gif_url)
            else:
                # Handle the case where the GIF cannot be downloaded
                print("Failed to download GIF")
                print("Form errors:", form.errors)
                return redirect('error')

            # Prepare email content
            html_content = render_to_string('email_template.html', {'recipient': recipient, 'subject': subject, 'message': message, 'gif_url': gif_url})
            text_content = strip_tags(html_content)

            # Send email using EmailMultiAlternatives
            try:
                email = EmailMultiAlternatives(subject, text_content, 'alba@revenuehive.io', [recipient])
                email.attach_alternative(html_content, "text/html")
                
                # Attach the GIF to the email
                email.attach(gif_filename, gif_data, 'image/gif')

                print('email', email, gif_url, subject)
                
                email.send()
                print("Email sent successfully")  # Debug print

                return redirect('success')  # Redirect to success page
            except Exception as e:
                print(f"Error sending email: {e}")  # Debug print
                return redirect('error')  # Redirect to error page
        else:
            # If form is invalid, handle it appropriately
            print("Form is invalid")
            print("Form errors:", form.errors)
           
            return redirect('error')  # Redirect to error page

    # If request method is not POST, handle it appropriately, perhaps render a form again
    # For example:
    form = EmailForm()
    return render(request, 'base.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def error(request):
    return render(request, 'error.html')