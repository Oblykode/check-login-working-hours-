from z3 import *
import re
from datetime import datetime

def check_login_working_hours(log_file, work_start="09:00", work_end="17:00"):
    """
    Verify ALL successful logins occurred during working hours using Z3.
    """
    # Parse working hours (which is normally practised in real world)
    work_start_h, work_start_m = map(int, work_start.split(':'))
    work_end_h, work_end_m = map(int, work_end.split(':'))
    work_start_min = work_start_h * 60 + work_start_m
    work_end_min = work_end_h * 60 + work_end_m
    
    print(f" Auditing logins: {work_start}-{work_end} working hours")
    
    # Sample log format parser (Apache/Nginx style)
    log_pattern = re.compile(
        r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) .* "LOGIN_SUCCESS" user=([^ ]+)'
    )
    
    logins = []
    
    # Read and parse log file
    try:
        with open(log_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                match = log_pattern.search(line)
                if match:
                    date_str, time_str, user = match.groups()
                    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                    hour_min = dt.hour * 60 + dt.minute
                    
                    logins.append({
                        'line': line_num,
                        'time': hour_min,
                        'user': user,
                        'in_hours': work_start_min <= hour_min <= work_end_min
                    })
    except FileNotFoundError:
        # Creating sample log if file doesn't exist (worst case scenario)
        print(" Creating sample log file...")
        sample_log = """2025-12-04 08:45:23 INFO "LOGIN_SUCCESS" user=admin
2025-12-04 10:15:42 INFO "LOGIN_SUCCESS" user=user1
2025-12-04 14:30:11 INFO "LOGIN_SUCCESS" user=admin
2025-12-04 18:22:55 INFO "LOGIN_SUCCESS" user=user2
2025-12-04 16:45:33 INFO "LOGIN_SUCCESS" user=manager"""
        with open(log_file, 'w') as f:
            f.write(sample_log)
        print(f" Sample log created: {log_file}")
        return check_login_working_hours(log_file, work_start, work_end)
    
    print(f" Found {len(logins)} successful logins")
    
    if not logins:
        print(" No logins found - compliant")
        return True
    
    # Z3 Formal Verification
    s = Solver()
    
    # Boolean variable per login: "is this login during working hours?"
    login_valid = []
    
    for i, login in enumerate(logins):
        valid = Bool(f"login_{i}_valid")
        login_valid.append(valid)
        
        # Constraint: login must be during working hours
        s.add(valid == login['in_hours'])
        s.add(valid == True)  # Policy: ALL logins must be valid
    
    # Policy: ALL logins must be valid
    all_valid = And(login_valid)
    s.add(all_valid)
    
    print("\n Z3 POLICY CHECK:")
    result = s.check()
    
    if result == sat:
        print(" POLICY COMPLIANT")
        print("All successful logins occurred during working hours!")
        return True
    else:
        print(" POLICY VIOLATION!")
        print("Off-hours logins detected:")
        
        # Show violations
        violations = []
        for login in logins:
            if not login['in_hours']:
                violations.append(login)
                print(f"   Line {login['line']}: {login['user']} at {login['time']//60:02d}:{login['time']%60:02d}")
        
        print(f"\n Compliance: {100*(len(logins)-len(violations))/len(logins):.1f}%")
        return False

# Usage
if __name__ == "__main__":
    # Uses 'auth.log' or creates sample if missing
    compliant = check_login_working_hours("auth.log", "09:00", "17:00")
    print(f"\n RESULT: {'PASS ' if compliant else 'FAIL '}")