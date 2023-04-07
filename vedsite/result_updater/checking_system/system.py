
from .ya_contest.authorization import YaContestAuthorizer
from .hse_online.authorization import HSEOnlineAuthorizer
# from hse_lms.authorization import Authorizer as HSELMSAuthorizer

from .ya_contest.fetching import YaContestUpdFetcher
from .hse_online.fetching import HSEOnlineTaskUpdFetcher

from .ya_contest.task_updating import YaContestUpdater
from .hse_online.task_updating import HSEOnlineTaskUpdater


_authorizers = {
    "yandex.contest": YaContestAuthorizer,
    "hse.online": HSEOnlineAuthorizer,
    # "hse.lms": HSELMSAuthorizer
}

_fetchers = {
    "yandex.contest": YaContestUpdFetcher,
    "hse.online": HSEOnlineTaskUpdFetcher,
}

_task_updaters = {
    "yandex.contest": YaContestUpdater,
    "hse.online": HSEOnlineTaskUpdater,
}

def get_authorizer(system_name):
    return _authorizers[system_name]()

def get_fetcher_class(system_name):
    return _fetchers[system_name]

def get_task_updater_class(system_name):
    return _task_updaters[system_name]
