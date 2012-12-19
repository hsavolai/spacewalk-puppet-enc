import xmlrpclib
import sys


class Spacewalk_manager:

    spacewalk_dao = None

    def __init__(self, url, username, password):
        try:
            self.spacewalk_dao = Spacewalk_dao(url, username, password)
        except IOError, e:
            print "Error connecting spacewalk server (check url). Error:", e
            exit(1)
        except:
            self.__handle_err(sys.exc_info())

    def __group_list(self, filter_prefix):
        try:
            # Filter the groups with some members
            membergroup = filter(lambda group: group['system_count'] > 0,
                                 self.spacewalk_dao.group_list())
            # Get the groups starting with filter_prefix
            return [group['name'] for group in membergroup
                    if group['name'].startswith(filter_prefix) == True]
        except:
            self.__handle_err(sys.exc_info())

    def __get_group_members(self, group_name):
        try:
            members = self.spacewalk_dao.member_list(group_name)
            return [member['hostname'] for member in members]
        except:
            self.__handle_err(sys.exc_info())

    def __get_system_list(self):
        try:
            system_list = self.spacewalk_dao.list_systems()
            return system_list
        except:
            self.__handle_err(sys.exc_info())

    def get_host_groups(self, filter_prefix):
        groups = {}
        for group_name in self.__group_list(filter_prefix):
            members = self.__get_group_members(group_name)
            for member in members:
                if member not in groups:
                    groups[member] = []
                groups[member].append(group_name[len(filter_prefix):])
        return groups

    def __handle_err(self, e):
        print "Error occurred in execution: ", e
        exit(1)


class Spacewalk_dao:

    username = None
    password = None
    url = None
    client = None
    key = None

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.__connect()

    def __connect(self):
        self.client = xmlrpclib.Server(self.url, verbose=0)
        self.key = self.client.auth.login(self.username, self.password)

    def __disconnect(self):
        self.client.auth.logout(self.key)

    def group_list(self):
        return self.client.systemgroup.listAllGroups(self.key)

    def member_list(self, group_name):
        return self.client.systemgroup.listSystems(self.key, group_name)

    def custom_info(self, server_id):
        return self.client.system.getCustomValues(self.key, server_id)

    def list_systems(self):
        return self.client.system.listSystems(self.key)

    def  __del__(self):
        self.__disconnect()
