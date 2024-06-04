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
    if "feature" not in event["queryStringParameters"]: 
        return {
            'statusCode': 400, 
            'body': json.dumps("Missing feature")
        }
    if "genre" not in event["queryStringParameters"]: 
        return {
            'statusCode': 400, 
            'body': json.dumps("Missing genre")
        }
        
    feature = event["queryStringParameters"]["feature"]
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
    
    if feature == 'danceability':
        tracks = request('/recommendations', token, {'limit':5, 'market':'US', 'seed_genres': genre, 'target_danceability':0.90})
    elif feature == 'energy':
        tracks = request('/recommendations', token, {'limit':5, 'market': 'US', 'seed_genres': genre, 'target_energy':0.90})
    elif feature == 'acousticness':
        tracks = request('/recommendations', token, {'limit':5, 'market': 'US', 'seed_genres': genre, 'target_acousticness':0.90})
    else: 
        return {
            'statusCode': 400, 
            'body': json.dumps("invalid feature selection")
        }
    song_recommendations = []
    if len(tracks["tracks"]) == 0: 
        return {
            'statusCode': 400, 
            'body': json.dumps("invalid feature/genre combination")
        }
    for i in range(len(tracks['tracks'])): 
        song_name = tracks['tracks'][i]['name']
        artist_name = tracks['tracks'][i]['album']['artists'][0]['name']
        song_recommendations.append(song_name + " by " + artist_name)

    return {
        'statusCode': 200,
        'body': json.dumps(song_recommendations)
    }
