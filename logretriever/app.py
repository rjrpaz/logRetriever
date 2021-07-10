import paramiko
import time
from scp import SCPClient
import tkinter as tk
from logretriever import default

port = 22

screen = tk.Tk()
w_hostname = tk.Entry()
w_username = tk.Entry()
w_password = tk.Entry(show="*", width=15)
w_directory = tk.Entry()
w_pattern = tk.Entry()

if 'hostname' in default:
    w_hostname.insert(0, default['hostname'])
if 'username' in default:
    w_username.insert(0, default['username'])
if 'password' in default:
    w_password.insert(0, default['password'])
if 'directory' in default:
    w_directory.insert(0, default['directory'])
if 'pattern' in default:
    w_pattern.insert(0, default['pattern'])

message = tk.StringVar()
w_notification = tk.Label(textvariable=message, width=100)

logfiles = []

def list_logs(ssh, directory, pattern):
    command = 'zgrep -l '+ pattern + ' ' + directory + '/*'
    stdin, stdout, stderr = ssh.exec_command(command)

    stdout=stdout.readlines()
    stdout=[l.strip('\n\r') for l in stdout]

    return stdout


def get_files(hostname, username, password, directory, pattern):
    ssh = ""

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=port, username=username, password=password)

    logfiles = list_logs(ssh, directory, pattern);
    scp = SCPClient(ssh.get_transport())
    for line in logfiles:
        print("Retrieving file " + line)
        message.set("Retrieving file " + line)
        screen.update()
        scp.get(line)

    message.set("Finished.")
    screen.update()

def check_input(event):
    if w_hostname.get() == "":
        message.set("hostname can't be empty")
        screen.update()
    elif w_username.get() == "":
        message.set("username can't be empty")
        screen.update()
    elif w_password.get() == "":
        message.set("password can't be empty")
        screen.update()
    elif w_pattern.get() == "":
        message.set("pattern can't be empty")
        screen.update()
    else:
        message.set(" ")
        screen.update()
        get_files(w_hostname.get(), w_username.get(), w_password.get(), w_directory.get(), w_pattern.get())

def run():
    screen.geometry("300x400")
    screen.title("Retrieve files with text pattern")
 
    tk.Label(text="Complete requested info:", bg="blue", width="300", height="2", font=("Calibri", 13)).pack() 
    tk.Label(text="").pack() 
 
    tk.label = tk.Label(text="Hostname").pack()
    w_hostname.pack()
 
    tk.label = tk.Label(text="Username").pack()
    w_username.pack()

    tk.label = tk.Label(text="Password").pack()
    w_password.pack()
 
    tk.label = tk.Label(text="Directory").pack()
    w_directory.pack()
 
    tk.label = tk.Label(text="Text w_pattern").pack()
    w_pattern.pack()

    w_notification.pack()
    tk.label = tk.Label(text="").pack()

    button = tk.Button(text="Retrieve logs")
    button.pack()

    screen.bind('<Return>', check_input)
    screen.bind('<space>', check_input)
    button.bind("<Button-1>", check_input)

    tk.label = tk.Label(text="").pack()

    screen.mainloop()

if __name__ == '__main__':
    run()
