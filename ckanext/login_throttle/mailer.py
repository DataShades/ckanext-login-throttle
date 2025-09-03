# encoding: utf-8
import os
import logging
import flask

from ckan.common import config
from ckan.lib.base import render
from ckan.lib.mailer import mail_user

import ckanext.login_throttle.config as throttle_config

log = logging.getLogger(__name__)


def _build_footer_content(extra_vars):
    custom_path = throttle_config.login_throttle_footer_path()
    if custom_path and os.path.exists(custom_path):
        log.warning("Overriding brute force lockout email footer with %s", custom_path)
        with open(custom_path, "r") as footer_file:
            footer_content = footer_file.read()
        env = flask.current_app.jinja_env
        template = env.from_string(footer_content)
        return "\n\n" + template.render(**extra_vars)
    else:
        footer_path = "login_throttle/emails/lockout_footer.txt"
        return "\n\n" + render(footer_path, extra_vars)


def notify_lockout(user, lockout_timeout):
    extra_vars = {
        "site_title": config.get("ckan.site_title"),
        "site_url": config.get("ckan.site_url"),
        "user_name": user.name,
        "password_reset_url": config.get("ckan.site_url").rstrip("/") + "/user/login",
        "lockout_mins": lockout_timeout // 60,
    }

    subject = render("login_throttle/emails/lockout_subject.txt", extra_vars)

    subject = subject.split("\n")[0]  # Make sure we only use the first line

    body = render(
        "login_throttle/emails/lockout_mail.txt", extra_vars
    ) + _build_footer_content(extra_vars)

    mail_user(user, subject, body)
