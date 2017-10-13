import numpy as np

from bokeh.layouts import row,widgetbox
from bokeh.models import CustomJS,Slider
from bokeh.plotting import figure,output_file,show,ColumnDataSource

x = np.linspace(-4,4,500)
y = x*0.0

source = ColumnDataSource(data=dict(x=x,y=y))

plot = figure(y_range = (-10,10),x_range = (-10,10),plot_width=600,plot_height=600)
plot.line('x','y',source=source,line_width=3,line_alpha=0.6)

callback = CustomJS(args = dict(source=source),code = """
    var data = source.data;
    var A = amp.value;
    var offsetx = offsetx.value;
    var offsety = offsety.value;
    var pow = pow.value;
    x=data['x']
    y=data['y']
    for(i=0; i<x.length; i++){
        y[i] = A*Math.pow((x[i] + offsetx),pow) + offsety;
    }
    source.change.emit();
    """)

amp_slider = Slider(start = -10,end = 10, value = 1, step = .1, title = "Amplitude", callback=callback)
callback.args["amp"] = amp_slider

xoff_slider = Slider(start=-10, end=10, value=0, step=.1,
                     title="X Offset", callback=callback)
callback.args["offsetx"] = xoff_slider

yoff_slider = Slider(start=-10, end=10, value=0, step=.1,
                      title="Y Offset", callback=callback)
callback.args["offsety"] = yoff_slider

pow_slider = Slider(start=0, end=10, value=0, step=.1,
                      title="Power", callback=callback)
callback.args["pow"] = pow_slider

layout = row(
    plot,
    widgetbox(amp_slider, xoff_slider, yoff_slider, pow_slider),
)

output_file("Parabola_Slider.html", title="Parabola Slider")

show(layout)
