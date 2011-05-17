
Usage
=====

Add the middlware class before the ``AuthenticationMiddleware``::

  MIDDLEWARE_CLASSES = (
      ...
      'authtkt.middleware.AuthTktMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      ...
  )

Callback
========

You can use a callback to use something to fill the newly created user in the third party app.

Settings::

  AUTHTKT_CALLBACK = 'yourmodule:update_user'

Callback::

  from sqlalchemy import engine_from_config, Table, MetaData
  from django.conf import settings


  def update_user(user):
      engine = engine_from_config({'sqlalchemy.url': settings.USER_DB})
      metadata = MetaData(engine)
      users = Table('auth_user', metadata, autoload=True)
      record = users.select(users.c.id==user.id).execute().fetchone()
      for k, v in record.items():
          setattr(user, str(k), v)


Manual identify/forget user
============================

Manualy identify user (eg: set a cookie). You need to set a correct
``request.user``::

  request.environ['authtkt.identify'](request, response)

Manualy forget user (eg: reset a cookie)::

  request.environ['authtkt.forget'](request, response)

