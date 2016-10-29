Factio MMO Mission Control
--------------------------
This is the website running on factoriommo.org

It contains a Django website wich collects data from the [Agent](https://github.com/factoriommo/factoriommo-agent)(s) with websockets. It has support for scenario's that can do something with the collected data and send messages, stats and winconditions.

Getting started
---------------

You need reddis (for django-channels) and a database backend.

```
virtualenv ~/your-virtualenv-dir/factoriomc
source ~/your-virtualenv-dir/factoriomc/bin/activate

pip install -r requirements.txt
cd factoriomc/settings
cp local.py.example local.py
vim local.py  # Set SECRET_KEY to random stuff, setup your database (see below)
cd -
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Now navigate to `http://localhost:8000`, you should see the factoriommo website.

[How to setup your Django database](https://docs.djangoproject.com/en/1.10/intro/tutorial02/)

Now you can navigate to `/admin/` and set some stuff up.

First of all you need to go to `/admin/core/game/` to setup a new Game. You can choose a scenario here, but currently only the production scenario is working.

Example scenario_data:

`{"targets": [{ "id": "productivity-module-3", "name": "Productivity", "target": 100 }, { "id": "effectivity-module-3", "name": "Effectivity", "target": 50 }, { "id": "speed-module-3", "name": "Speed", "target": 10 }]}`

The current Game is a constance that can be managed with Constance at `/admin/constance/config/`

Now you can go to `/admin/core/server/` and add one or two servers.

`name` can be anything, `player_limit` is currently ignored, `players_online` gets auto-updated, you can set it to 0 for now `auth_token` gets auto-generated.

Now you can start debugging your scenario.

You can simulate a server on `/serverdebug/<ID>/`. So if you made two servers, open two tabs and navigate to `/serverdebug/1/` and `/serverdebug/2/`.

Here you can press the auth button to authenticate. You can also send some test data. If you open de debugger in chrome, you will get a lot of feedback.
