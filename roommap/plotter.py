# coding=utf-8
# !/usr/bin/python

import plotly.offline as offline
import plotly.graph_objs as go


class Plotter(object):
    """
    Die Plotter-Klasse vereint die methoden um die Hindernisse
    und den gefahrenen Pfad zu zeichnen und in einer Datei zu speichern.
    """

    def __init__(self):
        super(Plotter, self).__init__()

    def plot(self, obstacles, path):
        print "start plotting"

        # array der x-werte der hindernisse und y-werte der hindernisse
        hindernisse_x = [item[0] for item in obstacles]
        hindernisse_y = [item[1] for item in obstacles]

        # das gleiche für den Weg
        wegX = [item[0] for item in path]
        wegY = [item[1] for item in path]

        # print "Hindernisse - x = {}; y = {}".format(hindernisse_x, hindernisse_y)
        # print "Weg - x = {}; y = {}".format(wegX, wegY)

        weg = go.Scatter(
            x=wegX,
            y=wegY,
            mode='lines',
            name='Weg'
        )

        hindernis = go.Scatter(
            x=hindernisse_x,
            y=hindernisse_y,
            mode='markers',
            name='Hindernisse'
        )

        data = [hindernis, weg]

        # plot data
        offline.plot(data, filename='test')


############
# run tests
p = Plotter()
p.plot([], [])

hindernisse = [[1, 1], [1.2, 1], [1.3, 1], [1.4, 1]]
weg = [[0, 0], [1, 0.9], [2, 1]]
p.plot(hindernisse, weg)
