# from plotly import __version__
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#
# print __version__ # requires version >= 1.9.0


import plotly.offline as offline
import plotly.graph_objs as go

# Create random data with numpy
import numpy as np

# offline.init_notebook_mode()

########
# plot a line between three points

p1 = [0,0]
p2 = [1,1]
p3 = [2,1]

trace0 = go.Scatter(
    x = [p1[0], p2[0], p3[0]],
    y = [p1[1], p2[1], p3[1]],
    mode = 'lines',
    name = 'path'
)

########
# plot several unique points
u0 = [1.3,1.7]
u1 = [1.2,1.5]
u2 = [0.3,0.3]

dots = go.Scatter(
    x = [u0[0], u1[0], u2[0]],
    y = [u0[1], u1[1], u2[1]],
    mode = 'markers',
    name = 'obstacles'
)

## plot everything
data = [trace0, dots]
offline.plot(data, filename='test')