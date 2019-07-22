import click
import requests
import sys
import time

from metaweather.exceptions import *


def get_url_content(url):
    max_retries = 2
    retry = 0
    while retry < max_retries:
        result = requests.get(url)
        if result.status_code == 200:
            if len(result.json()) > 0:
              return result.json()
            else:
              raise LocationUnavailableException('The location cannot be found in metaweather api.')
        time.sleep(2)
        retry += 1
    raise ServiceUnavailableException('The metaweather api is unavailable.')


def get_woeid(location):
    content = get_url_content('https://www.metaweather.com/api/location/search/?query=' + location)
    return content[0]['woeid']


def is_rainy_day(location_woeid):
    content = get_url_content('https://www.metaweather.com/api/location/' + str(location_woeid))
    weather_state_abbr = content['consolidated_weather'][0]['weather_state_abbr']
    return weather_state_abbr == 'hr' or weather_state_abbr == 'lr'


@click.command()
@click.argument('location')
def cli(location):
    try:
        location_woeid = get_woeid(location)
        is_rain = is_rainy_day(location_woeid)
    except LocationUnavailableException as exception:
        click.echo('Please retry with a new location available in metaweather.')
        sys.exit(1)
    except ServiceUnavailableException as exception:
        click.echo('Please retry in some minutes.')
        sys.exit(2)

    if is_rain:
        click.echo('The %s weather is rainy' % location)
    else:
        click.echo('The %s weather is not rainy' % location)
    sys.exit(0)


if __name__ == '__main__':
    cli('Paris')