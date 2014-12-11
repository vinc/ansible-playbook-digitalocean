Ansible Playbook for DigitalOcean
=================================

A simple [Ansible](http://www.ansible.com/) playbook
for [DigitalOcean](https://www.digitalocean.com/).


Usage
-----

    $ git clone https://github.com/vinua/ansible-playbook-digitalocean.git
    $ cd ansible-playbook-digitalocean
    $ sudo pip install -r requirements.txt
    $ export DO_CLIENT_ID=XXX DO_API_KEY=XXX
    $ ansible-playbook -i hosts site.yml


Configuration
-------------

The inventory file `hosts` defines the droplets to be created on DigitalOcean.

  [droplets]
  droplet1.example.net do_size=do_size_1gb do_region=do_region_sfo1 do_image=do_image_ubuntu1410x64
  droplet2.example.net do_size=do_size_1gb do_region=do_region_sfo1 do_image=do_image_ubuntu1410x64

The variables `do_size`, `do_region`, and `do_image` can be anything defined
in `group_vars/droplets.yml`.

The droplet's name are idempotents, the script can be run multiple times
without resulting in multiple droplets of the same name.

Ansible will connect to the droplets using their IP addresses instead of the
names defined in the inventory. The first task to run after this playbook will
probably be to add a DNS entry for each droplet.

You may want to update DigitalOcean's variables (regions, images, and sizes)
with the following script:

    $ python do_vars.py > group_vars/droplets.yml


Copyright
---------

Copyright (C) 2014 Vincent Ollivier. See LICENSE for details.
