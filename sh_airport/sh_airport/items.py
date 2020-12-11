# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShAirportItem(scrapy.Item):
    plan_departure_time = scrapy.Field()
    main_flight_id = scrapy.Field()
    sub_flight_id = scrapy.Field()
    airline = scrapy.Field()
    terminal = scrapy.Field()
    destination_via = scrapy.Field()
    check_in = scrapy.Field()
    actual_departure_time = scrapy.Field()
