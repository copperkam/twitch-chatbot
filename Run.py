import subprocess
FileP1 = "program.py"
FileP2 = "twitchchatgrab.py"

subprocess.Popen(['start', 'cmd', '/k', 'python', FileP1], shell=True)
subprocess.Popen(['start', 'cmd', '/k', 'python', FileP2], shell=True)
