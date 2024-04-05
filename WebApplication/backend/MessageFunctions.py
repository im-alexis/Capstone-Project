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
# Case = (Flag Number)                  #
#---------------------------------------#


import smtplib
from email.mime.text import MIMEText

subject = "Testing APWS Email System"
body = f"Now This...THIS is Epic\n\n\n\n"
sender = "apws.services@gmail.com"
recipient = "Kietvle2020@gmail.com"

#------MESSAGES-TODO--------#

# badData = f"""\
# Alert: Probe {pnum} of System {systemID} may have been tampered/damaged.

# Details: Probe {pnum} has been showing these values {badpval} against {goodpval} of Probe {pnum2}."""

# Stats = f"""\
# ."""

#---------------------------#

# CHECK REQUIRED INPUTS FOR EACH CASE BEFORE CALLING THIS FUNCTION

def send_email(subject, recipient, case, code, pnum, systemID, life, user, invite): # Work In Progress
    if case == 1: # Email Creation
        body = f"""\
Your Email Verification Code: {code}
."""
    elif case == 2: # Password Reset
        body = f"""\
Your Password Reset Code: {code}
."""
    elif case == 3: # Low Probe Battery
        body = f"""\
Alert: Battery of Probe {pnum} of System {systemID} needs to be replaced soon.

Current Battery Life: {life}
."""
    elif case == 4: # Low Hub Battery
        body = f"""\
Alert: Battery of the Hub of System {systemID} needs to be replaced soon.

Current Battery Life: {life}
."""
    elif case == 5: # Low Water Level
        body = f"""\
Alert: The Water Source of System {systemID} is low.

Current Water Level: {life}
."""
    elif case == 6: # System Invites
        body = f"""\
You Have Been Invited To {user}'s APWS.

Here Is Your Invite Code: {invite}
."""
    elif case == 7:
        body = f"""\
."""
    elif case == 8:
        body = f"""\
."""
    else:
        body = "Error"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, 'alhq eqqw frgs dpfo')
        smtp_server.sendmail(sender, recipient, msg.as_string())

    print("please work :(")