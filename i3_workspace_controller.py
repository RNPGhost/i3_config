#!/usr/bin/python3
import sys
import subprocess
import json

NAME_SEPERATOR = '-'

def create_default_workspaces():
  for i in range(get_workspaces().__len__(), 0, -1):
    subprocess.Popen(["i3-msg", "rename workspace " + str(i) + " to " + get_default_workspace_name(i)])

def move_to_workspace(targetWorkspace, moveContainer=False, focus=False):
  targetWorkspaceNumber = targetWorkspace
  if targetWorkspace == 'next':
    targetWorkspaceNumber = get_current_workspace_number() + 1
  elif targetWorkspace == 'prev':
    targetWorkspaceNumber = get_current_workspace_number() - 1
    if targetWorkspaceNumber == 0:
      return
  targetWorkspaceName = get_target_workspace_name(targetWorkspaceNumber)
  if moveContainer:
    subprocess.Popen(["i3-msg", "move to workspace " + targetWorkspaceName])
  if focus:
    subprocess.Popen(["i3-msg", "workspace " + targetWorkspaceName])

def get_workspaces():
  handle = subprocess.Popen(["i3-msg", "-t", "get_workspaces"], stdout=subprocess.PIPE)
  output = handle.communicate()[0]
  data = json.loads(output.decode())
  data = sorted(data, key=lambda k: k['name'])
  arr = []
  for i in data:
    arr.append(i['name'])
  return arr

def get_default_workspace_name(monitorNumber):
  return ("1:" + chr(64 + monitorNumber) + NAME_SEPERATOR + "1")

def get_target_workspace_name(workspaceNumber):
  print(workspaceNumber)
  return str(workspaceNumber) + ":" + get_focused_workspace().split(':')[1].split(NAME_SEPERATOR)[0] + NAME_SEPERATOR + str(workspaceNumber)

def get_focused_workspace():
  handle = subprocess.Popen(["i3-msg","-t","get_workspaces"], stdout=subprocess.PIPE)
  output = handle.communicate()[0]
  data = json.loads(output.decode())
  data = sorted(data, key=lambda k: k['name'])
  for i in data:
    if(i['focused']):
      return i['name']

def get_current_workspace_number():
  return get_workspace_number(get_focused_workspace())

def get_workspace_number(workspaceName):
  print("current workspace number is " + workspaceName.split(NAME_SEPERATOR)[1])
  return int(workspaceName.split(NAME_SEPERATOR)[1])

def enough_arguments(requiredNumberOfArguments):
  enoughArguments = (len(sys.argv) >= requiredNumberOfArguments)
  if not enoughArguments:
    print("Error: Not enough arguments provided")
  return enoughArguments

if enough_arguments(2):
  command = sys.argv[1]
  if command == 'start_up':
    if get_workspaces().__len__() > 1:
      create_default_workspaces()
  elif command == 'focus':
    if enough_arguments(3):
      workspace = sys.argv[2]
      move_to_workspace(workspace, focus=True)
  elif command == 'move':
    if enough_arguments(3):
      workspace = sys.argv[2]
      move_to_workspace(workspace, moveContainer=True)
  elif command == 'move_and_focus':
    if enough_arguments(3):
      workspace = sys.argv[2]
      move_to_workspace(workspace, moveContainer=True, focus=True)
  else:
    print("Error: Command '" + command + "' not recognised")
