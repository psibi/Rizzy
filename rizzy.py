#!/usr/bin/python
import gtk
import gtk.glade

class rizzy:
    def __init__(self):
        gladefile="rizzy.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.image_entry=builder.get_object("image_entry")
        self.key_radiobutton=builder.get_object("key_radiobutton")
        self.keyless_radiobutton=builder.get_object("keyless_radiobutton")
        self.encode_radiobutton=builder.get_object("encode_radiobutton")
        self.decode_radiobutton=builder.get_object("decode_radiobutton")
        self.secret_window=builder.get_object("secret_window")
        builder.connect_signals(self)
        self.keyless_radiobutton.set_active(True)

    def on_getimage_button_clicked(self,widget,data=None):
         dialog = gtk.FileChooserDialog("Open..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
         dialog.set_default_response(gtk.RESPONSE_OK)
         response=dialog.run()
         if response == gtk.RESPONSE_OK:
             filename = dialog.get_filename() 
             self.image_entry.set_text(str(filename))
         dialog.destroy()

    def on_key_radiobutton_toggled(self,widget,data=None):
        if self.key_radiobutton.get_active():
            self.secret_window.show()
        
    def on_rizzy_window_destroy(self,widget,data=None):
        gtk.main_quit()

    def on_start_button_clicked(self,widget,data=None):
        

if __name__=="__main__":
    steg = rizzy()
    gtk.main()

