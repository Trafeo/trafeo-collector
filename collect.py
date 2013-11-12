#!/usr/bin/python2.7

""" Collection of traffic and weather data for trafeo """
import Collector
from Collector.Weather import Weather, Collect as WeatherCollect
import Collector.Weather.API.Client as WeatherAPI


# get the main configuration

config = Collector.get_config('main.conf')


def main():
    print 'Initialising import of traffic and weather data...'
    print ''
    print 'Retrieving weather data...'

    #todo make option to manually specify cities to process
    manual_cities = []

    try:
        weather = Weather(config)
        weather_api_client = WeatherAPI.Client(config['weather']['api']['token'], config['weather']['api']['endpoint'])
        weather_collector = WeatherCollect.Collect(config, weather_api_client, weather.get_db())

        #if there is a list of cities passed, process them, otherwise use the configured list
        if len(manual_cities) > 0:
            weather_collector.set_cities(manual_cities)
        else:
            weather_collector.set_cities(config['weather']['api']['cities'])

        # start collecting the weather data
        weather_collector.collect()

    except Exception as exc:
        print 'A general exception has occurred: %s' % exc.message
        raise exc

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print 'Exit due to user input'
