# Login Working Hours Compliance Verifier (Z3)

A lightweight Python tool that audits successful login events and checks — using formal verification — whether **every login** happened during approved working hours.

## What it does

1. Reads a log file (Apache/Nginx style or similar)
2. Extracts successful logins (`LOGIN_SUCCESS`) with timestamp and username
3. Converts login times to minutes-of-day
4. Defines working hours (default: 09:00 – 17:00)
5. Uses **Z3** to check the policy:  
   **ALL successful logins MUST be within working hours**
6. If any login falls outside → reports violations with line numbers, users and times

If the log file doesn't exist, it creates a small **sample log** for demo purposes.

## Sample Output

**Compliant case:**
Auditing logins: 09:00-17:00 working hours
Found 3 successful logins

Z3 POLICY CHECK:
POLICY COMPLIANT
All successful logins occurred during working hours!
RESULT: PASS


**Violation case:**
Auditing logins: 09:00-17:00 working hours
Found 5 successful logins
Z3 POLICY CHECK:
POLICY VIOLATION!
Off-hours logins detected:
Line 1: admin at 08:45
Line 4: user2 at 18:22
Compliance: 60.0%
RESULT: FAIL

## Requirements

```bash
pip install z3-solver
How to use
Bash# Using your real log file
python check_login_hours.py


# Or specify different hours
python check_login_hours.py   # (edit the call inside __main__)
Or directly in code:
Pythoncheck_login_working_hours("auth.log", work_start="08:00", work_end="18:00")
Easy customizations
Python# Change working hours
check_login_working_hours("auth.log", "08:30", "17:30")


# Adjust log pattern (if your log format is different)
log_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}).*user=([^ ]+) success')

# More strict policy example (only some users allowed off-hours)
# You can extend constraints in Z3 part


Why Z3?
Even for this simple check, Z3 gives you:

A clean, declarative way to express security policy
Automatic detection of violations
Easy path to add more complex rules later
(e.g. "admins allowed 24/7", "certain IPs only during office hours", etc.)

Perfect for security audits, policy validation demos, or learning formal methods in security.
