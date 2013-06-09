import re
import sys
import os
import pwd
import socket
import subprocess
import shlex

def cd(argv):
  if os.path.exists(argv):
    os.chdir(argv)

while True:
  username = pwd.getpwuid(os.getuid()).pw_name
  hostname = socket.gethostname()
  cwd = os.getcwd()
  prompt = str(username) +  '@'+ str(hostname) + ':' + str(cwd) + '$ '

  try:
    line = raw_input(prompt)
    values = re.split('\s*\|\s*', line)
  except:
    print "Except.."
    sys.exit(1)

  i = 0
  precmd = ''
  for orgcmd in values:
    cmd = shlex.split(orgcmd)
    if len(cmd) == 0:
      continue
    elif cmd[0] == 'cd':
      if len(cmd) == 1:
        cd(os.environ['HOME'])
      elif len(cmd) == 2:
        cd(cmd[1])
    elif cmd[0] == 'exit':
      sys.exit(1)
    else:
      try:
        if i == 0 or precmd == '':
          if i+1 == len(values):
            precmd = subprocess.Popen(cmd, stderr=subprocess.STDOUT)
          else:
            precmd = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
          precmd.wait()
        else:
          if i+1 == len(values):
            precmd = subprocess.Popen(cmd, stdin=precmd.stdout, stderr=subprocess.STDOUT)
          else:
            precmd = subprocess.Popen(cmd, stdin=precmd.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
          precmd.wait()
      except:
        print "Except.."
    i = i + 1
