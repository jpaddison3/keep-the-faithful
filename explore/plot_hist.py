import plotly.plotly as py
from plotly.graph_objs import *
from explore import birth_years

data = Data([
    Histogram(
        x=birth_years
    )
])
layout = Layout(
    showlegend=False,
    hovermode='closest',
    bargap=-2.2737367544323206e-13,
    xaxis1=XAxis(
        range=[1900.0, 2020.0],
        domain=[0.0, 1.0],
        type='linear',
        showgrid=False,
        zeroline=False,
        showline=True,
        nticks=7,
        ticks='inside',
        tickfont=Font(
            size=12.0
        ),
        mirror='ticks',
        anchor='y1',
        side='bottom'
    ),
    yaxis1=YAxis(
        range=[0.0, 140.0],
        domain=[0.0, 1.0],
        type='linear',
        showgrid=False,
        zeroline=False,
        showline=True,
        nticks=8,
        ticks='inside',
        tickfont=Font(
            size=12.0
        ),
        mirror='ticks',
        anchor='x1',
        side='left'
    )
)
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)