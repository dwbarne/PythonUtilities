from math import *
from Tkinter import *
import tkFont
import Scientific.TkWidgets.TkPlotCanvas as plot

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.buttonFont =tkFont.Font ( family= "Helvetica",
            size= "40" )
        self.createWidgets()
        self.makePlot()

    def createWidgets(self):
        self.can = plot.PlotCanvas ( self, width= 600, height= 600,
            zoom= 1)
        self.can.grid(row= 0, column= 0)
        self.quitButton = Button ( self, text= "Quit",
            font= self.buttonFont,
            command= self.quit )
        self.quitButton.grid(row= 99, column= 0, columnspan= 99,
                             sticky= E+W)

    def makePlot(self):
        xrange = (0,6)
        yrange = (0, 40)
        squares  =  [(0,0), (1,1), (2,4), (3,9), (4,16),
                                (5,25), (6,36)]
        logs  =  [(1, log10(1)), (2, log10(2)), (3, log10(3)),
                  (4, log10(4)), (5, log10(5)), (6, log10(6))]
        self.plotSet ( squares, xrange, yrange, "circle", "red"
)
        self.plotSet ( logs, xrange, yrange, "cross", "cyan"
)

    def plotSet(self, pointSet, xrange, yrange, symbol, color):
        markers = plot.PolyMarker ( pointSet, marker= symbol, color= color
)
        self.can.draw ( markers, xaxis= xrange, yaxis= yrange )
        liner = plot.PolyLine ( pointSet, width= 2, color= color )
        self.can.draw(liner, xaxis= xrange, yaxis= yrange)

app=Application()
app.master.title("Sample application")
app.mainloop()
