import configparser
import os

from vk.vk_bot import VkBot
from abstractions.pages_manager import PagesManager
from abstractions.pages_container import PagesContainer
from pages.introduction import IntroductionPage

from config import cfg


def main():
    os.environ['NO_PROXY'] = '127.0.0.1'
    bot = VkBot(
        cfg.get('VK', 'TOKEN'),
        int(cfg.get('VK', 'GROUP_ID'))
    )
    pages_manager = PagesManager(PagesContainer(
        cfg.get('SETTINGS', 'DATABASE_NAME')),
        bot,
        IntroductionPage
    )
    bot.run()
