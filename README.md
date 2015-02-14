botler
======

The CCoWMU IRC bot.

# package management

You need to create a virtualenv in order to install packages which botler
depends on.

On yakko this might look something like:

    $ pyvenv-3.4 --without-pip env
    $ . env/bin/activate
    $ curl https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | python
    $ pip install -r requirements.txt

Every time you want to work on botler from a new terminal, you will need to run:

    $ . env/bin/activate
