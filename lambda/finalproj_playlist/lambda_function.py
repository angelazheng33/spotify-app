import json
import requests
from configparser import ConfigParser
from spotify import get_token, request

def lambda_handler(event, context):
    
    if "queryStringParameters" not in event: 
        return {
            'statusCode': 400, 
            'body': json.dumps("Missing Parameters")
        }
    if "genre" not in event["queryStringParameters"]: 
        return {
            'statusCode': 400, 
            'body': json.dumps("Missing genre")
        }
        
    genre = event["queryStringParameters"]["genre"]
    
    
    config_file = 'config.ini'
    configur = ConfigParser()
    configur.read(config_file)
    token = get_token(configur)
    if not token: 
        return {
            'statusCode': 500,
            'body': json.dumps("Token generation error")
        }
    
    #make sure to replace pop with user input
    data = request('/search', token, { 'q': 'genre:' + genre, 'type': 'artist', 'limit': 10 })
    artist_names = [artist['name'] for artist in data['artists']['items']]
    artist_id = [artist['id'] for artist in data['artists']['items']]
    playlist = []
    for i in range(len(artist_id)): 
        tracks = request('/artists/' + artist_id[i] + '/top-tracks', token, {'market': 'US'})
        song_name = tracks['tracks'][0]['name']
        playlist.append(song_name + " by " + artist_names[i])

    return {
        'statusCode': 200,
        'body': json.dumps(playlist)
    }
