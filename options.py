__author__ = 'bluzky'
from Tkinter import Tk, Frame, Toplevel
import pygubu
import pygubu.builder.tkstdwidgets
import os
from utils import *

class OptionWindow(Toplevel):

    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.resizable(width=False, height=False)

        self.wm_title("Setting")

        #1: Create a builder
        self.builder = builder = pygubu.Builder()
        #2: Load an ui file
        builder.add_from_file(PoResources.OPTION_DEF)

        #3: Set images path before creating any widget
        img_path = os.getcwd() + "/img"
        img_path = os.path.abspath(img_path)
        builder.add_resource_path(img_path)

        #4: Create the widget using a master as parent
        self.mainwindow = builder.get_object('option_frame', self)
        builder.import_variables(self)

        self.settings = Settings()
        self.load_config()

        # Connect method callbacks
        builder.connect_callbacks(self)

    def load_config(self):
        '''
        Load setting data and show on UI
        :return:
        '''
        self.sb_wminute.set(self.settings.short_work_time/60)
        self.sb_bminute.set(self.settings.short_break_time/60)
        self.sb_bsecond.set(self.settings.short_break_time%60)
        self.lb_whour.set(self.settings.long_work_time/3600)
        self.lb_wminute.set((self.settings.long_work_time%3600)/60)
        self.lb_bminute.set(self.settings.long_break_time/60)
        self.lb_bsecond.set(self.settings.long_break_time%60)

    def btn_ok_clicked(self):
        #update setting
        sb_wminute = self.sb_wminute.get()
        sb_bminute = self.sb_bminute.get()
        sb_bsecond = self.sb_bsecond.get()
        lb_whour = self.lb_whour.get()
        lb_wminute = self.lb_wminute.get()
        lb_bminute = self.lb_bminute.get()
        lb_bsecond = self.lb_bsecond.get()

        self.settings.short_work_time = sb_wminute*60
        self.settings.short_break_time = sb_bminute*60 + sb_bsecond
        self.settings.long_work_time = lb_whour*3600 + lb_wminute*60
        self.settings.long_break_time = lb_bminute*60 + lb_bsecond

        #write new setting to file
        self.settings.save_config()
        self.destroy()

    def btn_cancel_clicked(self):
        '''
        Close setting dialog when  user click Cancel button
        :return:
        '''
        self.destroy()

    # These callback used to validate user input
    def sb_wminute_lostfocus(self, event):
        new_wminute = self.sb_wminute.get()
        if new_wminute <= 0:
            self.sb_wminute.set(self.settings.short_work_time/60)# reset default

    def sb_bminute_lostfocus(self, event):
        new_bminute = self.sb_bminute.get()
        if new_bminute <= 0 or new_bminute > 20:
            self.sb_bminute.set(self.settings.short_break_time/60)# reset default

    def sb_bsecond_lostfocus(self, event):
        new_bsecond = self.sb_bsecond.get()
        if new_bsecond <= 0:
            new_bsecond = 0
            self.sb_bsecond.set(new_bsecond)# reset default
        elif new_bsecond >= 60:
            new_bsecond = 59
            self.sb_bsecond.set(new_bsecond)

    def lb_whour_lostfocus(self, event):
        new_whour = self.lb_whour.get()
        if new_whour <= 0 or new_whour > 10: # max long work period is 10 hour, this is my default
            self.lb_whour.set(self.settings.long_work_time/3600)# reset default

    def lb_wminute_lostfocus(self, event):
        new_wminute = self.lb_wminute.get()
        if new_wminute <= 0:
            new_wminute = 0
            self.lb_wminute.set(new_wminute)# reset default
        elif new_wminute >= 60:
            new_wminute = 59
            self.lb_wminute.set(new_wminute)

    def lb_bminute_lostfocus(self, event):
        new_bminute = self.lb_bminute.get()
        if new_bminute <= 0 or new_bminute > 40:
            self.lb_bminute.set(self.settings.long_break_time/60)# reset default

    def lb_bsecond_lostfocus(self, event):
        new_bsecond = self.lb_bsecond.get()
        if new_bsecond <= 0:
            new_bsecond = 0
            self.lb_bsecond.set(new_bsecond)# reset default
        elif new_bsecond >= 60:
            new_bsecond = 59
            self.lb_bsecond.set(new_bsecond)

