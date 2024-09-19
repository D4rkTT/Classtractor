import subprocess
import re
import time
import platform
import os

AAPT_PATH = "aapt"
ADB_PATH = "adb"

def extract_package_id_from_apk(apk_path, debug = False):
    try:
        result = subprocess.run(
            [AAPT_PATH, "dump", "xmltree", apk_path, "AndroidManifest.xml"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        package_pattern = re.compile(r'A:\s+package="([^"]+)"')
        package_id = package_pattern.search(result.stdout)

        if package_id:
            return package_id.group(1)
        else:
            return None
    except subprocess.CalledProcessError as e:
        if debug:
            print(f"[Debug] Error occurred while extracting package ID: {e.stderr}")
        return None

def extract_activities_from_apk(apk_path, debug = False):
    try:
        result = subprocess.run(
            [AAPT_PATH, "dump", "xmltree", apk_path, "AndroidManifest.xml"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        activity_pattern = re.compile(r'E: activity[^:]*:.*\n.*A: android:name\(\S+\)="([^"]+)"')
        activities = activity_pattern.findall(result.stdout)
        
        if activities:
            return activities
        else:
            return []
    except subprocess.CalledProcessError as e:
        if debug:
            print(f"[Debug] Error occurred while extracting activities: {e.stderr}")
        return []

def enable_adb_root(debug = False):
    try:
        result = subprocess.run(
            [ADB_PATH, "root"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        if debug:
            print(f"[Debug] Error occurred enabling adb root: {e.stderr}")
        return False

def printLogo():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    l = '''
   ____ _               _                  _             
  / ___| | __ _ ___ ___| |_ _ __ __ _  ___| |_ ___  _ __ 
 | |   | |/ _` / __/ __| __| '__/ _` |/ __| __/ _ \| '__|
 | |___| | (_| \__ \__ \ |_| | | (_| | (__| || (_) | |   
  \____|_|\__,_|___/___/\__|_|  \__,_|\___|\__\___/|_|                                
   V0.1                                       By DarkT
   '''
    print(l)

def main():
    global AAPT_PATH, ADB_PATH

    printLogo()

    apk_file = input("APK Path: ")
    if not os.path.isfile(apk_file):
        print("[-] APK file not exist.")
        return

    AAPT_PATH = input("AAPT binary Path: ")
    if not os.path.isfile(AAPT_PATH):
        print("[-] AAPT binary not exist.")
        return
    
    ADB_PATH = input("ADB binary Path: ")
    if not os.path.isfile(ADB_PATH):
        print("[-] ADB binary not exist.")
        return

    DEBUG = input("Debug? (y or N): ")
    if DEBUG == "y":
        debug = True
    else:
        debug = False
    
    print("[+] Enabling ADB root...")
    if not enable_adb_root(debug):
        print("[-] Failed to enable ADB root, make sure the emulator/device are running.")
        return

    package_id = extract_package_id_from_apk(apk_file, debug)
    if package_id == None:
        print("[-] Error extracting package id")
        return

    activities = extract_activities_from_apk(apk_file, debug)
    if len(activities) < 1:
        print("[-] Error extracting activites")
        return
    
    for activity in activities:   
        try:
            full_activity = f"{package_id}/{activity}"
            printLogo()
            print(f"[+] Killing app: {package_id}")
            subprocess.run([ADB_PATH, "shell", "am", "force-stop", package_id], check=False, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)
            time.sleep(1)
            print(f"[+] Spawning activity: {full_activity}")
            subprocess.run([ADB_PATH, "shell", "am", "start", "-n", full_activity], check=False, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)
            next = input("\nNext? (N to exit, Enter to continue): ")
            if next == "N":
                break
            
        except BaseException as e:
            if debug:
                print(f"[-] Failed to start activity: {full_activity}. Error: {e}")

    print("[#] Finished!")

if __name__ == "__main__":
    main()
