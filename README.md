ProfileGrid django-cms Plugin
====================

django-cms Plugin that shows a responsive gallery of profiles with dropdown information.

Also contains a Promotion Plugin for promoting ProfileGrid Plugins. These show a reduced number of profiles.

Demo application.
====================

For a quick startup, there is a demo application with django-cms 3.2.0.
This demo application uses resources from https://github.com/divio/django-cms-demo

virtualenv demo_env
. demo_env/bin/activate
cd demo
pip install -r requirements.txt
pip install -e .. --no-deps
./manage.py runserver
