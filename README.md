
# ckanext-login-throttle

A CKAN extension that helps protect your portal from brute-force login attacks by **tracking failed login attempts** and **temporarily locking accounts or IPs** after too many failures.

The original code was taken as an base from [ckanext-security](https://github.com/data-govt-nz/ckanext-security).

Check the [documentation](https://datashades.github.io/ckanext-login-throttle/).

## Features

- 🔒 Tracks **unsuccessful login attempts** in **Redis**  
- 🔑 Lock based on **IP address** (default) or **username**  
- ⏳ **Temporary lockout** (default: 15 minutes) after too many failed attempts  
- 📧 Sends **warning email** to the affected user when lockout occurs  
- ⚙️ Fully configurable via CKAN config settings


## Requirements

If your extension works across different versions you can add the following table:

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.10+           | not tested    |
| 2.11.3            | tested    |

Suggested values:

* "yes"
* "not tested" - I can't think of a reason why it wouldn't work
* "not yet" - there is an intention to get it working
* "no"


## Installation

To install ckanext-login-throttle:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/Datashades/ckanext-login-throttle.git
    cd ckanext-login-throttle
    pip install -e .

3. Add `login-throttle` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

Check for settings at the [documentation](https://datashades.github.io/ckanext-login-throttle/config_settings/).

## Developer installation

To install ckanext-login-throttle for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/Datashades/ckanext-login-throttle.git
    cd ckanext-login-throttle
    pip install -e .


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
