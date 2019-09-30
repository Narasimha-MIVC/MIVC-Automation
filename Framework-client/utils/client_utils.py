import os
import sys
import zipfile
import glob
import re
import json
import shutil
import time
import autoit
import subprocess
# import win32com.client
import win32com.client as win32
from selenium import webdriver
from robot.api.logger import console

if re.match(r'^2.7.', sys.version):
    import _winreg as winreg
else:
    import winreg


def install_client_silently(**params):
    """
    Author: Simmi LNU
    install_client() - Installs connect client
    """
    # checking whether Mt installer or St installer
    if params["is_runtype_mt"] == '1':
        srcDir = "\\\\10.17.1.56\\Builds\\" + params["version"] + "\\install-win\cloud\MitelConnect.exe"
        dstDir = "C:\ClientInstaller"
    else:
        srcDir = "\\\\10.17.1.56\\Builds\\" + params["version"] + "\\install-win\MitelConnect.exe"
        dstDir = "C:\ClientInstaller"
    # copy the required installer into ClientInstaller location
    dst_file = os.path.join(dstDir, "MitelConnect.exe")
    if os.path.exists(dst_file):
        os.remove(dst_file)
    cmd = "cmd /c xcopy " + srcDir + " " + dstDir + " /e /y"
    os.system(cmd)
    # install the required installer
    command = r'start /wait C:\ClientInstaller\MitelConnect.exe /s /sms /v"/qn INSTALLDIR=C:\NodeWebKit'
    os.system(command)
    console("Installation Completed!!!")


def uninstall_client():
    """
    Author: Simmi LNU
    uninstall_client() - Uninstalls connect client
    """
    command1 = r'wmic product where name="Mitel Connect" call uninstall /nointeractive'
    command2 = r'wmic product where name="Mitel Presenter" call uninstall /nointeractive'
    command3 = r'wmic product where name="Mitel Teamwork" call uninstall /nointeractive'
    os.system(command1)
    os.system(command2)
    os.system(command3)


def verify_client_plugins():
    """
    Author: UKumar
    verify_client_plugins() - To verify that all the plugins required for Connect Client are installed
    """
    try:
        client_add_ins_to_verify = ['ShoreTelConnectCASConnHostAddIn', 'ShoreTelConnectContactUploadAddIn',
                                    'ShoreTelConnectSTVMAddIn', 'ShoreTelConnectUCBAddIn']

        connection = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        akeys = winreg.OpenKey(connection, r'SOFTWARE\Microsoft\Office\Outlook\Addins')
        installed_add_ins = []
        for i in range(10):
            try:
                x = winreg.EnumKey(akeys, i)
                y = winreg.OpenKey(akeys, x)
                val = winreg.QueryValueEx(y, "FriendlyName")
                installed_add_ins.append(val[0])
            except EnvironmentError:
                break
        winreg.CloseKey(akeys)

        for add_in in client_add_ins_to_verify:
            if add_in in installed_add_ins:
                # log.mjLog.LogReporter("ManhattanComponent", "info", "verify_client_plugins - %s plugin installed" %add_in)
                print("verify_client_plugins - %s plugin installed" % add_in)
            else:
                raise AssertionError("%s plugin not installed" % add_in)
    except:
        raise


def delete_registry_entry():
    """
    Author: Simmi LNU
    delete_registry_entry() - Delets ShoreTel key from the registry
    """
    try:
        connection = winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT)
        print(connection)
        akeys = winreg.OpenKey(connection, r'')
        print(akeys)
        winreg.DeleteKeyEx(akeys, 'miconnect\shell\open\command')
        winreg.DeleteKeyEx(akeys, 'miconnect\shell\open')
        winreg.DeleteKeyEx(akeys, 'miconnect\shell')
        winreg.DeleteKeyEx(akeys, 'miconnect')
        winreg.CloseKey(akeys)
        
        connection = winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT)
        print(connection)
        akeys = winreg.OpenKey(connection, r'')
        print(akeys)
        # winreg.DeleteKeyEx(akeys, 'mitwd\shell\open\command')
        winreg.DeleteKeyEx(akeys, 'mitwd\shell\open')
        winreg.DeleteKeyEx(akeys, 'mitwd\shell')
        winreg.DeleteKeyEx(akeys, 'mitwd')
        winreg.CloseKey(akeys)

        connection = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        print(connection)
        akeys = winreg.OpenKey(connection, r'SOFTWARE')
        print(akeys)
        winreg.DeleteKeyEx(akeys, 'ShoreTel\Client')
        winreg.DeleteKeyEx(akeys, 'ShoreTel')
        winreg.CloseKey(akeys)

        connection = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        print(connection)
        akeys = winreg.OpenKey(connection, r'SOFTWARE\WOW6432Node')
        print(akeys)
        winreg.DeleteKeyEx(akeys, 'ShoreTel\ShoreTel Connect')
        winreg.DeleteKeyEx(akeys, 'ShoreTel')
        winreg.DeleteKeyEx(ikeys, 'Shoreline Communications\InstallState\Products\ShoreTel Connect')
        winreg.DeleteKeyEx(ikeys, 'Shoreline Communications\InstallState\Products')
        winreg.DeleteKeyEx(ikeys, 'Shoreline Communications\InstallState')
        winreg.DeleteKeyEx(ikeys, 'Shoreline Communications')
        winreg.CloseKey(akeys)

    except:
        return False


