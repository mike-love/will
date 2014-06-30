# Configuring Will

Most of will's configuration is done interactively, using `run_will.py`, or specifying via the plugins.  There are, however a few built-in settings and config worth covering.  We'll aim to address all of them here.

## Environment variables

All environment variables prefixed with `WILL_` are imported into will's `settings` modules.

In best practices, you should keep all of the following in environment variables:

- `WILL_USERNAME`
- `WILL_PASSWORD`
- `WILL_REDIS_URL`
- `WILL_V2_TOKEN`
- `WILL_V1_TOKEN`
- Any other tokens, keys, passwords, or sensitive URLS.

We've made it easy.  No excuses. :)

## config.py

Config.py is where all of your non-sensitive settings should go.   This includes things like:

- `PLUGINS`: The list of plugins to run,
- `PLUGIN_BLACKLIST`: The list of plugins to ignore, even if they're in `PLUGINS`,
- `PUBLIC_URL`: The publicly accessible URL will can reach himself at (used for [keepalive](plugins/bundled.md#administration),
- `HTTPSERVER_PORT`: The port will should handle HTTP requests on.  Defaults to 80, set to > 1024 if you don't have sudo,
- `ROOMS`: The list of rooms to join,
- `DEFAULT_ROOM`: The room to send messages that come from web requests to,
- `TEMPLATE_DIRS`: Extra directories to look for templates,
- `ADMINS`: The mention names of all the admins,
- `LOGLEVEL`: What logging level to use,
- and all of your non-sensitive plugin settings.

More expansive documenation on all of those settings is in `config.py`, right where you need it.

## How environment variables and config.py are combined

The environment variables and config.py are combined, and made available to the rest of the app at:

```python
from will import settings

print settings.MY_SETTING_NAME
```

The rules for combining are fairly straightforward:

1. All environment variables that start with `WILL_` are imported, and `WILL_` is stripped off their name. (i.e. `WILL_PORT` becomes `PORT`)
2. All variables from `config.py` are imported.  If there is a conflict, `config.py` wins, and a message is displayed:

    ![Config Conflict](../img/config_conflict.gif)

3. Some smart defaulting happens inside settings.py for important variables.  For the moment, I'm going to leave that out of the docs, and refer you to `settings.py` as I *believe* things should Just Work, and most people should never need to care.  If this decision's wrong, please open an issue, and these docs will be improved!

Thats's it for config.  Now, let's get your will [deployed](deploy.md).



