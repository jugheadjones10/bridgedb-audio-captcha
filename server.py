import mako.exceptions
from mako.template import Template
from mako.lookup import TemplateLookup

import os
import random

from captcha.audio import AudioCaptcha

from twisted.internet import reactor
from twisted.web import resource
from twisted.web import static
from twisted.web.server import Site
from twisted.web.util import redirectTo

TEMPLATE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
lookup = TemplateLookup(directories=[TEMPLATE_DIR],
        output_encoding='utf-8',
        filesystem_checks=False,
        collection_size=500)
audio = AudioCaptcha(voicedir=os.path.join(TEMPLATE_DIR, "assets/captcha-audio"))
print(os.path.join(TEMPLATE_DIR, "assets"))

def stringifyRequestArgs(args):
    """Turn the given HTTP request arguments from bytes to str.
    :param dict args: A dictionary of request arguments.
    :rtype: dict
    :returns: A dictionary of request arguments.
    """

    # Convert all key/value pairs from bytes to str.
    str_args = {}
    for arg, values in args.items():
        arg = arg if isinstance(arg, str) else arg.decode("utf-8")
        values = [value.decode("utf-8") if isinstance(value, bytes)
                else value for value in values]
        str_args[arg] = values

    return str_args


class TemplateResource(resource.Resource):
    """A generalised resource which uses gettext translations and Mako
        templates.
    """

    def __init__(self, template=None):
        """Create a new :api:`Resource <twisted.web.resource.Resource>` for a
            Mako-templated webpage.
        """
        resource.Resource.__init__(self)
        self.template = template
        self.audiocaptcha = None

    def getChild(self, name, request):
        if name == '':
            return self


    def render_GET(self, request):
        print("Get has been CALLED!@!!!!")
        self.audiocaptcha = str(random.randrange(1000, 10000, 1))
        audio.write(self.audiocaptcha, TEMPLATE_DIR + "/assets/out.wav")

        template = lookup.get_template(self.template)
        rendered = template.render(hey="hey")

        request.setHeader("Content-Type", "text/html; charset=utf-8")

        return rendered

    def render_POST(self, request):
        print("POST has been CALLED")
        request.setHeader("Content-Type", "text/html; charset=utf-8")
        request.args = stringifyRequestArgs(request.args)
        print("request args : " + str(request.args))
        #print("current self audiocaptcha : " + self.audiocaptcha) 
        #print("audioguess extracted from request : " + request.args["audioguess"][0])
      
        if "audioguess" in request.args: 
            if request.args["audioguess"][0] == self.audiocaptcha:
                print("Audio guess from client side : " + request.args["audioguess"][0])
                print("Self captcha from server : " + self.audiocaptcha)
                return "audio captcha success!"
        return self.render_GET(request)

assets = static.File(os.path.join(TEMPLATE_DIR, 'assets/'))
root = TemplateResource("captcha.html")
root.putChild(b'assets', assets)

site = Site(root)
reactor.listenTCP(8000, site)
reactor.run()

