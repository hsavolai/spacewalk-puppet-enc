'''

This file is part of Spacewalk sync tool.

spacewalk-puppet-enc program is free software: you can redistribute it and/or modify
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
import ast
import ConfigParser
import os
from spacewalk import Spacewalk_manager

# pylint: disable=W0613
def main(argv=None):
    """Module main entry"""

    if len(sys.argv) < 2:
         print "Usage:"
         print sys.argv[0] + " [hostname]"
         print "Set environmental variable SYNCFILE to change the file name / path."
         print "Default is enc.conf in current dir."
         exit(1)

    host = sys.argv[1]

    config = ConfigParser.SafeConfigParser()
    if os.environ.get('SYNCFILE') is not None:
         config.read(os.environ['SYNCFILE'])
    else:
         config.read("enc.conf")

    classes = []

    if config.has_option(host, "classes"):
        classes = ast.literal_eval(config.get(host, "classes"))

    class_dict = {}
    class_dict['classes'] = classes;
    yaml.dump(class_dict, sys.stdout, default_flow_style=False, explicit_start=True, indent=10)


if __name__ == '__main__':
    sys.exit(main())
