import requests

API_KEY = 'tsAk2y5Pi44mtiGXVFVUxRPP4dzjhPxv'

def fetch_trending_gifs():
    url = f'https://api.giphy.com/v1/gifs/trending?api_key={API_KEY}&limit=5'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        gifs = data.get('data', [])
        for gif in gifs:
            print(gif.get('images', {}).get('fixed_height', {}).get('url'))
    else:
        print("Failed to fetch trending GIFs.")

# Call the function to fetch trending GIFs
fetch_trending_gifs()
