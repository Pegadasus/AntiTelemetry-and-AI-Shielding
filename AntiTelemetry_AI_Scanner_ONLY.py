import subprocess
import os

# ======================
# ENABLE ANSI COLORS
# ======================
os.system("")

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ======================
# HELPERS
# ======================
def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, text=True)
    except subprocess.CalledProcessError:
        return ""

def header(title):
    print(f"\n{BLUE}=== {title} ==={RESET}")

def status_line(name, state, start=None):
    color = GREEN if state in ("STOPPED", "DISABLED") else YELLOW
    print(f"{color}{name:<25} State: {state:<10}", end="")
    if start:
        print(f" Start: {start}{RESET}")
    else:
        print(RESET)

# ======================
# SERVICE SCAN
# ======================
SERVICES = [
    "DiagTrack",
    "dmwappushservice",
    "WerSvc",
    "DiagSvc",
    "DPS",
    "WdiServiceHost",
    "WdiSystemHost",
    "PcaSvc",
    "RetailDemo",
    "RemoteRegistry",
    "WSearch"
]

def scan_services():
    header("Telemetry & Diagnostics Services")
    for svc in SERVICES:
        q = run(f"sc query {svc}")
        qc = run(f"sc qc {svc}")

        if not q:
            print(f"{RED}{svc:<25} NOT PRESENT{RESET}")
            continue

        state = "UNKNOWN"
        if "RUNNING" in q:
            state = "RUNNING"
        elif "STOPPED" in q:
            state = "STOPPED"

        start = "UNKNOWN"
        if "AUTO_START" in qc:
            start = "AUTO"
        elif "DEMAND_START" in qc:
            start = "MANUAL"
        elif "DISABLED" in qc:
            start = "DISABLED"

        status_line(svc, state, start)

# ======================
# PROCESS SCAN
# ======================
TELEMETRY_PROCESSES = [
    "CompatTelRunner.exe",
    "DeviceCensus.exe",
    "DiagTrackRunner.exe",
    "SearchIndexer.exe",
    "WmiPrvSE.exe",
    "WerFault.exe",
]

AI_PROCESSES = [
    "Copilot.exe",
    "msedgewebview2.exe",
    "SearchHost.exe",
    "TextInputHost.exe",
    "RuntimeBroker.exe",
]

def scan_processes(title, processes):
    header(title)
    out = run("tasklist")
    found = False
    for p in processes:
        if p.lower() in out.lower():
            print(f"{YELLOW}{p:<30} RUNNING{RESET}")
            found = True
    if not found:
        print(f"{GREEN}None detected{RESET}")

# ======================
# POLICY SCAN
# ======================
def scan_policy(title, key, value):
    header(title)
    out = run(f'reg query "{key}" /v {value}')
    if not out:
        print(f"{YELLOW}NOT CONFIGURED{RESET}")
    elif "0x1" in out or "0x0" in out:
        print(f"{CYAN}{out.strip()}{RESET}")
    else:
        print(out)

# ======================
# MAIN
# ======================
print(f"\n{CYAN}ANTI-TELEMETRY & AI SCANNER (READ-ONLY){RESET}")
print(f"{CYAN}No changes will be made to this system{RESET}")

scan_services()

scan_processes("Telemetry Processes (Running)", TELEMETRY_PROCESSES)
scan_processes("AI / Copilot Processes (Running)", AI_PROCESSES)

scan_policy(
    "Telemetry Policy (AllowTelemetry)",
    r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection",
    "AllowTelemetry"
)

scan_policy(
    "Windows Copilot Policy",
    r"HKLM\Software\Policies\Microsoft\Windows\WindowsCopilot",
    "TurnOffWindowsCopilot"
)

scan_policy(
    "Widgets (News & Interests)",
    r"HKLM\Software\Policies\Microsoft\Dsh",
    "AllowNewsAndInterests"
)

scan_policy(
    "Edge Background Mode",
    r"HKLM\Software\Policies\Microsoft\Edge",
    "BackgroundModeEnabled"
)

header("Protected Components (Informational)")
print(f"{CYAN}WmiPrvSE.exe        → Core system (should be running){RESET}")
print(f"{CYAN}RuntimeBroker.exe  → Core system (should be running){RESET}")
print(f"{CYAN}Defender AI        → Security critical{RESET}")

print(f"\n{GREEN}✔ SCAN COMPLETE — NO CHANGES MADE{RESET}\n")
