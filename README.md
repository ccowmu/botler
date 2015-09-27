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
Also for the db, you're going to need to export the DB_PASS variable so that botler can run.
    $ export DB_PASS=$ASKSOMEONEFORTHEPASS

#Usage Advice
If your /command is throwing errors then try and !reload ; The status window will give you error locations; highly useful for debugging.

Make sure that your @command is (aside from #comment_blocks) the very first line in the file, or the command will not load properly.

Its recommended to use 4 spaces, instead of tabs. Set this in .vimrc to with the following;

    $ tabstop=4
    $ shiftwidth=4
    $ set expandtab
