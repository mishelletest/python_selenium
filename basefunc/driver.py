import os
from sys import platform
if(platform == "win32"):
    import winreg
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from shutil import copyfile
import zipfile

from selenium.webdriver.chrome.options import Options

from basefunc.config import TEST_CONFIG

class Driver(object):
    def __init__(self):
        pass

    def extract_zip(self, zipfileName, extractedFile, destinationFolder):
        archive = zipfile.ZipFile(zipfileName)
        try:
            archive.extract(extractedFile, destinationFolder)
        except Exception as e:
            if e.args[0] not in [26, 13] and e.args[1] not in ['Text file busy', 'Permission denied']:
                raise e
        return True

    def get_name(self):
        raise NotImplementedError("get_name() is not implemented for the generic driver")

    def get_os_type(self):
        #pl = sys.platform
        # we'll just stick with win32 for now
        return "win32"

    def get_tmp_zipped_drv_path(self):
        return os.path.join(TEST_CONFIG['driverfolder'], "tmp.zip")

    def get_web_driver_instance(self):
        raise NotImplementedError("get_web_driver_instance() is not implemented for the generic driver")

    def download_latest(self):
        raise NotImplementedError("download_latest() is not implemented for the generic driver")

    def get_driver_version(self):
        raise NotImplementedError("get_driver_version() is not implemented for the generic driver")

    def download_latest_from_url(self, download_url, download_to_file):
        if os.path.exists(download_to_file):
            os.remove(download_to_file)

        downloadZipPath = self.get_tmp_zipped_drv_path()

        if os.path.exists(downloadZipPath):
            os.remove(downloadZipPath)

        latestVersion = self.get_driver_version()
        downloadUrl = f"{download_url}/{latestVersion}/{self.get_name()}_{self.get_os_type()}.zip"
        print(f"Downloading driver from {downloadUrl} ...")
        downloadResponse = requests.get(downloadUrl, stream=True)
        if downloadResponse.status_code != 200:
            raise Exception(f"Error downloading driver from: {downloadUrl}")

        with open(downloadZipPath, "wb") as zippedDrv:
            zippedDrv.write(downloadResponse.content)

        print(f"Downloaded driver archive to {downloadZipPath}")

        (_, downloadFileName) = os.path.split(download_to_file)
        self.extract_zip(downloadZipPath, downloadFileName, TEST_CONFIG['driverfolder'])

        print(f"Zip file extracted to: {download_to_file}")

        if os.path.exists(downloadZipPath):
            os.remove(downloadZipPath)

    def try_load_web_driver(self):
        loadResult = False
        attemptToDownload = True
        try:
            inst = self.get_web_driver_instance()
            loadResult = True
        except WebDriverException as wde:
            if "executable needs to be in PATH" in wde.msg:
                print("The driver is not found. Will try to download the latest")
            elif "session not created" in wde.msg:
                print("Incompatible version of the driver found. Will try to download the latest. " + wde.msg)
            else:
                attemptToDownload = False
                print("Unknown error. Exiting ..." + wde.msg)
        if loadResult:
            inst.close()
            inst.quit()
        return (loadResult, attemptToDownload)

    @staticmethod
    def getDriverClass():
        driverName = TEST_CONFIG['driver'].lower()
        if driverName == "chrome":
            if platform == "win32":
                return ChromeDriver()
            elif platform == "linux":
                return RemoteChromeDriverHeadless()
            elif platform == "darwin":
                return ChromeDriver()
        elif driverName == "chrome headless":
            if platform == "win32":
                return ChromeDriverHeadless()
            elif platform == "linux":
                return ChromeDriverHeadless()
            elif platform == "darwin":
                return ChromeDriver()
        elif driverName == "ie":
            return IEDriver()
        elif driverName == "edge":
            return EdgeChromiumDriver()
        elif driverName == "remote chrome headless":
            return RemoteChromeDriverHeadless()
        else:
            raise Exception(f"{driverName} is unsupported driver")

