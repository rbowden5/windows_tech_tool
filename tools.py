import tkinter as tk
from tkinter import messagebox
import subprocess
from pathlib import Path

PS1 = Path(__file__).parent / "windowsupdate.ps1"

def cmd_abortshutdown():
    cmd = "shutdown /a"
    result = subprocess.run(
        ["powershell", "-Command", cmd],
        capture_output=True, text=True
    )
    output.delete("1.0", tk.END)
    output.insert(tk.END, "Shutdown/Restart has been canceled. Please save worka and try again")

def cmd_chkdsk():
    cmd = "Start-Process cmd -Verb RunAs -ArgumentList '/c echo Y| chkdsk C: /f & shutdown /r /t 60'"
    subprocess.Popen(["powershell", "-Command", cmd])

def cmd_checkps(function_name):
	# command_start = "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"
	# subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", -Command", command_start])
	command = f". '{PS1}'; UpdateTest"
	subprocess.Popen(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command])

def cmd_dismsfc():
    ps_cmd = """Start-Process powershell -Verb RunAs -Wait -ArgumentList '-Command "DISM /Online /Cleanup-Image /RestoreHealth; sfc /scannow; Read-Host ''Press Enter to close''"'"""
    subprocess.Popen(["powershell", "-Command", ps_cmd])

def cmd_restart():
    cmd = "shutdown /r /t 60"
    result = subprocess.run(
        ["powershell", "-Command", cmd],
        capture_output=True, text=True
    )
    output.delete("1.0", tk.END)
    output.insert(tk.END, result.stdout)

def get_uptime():
    #cmd = "$uptime = (Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime"
    cmd = "((Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime) | Select-Object -ExpandProperty Days" 
    result = subprocess.run(
        ["powershell", "-Command", cmd],
        capture_output=True, text=True
    )
    return str(result.stdout)
   
def run_check():
    result = subprocess.run(
        ["powershell", "-Command", "Get-Date"],
        capture_output=True, text=True
    )
    output.delete("1.0", tk.END)
    output.insert(tk.END, result.stdout)


root = tk.Tk()
root.title("Tech Support Tool")
tk.Label(root, text=f"Your computer has been on for {get_uptime()} days").pack(pady=5)
tk.Button(root, text="Abort any upcoming shutdown to save work", command=cmd_abortshutdown).pack(pady=5)
tk.Button(root, text="Windows Update Check", command=cmd_checkps("UpdateTest")).pack(pady=5)
tk.Button(root, text="Check Date", command=run_check).pack(pady=5)
tk.Button(root, text="Restart Computer", command=cmd_restart).pack(pady=5)
tk.Button(root, text="DISM and SFC", command=cmd_dismsfc).pack(pady=5)
tk.Button(root, text="Check Disk", command=cmd_chkdsk).pack(pady=5)
output = tk.Text(root, height=10, width=60)
output.pack()

root.mainloop()