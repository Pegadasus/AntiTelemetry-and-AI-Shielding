# AntiTelemetry-and-AI-Shielding
Few scripts for scanning windows machines for AI, COPILOT and telemetry, also a script to disabled safely this processes  


🛡️ Safe Telemetry & AI Controller (DEBUGGED)
Overview

Safe_Telemetry_AI_Controller_DEBUGGED.py is a Windows hardening script designed to minimize telemetry and AI surface exposure using supported, policy-based methods only.

It is NOT a debloating script, NOT a system breaker, and does NOT remove core Windows components.

This script focuses on:

Privacy

Stability

Reversibility

Transparency

It is suitable for Windows 10 / 11 (Home, Pro, Enterprise).

⚠️ VERY IMPORTANT (READ FIRST)

✅ Run as Administrator

✅ Windows-supported changes only

❌ Does NOT kill system processes

❌ Does NOT disable WMI, RuntimeBroker, Defender, or Update stack

🔄 Fully reversible (registry + service changes only)

🎯 What This Script Does
1️⃣ Telemetry Hardening (Safe)

The script disables non-essential telemetry services while keeping Windows functional:

Component	Action	Reason
DiagTrack	Disabled	Core telemetry service
Windows Error Reporting (WerSvc)	Disabled	Crash data telemetry
AllowTelemetry policy	Set to 0	Minimum telemetry level

✔ Does not affect:

Windows Update

Defender

Event Viewer

PowerShell / WMI

2️⃣ Search Indexing Control
Component	Action
Windows Search Indexer (WSearch)	Disabled

✔ Start Menu still works
✔ File search still works (slower, non-indexed)
✔ Prevents background indexing telemetry

3️⃣ Copilot & AI Feature Disable
Feature	Method
Windows Copilot	Disabled via policy
Widgets (News & Interests)	Disabled via policy
AI UI Surfaces	Prevented from loading

✔ This blocks Copilot fully, not just hiding it
✔ Prevents re-enablement after updates (policy-based)

4️⃣ Edge / WebView AI Reduction
Component	Action
Edge Background Mode	Disabled

✔ Reduces:

WebView2 background activity

AI UI preloading

Edge background telemetry

✔ Does NOT uninstall Edge or WebView (safe)

5️⃣ Protected Components (Explicitly NOT Touched)

The script intentionally avoids critical Windows components:

❌ WmiPrvSE.exe – required for system operation
❌ RuntimeBroker.exe – required for app permissions
❌ Defender ML / Security AI – required for protection

These are logged as protected, not modified.

🧪 Verification Mode (Built-In)

After applying changes, the script visibly verifies:

Telemetry service states

Search service state

Copilot registry policy

This ensures:

No silent failures

No misleading “[OK]” messages

Clear confirmation of applied changes

🎨 Visual Output

🟢 Green → Successfully applied

🟡 Yellow → Informational / status

🔴 Red → Skipped / protected

🔵 Blue → Section headers

ANSI colors are enabled automatically for Windows 10/11.

🔄 Reversibility

All changes are:

Service configuration changes

Registry policy changes

No files are deleted.
No components are removed.

A restore script can fully revert all changes.

🧠 Why This Script Exists

Most “telemetry removal” scripts:

Break Windows

Kill critical processes

Cause update failures

Get reverted by updates

This script is different:

Uses enterprise-style policies

Keeps Windows stable

Minimizes telemetry without breaking the OS

Survives feature updates better

This is hardening, not sabotage.

🧾 What Was Added in the DEBUGGED Version

Compared to earlier versions, this script adds:

✔ Proper admin detection
✔ Reliable ANSI color support
✔ Accurate service existence checks
✔ Real verification output (not suppressed)
✔ Clear distinction between disabled vs protected
✔ Safer error handling
✔ No false-positive success messages

🚀 Recommended Usage

Right-click Command Prompt

Select Run as Administrator

Run:

python Safe_Telemetry_AI_Controller_DEBUGGED.py


Reboot after completion

📌 Disclaimer

This script assumes full authorization on the system.
Use at your own discretion.
Always test in a non-production environment first.
