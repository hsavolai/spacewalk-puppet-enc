'''

This file is part of Spacewalk Sync tool.

spacewalk-puppet-sync program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2012 Harri Savolainen

@author: hsavolai
@license: GPLv3

Created on Nov 10, 2012

'''

import sys
import yaml
import ConfigParser
from optparse import OptionParser
from spacewalk import Spacewalk_manager


# pylint: disable=W0613
def main(argv=None):
    """Module main entry"""
    parser = OptionParser(version='%prog version 1.0')
    parser.add_option("-s", "--satellite", dest="url",
                      help="Spacewalk/RHN server URL", metavar="URL")
    parser.add_option("-u", "--user", dest="username",
                      help="Spacewalk/RHN server username", metavar="USERNAME")
    parser.add_option("-p", "--password", dest="password",
                      help="Spacewalk/RHN server password", metavar="PASSWORD")
    parser.add_option("-o", "--output", dest="outfile",
                      help="Output configuration data, defaults to enc.conf",
                      metavar="FILE", default="enc.conf")
    parser.add_option("-q", "--quiet",
                      action="store_true",dest="quiet", default=False,
                  help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    if not check_options(options, parser):
        exit(1)

    manager = Spacewalk_manager(options.url, options.username, options.password)
    puppet_groups = manager.get_host_groups("Puppet:")

    all_hosts = set(puppet_groups.keys())

    cfgfile = open(options.outfile, 'w')
    config = ConfigParser.ConfigParser()
    for host in all_hosts:
        if not options.quiet:
            print "Host info synced: " + host
        config.add_section(host)
        if host in puppet_groups:
            config.set(host, "classes", puppet_groups.get(host))
    config.write(cfgfile)
    cfgfile.close()

    # yaml.dump(manager.get_host_groups("puppet-"), sys.stdout)


def check_options(options, parser):
    mandatories = ['username', 'url', 'password']
    for m in mandatories:
        if not options.__dict__[m]:
            parser.error("Mandatory option (" + m + ") is missing!")
            return False
    return True

if __name__ == '__main__':
    sys.exit(main())
