import subprocess
import ctypes
import platform
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

LOG_FILE = "telemetry_ai_scanner_log.json"

KEYWORDS = [
    "telemetry", "diagnostic", "diagtrack",
    "cortana", "copilot", "ai",
    "feedback", "experience", "onedrive"
]

COPILOT_KEYWORDS = [
    "copilot", "windowscopilot", "ai experience"
]

# ---------------- ADMIN CHECK ----------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    messagebox.showerror("Admin Required", "Run this tool as Administrator.")
    raise SystemExit

# ---------------- POWERSHELL ----------------
def run_ps(cmd):
    return subprocess.check_output(
        ["powershell", "-NoProfile", "-Command", cmd],
        text=True,
        stderr=subprocess.DEVNULL
    )

# ---------------- LOGGING ----------------
def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def write_log(entry):
    log = load_log()
    log.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

# ---------------- SERVICE STATUS ----------------
def get_service_status(service_name):
    try:
        state = run_ps(
            f"(Get-Service -Name '{service_name}').StartType"
        ).strip()
        return "DISABLED" if state.lower() == "disabled" else "ENABLED"
    except:
        return "UNKNOWN"

# ---------------- SCAN ----------------
def scan():
    tree.delete(*tree.get_children())

    # -------- Appx --------
    try:
        appx = json.loads(run_ps(
            "Get-AppxPackage | Select Name, PackageFullName | ConvertTo-Json"
        ))
        if isinstance(appx, dict):
            appx = [appx]

        for p in appx:
            if any(k in p["Name"].lower() for k in KEYWORDS):
                tag = "COPILOT" if any(c in p["Name"].lower() for c in COPILOT_KEYWORDS) else "AI"
                tree.insert(
                    "",
                    "end",
                    values=("Appx", p["Name"], p["PackageFullName"], tag, "SYSTEM"),
                    tags=("neutral",)
                )
    except:
        pass

    # -------- Services --------
    try:
        svcs = json.loads(run_ps(
            "Get-Service | Select Name, DisplayName | ConvertTo-Json"
        ))
        if isinstance(svcs, dict):
            svcs = [svcs]

        for s in svcs:
            if any(k in s["DisplayName"].lower() for k in KEYWORDS):
                status = get_service_status(s["Name"])
                color = "disabled" if status == "DISABLED" else "enabled"
                tag = "COPILOT" if any(c in s["DisplayName"].lower() for c in COPILOT_KEYWORDS) else "AI"

                tree.insert(
                    "",
                    "end",
                    values=("Service", s["DisplayName"], s["Name"], tag, status),
                    tags=(color,)
                )
    except:
        pass

# ---------------- DISABLE ----------------
def disable_selected():
    for item in tree.selection():
        t, name, ident, tag, status = tree.item(item, "values")

        if t == "Service" and status != "DISABLED":
            start_type = run_ps(
                f"(Get-Service -Name '{ident}').StartType"
            ).strip()

            run_ps(f"Stop-Service -Name '{ident}' -Force")
            run_ps(f"Set-Service -Name '{ident}' -StartupType Disabled")

            write_log({
                "time": str(datetime.now()),
                "action": "disable",
                "type": t,
                "name": name,
                "id": ident,
                "original_start": start_type
            })

    scan()
    messagebox.showinfo("Done", "Selected services disabled (safe mode).")

# ---------------- RESTORE ----------------
def restore_selected():
    log = load_log()

    for item in tree.selection():
        t, name, ident, tag, status = tree.item(item, "values")

        if t != "Service":
            continue

        for entry in reversed(log):
            if entry.get("id") == ident and entry.get("action") == "disable":
                run_ps(
                    f"Set-Service -Name '{ident}' -StartupType {entry['original_start']}"
                )
                run_ps(f"Start-Service -Name '{ident}'")
                break

    scan()
    messagebox.showinfo("Restored", "Selected services restored.")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Telemetry & AI Scanner by FoxxCom")
root.configure(bg="#0b0b0b")
root.geometry("1000x520")

style = ttk.Style()
style.theme_use("default")
style.configure(
    "Treeview",
    background="#0b0b0b",
    foreground="#00ff00",
    fieldbackground="#0b0b0b",
    rowheight=24
)

tree = ttk.Treeview(
    root,
    columns=("Type", "Name", "ID", "Tag", "Status"),
    show="headings"
)

for col in ("Type", "Name", "ID", "Tag", "Status"):
    tree.heading(col, text=col)
    tree.column(col, width=180)

tree.tag_configure("disabled", foreground="#ff4444")
tree.tag_configure("enabled", foreground="#00ff00")
tree.tag_configure("neutral", foreground="#aaaaaa")

tree.pack(fill="both", expand=True, padx=10, pady=10)

btn_frame = tk.Frame(root, bg="#0b0b0b")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Scan", command=scan, bg="black", fg="#00ff00").pack(side="left", padx=10)
tk.Button(btn_frame, text="Disable Selected", command=disable_selected, bg="black", fg="#00ff00").pack(side="left", padx=10)
tk.Button(btn_frame, text="Restore Selected", command=restore_selected, bg="black", fg="#00ff00").pack(side="left", padx=10)

scan()
root.mainloop()
