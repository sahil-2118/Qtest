import pytest
import subprocess
import os
import signal
import time
import requests
import json


@pytest.fixture(scope="function")
def server():
    # Start the server as a background process
    args = ["python3", "server.py", "--port", "7878", "--ip", "127.0.0.1"]
    server_process = subprocess.Popen(args)
    # Get the process ID
    pid = server_process.pid
    # Wait for the server to be ready
    time.sleep(2)
    # Yield the process ID
    yield pid
    # Terminate the server process
    os.kill(pid, signal.SIGTERM)



def test_sign_up(server):
    # Use the fixture to start and stop the server
    # Send a sign up request to the server with valid data
    args = ["python3", 
            "client.py", 
            "--port", "7878", 
            "--ip", "127.0.0.1", 
            "--file", 
            "commands/sign-up.json",
            ]
    client_process = subprocess.run(
                                args,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding="utf-8"
                                )
    time.sleep(2)
   
    assert client_process.returncode == 0
    assert "Response is" in client_process.stdout
    assert client_process.stderr == ""    
    
    