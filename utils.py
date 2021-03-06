__author__ = 'bluzky'
import json
import sys
import os.path

exe_path = ""
exe_dir = ""

if hasattr(sys, 'frozen'):
    exe_path = sys.executable
    exe_dir = os.path.dirname(exe_path)
else:
    exe_path = sys.argv[0]
    exe_dir = os.path.dirname(exe_path)

img_path = os.path.join(exe_dir, "img")
sound_path = os.path.join(exe_dir, "sound")

def get_image( img_name):
    return os.path.join(img_path, img_name)

def get_sound( sound_name):
    return os.path.join(sound_path, sound_name)

def get_resource( resource_name):
    return os.path.join(exe_dir, resource_name)

class Settings(object):
    """
    Singleton class used to store all application setting
    """
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance =  object.__new__(cls)
            cls.__instance.initialized = False
        return cls.__instance

    def __init__(self):
        if self.initialized:
            return
        self.initialized = True

        # default value
        self.short_work_time = 1500
        self.short_break_time = 300
        self.long_work_time = 4
        self.long_break_time = 900

    def to_json(self):
        return json.dumps(self.__dict__)

    def load_config(self):
        """
        load user config from file. If getting exception, use default setting
        :return:
        """
        try:
            with open(PoResources.FILE_CONFIG) as config_file:
                conf_string = config_file.read()
                config = json.loads(conf_string)
                for key, value in config.iteritems():
                    if key in self.__dict__:
                        setattr(self, key, value)
        except Exception as e:
            print "Use default config"

    def save_config(self):
        """
        write setting to config file
        :return:
        """
        with open(PoResources.FILE_CONFIG, mode="w") as config_file:
            config_str = self.to_json()
            config_file.write(config_str)


class PoResources(object):
    """
    Define all resource path
    """
    UI_DEF = 'tomor.ui'
    OPTION_DEF = 'option.ui'
    IMG_PLAY = 'img/play.png'
    IMG_PAUSE = 'img/pause.png'
    IMG_SKIP = 'img/skip.png'
    IMG_SETTING = 'img/setting.png'
    IMG_RESET = 'img/reset.png'
    SOUND_BELL = 'sound/bell.wav'
    FILE_CONFIG = 'conf.ini'