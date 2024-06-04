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
    if "artist" not in event["queryStringParameters"]: 
        return {
            'statusCode': 400, 
            'body': json.dumps("Missing artist")
        }
        
    artist = event["queryStringParameters"]["artist"]
    
    
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
    data = request('/search', token, { 'q': 'artist:' + artist, 'type': 'artist', 'limit': 1 })
    artists = data['artists']['items']
    if len(artists) == 0: 
        return {
            'statusCode': 404,
            'body': json.dumps("Artist not found")
        }
    artist_id = artists[0]['id']
    song_recommendations = []
    artist_recommendations = request('/artists/' + artist_id + '/related-artists', token, {})
    artist_names = []
    for artist in artist_recommendations['artists']: 
        artist_names.append(artist["name"])
        if len(artist_names) >= 5: 
            break 

    return {
        'statusCode': 200,
        'body': json.dumps(artist_names)
    }
