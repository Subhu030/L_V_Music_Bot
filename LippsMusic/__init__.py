from LippsMusic.core.bot import Lipps
from LippsMusic.core.dir import dirr
from LippsMusic.core.git import git
from LippsMusic.core.userbot import Userbot
from LippsMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Lipps()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
