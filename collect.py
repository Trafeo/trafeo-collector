#!/usr/bin/python2.7

""" Collection of traffic and weather data for trafeo """
import Collector
from Collector.Weather import Collect as WeatherCollect
import Collector.Weather.API.Client as WeatherAPI
import argparse
import time


p = argparse.ArgumentParser(description='Trafeo collector agent')
p.add_argument('--verbose', '-v', default=None, help="Run in verbose mode")

# todo imlement at some point?
#p.add_argument('--retry', '-r', default=2, metavar='N', type=int, help="If any API fails, retry N times")

p.add_argument('--interval', '-i', default=900, metavar='N', type=int, help="Collect data every N seconds")
args = p.parse_args()

# get the main configuration
config = Collector.get_config('main.conf')

def main():

    while True:

        print 'Initialising import of traffic and weather data...'
        print ''
        print 'Retrieving weather data...'

        #todo make option to manually specify cities to process
        manual_cities = []

        try:
            collector = Collector.Collector(config)
            logger = collector.get_logger()
            db = collector.get_db()

            weather_api_client = WeatherAPI.Client(config['weather']['api']['token'], config['weather']['api']['endpoint'], logger)
            weather_collector = WeatherCollect.Collect(config, weather_api_client, db)

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

        print '\n Resuming collecion task in %d seconds.' % args.interval
        # rest until the interval timer has expired
        time.sleep(args.interval)

if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt:
        print 'Exit due to user input'
