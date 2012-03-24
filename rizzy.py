#!/usr/bin/python
# Copyright (C) 2012 Sibi <sibi@psibi.in>
#
# This file is part of Rizzy.
#
# Rizzy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Rizzy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Rizzy.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Author:   Sibi <sibi@psibi.in>
import gtk
import gtk.glade
import shlex
import subprocess
import time
from Crypto.Cipher import AES

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
        self.ofile_entry=builder.get_object("ofile_entry")
        self.rizzy_pb=builder.get_object("rizzy_pb")
        self.key_entry=builder.get_object("key_entry")
        self.smsg_entry=builder.get_object("smsg_entry")
        self.stxtfile_entry=builder.get_object("stxtfile_entry")
        self.smsg_radiobutton=builder.get_object("smsg_radiobutton")
        self.sfile_radiobutton=builder.get_object("sfile_radiobutton")
        builder.connect_signals(self)
        self.keyless_radiobutton.set_active(True)
        self.prefix= '2324234342342342'

    def on_getimage_button_clicked(self,widget,data=None):
         dialog = gtk.FileChooserDialog("Open..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
         dialog.set_default_response(gtk.RESPONSE_OK)
         response=dialog.run()
         if response == gtk.RESPONSE_OK:
             filename = dialog.get_filename() 
             self.image_entry.set_text(str(filename))
         dialog.destroy()

    def on_gettfile_button_clicked(self,widget,data=None):
        dialog = gtk.FileChooserDialog("Select Secret File..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
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
        if self.smsg_radiobutton.get_active():
            if self.smsg_entry.get_text()=="":
                return False
        else:
            if self.stxtfile_entry.get_text()=="":
                return False
        if self.ofile_entry.get_text()=="":
            return False
        return True

    def decode_validate(self):
        if self.image_entry.get_text()=="Image Not Selected":
            return False
        return True

    def encrypt_aes(self,text):
        length = len(text)
        if length >= 16:
            spaces = length%16
            spaces = 16 - spaces
        else:
            spaces = 16 -length
        a = ""
        for i in range(spaces):
            a = a + " "
        text = text + a
        print len(text)
        return AES.new(self.key, AES.MODE_CBC, self.prefix).encrypt(text)

    def decrypt_aes(self,enc_text):
        print len(enc_text)
        return AES.new(self.key, AES.MODE_CBC, self.prefix).decrypt(enc_text)

    def create_temp_file(self):
        if self.sfile_radiobutton.get_active():
            fname = self.stxtfile_entry.get_text()
            fhandler = open(fname,"r")
            text = fhandler.read()
            fhandler.close()
        else:
            text = self.smsg_entry.get_text()
        if self.key_radiobutton.get_active():
            text = self.encrypt_aes(text)
        filename = ".secret"
        fhandler = open(filename,"w")
        fhandler.write(text)
        fhandler.close()
        
    def get_spaces(self,num):
        space = ""
        for i in range(num):
            space = space + " "
        print len(space)
        return space

    def initial_values(self):
        self.rizzy_pb.set_fraction(0.0)
        self.image_entry.set_text("Image Not Selected")
        self.ofile_entry.set_text("")
        self.smsg_entry.set_text("")
        self.stxtfile_entry.set_text("")
        self.key_entry.set_text("")

    def on_encode_radiobutton_toggled(self,widget,data=None):
        if self.decode_radiobutton.get_active():
            self.ofile_entry.set_can_focus(False)
        if self.encode_radiobutton.get_active():
            self.ofile_entry.set_can_focus(True)
                
    def on_smsg_radiobutton_toggled(self,widget,data=None):
        if self.smsg_radiobutton.get_active():
            self.smsg_entry.set_can_focus(True)
            self.stxtfile_entry.set_can_focus(False)
        else:
            self.smsg_entry.set_text("")
            self.smsg_entry.set_can_focus(False)
            self.stxtfile_entry.set_can_focus(True)
            dialog = gtk.FileChooserDialog("Open..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            dialog.set_default_response(gtk.RESPONSE_OK)
            response=dialog.run()
            if response == gtk.RESPONSE_OK:
                filename = dialog.get_filename() 
                self.stxtfile_entry.set_text(str(filename))
            dialog.destroy()
    
    def on_start_button_clicked(self,widget,data=None):
        if self.encode_radiobutton.get_active():
            if self.encode_validate():
                iimage = self.image_entry.get_text()
                self.create_temp_file()
                ofile = self.ofile_entry.get_text()
                fname = ".secret"
                cmd="./rstep.py -e -i "
                cmd = cmd + iimage + " -t "+ fname + " -o " + ofile
                args=shlex.split(cmd)
                self.rizzy_pb.set_fraction(0.4)
                process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
                self.rizzy_pb.set_fraction(0.9)
                self.rizzy_pb.set_fraction(1)
                dlg=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,"Message Hidden in Image")
                dlg.run()
                dlg.destroy()
                self.initial_values()
                self.keyless_radiobutton.set_active(True)
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
                    print output[0]
                    if self.key_radiobutton.get_active():
                        secret = self.decrypt_aes(output[0])
                        print "se:" + secret
                        self.smsg_entry.set_text(secret.strip())
                    else:
                        self.smsg_entry.set_text(str(output[0]))
                self.rizzy_pb.set_fraction(0.0)

    def on_ok_button_clicked(self,widget,data=None):
        self.key=self.key_entry.get_text()
        key_length = len(self.key)
        if key_length < 16:
            self.key = self.key + self.get_spaces(16 - key_length)
        self.secret_window.hide()

    def on_secret_window_destroy(self,window,data=None):
        self.secret_window.hide()
        self.keyless_radiobutton.set_active(True)
        return True

    def on_secret_window_destroy_event(self,widget,data=None):
        self.secret_window.hide()
        self.keyless_radiobutton.set_active(True)
        return True

if __name__=="__main__":
    steg = rizzy()
    gtk.main()

