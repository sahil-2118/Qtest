import pytest
import subprocess
import os
import signal
import time

__TEST_FILE_BASE_ADDRESS = r"commands/sign-up/"


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



def sign_up_functiona(cammand_address : str)-> str:
    args = ["python3", 
            "client.py", 
            "--port", "7878", 
            "--ip", "127.0.0.1", 
            "--file", 
            cammand_address ,
            ]
    client_process = subprocess.run(
                                args,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding="utf-8"
                                )
    time.sleep(2)
   
    assert client_process.returncode == 0
    assert client_process.stderr == ""  

    return client_process.stdout


def test_sign_up(set_up):
      with open(__TEST_FILE_BASE_ADDRESS + 'commands_file_names') as f:
           lines = f.readlines()
           for commands_address in lines:
                out_message = sign_up_functiona(__TEST_FILE_BASE_ADDRESS + commands_address)
                assert 'successfully' in out_message
    