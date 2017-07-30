# Import the Shotgun software API
import shotgun_api3
# Import PrettyPrint
from pprint import pprint
import urllib
import sys

# Server details and authentication
SERVER_URL = "https://noobxgenesis.shotgunstudio.com"
SCRIPT_NAME = "Pull Playlist"
API_KEY = "4de7568c48239687deadba1478377889f312f87d13784701606a433a5752bc30"

class ShotgunAction():

    # url is provided by the Action Menu
    def __init__(self, url):
        self.url = url
        pprint(self.url)
        #
        self.protocol, self.action, self.params = self._pars_url()

        self.entity_type = self.params['entity_type']
        pprint(self.entity_type)

    def _parse_url(self):

        # get the protocol used
        protocol, path = self.url.split(":", 1)

        # extract the action
        action, params = path.split("?", 1)
        action = action.strip("/")

        # extract the parameters
        # 'column_display_names' and 'cols' occurs once for each column displayed so we store it as a list
        params = params.split("&")
        p = {'column_display_names':[], 'cols':[]}
        for arg in params:
            key, value = map(urllib.unquote, arg.split("=", 1))
            if key == 'column_display_names' or key == 'cols' :
                p[key].append(value)
            else:
                p[key] = value
        params = p
        return (protocol, action, params)

if __name__ == "__main__":
    # Assign all commands via script based authentication to sg variable
    sg = shotgun_api3.Shotgun(SERVER_URL, SCRIPT_NAME, API_KEY)

    sa = ShotgunAction(sys.argv[1])
