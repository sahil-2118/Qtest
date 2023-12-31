import pytest
import subprocess
import os
import signal
import time
import json
from ..core.models import before_request, Users, teardown_request


__TEST_FILE_BASE_ADDRESS = r"commands/sign_in/"
with open(__TEST_FILE_BASE_ADDRESS + 'test_case_dictionary.json') as f:
    __TEST_CASE_DICT = json.load(f)
__TEST_FILE_NAMES_LIST = list(__TEST_CASE_DICT.keys())


@pytest.fixture(scope="function")
def set_up():
    args = [
            "python3", 
            "server.py", 
            "--port", 
            "7878", 
            "--ip", 
            "127.0.0.1"
            ]
    server_process = subprocess.Popen(args)
    pid = server_process.pid
    time.sleep(2)
    yield pid
    os.kill(pid, signal.SIGTERM)


@pytest.fixture(params = list(map(lambda x: __TEST_FILE_BASE_ADDRESS + x, __TEST_FILE_NAMES_LIST)))
def functionality(request):
    print(request.param)
    args = ["python3", 
            "client.py", 
            "--port", "7878", 
            "--ip", "127.0.0.1", 
            "--file", 
            request.param ,
            ]
    client_process = subprocess.run(
                                args,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding="utf-8"
                                )
   
    path = request.param
    yield client_process, path.split('/')[2]





def test_sign_in(set_up: int, functionality):

    process, test_case = functionality
     
    assert process.returncode == 0
    assert process.stderr == ""  
    assert __TEST_CASE_DICT[test_case] in process.stdout
    