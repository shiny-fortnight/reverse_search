# System imports
import json

# Third-party dependencies
from geopy import Nominatim
import requests
import twython as tw
from motionless import DecoratedMap, LatLonMarker

WHITE_PAGES_API_KEY = 'ea04b1f16b56a1b1a21b0159b8b1990e'

TWITTER_KEY = 'YABlxDeSUvuJGLcJoGsuFpCvA'
TWITTER_SECRET = 'ALttKP1BNhsRqvGL2PR9mkcGwdgh3gKs05v8pfjJrLElrxjQ8L'
TWITTER_TOKEN = '4840597894-HxW7lZoZQIbmkEHTjfaeb9wCDVZyLNPxAvczMZr'
TWITTER_TOKEN_SECRET = 'ULfOa5W84nJCj5mEvULVqtmTDFWI2x8ooqgvzNonVqhIR'

SEARCH_RADIUS = '100'  # tweet search radius
SEARCH_UNITS = 'mi'

TWITTER = tw.Twython(
    TWITTER_KEY, TWITTER_SECRET, TWITTER_TOKEN, TWITTER_TOKEN_SECRET)


def query_white_pages(phone_number):
    '''
        Returns the address of an input phone number
    '''
    req = 'https://proapi.whitepages.com/2.1/phone.json?api_key=%s&phone_number=%s' % (WHITE_PAGES_API_KEY,
                                                                                       phone_number)
    result = requests.get(req)

    asDict = json.loads(result.text)

    locationValues = asDict['results'][0]['best_location']

    locKeys = ['standard_address_line1', 'standard_address_line2',
               'city', 'standard_address_location']
    streetAddr = ''

    for name in locKeys:
        streetAddr += locationValues[name] + \
            ' ' if locationValues[name] else ''

    return streetAddr


def create_twitter_map(coordinates):
    dmap = DecoratedMap()

    for coordinate in coordinates:
        if coordinate is None:
            continue

        lon = coordinate[0]
        lat = coordinate[1]

        tweet_marker = LatLonMarker(lat=lat, lon=lon)
        dmap.add_marker(tweet_marker)

    return dmap.generate_url()


def search_twitter(phone_number=None, keywords=None):
    if phone_number is None or not phone_number.isdigit():
        return ValueError('Invalid phone #')

    if keywords is '' or keywords is None:
        return ValueError("No keywords provided")

    streetAddr = query_white_pages(phone_number)

    geolocator = Nominatim()
    location = geolocator.geocode(streetAddr)

    if location is None:
        return ValueError('Invalid phone #')

    lat, lon = location.latitude, location.longitude

    tweets = []
    tweet_coordinates = []
    geocode = '%s,%s,%s%s' % (lat, lon, SEARCH_RADIUS, SEARCH_UNITS)
    keywords = keywords.split(',')

    for keyword in keywords:
        result = TWITTER.search(q=keyword, count=100, geocode=geocode)
        num_tweets = len(result['statuses'])

        for tweet in range(num_tweets):
            tweet_text = result['statuses'][tweet]['text']
            name = result['statuses'][tweet]['user']['screen_name']
            coordinates = result['statuses'][tweet]['coordinates']

            if coordinates is not None:
                coordinates = coordinates['coordinates']

            tweets.append(["@%s: %s %s" % (name, tweet_text, coordinates)])
            tweet_coordinates.append(coordinates)

    map_url = create_twitter_map(tweet_coordinates)

    return tweets, map_url

if __name__ == '__main__':
    search_twitter('6176354500', 'sex')
