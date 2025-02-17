import abc
from CONSTS import C

__version__ = "0.1.6"


class TYLHelpers(object):
    @classmethod
    def get_hostnames_from_tfstate(cls, json_obj):
        if not json_obj:
            return []

        import json
        from jsonpath import jsonpath

        if isinstance(json_obj, str):
            json_obj = json.loads(json_obj)

        path = '$.modules[*].resources.[?(@.type in ["%s"])].type' % '", "'.join(
            C.HELPER_HOSTNAME_QUERY_MAP.keys()
        )
        resource_types = set(jsonpath(json_obj, path) or [])

        host_list = []
        for resource_type in resource_types:
            host_list += jsonpath(json_obj, C.HELPER_HOSTNAME_QUERY_MAP[resource_type])

        return host_list


class TYLPersistent(object):
    __metaclass__ = abc.ABCMeta
    _lock_state_ = C.LOCK_STATE_UNLOCKED

    @abc.abstractmethod
    def set_locked(self, state_obj, raw=""):
        """
        :param state_obj: Object (from json) with the lock ID and details of who made the lock.
        :param raw: The raw json text
        :return: True on successful lock, False if something prevented the lock from happening.
        """
        pass

    @abc.abstractmethod
    def set_unlocked(self, state_obj, raw=""):
        """
        :param state_obj: Object (from json) with the lock ID and details of who made the lock.
        :param raw: The raw json text
        """
        pass

    @abc.abstractmethod
    def get_lock_state(self):
        """
        :return: The request/JSON string provided by terraform of the current lock, None if there is no lock.
        """
        pass

    @abc.abstractmethod
    def store_tfstate(self, tfstate_obj, raw=""):
        """
        :param tfstate_obj: JSON string of the current terraform.tfstate file.
        :param raw: The raw json text
        :return:
        """
        pass

    @abc.abstractmethod
    def get_tfstate(self):
        """
        :return: JSON string of the current terraform.tfstate file.
        """
        pass

    def backend_status(self):
        """
        :return: Health and status information in a JSON compatible format.
        """
        return None


class TYLNonpersistent(object):
    __metaclass__ = abc.ABCMeta
    _logged_errors_ = 0
    _recent_error_ = ""

    @abc.abstractmethod
    def on_locked(self, state_obj, raw=""):
        """
        :param state_obj: Object (from json) with the lock ID and details of who made the lock.
        :param raw: The raw json text
        :return: None
        """
        pass

    @abc.abstractmethod
    def on_unlocked(self, state_obj, raw=""):
        """
        :param state_obj: Object (from json) with the lock ID and details of who made the lock.
        :param raw: The raw json text
        """
        pass

    @abc.abstractmethod
    def process_tfstate(self, tfstate_obj, raw=""):
        """
        :param tfstate_obj: JSON string of the current terraform.tfstate file.
        :param raw: The raw json text
        :return:
        """
        pass

    def post_processor_status(self):
        """
        :return: Health and status object in a JSON compatible format.
        """
        return None
