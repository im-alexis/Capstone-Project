# IF YOU WANT TO RUN, IT WILL ONLY SEND IN MAILTRAP'S TESTING SITE #

#---------------------------------------#
#           APWS Gmail Login            #
#---------------------------------------#
# Login = "apws.services@gmail.com"     #
# Password = "Jejkijar24"               #
#---------------------------------------#

#---------------------------------------#
#           Example Data                #
#---------------------------------------#
# sender = "apws.services@gmail.com"    #
# receiver = "Kietle24@utexas.com"      #
# subject = "Your Water Tank is Low"    #
# Body = f"{Detailed Report}"           #
#---------------------------------------#

import smtplib
from email.mime.text import MIMEText

subject = "Testing APWS Email System"
body = f"Now This...THIS is Epic\n\n\n\n"
sender = "apws.services@gmail.com"
recipient = "Kietvle2020@gmail.com"

battery = f"""\
Alert: Battery of Probe {pnum} of System {systemID} needs to be replaced soon.

Current Battery Life: {life}."""

Hub = f"""\
Alert: Battery of the Hub of System {systemID} needs to be replaced soon.

Current Battery Life: {life}."""

Water = f"""\
Alert: The Water Source of System {systemID} is low.

Current Water Level: {life}."""

badData = f"""\
Alert: Probe {pnum} of System {systemID} may have been tampered/damaged.

Details: Probe {pnum} has been showing these values {badpval} against {goodpval} of Probe {pnum2}."""

Reset = f"""\
."""

Stats = f"""\
."""

SystemInvites = f"""\
."""

def send_email(subject, body, recipient):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, 'alhq eqqw frgs dpfo')
        smtp_server.sendmail(sender, recipient, msg.as_string())

    print("please work :(")