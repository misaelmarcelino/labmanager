import smtplib

EMAIL = "misael.marcelino@fleetcor.com.br"
PASS = "Morfblack@20250003"

server = smtplib.SMTP("smtp.office365.com", 587)
server.set_debuglevel(1)
server.starttls()
server.login(EMAIL, PASS)

print("✅ Login OK!")
server.quit()