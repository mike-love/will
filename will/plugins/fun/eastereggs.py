# coding: utf-8
from will.utils import show_valid, error, warn, print_head

from will.plugin import WillPlugin
from will.decorators import (respond_to, hear, randomly, route, rendered_template,
                             require_settings)
from will.decorators import (respond_to, hear, randomly, route, rendered_template, require_settings)

from will import settings
import logging
import random

class EasterEggPlugin(WillPlugin):

    @hear(".*?(meaning of life).*")
    def meaning_of_life(self, message):
        self.reply(message, 'The answer to the ultimate question of life, the universe, and everything is 42.')

    @hear(".*?(flip a coin)|(flip for it).*")
    def flip_coin(self, message):
        self.reply(message, (random.choice(['Heads','Tails'])))

    @hear("What is the airspeed velocity of an unladen swallow")
    def holy_grail(self,message):
        self.reply(message, 'What do you mean? An African or European swallow?')

    @hear(".*?(i want the truth).*")
    def the_truth(self, message):
        self.reply(message, "You can't handle the truth! \n \
                https://i.ytimg.com/vi/wtpOtFIEkbs/maxresdefault.jpg")
#
#    @hear("")
#    def am_your_father(self, message):
#        self.reply(message, "No I am your father. \n \
#                http://www.slate.com/content/dam/slate/blogs/browbeat/2015/04/14/darth_vader_no_i_am_your_father_said_in_20_different_languages_video/150414_vader1.png.CROP.cq5dam_web_1280_1280_png.png")

    @hear(".*?(go fuck yourself|fuck you).*")
    def gfy(self, message):
        gfyo_img = ['https://media.giphy.com/media/10MbJV76Ppp2LK/giphy.gif',
                    'https://i.ytimg.com/vi/BF5Dtf7u6tQ/hqdefault.jpg',
                    'https://i.imgur.com/M2psY.gif',
                    'https://media.giphy.com/media/sQDvTm7UQAKqs/giphy.gif',
                    'https://replygif.net/i/181.gif',
                    'https://media.tenor.co/images/774b134dca5681aa1d40a271207eef12/tenor.gif',
                    'https://i.imgur.com/O9ELynV.gif',
                    'https://gif-finder.com/wp-content/uploads/2014/04/Jason-Mantzoukasmiddle-finger.gif']

        self.reply(message, 'Fuck me? No, fuck you! \n %s' % random.choice(gfyo_img))

    @hear(".*?(what is love).*")
    def what_is_love(self, message):
        self.reply(message, "Baby don't hurt me, don't hurt me, No more \n \
                https://media.giphy.com/media/12mgpZe6brh2nu/giphy.gif")

    @respond_to(".*?(i love you).*")
    def prop_infinity(self, message):
        self.reply(message, "Robosexuality is still illegal; remeber to vote yes on \
                    proposition infinity: \n \
                    http://img02.deviantart.net/a425/i/2011/314/a/5/yes_on_proposition_infinity_by_spider_matt-d4fpj3r.png")

    @respond_to("up up down down left right left right b a start")
    def konami(self, message):
        self.reply(message, "Bonus features unlocked")

    @respond_to(".*?(easter eggs).*")
    def easter_egg(self, message):
        self.reply(message, "You've got to try harder then that")

    @respond_to("^(make me a sandwich).*$")
    def sandwich(self, message):
        self.reply(message, "What? Make it yourself.\r\n https://imgs.xkcd.com/comics/sandwich.png")

    @respond_to("^(sudo make me a sandwich).*$")
    def sudo_sandwich(self, message):
        self.reply(message, "Okay; \r\n https://upload.wikimedia.org/wikipedia/commons/e/e6/BLT_sandwich_on_toast.jpg")

