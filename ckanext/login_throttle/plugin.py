import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

from .authenticator import authenticate
from . import cli


@tk.blanket.config_declarations
@tk.blanket.cli(cli.get_commands)
@tk.blanket.actions
@tk.blanket.auth_functions
class LoginThrottlePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthenticator, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "login_throttle")

    # IAuthenticator

    def authenticate(self, identity):
        return authenticate(identity)
