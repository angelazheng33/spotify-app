

import requests
import jsons

import uuid
import pathlib
import logging
import sys
import os
import base64

from configparser import ConfigParser
from getpass import getpass

############################################################
#
# prompt
#
def prompt():
  """
  Prompts the user and returns the command number

  Parameters
  ----------
  None

  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """
  print()
  print(">> Enter a command:")
  print("   0 => end")
  print("   1 => Make A Playlist")
  print("   2 => Get Artist Recommendations")
  print("   3 => Get Song Recommendations")
  cmd = input()

  if cmd == "":
    cmd = -1
  elif not cmd.isnumeric():
    cmd = -1
  else:
    cmd = int(cmd)

  return cmd


############################################################
#
# playlist
#
def playlist(baseurl):
  """
  Prints out all the users in the database

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    genres_string = """
    Pick genre: acoustic, afrobeat, alternative, ambient, anime, bluegrass, blues, bossanova, children, chill, classical, club, comedy, country, dance, disco, disney, dub, dubstep, edm, electro, electronic, emo, folk, funk, gospel, goth, grindcore, groove, grunge, guitar, happy, hard-rock, heavy-metal, hip-hop, holidays, honky-tonk, house, indie, industrial, j-pop, jazz, k-pop, kids, latin, latino, mandopop, metal, metalcore, movies, new-age, new-release, opera, party, philippines-opm, piano, pop, progressive-house, punk, r-n-b, rainy-day, reggae, reggaeton, road-trip, rock, rock-n-roll, rockabilly, romance, sad, salsa, samba, sertanejo, ska, sleep, songwriter, soul, soundtracks, spanish, study, summer, synth-pop, tango, techno, trance, trip-hop, work-out, world-music
    """

    print("Enter a genre: " + genres_string + ">")
    print("(type genre as listed)")
    genre = input()

    api = '/playlist'
    url = baseurl + api

    res = requests.get(url, params={"genre": genre})

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    body = res.json()

    print("\n")
    print("Generated " + genre + " playlist:" + "\n")
    for i in range(len(body)):
      print(str(i + 1) + ". " + body[i])
    #
    return

  except Exception as e:
    logging.error("playlist() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################
#
# artist_recommendations
#
def artist_recommendations(baseurl):
  """
  Prints out all the jobs in the database

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """

  print("Enter artist name>")
  artist = input()

  if not artist:
    print("No artist name entered")
    return

  try:
    #
    # call the web service:
    #
    api = '/artist-recommendations'
    url = baseurl + api
    res = requests.get(url, params={'artist': artist})

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      body = res.json()
      print("Error message:", body)
      return 

    body = res.json()

    print("\n")
    print("Recommended artists based on " + artist + ":" + "\n")
    for i in range(len(body)):
      print(str(i + 1) + ". " + body[i])
    #
    return

  except Exception as e:
    logging.error("artist_recommendations() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################
#
# song_features
#
def song_features(baseurl):
  """
  Resets the database back to initial state.

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    api = '/track-features'
    url = baseurl + api

    print(
        "Pick a track feature: danceability, energy, acousticness>"
    )
    feature = input()

    genres_string = """
    Enter a genre: acoustic, afrobeat, alternative, ambient, anime, bluegrass, blues, bossanova, children, chill, classical, club, comedy, country, dance, disco, disney, dub, dubstep, edm, electro, electronic, emo, folk, funk, gospel, goth, grindcore, groove, grunge, guitar, happy, hard-rock, heavy-metal, hip-hop, holidays, honky-tonk, house, indie, industrial, j-pop, jazz, k-pop, kids, latin, latino, mandopop, metal, metalcore, movies, new-age, new-release, opera, party, philippines-opm, piano, pop, progressive-house, punk, r-n-b, rainy-day, reggae, reggaeton, road-trip, rock, rock-n-roll, rockabilly, romance, sad, salsa, samba, sertanejo, ska, sleep, songwriter, soul, soundtracks, spanish, study, summer, synth-pop, tango, techno, trance, trip-hop, work-out, world-music
    """

    print("Pick genre: ", genres_string + ">")
    genre = input()

    res = requests.get(url, params={"feature": feature, "genre": genre})

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    body = res.json()

    print("\n")
    print("Recommended songs based on " + feature + ":" + "\n")
    for i in range(len(body)):
      print(str(i + 1) + ". " + body[i])
    #
    return

  except Exception as e:
    logging.error("track_features() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################
# main
#
try:
  print('** Welcome to Spotify App **')
  print()

  # eliminate traceback so we just get error message:
  sys.tracebacklimit = 0

  #
  # what config file should we use for this session?
  #
  config_file = 'client-config.ini'

  print("Config file to use for this session?")
  print("Press ENTER to use default, or")
  print("enter config file name>")
  s = input()

  if s == "":  # use default
    pass  # already set
  else:
    config_file = s

  #
  # does config file exist?
  #
  if not pathlib.Path(config_file).is_file():
    print("**ERROR: config file '", config_file, "' does not exist, exiting")
    sys.exit(0)

  #
  # setup base URL to web service:
  #
  configur = ConfigParser()
  configur.read(config_file)
  baseurl = configur.get('client', 'webservice')

  #
  # make sure baseurl does not end with /, if so remove:
  #
  if len(baseurl) < 16:
    print("**ERROR: baseurl '", baseurl, "' is not nearly long enough...")
    sys.exit(0)

  if baseurl == "https://YOUR_GATEWAY_API.amazonaws.com":
    print("**ERROR: update config file with your gateway endpoint")
    sys.exit(0)

  if baseurl.startswith("http:"):
    print("**ERROR: your URL starts with 'http', it should start with 'https'")
    sys.exit(0)

  lastchar = baseurl[len(baseurl) - 1]
  if lastchar == "/":
    baseurl = baseurl[:-1]

  #
  # initialize login token:
  #
  token = None

  #
  # main processing loop:
  #
  cmd = prompt()

  while cmd != 0:
    #
    if cmd == 1:
      playlist(baseurl)
    elif cmd == 2:
      artist_recommendations(baseurl)
    elif cmd == 3:
      song_features(baseurl)
    else:
      print("** Unknown command, try again...")
    #
    cmd = prompt()

  #
  # done
  #
  print()
  print('** done **')
  sys.exit(0)

except Exception as e:
  logging.error("**ERROR: main() failed:")
  logging.error(e)
  sys.exit(0)
