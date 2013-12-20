import os
import commands
from __builtin__ import Exception
from version_updates import update_small, update_mid, update_large

VERSIONFILE = '.version'

class ProjectDirError(Exception):
    message = 'This is not a project dir with a version!'


def get_version():
    ver = make_version()
    return '.'.join(ver)

def make_version():
    '''
        this checks if the cfg file needs to be created
        or just read
        then returns the version as a 3 item tuple
        (x,x,x)
    '''
    if not check_project_dir():
        raise ProjectDirError('This is not a project dir with a version!')
    if not check_version_file():
        make_version_file(get_setup_version())
    return tuple(open(VERSIONFILE,'r').read()[:-1].split(' '))

def check_project_dir():
    rtn = False
    if not 'setup.py' in os.listdir(os.curdir):
        rtn = False
    else:
        rtn = True
    return rtn

def check_version_file():
    return os.path.exists(VERSIONFILE)

def make_version_file(version=None):
    if version is None:
        ver = '0 0 1\n'
    else:
        ver = version.replace('.',' ') + '\n'
    tmp = open(VERSIONFILE,'w')
    START_VERSION = ver
    tmp.write(START_VERSION)
    tmp.close()

def write_new_setup(txt):
    f = open('setup.py','w')
    f.write(txt)
    f.close()

def get_setup_version():
    rtn = None
    try:
        ver = commands.getoutput('python setup.py --version')
        if raw_input('''Would you like me to update your setup.py file,
            right now, to use the versionup tool?
            if not, you need to see the README to do it yourself
            be warned I will overwrite it. (Y / N): ''').lower().startswith('y'):
            newSetup = update_setup_file()
            s = "{}\n write this file to disk?(Y / N): ".format(newSetup)
            if raw_input(s).lower().startswith('y'):
                write_new_setup(newSetup)

        rtn = ver
    except:
        pass
    return rtn

def change_version(txt):
    newline = (' '*4) + "'version': version,"
    rtn = ''
    txt = txt.split('\n')
    for line in txt:
        if "'version'" in line:
            line = newline[:]
        rtn += line + '\n'
    return rtn

def update_setup_file():
    '''
        warning this changes the setup.py file,
        always ask before calling this function
    '''
    txt = open('setup.py','r').readlines()
    newfile = ''

    lineone = "from versionup import get_version\n"
    linetwo = "version = get_version()\n"
    wroteOneAndTwo = False

    for line in txt:
        printed = False
        if 'config' in line or 'setup(' in line:
            if not wroteOneAndTwo:

                newfile += lineone
                newfile +=  linetwo
                newfile += '\n\n'
                wroteOneAndTwo = True

        newfile += line
    return change_version(newfile)

def update_version(grade=None):
    '''
        updates the number in the version file based on the grade s, m, or l
        grade s or small = updates 1.0.2 to 1.0.3
        grade m or mid =   updates 1.0.2 to 1.1.0
        grade l or large = updates 1.0.2 to 2.0.0
        default id small
    '''
    GRADES = {'s':update_small,
              'm':update_mid,
              'l':update_large}
    if grade is None:
        grade = 's'
    GRADES[grade]()

