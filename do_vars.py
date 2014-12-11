# Inspired by the DigitalOcean inventory plugin:
# https://github.com/ansible/ansible/blob/devel/plugins/inventory/digitalocean.py

import os
import sys
import re

try:
    from dopy.manager import DoError, DoManager
except ImportError, e:
    print "failed=True msg='`dopy` library required for this script'"
    sys.exit(1)


class DigitalOceanInventory(object):

    ###########################################################################
    # Main execution path
    ###########################################################################

    def __init__(self):
        ''' Main execution path '''

        # DigitalOceanInventory data
        self.data = {}      # All DigitalOcean data

        # Verify credentials were set
        if not os.getenv("DO_CLIENT_ID") or not os.getenv("DO_API_KEY"):
            print '''Could not find values for DigitalOcean client_id and api_key.
They must be specified via environment variables (DO_CLIENT_ID and DO_API_KEY)'''
            sys.exit(-1)

        # Read environment variables
        self.client_id = os.getenv("DO_CLIENT_ID")
        self.api_key = os.getenv("DO_API_KEY")

        self.load_all_data_from_digital_ocean()

        # Print YAML
        print '---'
        for k in ['regions', 'images', 'sizes']:
            for d in self.data[k]:
                print 'do_%s_%s: %s' % (k[0:-1], d['slug'].replace('-', ''), d['id'])


    ###########################################################################
    # Data Management
    ###########################################################################

    def load_all_data_from_digital_ocean(self):
        ''' Use dopy to get all the information from DigitalOcean '''
        manager  = DoManager(self.client_id, self.api_key)

        self.data = {}
        self.data['regions']  = self.sanitize_list(manager.all_regions())
        self.data['images']   = self.sanitize_list(manager.all_images(filter=None))
        self.data['sizes']    = self.sanitize_list(manager.sizes())


    ###########################################################################
    # Utilities
    ###########################################################################

    def to_safe(self, word):
        ''' Converts 'bad' characters in a string to underscores so they can be used as Ansible groups '''
        return re.sub("[^A-Za-z0-9\-\.]", "_", word)

    def sanitize_dict(self, d):
        new_dict = {}
        for k, v in d.items():
            if v != None:
                new_dict[self.to_safe(str(k))] = self.to_safe(str(v))
        return new_dict

    def sanitize_list(self, seq):
        new_seq = []
        for d in seq:
            new_seq.append(self.sanitize_dict(d))
        return new_seq


###########################################################################
# Run the script
DigitalOceanInventory()
