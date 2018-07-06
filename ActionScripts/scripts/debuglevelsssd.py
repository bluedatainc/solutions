#!/usr/bin/python

'''
    Copyright (c) 2018 BlueData Corp.  All Rights Reserved.

    This file contains routines necessary to configure an sssd.conf file
    to change the debug level for all domains.

    This routine must be run as root to edit sssd.conf.

    Usage:
        root>  debuglevelsssd.py 15

'''

from SSSDConfig import SSSDConfig
import sys
import subprocess

SSSD_CONF_PATH = '/etc/sssd/sssd.conf';


class BdSSSDConfig(SSSDConfig):
    '''
        This class SSSDConfig provides extension methods to the already existing
        SSSDConfig object so we may manipulate the sssd domains to modify sssd
        debug levels.

        It also allows us to choose separate sssd.conf files for input or output
        for testing and debug purposes.  This way the original sssd.conf file can
        remain pristine until config changes can be verified.
    '''
    _config_file = SSSD_CONF_PATH

    def __init__(self):
        SSSDConfig.__init__(self)

    def bd_import_config(self, config_file = None):
        '''
            bd_import_config lets us read in from any arbitrary config file for
            test purposes.
        '''
        if config_file is not None:
            self._config_file = config_file

        self.import_config(self._config_file)

    def bd_write_config(self, config_file = None):
        '''
             bd_write_config lets us write configs to other locations to test before
            we write to the default, possibly hosing the original.
        '''
        if config_file is not None:
            self.write(config_file)
        else:
            self.write(self._config_file)

    def set_loglevels(self, loglevel):
        '''
            Set the log level for all domains in sssd.conf.
        '''
        alldomains = self.list_domains()
        for thisdomain in alldomains:
            domain = self.get_domain(thisdomain)
            domain.set_option("debug_level", loglevel)
            self.save_domain(domain)

def main():

    if len(sys.argv) != 2:
        print "USAGE: Please enter the loglevel using a base 10 integer."
        return

    loglevel = int(sys.argv[1])

    config = BdSSSDConfig()
    config.bd_import_config(SSSD_CONF_PATH)
    config.set_loglevels(loglevel)


    # For debugging, you can put a different output file than what was used on
    # input so you may verify results before performing the action on the real
    # sssd.conf file, e.g.
    # config.bd_write_config( '/etc/sssd/test-sssd.conf')

    config.bd_write_config()

    # Restart sssd so it can pickup the change.
    subprocess.call("/bin/systemctl restart sssd.service", shell=True)

if __name__ == "__main__":

    main()
    print "Script Complete!"

