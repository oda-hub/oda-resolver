import pytest
import os
import copy
import subprocess
import re
import time
import signal
import psutil

from threading import Thread

import tnr.service

__this_dir__ = os.path.join(os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture
def app():
    os.environ['POLAR_GRB_DATA_CSV'] = 'data/polar/polar_grbs.csv'
    os.environ['TNR_PLUGIN_GWPROXY_ENABLED'] = 'yes'
    app = tnr.service.app
    return app


@pytest.fixture()
def resolver_live_fixture(pytestconfig):

    resolver_state = start_resolver(pytestconfig.rootdir)
    service = resolver_state['url']
    pid = resolver_state['pid']

    yield service

    kill_child_processes(pid, signal.SIGINT)
    os.kill(pid, signal.SIGINT)


def start_resolver(rootdir):
    env = copy.deepcopy(dict(os.environ))
    print(("rootdir", str(rootdir)))
    env['PYTHONPATH'] = str(rootdir) + ":" + str(rootdir) + "/tests:" + \
                        __this_dir__ + ":" + os.path.join(__this_dir__, "../tnr:") + \
                        env.get('PYTHONPATH', "")
    print(("pythonpath", env['PYTHONPATH']))
    env['POLAR_GRB_DATA_CSV'] = 'data/polar/polar_grbs.csv'
    env['TNR_PLUGIN_GWPROXY_ENABLED'] = 'yes'
    env['IVOA_RDF_DATA'] = 'data/ivoa_rdf_data/object-type.ttl'

    fn = os.path.join(__this_dir__, "../tnr/service.py")
    cmd = [
        "python",
        fn,
        "-d",
        "-debug"
    ]

    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        env=env,
    )

    url_store = [None]

    def follow_output():
        url_store[0] = None
        for line in iter(p.stdout):
            line = line.decode()

            NC = '\033[0m'
            if 'ERROR' in line:
                C = '\033[31m'
            else:
                C = '\033[34m'

            print(f"{C}following server: {line.rstrip()}{NC}")
            m = re.search(r"Running on (.*?) \(Press CTRL\+C to quit\)", line)
            if m:
                url_store[0] = m.group(1).strip()  # alternatively get from configenv
                print(f"{C}following server: found url: {url_store[0]}")

            if re.search("\* Debugger PIN:.*?", line):
                url_store[0] = url_store[0].replace("0.0.0.0", "127.0.0.1")
                print(f"{C}following server: server ready, url {url_store[0]}")

    thread = Thread(target=follow_output, args=())
    thread.start()

    started_waiting = time.time()
    while url_store[0] is None:
        print("waiting for server to start since", time.time() - started_waiting)
        time.sleep(0.2)
    time.sleep(0.5)

    service = url_store[0]

    return dict(
        url=service,
        pid=p.pid
    )


def kill_child_processes(parent_pid, sig=signal.SIGINT):
    try:
        parent = psutil.Process(parent_pid)
        children = parent.children(recursive=True)
        for process in children:
            process.send_signal(sig)
    except psutil.NoSuchProcess:
        return