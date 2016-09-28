 Factorio_Mc
========================

Getting started:
```
# Make a virtualenv
pip install -r requirements.txt
cd factorio_mc/settings
cp local.py.example local.py
vim local.py  # Set SECRET_KEY to random stuff.
createdb factorio_mc_0  # If psql
cd ../..
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```
