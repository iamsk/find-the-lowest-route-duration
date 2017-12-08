# -*- coding: utf-8 -*-
import itertools
from datetime import datetime
import baidumaps

from models import Duration


class Router(object):
    def __init__(self, ak='3dd08864e4ced5da7d6004e46e26502d'):
        self.map = baidumaps.Client(ak)

    def duration(self, origin, destination):
        ret = self.map.direct(origin, destination, origin_region='北京', destination_region='北京')
        return ret['routes'][0]['duration']

    def matrix(self, locations):
        location_string = '|'.join(locations)
        ret = self.map.route_matrix(origins=location_string, destinations=location_string)
        return ret

    @classmethod
    def save(cls, origin, destination, n, duration):
        Duration(origin=origin, destination=destination, hour=n.hour, minute=n.minute, duration=duration).save()


def store_routes_duration(locations):
    routes = list(itertools.permutations(locations, 2))
    r = Router()
    n = datetime.now()
    for route in routes:
        origin = route[0]
        destination = route[1]
        d = r.duration(origin, destination)
        print origin, destination, d
        r.save(origin, destination, n, d)


if __name__ == '__main__':
    _locations = ['清秀阁', '华控大厦-北门']
    store_routes_duration(_locations)
