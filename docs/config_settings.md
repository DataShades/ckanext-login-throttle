**`ckanext.login_throttle.lock_timeout`** - (integer) (optional) The time User is going to be locked while reaching the Attempts limit. By default its `900` seconds (e.g. 15 minutes).

**`ckanext.login_throttle.login_max_count`** - (integer) (optional) The amount of tries User can do before being locked. By default its `10`.

**`ckanext.login_throttle.brute_force_key`** - (optional) Updates the logic based on what information the User will be locked. By default it using IP Address. Accepts only and string `user_name` value as an alternative to lock User by `name`.

**`ckanext.login_throttle.brute_force_footer_path`** - (path) (optional) Can be used to override the footer text of the Email notification. By default it takes local file in the repo `lockout_footer.txt`.

**`ckanext.login_throttle.disable_lock_notification`** - (boolean) (optional) If `True` provided, notification won't be sent to the User. By default its `False`
