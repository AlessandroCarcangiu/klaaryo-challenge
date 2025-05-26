#!/bin/bash
exec >> /var/log/django/django.log 2>&1

# migrate
if [ "${DJANGO_MIGRATIONS}" = True ] ; then
    doing_what="Applying migrations"
    echo "$(date '+%Y-%m-%d %H:%M:%S') ... ${doing_what}"
    python manage.py migrate
    echo "$(date '+%Y-%m-%d %H:%M:%S') ... ${doing_what} is DONE"
fi


# load initial_data
if [ "${DJANGO_LOADDATA}" = True ] ; then
    doing_what="Loading Initial data"
    echo "$(date '+%Y-%m-%d %H:%M:%S') ... ${doing_what}"
    python ${WEB_APP_ROOT}manage.py loaddata ${DJANGO_INTIAL_DATA_PATH}/*
    echo "$(date '+%Y-%m-%d %H:%M:%S') ... ${doing_what} is DONE"
fi


doing_what="Running the Server"
echo "$(date '+%Y-%m-%d %H:%M:%S') ... ${doing_what}"
python manage.py runserver 0.0.0.0:${DJANGO_PORT}
