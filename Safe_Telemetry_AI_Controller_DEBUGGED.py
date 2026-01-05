import subprocess
import sys
import os

# ======================
# ENABLE ANSI COLORS
# ======================
os.system("")

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# ======================
# HELPERS
# ======================
def run_silent(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode

def run_show(cmd):
    subprocess.run(cmd, shell=True)

def header(title):
    print(f"\n{BLUE}=== {title} ==={RESET}")

def ok(msg):
    print(f"{GREEN}[OK]{RESET} {msg}")

def info(msg):
    print(f"{YELLOW}[INFO]{RESET} {msg}")

def skip(msg):
    print(f"{RED}[SKIPPED]{RESET} {msg}")

# ======================
# ADMIN CHECK
# ======================
if run_silent("net session") != 0:
    print(f"{RED}ERROR: Run this script as Administrator{RESET}")
    sys.exit(1)

# ======================
# TELEMETRY
# ======================
header("Telemetry Hardening (Safe)")

if run_silent("sc query DiagTrack") == 0:
    run_silent("sc stop DiagTrack")
    run_silent("sc config DiagTrack start= disabled")
    ok("DiagTrack disabled")
else:
    skip("DiagTrack not present")

if run_silent("sc query WerSvc") == 0:
    run_silent("sc stop WerSvc")
    run_silent("sc config WerSvc start= disabled")
    ok("Windows Error Reporting disabled")
else:
    skip("WerSvc not present")

run_silent(
    r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" '
    r'/v AllowTelemetry /t REG_DWORD /d 0 /f'
)
ok("Telemetry policy set to minimum (0)")

# ======================
# SEARCH INDEXER
# ======================
header("Search Indexing")

if run_silent("sc query WSearch") == 0:
    run_silent("sc stop WSearch")
    run_silent("sc config WSearch start= disabled")
    ok("Search Indexer disabled")
else:
    skip("Search service not present")

# ======================
# COPILOT & AI
# ======================
header("Copilot & AI")

run_silent(
    r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot" '
    r'/v TurnOffWindowsCopilot /t REG_DWORD /d 1 /f'
)
ok("Copilot disabled by policy")

run_silent(
    r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Dsh" '
    r'/v AllowNewsAndInterests /t REG_DWORD /d 0 /f'
)
ok("Widgets disabled")

# ======================
# EDGE BACKGROUND
# ======================
header("Edge & WebView")

run_silent(
    r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" '
    r'/v BackgroundModeEnabled /t REG_DWORD /d 0 /f'
)
ok("Edge background mode disabled")

# ======================
# PROTECTED COMPONENTS
# ======================
header("Protected Components")

info("WmiPrvSE.exe → NEVER touched (critical)")
info("RuntimeBroker.exe → NEVER touched (critical)")
info("Defender ML → REQUIRED for security")

# ======================
# VERIFICATION (VISIBLE)
# ======================
header("Verification")

print(f"{YELLOW}DiagTrack status:{RESET}")
run_show("sc query DiagTrack")

print(f"\n{YELLOW}WerSvc status:{RESET}")
run_show("sc query WerSvc")

print(f"\n{YELLOW}Search service status:{RESET}")
run_show("sc query WSearch")

print(f"\n{YELLOW}Copilot policy:{RESET}")
run_show(r'reg query "HKLM\Software\Policies\Microsoft\Windows\WindowsCopilot"')

print(f"\n{GREEN}✔ SAFE HARDENING COMPLETE{RESET}")
print(f"{YELLOW}Reboot recommended for full effect{RESET}\n")
