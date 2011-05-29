========
githooks
========

githooks is a simple module that adds several python related useful hooks to use
with Git hooks system.

It uses the hghooks module as backend. It implements part of the Mercurial API
for hooks, and calls hghooks for the heavy lifting. It supports what hghooks
module supports, currently:

    * pep8 checking of python files
    * pyflakes checking of python files
    * Checking for forgotten pdb statements in python files
    * Trac integration. This includes:
        - Making sure at least a ticket is mentioned in the changeset message
        - Updating the Trac ticket with the changeset

hghooks
=======

hghooks is being developed by Lorenzo Gil Sanchez. It's released under a LGPLv3,
and it's hosted on::

    https://bitbucket.org/lgs/hghooks

Documentation
=============

Soon :P
