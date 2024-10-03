import os
from sys import platform
from basefunc.localconfig import addlocalsettings


TEST_CONFIG = {
   'server': 'https://test.x.com/',
    # 'driver': 'chrome headless',
    'driver':  'chrome',

}


def getProjectFolder():
    startPath = __file__
    projectFolder = ""
    while True:
        (pre, post) = os.path.split(startPath)
        if post == "basefunc":
            projectFolder = pre
            break
        else:
            startPath = pre
    return projectFolder


TEST_CONFIG['projectroot'] = getProjectFolder()
TEST_CONFIG['baselinefolder'] = os.path.join(TEST_CONFIG['projectroot'], 'files')
TEST_CONFIG['driverfolder'] = os.path.join(TEST_CONFIG['projectroot'],'sel-driver')
TEST_CONFIG['screenshotsfolder'] = os.path.join(TEST_CONFIG['projectroot'],'screenshots')
TEST_CONFIG['filessfolder'] = os.path.join(TEST_CONFIG['projectroot'],'files/')
TEST_CONFIG['remotepath'] = "C:\\python\\files\\"

if platform == "win32":
  TEST_CONFIG['FILES'] = "C:\\automation\\intouch-ui-python\\files\\"
else:
  TEST_CONFIG['FILES'] = os.path.join(TEST_CONFIG['projectroot'], 'files/')

addlocalsettings(TEST_CONFIG)
