"""
Конфигурационный файл.
"""

import configparser

cfg: configparser.ConfigParser = configparser.ConfigParser()
cfg.read('settings.cfg')
