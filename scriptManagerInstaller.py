import maya.utils as utils
import os
import subprocess
import sys
import maya.cmds as cmds

user_setup_cod = """
import maya.cmds as cmds
import os

# insert path string
path = os.environ["MAYA_APP_DIR"] + "/scripts"
cmds.evalDeferred("print('\\nFile userSetup.py execute from " + path + "')")

# connect pycharm
try:
    if not cmds.commandPort(":4434", query=True):
        cmds.commandPort(name=":4434")
except Exception as message:
    print(message)

# load an_scriptManager
cmds.evalDeferred('from an_scriptManager import *')

# insert empty string
cmds.evalDeferred("print('')")
"""

script_manager_cod = '''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main Procedure:
    scriptManager()

Creation Date:
    march 27, 2020

Authors:
    Belyaev Andrey
    andreikin@mail.ru

Description:
    Creates a menu "Scripts" and loads a hierarchy of scripts into it.

Installation:
    1. Save the an_scriptManager.py to your local user/scripts folder
	                   example: ../my documents/maya/scripts/
	2. Add a few lines to the file userSetup.py:
            	    import maya.cmds as cmds
                    cmds.evalDeferred('from an_scriptManager import *')
	3. Start Maya

*************************************************************************************************************************
 version History
*************************************************************************************************************************
	v3.0.1
	- Add the ability to work with Maya 2023
	- Add an exception in case of an error
	- Add set path command
	- Edit an_sourceProcedures
	- Edit discription
	- Find procedures in hierarhy
*************************************************************************************************************************
"""

import maya.mel as mm
import maya.cmds as cmds
import os, sys
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QSettings

PROCEDURES = 'procedures'
FORBID_LIST = [PROCEDURES, 'scriptManagerInstaller', 'an_scriptManager', ".idea", ".git", "userSetup", "venv", "__init__", "__pycache__"]
VERSION = '3.0.1'


def scriptManager(path=""):
    p_menu = 'an_menu'
    if cmds.menu(p_menu, exists=True):  cmds.deleteUI(p_menu)
    cmds.menu(p_menu, l='Scripts', p='MayaWindow', tearOff=True)
    try:
        if not path:
            path = QSettings("scriptManager", "Settings").value("path")
            if not os.path.exists(str(path)):
                path = ""
        if path:
            sourceProcedures(os.path.abspath(path))
            checkContent(path, p_menu)
            print('Script manager v.'+VERSION+' loading scripts from: ' + path)
    except Exception as message:
        print('\\nScript manager not loaded :')
        print(message)
        print('\\n')
    finally:
        cmds.menuItem(divider=True, p=p_menu)
        cmds.menuItem("set path", l="Set path to scripts folder", p=p_menu, c='set_path()')
        # cmds.menuItem("Open", l="Open scripts folder", p=p_menu, c='open_dir()')


def open_dir():
    path = QSettings("scriptManager", "Settings").value("path")
    if path :
        os.startfile(path)


def set_path():
    path = QtWidgets.QFileDialog.getExistingDirectory(directory=QtCore.QDir.currentPath())
    try:
        if path and os.path.exists(path) and os.path.isdir(path):
            QSettings("scriptManager", "Settings").setValue("path", path)
            scriptManager(path)
    except Exception as e:
        print(e)


def sort_path(path):
    directories = sorted([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d != ".git"])
    files_py = sorted([f[:-3] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f[-3:] == '.py'])
    files_mel = sorted([f[:-4] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f[-4:] == '.mel'])
    return directories, files_py, files_mel


def sourceProcedures(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            forbid_folder = any([x in dir_path for x in FORBID_LIST[1:]])
            if not dir_path in list(sys.path) and not forbid_folder:
                sys.path.insert(0, dir_path)
                print(dir_path + " added to path list")


def checkContent(path, p_menu):
    directories, files_py, files_mel = sort_path(path)
    for fld in [d for d in directories if not d in FORBID_LIST]:
        cmds.menuItem(fld + "name", l=fld, tearOff=True, sm=True, p=p_menu)
        if os.listdir(os.path.join(path, fld)):
            checkContent(os.path.join(path, fld), fld + "name")

    if directories: cmds.menuItem(divider=True, p=p_menu)

    for p_file in [d for d in files_py if not d in FORBID_LIST]:
        norm = os.path.join(path, p_file + '.py')
        mc = 'run_python(r"' + norm + '")'
        cmds.menuItem(p_file, l=p_file, p=p_menu, c=mc)

    for m_file in [d for d in files_mel if not d in FORBID_LIST]:
        cmds.menuItem(m_file, l=m_file, p=p_menu, c=r'run_mel(" {}\{}.mel")'.format(path, m_file).replace('\\\\', '/'))


def run_mel(data):
    mm.eval(r'source "' + data[1:] + '"')
    fl = data.split("/")[-1].split(".")[0]
    mm.eval(fl)


def run_python(data):
    data = os.path.abspath(data)
    path = os.path.dirname(data)
    fl, ex = os.path.basename(data).split(".")
    system_paths = list(sys.path)
    if not path in system_paths:
        sys.path.insert(0, path)
    cmds.evalDeferred('from ' + fl + ' import *; ' + fl + '()')

scriptManager()
'''



def onMayaDroppedPythonFile(obj):

    path = os.path.join(os.environ['MAYA_APP_DIR'].split(";")[0], "scripts", "userSetup.py")
    script_manager_path = os.path.join(os.environ['MAYA_APP_DIR'].split(";")[0], "scripts", "an_scriptManager.py")

    if not os.path.exists(path):
        with open(path, "w") as file:
            file.write(user_setup_cod)

    with open(script_manager_path, "w") as file:
        file.write(script_manager_cod)

    skript_folder =  os.path.join(os.environ['MAYA_APP_DIR'].split(";")[0], "scripts")
    sys.path.insert(0, skript_folder)

    cmds.evalDeferred("from an_scriptManager import *")



# from an_scriptManager import *