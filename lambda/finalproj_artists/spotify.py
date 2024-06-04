import requests

url = 'https://api.spotify.com/v1'

def get_token(config):
    spotify_client_id = config.get('spotify', 'client_id')
    spotify_client_secret = config.get('spotify', 'client_secret')

    url = 'https://accounts.spotify.com/api/token'
    payload = {'grant_type': 'client_credentials'}
    r = requests.post(url, auth=(spotify_client_id, spotify_client_secret), data=payload)

    if r.status_code != 200: 
        return None 
    return r.json()['access_token']
    
def request(endpoint, token, params): 
    headers = {'Authorization': 'Bearer ' + token}
    try: 
        r = requests.get(url + endpoint, headers=headers, params=params)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
        
    return r.json()