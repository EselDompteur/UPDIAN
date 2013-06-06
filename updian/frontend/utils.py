import os.path
import time

from glob import glob

from .. import config

def get_data_filename(hostname):
    return os.path.join(config.data_dir, hostname) + '.txt'

def has_updates(hostname):
    return os.path.exists(get_data_filename(hostname))

def get_todo_filename(hostname):
    return os.path.join(config.todo_dir, hostname) + '.txt'

def is_queued(hostname):
    return os.path.exists(get_todo_filename(hostname))

def get_log_filename(hostname):
    return os.path.join(config.log_dir, hostname) + '.log'

def hostlist_decorator(basedir, extension='txt'):
    def decorator(fun):
        def get_hostlist():
            for host_file in glob(os.path.join(basedir, '*.' + extension)):
                host = os.path.splitext(os.path.basename(host_file))[0]
                yield host

        return get_hostlist
    return decorator

@hostlist_decorator(config.data_dir)
def hosts_with_updates():
    pass

@hostlist_decorator(config.todo_dir)
def queued_hosts():
    pass

@hostlist_decorator(config.log_dir, 'log')
def available_logs():
    pass

def get_update_details(hostname):
    if not has_updates(hostname):
        return None

    with open(get_data_filename(hostname), 'r') as f:
        update_list = [line.replace('Inst ', '') for line in f]

    return dict(host=hostname,
                queued=is_queued(hostname),
                updates=update_list)

def formatted_mtime(filename):
    timeformat = '%B %d %Y %H:%M'
    try:
        mtime = os.path.getmtime(filename)
    except os.error:
        if os.path.exists(statfile):
            raise

    return time.strftime(timeformat, time.localtime(mtime))