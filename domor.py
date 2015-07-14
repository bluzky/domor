from Tkinter import Tk, Frame
import os

from PIL import Image, ImageTk
import pygubu
import pygubu.builder.tkstdwidgets
import pyglet
import sys
from utils import *
from options import OptionWindow


class MainWindow(Frame):
    (PAUSE, RUN, STOP) = xrange(0, 3)
    (IDLE, WORK, BREAK) = xrange(0, 3)

    def __init__(self, parent):
        Frame.__init__(self, parent, width=400, height=250)
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file(PoResources.UI_DEF)

        # 3: Set images path before creating any widget
        img_path = os.getcwd() + "/img"
        print img_path
        img_path = os.path.abspath(img_path)
        builder.add_resource_path(img_path)

        # 4: Create the widget using a master as parent
        self.mainwindow = builder.get_object('main_frame', self.master)
        builder.import_variables(self)

        # 5 Connect method callbacks
        builder.connect_callbacks(self)

        # 6 load config
        self.settings = settings = Settings()
        settings.load_config()

        # 7 init class state
        self.btn_state = self.PAUSE
        self.state = self.IDLE
        self.time = settings.short_work_time
        self.work_time = 0
        self.count = 0
        self.reset()

        # set button setting icon
        self._update_button_image('btn_setting', PoResources.IMG_SETTING)
        self._update_button_image('btn_reset', PoResources.IMG_RESET)

    def _update_time(self):
        """
        Update display time on UI
        :return:
        """
        time_string = "%02d:%02d" % (self.time / 60, self.time % 60)
        content = self.builder.get_variable("remaining_time")
        content.set(time_string)

    def _update_pomodoro_count(self):
        self.lb_po_count.set(self.count)
        label  = "pomodoro" if self.count == 1 else "pomodoros"
        self.lb_po_name.set(label)

    def _update_button_image(self, button_id, img_path):
        """
        Update image for button
        :param button_id: id of button which is updated
        :param img_path: path to image
        :return: None
        """
        try:
            btn = self.builder.get_object(button_id)
            img2 = ImageTk.PhotoImage(Image.open(img_path))
            btn.configure(image=img2)
            btn.image = img2
        except Exception as e:
            print e.message

    def reset(self):
        '''
        Reset to default state
        :return:
        '''
        self.state = self.IDLE
        self.time = self.settings.short_work_time
        self.btn_state = self.STOP

        self._update_button_image('btn_start', PoResources.IMG_PLAY)
        self._update_time()

    def btn_start_clicked(self):
        count_down = self.builder.get_object("count_down")

        # if timer state is paused, start/resume counting
        if self.btn_state != self.RUN:
            self.btn_state = self.RUN
            self.state = self.WORK
            self._update_button_image('btn_start', PoResources.IMG_PAUSE)
        elif self.state == self.BREAK:
            # if time is counting and in break period and user click PAUSE button
            # reset timer and button state
            self.reset()
        else:  # if timer is counting, pause it
            self.btn_state = self.PAUSE
            self.state = self.IDLE
            self._update_button_image('btn_start', PoResources.IMG_PLAY)

    def btn_setting_clicked(self):
        """
        Open setting dialog
        :return:
        """
        optionwd = OptionWindow(self)

    def btn_reset_clicked(self):
        self.reset()

    def start_break_period(self, break_time):
        self.state = self.BREAK
        self.time = break_time

        # play a sound
        song = pyglet.media.load(PoResources.SOUND_BELL)
        song.play()

        # restore window
        self.master.wm_state("normal")

        # active window
        self.master.focus_force()
        self.master.wm_attributes("-topmost", 1)
        self.master.wm_attributes("-topmost", 0)

        # change button to skip
        self._update_button_image('btn_start', PoResources.IMG_SKIP)

    def start_work_period(self):
        self.state = self.WORK
        self.time = self.settings.short_work_time

        # play a sound
        song = pyglet.media.load(PoResources.SOUND_BELL)
        song.play()

        # minimize to task ba
        self.master.wm_state("iconic")

        # change button to play
        self._update_button_image('btn_start', PoResources.IMG_PAUSE)

    def count_down(self):
        self.master.after(1000, self.count_down)
        if self.state != self.IDLE:

            if self.state == self.WORK:
                if self.time == 0:
                    self.count += 1

                    # long_work_time is the number of short working session between long break
                    if self.count % self.settings.long_work_time == 0:
                        self.start_break_period(self.settings.long_break_time)
                    else:
                        self.start_break_period( self.settings.short_break_time )
                    self._update_pomodoro_count()
                else:
                    self.time -= 1
                    self.work_time += 1

            else:
                if self.state == self.BREAK and self.time == 0:
                    # end of break period star new short work period
                    self.start_work_period()
                else:
                    self.time -= 1
            self._update_time()

def main():
    root = Tk()
    app = MainWindow(root)
    app.count_down()
    app.pack_propagate(False)
    root.wm_title("Domor")
    if sys.platform == "win32":
        img = ImageTk.PhotoImage(file='img/app.ico')
    else:
        img = ImageTk.PhotoImage(file='img/app.png')
    root.tk.call('wm', 'iconphoto', root._w, img)
    root.resizable(width=False, height=False)
    root.mainloop()


main()
