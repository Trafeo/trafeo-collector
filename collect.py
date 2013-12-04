#!/usr/bin/python2.7

""" Collection of traffic and weather data for trafeo """
import Collector

from Collector.Weather import Collect as WeatherCollect
import Collector.Weather.API.Client as WeatherAPI

from Collector.Traffic import Collect as TrafficCollect
import Collector.Traffic.API.Client as TrafficAPI


import argparse
import time
import os


p = argparse.ArgumentParser(description='Trafeo collector agent')
p.add_argument('--verbose', '-v', default=None, help="Run in verbose mode")

# todo imlement at some point?
#p.add_argument('--retry', '-r', default=2, metavar='N', type=int, help="If any API fails, retry N times")

p.add_argument('--interval', '-i', default=900, metavar='N', type=int, help="Collect data every N seconds")
p.add_argument('--skip-traffic', '-s', action="store_true", help="skip traffic collection")
p.add_argument('--skip-weather', '-w', action="store_true", help="skip weather collection")
args = p.parse_args()
print args

# get the main configuration
config = Collector.get_config('main.conf')

if not os.access('/var/log/collect', os.W_OK):
    print 'Cannot write to /var/log/collect, make sure that you run this script elevated'
    exit(1)

def main():

    while True:

        logger = None

        try:
            collector = Collector.Collector(config)
            logger = collector.get_logger()
            db = collector.get_db()

            if not args.skip_weather:
                print '\nInitialising import of traffic and weather data...\n'
                print '\nRetrieving weather data...'

                #todo make option to manually specify cities to process? (maybe)
                manual_cities = []

                weather_api_client = WeatherAPI.Client(config['weather']['api']['token'], config['weather']['api']['endpoint'], logger)

                # set the rate limit to 2 seconds per request
                weather_api_client.set_rate_limit(2)

                weather_collector = WeatherCollect.Collect(config, weather_api_client, db)
                cities = config['weather']['api']['cities']

                #if there is a list of cities passed, process them, otherwise use the configured list
                if len(manual_cities) > 0:
                    weather_collector.set_cities(manual_cities)
                else:
                    weather_collector.set_cities(cities)

                logger.info('Processing the following cities for weather data: %s', ", ".join(cities))
                # start collecting the weather data
                stats = weather_collector.collect()

                # log information regarding collection
                logger.info('Collected statistics for %d cities successfully, %d failed.' % (stats['success'],
                                                                                             stats['failed']))
            else:
                print '\nSkipping weather collection...'

            if not args.skip_traffic:
                logger.info('Starting collection of traffic data')
                print '\nRetrieving traffic data...'
                traffic_api_client = TrafficAPI.Client(config['traffic'], logger)
                traffic_collector = TrafficCollect.Collect(config, traffic_api_client, db)

                if len(config['traffic']['regions']) > 0:

                    # add the regions to the collector
                    for region in config['traffic']['regions']:
                        region_name = region.keys()[0]
                        traffic_collector.add_region(region_name, region)

                    # start collecting the data
                    stats = traffic_collector.collect()

                    # log information regarding collection
                    logger.info('Collection for %d regions successfully, %d failed.' % (stats['success'],
                                                                                        stats['failed']))
                else:
                    print '\nNo regions configured, not processing traffic information'

            else:
                print '\nSkipping traffic collection...'


        except Exception as exc:

            if logger is not None:
                logger.error(exc.message)

            raise exc

        print '\n Resuming collecion task in %d seconds.' % args.interval
        # rest until the interval timer has expired
        time.sleep(args.interval)

if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt:
        print 'Exit due to user input'