class ChromeDriver(Driver):
    download_url = "http://chromedriver.storage.googleapis.com"
    latest_ver_url = "http://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    if (platform == "win32"):
        path_to_driver = os.path.join(TEST_CONFIG['driverfolder'], "chromedriver.exe")
    elif (platform == "linux"):
        path_to_driver = os.path.join(TEST_CONFIG['driverfolder'], "chromedriver_linux_98")
    else:
        path_to_driver = os.path.join(TEST_CONFIG['driverfolder'], "chromedriver")

    def get_name(self):
        return "chromedriver"

    def get_web_driver_instance(self):
        opt=Options()
        opt.add_argument("--width=1936")
        opt.add_argument("--height=1056")
        return webdriver.Chrome(executable_path=self.path_to_driver, chrome_options=opt)


class ChromeDriverHeadless(Driver):
    download_url = "http://chromedriver.storage.googleapis.com"
    latest_ver_url = "http://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    if (platform == "win32"):
        path_to_driver = os.path.join(TEST_CONFIG['driverfolder'], "chromedriver.exe")
    elif (platform == "linux"):
        path_to_driver = os.path.join(TEST_CONFIG['driverfolder'], "chromedriver_linux_98")
    else:
        path_to_driver = os.path.join(TEST_CONFIG['driverfolder'], "chromedriver")

    def get_name(self):
        return "chromedriver"

    def get_web_driver_instance(self):
        opt=Options()
        opt.add_argument("--headless")
        opt.add_argument("--width=1936")
        opt.add_argument("--height=1056")
        return webdriver.Chrome(executable_path=self.path_to_driver, chrome_options=opt)


    def get_driver_version(self):
        if(platform == "win32"):
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Google\Chrome\BLBeacon")
            (chromeversion, _) = winreg.QueryValueEx(key, "version")
            print(f"chrome version from registry: {chromeversion}")
            major = int(chromeversion.split('.')[0])
            latestVersionResponse = requests.get(f"{self.latest_ver_url}_{major}")
            if latestVersionResponse.status_code != 200 and major > 0:
                latestVersionResponse = requests.get(f"{self.latest_ver_url}_{major-1}")
                if latestVersionResponse.status_code != 200:
                    latestVersionResponse = requests.get(f"{self.latest_ver_url}")
                    if latestVersionResponse.status_code != 200:
                        raise Exception(f"Error retrieving driver's latest version information from: {self.latest_ver_url} for chrome major version: {major}")
            return latestVersionResponse.text.rstrip()

    def download_latest(self):
        self.download_latest_from_url(self.download_url, self.path_to_driver)

class RemoteChromeDriverHeadless(ChromeDriverHeadless):
    def get_name(self):
        return "chromedriver"

    def get_web_driver_instance(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless")
        opt.add_argument("--width=1936")
        opt.add_argument("--height=1056")
        return webdriver.Remote( "http://grid.selenium.td-dev-second.com:4444/wd/hub", opt.to_capabilities())

class EdgeChromiumDriver(Driver):
    download_url = "https://msedgedriver.azureedge.net"
    latest_ver_url = "https://msedgedriver.azureedge.net/LATEST_STABLE"
    path_to_driver = os.path.join(TEST_CONFIG['driverfolder'], "msedgedriver.exe")

    def get_name(self):
        return "edgedriver"

    def get_web_driver_instance(self):
        return webdriver.Edge(executable_path=self.path_to_driver)

    def get_driver_version(self):
        latestVersionResponse = requests.get(self.latest_ver_url)
        if latestVersionResponse.status_code != 200:
            raise Exception(f"Error retrieving driver's latest version information from: {self.latest_ver_url}")
        return latestVersionResponse.text.rstrip()

    def download_latest(self):
        self.download_latest_from_url(self.download_url, self.path_to_driver)

class IEDriver(Driver):
    drv_exe_name = "IEDriverServer.exe"
    path_to_driver = os.path.join(TEST_CONFIG['driverfolder'], drv_exe_name)

    def get_name(self):
        return "IEDriverServer"

    def get_web_driver_instance(self):
        return webdriver.Ie(executable_path=self.path_to_driver)

    def download_latest(self):
        if os.path.exists(self.path_to_driver):
            os.remove(self.path_to_driver)
        srcFile = os.path.join(TEST_CONFIG['driverfolder'], "windows")
        srcFile = os.path.join(srcFile, "ie")
        srcFile = os.path.join(srcFile, self.drv_exe_name)
        print(f"Copying driver from {srcFile} ...")
        copyfile(srcFile, self.path_to_driver)
