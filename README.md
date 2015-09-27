botler
======

The CCoWMU IRC bot.

# package management

You need to create a virtualenv in order to install packages which botler
depends on.

You can use the ```Makefile``` to do this:
    $ make setup

The ```Makefile``` specifies the configuration file to use with botler, botler will use ```config.json``` if no file is specified.

To run botler:
    $ make run

