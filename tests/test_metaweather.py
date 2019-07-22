import pytest
import requests

from click.testing import CliRunner
from metaweather.exceptions import *
from metaweather.metaweather import *


@pytest.mark.parametrize('url,location_woeid,json,status_code,exception', [
    ('https://www.metaweather.com/api/location/search/?query=london', 44418, [{"woeid": 44418}], 200, None),
    ('https://www.metaweather.com/api/location/search/?query=nantes', None, [], 200, LocationUnavailableException('The location cannot be found in metaweather api.')),
    ('https://www.metaweather.com/api/location/search/?query=paris', None, None, 503, ServiceUnavailableException('The metaweather api is unavailable.'))
])
def test_get_url_content(requests_mock, url, location_woeid, json, status_code, exception):
    requests_mock.register_uri(
        'GET',
        url,
        json=json,
        status_code=status_code
    )
    requests.Session().get(url)
    try:
        content = get_url_content(url)
    except (LocationUnavailableException, ServiceUnavailableException) as inst:
        assert isinstance(inst, type(exception))
        assert inst.args == exception.args
    else:
        assert content[0]['woeid'] == location_woeid


def test_get_woeid(requests_mock):
    requests_mock.get("https://www.metaweather.com/api/location/search/?query=london", json=[{'woeid': 44418}])
    assert get_woeid('London') == 44418


@pytest.mark.parametrize('url,location_woeid,weather_state_abbr,is_rainy', [
    ('https://www.metaweather.com/api/location/44418', 44418, 'hr', True),
    ('https://www.metaweather.com/api/location/615702', 615702, 'lr', True),
    ('https://www.metaweather.com/api/location/2487956', 2487956, 's', False)
])
def test_is_rainy_day(requests_mock, url, location_woeid, weather_state_abbr, is_rainy):
    requests_mock.get(url, json={'consolidated_weather': [{'weather_state_abbr': weather_state_abbr}]})
    assert is_rainy_day(location_woeid) == is_rainy


@pytest.mark.parametrize('url1,url2,location_woeid,weather_state_abbr,location,output,exit_code', [
    ('https://www.metaweather.com/api/location/search/?query=london', 'https://www.metaweather.com/api/location/44418', 44418, 'hr', 'London', 'The London weather is rainy\n', 0),
    ('https://www.metaweather.com/api/location/search/?query=paris', 'https://www.metaweather.com/api/location/2487956', 2487956, 's', 'Paris','The Paris weather is not rainy\n', 0)
])
def test_cli(requests_mock, url1, url2, location_woeid, weather_state_abbr, location, output, exit_code):
    requests_mock.get(url1, json=[{'woeid': location_woeid}])
    requests_mock.get(url2, json={'consolidated_weather': [{'weather_state_abbr': weather_state_abbr}]})
    runner = CliRunner()
    result = runner.invoke(cli, [location])
    assert result.output == output
    assert result.exit_code == exit_code