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
    data = {
        "command_name": "sign_up",
        "parameters": {
        "username": "admin22",
        "password": "admin",
        "email": "admin@dshasin.net"
        }
    }
    args = ["python3", "server.py", "--port", "7878", "--ip", "127.0.0.1", "--file", "commands/sign-up.json"]
    client_process = subprocess.Popen(args)
    time.sleep(2)
    pid = client_process.pid
    os.kill(pid, signal.SIGTERM)
    # Assert that the response is successful and contains the expected message
    # assert response.status_code == 200
    # assert result == "User admin signed up successfully"