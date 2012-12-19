Copyright 2012 Harri Savolainen 
(GPLv3)

SPACEWALK-PUPPET-ENC
--

This is ENC (External Node Classifier) for integrating two great systems,
Spacewalk Server (or RHN Satellite) and the Puppet configuration management server.

SUMMARY
--

The tool is divided in two parts: 

- The sync tool is used to retrieve class information from the Spacewalk server.
The information is stored in text file, which acts as a cache for ENC. This 
should be scheduled run in cron jobs as frequently as needed. Practical value is
probably every 2-3 minutes.

- The ENC tool is configured to Puppet Master. It reads the classification 
information and turns it to yaml which is understood by the Puppet server.

Version requirements:

- Tested with Puppet v3, Red Hat Satellite 5.5, and Python v2.6
- PyYAML is required. (This is distributed at least as part of RHN Satellite)


USAGE
--

- Place the scripts on puppet master server, e.g. to directory /opt/puppet/spacewalk-enc.

In enc.sh, configure parameters  
SW_SYNC_PATH  

In sync.sh, configure parameters  
SW_SYNC_PATH  
SPACEWALK_USERNAME  
SPACEWALK_PASSWORD  
SPACEWALK_URL  

- Configuring puppet master. 

Add the following lines to puppet master configuration under [master].


    [master]
     ...
     node_terminus = exec
     external_node = /opt/puppet/spacewalk-enc/enc.sh
     external_nodes = /opt/puppet/spacewalk-enc/enc.sh
     ...

- Configuring Spacewalk Server / RHN Satellite Server:

Create a system groups with name prefixed text "Puppet:". 
Append the module name after the colon. e.g. Puppet:[module name]

_example_
Puppet:ntp_server_configurations

Add some hosts to the system group and wait for sync.sh to run or execute manually.
By default the sync file is called "enc.conf" which should appear to same directory 
with the scripts.

If ENC is configured correctly, enc picks up the group information and tries to apply the module
to selected hosts defined in the group name. Any groups prefixed with "Puppet:" with any hosts
will be turned into puppet classifications. 

Note: To make group names to match completely (as they most likely are like that in the Spacewalk
or RHN Satellite DB), you probably want to enable strict_hostname_checking=true on puppet server.


LICENCE
--
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
--




