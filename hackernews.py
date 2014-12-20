import pygtk
pygtk.require("2.0")

import gtk
import gobject
import json
import urllib2
from subprocess import call

from pdb import set_trace as dbg

class IHackerNews(object):
    _timelaps = 60 #in seconds
    
    def __init__(self, parser):
        """
        Begin with init the parser thread every minutes
        """
        self._parser = parser
        """
        initiliaze ui
        """
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("IHackerNews")
        scroll = gtk.ScrolledWindow()

        self.lstStore = gtk.ListStore(str)
        tree = gtk.TreeView(self.lstStore)
        rendCol = gtk.CellRendererText()
        col = gtk.TreeViewColumn("iHackerNews", rendCol, text=0)
        tree.append_column(col)
        self.updateItems()

        
        tree.connect("button-press-event", self.onBtnPress)
        tree.connect("key-press-event", self.onKeyPress)
        self.window.connect("destroy", self.destroy_event)
        scroll.add(tree)
        self.window.add(scroll)
        self.window.set_default_size(500, 800)
        self.window.show_all()
        self.ot = float("-inf")

    def onBtnPress(self, widget, evt, data=None):
        if evt.type == gtk.gdk.BUTTON_PRESS+1:
            self.selectRow(widget)

    def onKeyPress(self, widget, evt, data=None):
        if evt.keyval == 65293:
            self.selectRow(widget)

    def selectRow(self, widget):
        row = widget.get_selection().get_selected_rows()[1][0][0]
        call(["xdg-open", self.items[row][2]])

    def destroy_event(self, widget, data=None):
        gtk.main_quit()

    def updateItems(self):
        self._parser.readData()
        self.items = self._parser.getItems()
        self.lstStore.clear()
        [self.lstStore.append((item[0],)) for item in self.items]
        
    def main(self):
        gtk.main()

class IHackerNewsParser(object):
    _items = "items"
    _url = "http://api.ihackernews.com/page"
    _keysParse = ("title", "postedBy", "url")

    def readData(self):
        try:
            self._data = json.load(urllib2.urlopen(self._url))
        except:
            print("Failed to get  page")
        
    def getItems(self):
        """
        Return all item from the url 
        format is a list of tuple (title, postedBy, url)
        """
        try:
            return [(item[self._keysParse[0]], item[self._keysParse[1]], item[self._keysParse[2]])
                    for item in self._data[self._items]]
        except:
            return []
        

    

print(__name__)
if __name__ == "__main__":
    IHackerNews(IHackerNewsParser()).main()