def unzip_recording(file_path):
    """
    Author: UKumar
    unzip_recording() - extracts recording file from zip file
    """
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            z.extractall(os.path.dirname(file_path))

        for file in glob.glob(os.path.join(os.path.dirname(file_path), '*.zip')):
            os.remove(file)
    except FileNotFoundError as e:
        raise e


def launch():
    browser = webdriver.Chrome("C:\\NodeWebKit\\chromedriver.exe")


def delete_mitel_folder():
    """
    Author: Indresh
    delete_shoretel_folder() - Deletes Mitel folder from "\\AppData\\Local\\Mitel"
    """
    try:
        local_path = os.getenv('LOCALAPPDATA') + "\Mitel"
        connect_path = "C:\Program Files (x86)\Mitel"
        presenter_path = "C:\Program Files (x86)\Mitel Presenter"
        teamwork_path = "C:\Program Files (x86)\Mitel Teamwork"
        path_list = [local_path, connect_path, presenter_path, teamwork_path]
        for i in path_list:
            if os.path.exists(i):
                shutil.rmtree(i, ignore_errors=True)
            else:
                continue
    except:
        return False


def close_program(**params):
    '''
    Author: Indresh
    Closes the desired program
    params["program"] will contain the program name which needs to be closed
    '''
    try:
        killCommand = "taskkill.exe /f /im " + params["program"] + ".exe"
        os.system(killCommand)
    except:
        raise
        

def verify_installation_folder(**params):
    '''
    Author: Simmi
    Verify the Installation Folder
    params["is_runtype_mt"] will contain the whether Mt or St
    '''
    try:
      tw_dir = "C:\Program Files (x86)\Mitel Teamwork"
      tw_exe = "C:\Program Files (x86)\Mitel Teamwork\Mitel Teamwork.exe"
      if params["is_runtype_mt"] == '1':
        #verify the Mitel Teamwork exe install
        if os.path.isdir(tw_dir):
            if not os.path.isfile(tw_exe):
                raise AssertionError("Teamwork exe should be present")
            #create json file
            # console("Started")
            # json_file_path = "C:\Users\Administrator\AppData\Roaming"
            # json_file_name = "teamwork.dev.setting"
            # data = {"mainUrl":"https://ws.qa.shoretel.com/tww-sco/web/index.html","showDevTool":False}
            # filePathNameWExt = json_file_path + '/' + json_file_name + '.json'
            # with open(filePathNameWExt, 'w') as fp:
              # json.dump(data, fp)
        else:
          raise AssertionError("Mitel Teamwork is not created;installed with MT")
      else:
        #verify the Mitel Teamwork exe not present
        if os.path.isdir(tw_dir):
          raise AssertionError("Mitel Teamwork is created;installed with ST")
    except:
        raise

def compose_new_outlook_mail():
    '''
    Author: Simmi LNU
    compose_new_outlook_mail() - Display/compose the new outlook mail
    '''
    try:
        outlook = win32.Dispatch('outlook.application')
        time.sleep(2)
        mail = outlook.CreateItem(0)
        mail.To = "connectauto2"
        
        autoit.control_click("[TITLE:Untitled - Message (HTML)]", "[CLASS:RichEdit20WPT;INSTANCE:2]")
        autoit.control_send("[TITLE:Untitled - Message (HTML)]", "[CLASS:RichEdit20WPT;INSTANCE:3]", "{TAB}")
        mail.Display(True)
    except:
        raise
        
if __name__ == "__main__":
    param_name = sys.argv[1]
    if param_name == "install":
        install_client(sys.argv[2])
    elif param_name == "uninstall":
        uninstall_client()
    elif param_name == "verify_client_plugins":
        verify_client_plugins()
    elif param_name == "delete_registry_entry":
        delete_registry_entry()
    elif param_name == "launch":
        launch()
    else:
        pass
