#!/usr/bin/python
# Copyright (C) 2012 Sibi <sibi@psibi.in>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Author:   Sibi <sibi@psibi.in>
import gtk
import gtk.glade
import shlex
import subprocess
import time

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
        self.secret_textbuffer=builder.get_object("secret_textbuffer")
        self.oimage_entry=builder.get_object("oimage_entry")
        self.rizzy_pb=builder.get_object("rizzy_pb")
        self.smsg_label=builder.get_object("smsg_label")
        self.secret_text=builder.get_object("secret_text")
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

    def encode_validate(self):
        if self.image_entry.get_text()=="Image Not Selected":
            return False
        start,end = self.secret_textbuffer.get_bounds()
        text = self.secret_textbuffer.get_text(start,end)
        if text=="":
            return False
        if self.oimage_entry.get_text()=="":
            return False
        return True

    def decode_validate(self):
        if self.image_entry.get_text()=="Image Not Selected":
            return False
        return True

    def create_temp_file(self):
        start,end = self.secret_textbuffer.get_bounds()
        text = self.secret_textbuffer.get_text(start,end)
        filename = ".secret"
        fhandler = open(filename,"w")
        fhandler.write(text)
        fhandler.close()

    def initial_values(self):
        self.rizzy_pb.set_fraction(0.0)
        self.image_entry.set_text("Image Not Selected")
        self.oimage_entry.set_text("")
        self.secret_textbuffer.set_text("")

    def on_encode_radiobutton_toggled(self,widget,data=None):
        if self.decode_radiobutton.get_active():
            self.secret_text.set_can_focus(False)
            self.oimage_entry.set_can_focus(False)
        if self.encode_radiobutton.get_active():
            self.secret_text.set_can_focus(False)
            self.oimage_entry.set_can_focus(False)

    def on_start_button_clicked(self,widget,data=None):
        if self.encode_radiobutton.get_active():
            if self.encode_validate():
                iimage = self.image_entry.get_text()
                self.create_temp_file()
                oimage = self.oimage_entry.get_text()
                cmd="./rstep.py -e -i "
                cmd = cmd + iimage + " -t .secret -o " + oimage
                args=shlex.split(cmd)
                self.rizzy_pb.set_fraction(0.4)
                process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
                self.rizzy_pb.set_fraction(0.9)
                self.rizzy_pb.set_fraction(1)
                dlg=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,"Message Hidden in Image")
                dlg.run()
                dlg.destroy()
                self.initial_values()
            else:
                dlg=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Parameters Missing")
                dlg.run()
                dlg.destroy()
        if self.decode_radiobutton.get_active():
            if self.decode_validate():
                cmd="./rstep.py -d -i "
                iimage = self.image_entry.get_text()
                cmd = cmd + iimage 
                args=shlex.split(cmd)
                self.rizzy_pb.set_fraction(0.4)
                process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
                self.rizzy_pb.set_fraction(0.9)
                self.rizzy_pb.set_fraction(1.0)
                output=process.communicate()
                if output[0]:
                    self.secret_textbuffer.set_text(output[0])

if __name__=="__main__":
    steg = rizzy()
    gtk.main()

