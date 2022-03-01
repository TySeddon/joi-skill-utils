# joi-skill-utils
The purpose of this project is to provide a central place for all shared and utility classes used by the Mycroft Skills developed for the Joi project.  By centralizing these classes, we not only share our code easier, but we also make our skills smaller.  In addition, this package install process will install all the necessary 3rd party Python packages, which simplifies the setup of skills on Mycroft.

# Required Packages
    pip install msk
    pip install munch
    pip install requests
    pip install pyyaml
    pip install google-api-python-client
    pip install google-auth-oauthlib
    pip install google-auth-httplib2
    pip install azure-ai-textanalytics==5.2.0b1
    pip install azure-ai-language-questionanswering    
    pip install spotipy==2.19.0
    pip install amcrest
    pip install numpy
    pip install pandas
    pip install ifaddr

# Running Example Scripts
*NOTE: the -m switch and use of module name (not script name)*
    python -m examples.test_joiclient

# Updating Version Information
Each time you edit this package's code, you will need to increment the version attribute  in setup.py.

# How to install this package from Git
Use this install this package into one of your virtual environments
    pip install git+https://github.com/TySeddon/joi-skill-utils

# 3rd API Documentation

## Spotify 

### Spotify Web API
Based on simple REST principles, the Spotify Web API endpoints return JSON metadata about music artists, albums, and tracks, directly from the Spotify Data Catalogue.

https://developer.spotify.com/documentation/web-api/reference/

#### Web Playback SDK
The Spotify Web Playback SDK is a public JavaScript SDK that allows you to implement local streaming playback of Spotify content in their web applications.

https://developer.spotify.com/documentation/web-playback-sdk/reference/

## Google Photos

## Amcrest Camera

## Azure Cognitive Services

### Azure Text Analytics Service

### Azure QnA Service