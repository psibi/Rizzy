#!/usr/bin/python
import gtk

class rizzy:
    def __init__(self):
        gladefile="rizzy.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.image_entry=builder.get_object("image_entry")
        builder.connect_signals(self)

    def on_getimage_button_clicked(self,widget,data=None):
         dialog = gtk.FileChooserDialog("Open..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
         dialog.set_default_response(gtk.RESPONSE_OK)
         response=dialog.run()
         if response == gtk.RESPONSE_OK:
             filename = 
             self.image_entry.set_text(str(filename))
         dialog.destroy()

if __name__=="__main__":
    steg = rizzy()
    gtk.main()

