# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.ticker import FuncFormatter as ff


def get_durations():
    conn = sqlite3.connect('duration.db')
    c = conn.cursor()
    c.execute('SELECT * FROM duration;')
    results = c.fetchall()
    c.close()
    conn.close()
    return results


def main():
    conn = sqlite3.connect('duration.db')
    df = pd.read_sql_query("SELECT * FROM duration;", conn)
    print df
    df.plot.bar()
    plt.show()


def group():
    durations = get_durations()
    d = defaultdict(dict)
    for duration in durations:
        r = u'{}-{}'.format(duration[1], duration[2])
        minutes = duration[4] * 60 + duration[5]
        d[r].setdefault(minutes, {'duration': 0, 'count': 0})
        d[r][minutes]['duration'] += duration[6]
        d[r][minutes]['count'] += 1
    print d


colors = {u'龙域西二路二号院-融科融智蜂巢工场': 'red', u'融科融智蜂巢工场-华控大厦-北门': 'green'}


def m2hm(x, _):
    h = int(x / 60)
    m = int(x % 60)
    return '%(h)02d:%(m)02d' % {'h': h, 'm': m}


def init():
    mpl_fig = plt.figure()
    ax = mpl_fig.add_subplot(111)
    ax.xaxis.set_major_formatter(ff(m2hm))


def last():
    plt.title('Route duration')
    plt.xlabel('Minute')
    plt.ylabel('Seconds')
    plt.show()


def show_points():
    init()
    durations = get_durations()
    for duration in durations:
        route = u'{}-{}'.format(duration[1], duration[2])
        minutes = duration[4] * 60 + duration[5]
        if route in colors and duration[4] in [8, 9]:
            plt.plot([minutes], [duration[6]], marker='o', markersize=3, color=colors[route])
    last()


if __name__ == '__main__':
    group()
