========
githooks
========

githooks is a simple module that adds several python related useful hooks to use
with Git hooks system.

**It's still alpha software!**

It uses the hghooks module as backend. It implements part of the Mercurial API
for hooks, and calls hghooks for the heavy lifting. It supports what hghooks
module supports, currently:

* pep8 checking of python files
* pyflakes checking of python files
* Checking for forgotten pdb statements in python files
* Trac integration. This includes:

  - Making sure at least a ticket is mentioned in the changeset message
  - Updating the Trac ticket with the changeset

PyPi package:

http://pypi.python.org/pypi/githooks

hghooks
=======

hghooks is being developed by Lorenzo Gil Sanchez. It's released under a LGPLv3,
and it's hosted on:

https://bitbucket.org/lgs/hghooks

Documentation
=============

How to use
----------

Soon :P

Configuration
-------------

Githooks has serveral options. It uses **git config** as configuration
backend.

All githooks options has "githooks" as family, so a git configuration file looks
like similar to this:

::

 [user]
         name = John Doe
         email = johndoe@example.com
 [githooks "pep8"]
         ignore = E501
 [githooks "trac"]
         hook-active = False

How to read:

::

 $ git config --global githooks.pep8.ignore
 E501
 $

How to set:

::

 $ git config --global githooks.pep8.ignore E501

You can find more details about git configuration on the git help:

::

 $ git config --help

In git configuration there are several contexts. Githooks uses two of them.

Global
~~~~~~

Global context is user level. This configuration is common for all the
repositories of the user.

* **pep8.ignore**

  - pep8 error list to ignore
  - defaults to None

Local
~~~~~

Local context is repository level. This configuration only affects one
repository.

* **trac.hook-active**

  - activate trac integration hook
  - defaults to False

* **trac.repo-name**
* **trac.changeset-style**
* **trac.msg-template**

.. note::

 More and better documentation soon :P
