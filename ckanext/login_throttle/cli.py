import click

import ckan.plugins.toolkit as tk


def get_commands():
    return [login_throttle]


@click.group()
def login_throttle():
    """ckanext-login-throttle management commands."""


@login_throttle.command()
@click.argument("username")
def reset_user_throttle(username):
    """
    Reset User Throttle lock
    """
    tk.get_action("login_throttle_user_reset")(
        {"ignore_auth": True}, {"user": username}
    )
    click.echo(click.style("Done", fg="green"))


@login_throttle.command()
@click.argument("username")
def user_throttle_show(username):
    """
    Show User Throttle lock
    """
    result = tk.get_action("login_throttle_user_show")(
        {"ignore_auth": True}, {"user": username}
    )
    print(result)


@login_throttle.command()
@click.argument("address")
def reset_address_throttle(address):
    """
    Reset Address Throttle lock
    """
    tk.get_action("login_throttle_address_reset")(
        {"ignore_auth": True}, {"address": address}
    )
    click.echo(click.style("Done", fg="green"))


@login_throttle.command()
@click.argument("address")
def address_throttle_show(address):
    """
    Show Address Throttle lock
    """
    result = tk.get_action("login_throttle_address_show")(
        {"ignore_auth": True}, {"address": address}
    )
    print(result)
