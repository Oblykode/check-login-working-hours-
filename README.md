# check-login-working-hours-
Uses Z3 to formally verify authentication logs comply with working hours (09:00-17:00). It parses "LOGIN_SUCCESS" events via regex, converts times to minutes, and creates sample logs if missing. Z3 models each login as a boolean forced True within hours; sat = PASS, else lists violations with compliance %. Ideal for cybersecurity policy auditing. 
