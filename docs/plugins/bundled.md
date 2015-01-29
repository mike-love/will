# Included Plugins

Will comes with batteries included, and already does a number of useful things - more are welcome via PR!  Note that not all of these commands are listed in `@will help` - some are rare enough that they didn't make sense to add.

Here's what he does out of the box:


## Administration

#### Keepalive

This plugin pings will once a minute at `PUBLIC_URL`, making sure his processes aren't idled in installations like heroku.

#### Ping

He's a robot. He should respond to ping. :)

![Ping](../../img/ping.gif)

#### Say

This provides a web endpoint at `/say/some-phrase` that will will speak into `DEFAULT_ROOM`.  Helpful for pay-no-attention-to-the-hand-behind-the-curtain demos.

![Say](../../img/say.gif)

#### Storage

Provides several **admin-only** commands for manipulating will's underlying storage.  These methods are also case-sensitive, because they can do Bad Things.

- **@will How big is the db?**: Lists the db size in human-friendly units.
- **@will SERIOUSLY. Clear ____**: Clears a key from the storage
- **@will SERIOUSLY. REALLY. Clear all keys.**: Clears *everything* from storage.  Will will definitely not work after this without a restart, and will tell you so.
- **@will Show me the storage for ____**: Shows the raw storage value for a given key.


## Chat rooms

Provides a couple of methods for listing and updating will's internal chat room knowledge, and manipulating the current room.

- **@will what are the rooms?**:  List the rooms he knows about, including their hipchat IDs.
- **@will update the room list**:  Get a new list of rooms from the chat server.
- **@will new topic ____**:   Set the room topic.

## Devops

Will is our devops team at GreenKahuna, and in the long term, we plan to abstract and include our stack deployer as a plugin.  For the moment, he just includes a couple basics:

#### Emergency Contacts

Saves a set of emergency contacts for team members, and provides a way for anyone on the team to get them in, well, emergencies.

- **@will set my contact info to ____**: Accepts a multi-line string with whatever contact info you want to provide.
- **@will contact info**: Lists contact info for all the team members who have provided it.

#### Github status

Github is a critical piece of infrastructure for most dev shops.  When it's having troubles, it's good to know.  This plugin checks github's [status api](https://status.github.com/api/), and alerts chat with the problem when they go down, and again when they're back up.


#### Heroku status

Heroku is also really widely used, and if you use it, when it's having troubles, it's good to know.  This plugin checks heroku's [status api](http://status.heroku.com), and alerts chat with the problem when they go down, and again they're back up.

Note: if you don't use heroku, remember you can always disable this plugin in `config.py`:

```python
PLUGIN_BLACKLIST = [
    "will.plugins.devops.heroku_is_up",
]
```

## Friendly

Will has personality, and we love that about him.  The friendly module includes some nice, silly, and appreciative aspects to will that really rounds out his personality.

#### Good morning / Good night

Will responds to "good morning", and "good night" appropriately, if he hears it.  If it's Friday, he'll even tell you to have a good weekend!

#### Hello

Saying hello is important.

![Hello](../../img/hi_hello.gif)

#### Thanks

A little politeness goes a long way.

![Thanks](../../img/thanks.gif)

#### Cookies

We promised silly.

![Cookies](../../img/cookies.gif)

#### Love

One day, you'll find yourself saying this.  The response will make your week.

![Love](../../img/love.gif)



## Help

#### Help

Lists all the plugin commands with docstrings, bundled by module.

![Help, will](../../img/help.gif)

#### Programmer help

List all regexes for registered `@hear` and `@respond_to` decorators.  This is what help used to be, and may be pulled in the near future.

![Programmer help](../../img/programmer_help.gif)

## Productivity

#### Hangout

If you've set a `HANGOUT_URL`, will will toss it in chat for you:

![Hangout](../../img/hangout.gif)

#### Image me

Sometimes, a picture is worth a thousand words.

![Image me a crazy squirrel](../../img/image_me.gif)

#### Remind me

This saves our bacon every day. Timeboxes meetings, helps people remember appointments, and enforces self-control.

![Remind me](../../img/remind_food.gif)

Then, when it's 3pm, and I still haven't stopped coding to eat:

![Remind me](../../img/remind_then.gif)

Or, more practically,

![Remind me](../../img/remind_client.gif)


#### World time

We're a remote company. Maybe you are too. Or your clients are.  Or the light/dark cycle of the world just fascinates you.  If any of these are you,

1. Get a free `WORLD_WEATHER_ONLINE_V2_KEY` from [world weather online](http://developer.worldweatheronline.com).
2. Get the time in pretty much any city on earth.  Even our globe-trotting CEO hasn't been able to stump him.

![World time](../../img/world_time.gif)

## Web

This module's all about web-facing content.

#### Home page
Will also includes a home page, so you can fire him, up, browse to his URL, and see his smiling face.

![Home page](../../img/home.png)


You now know everything about plugins.  Maybe you're wondering about the [finer points of config](../config.md)?  Or perhaps, you're ready to [deploy your will](../deploy.md)?