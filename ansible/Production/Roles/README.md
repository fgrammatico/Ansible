nas.yaml playbook
=========

This playbook will install the latest Plex version using docker. /data will be linked to a share with and pre-existing Raid 1 so keep in mind to change it to your own share.
This is just an example and is meant to be used as template.

Requirements
------------
This playbook was tested on a Ubuntu server so any other flavour of Linux will probably fail.

Host Variables
--------------
You'll need to setup the sudoer credentials to perform the installation and the Db credentials. Up to you to encrytp (or not) the credentials.
Keep in mind !The SSH port is set to 2222.

Dependencies
------------

A valid SSH configuration.


License
-------

BSD

To Do
------------------

