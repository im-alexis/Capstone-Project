import smtplib

# IF YOU WANT TO RUN, IT WILL ONLY SEND IN MAILTRAP'S TESTING SITE #

#---------------------------------------#
#           APWS Gmail Login            #
#---------------------------------------#
# Login = "apws.services@gmail.com"     #
# Password = "Jejkijar24"               #
#---------------------------------------#

#---------------------------------------#
#           MailTrap Login              #
#---------------------------------------#
#                                       #
#          Use APWS Gmail Login         #
#                                       #
#---------------------------------------#

#---------------------------------------#
#           Example Data                #
#---------------------------------------#
# sender = "apws.services@gmail.com"    #
# receiver = "Kietvle2020@gmail.com"    #
# subject = "Your Water Tank is Low"    #
# Body = "(Detailed Report)"            #
#---------------------------------------#

sender = "apws.services@gmail.com"


def send_email(receiver, subject, body):
    message = f"""\
    Subject: {subject}
    To: {receiver}
    From: {sender}

    {body}"""

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("121b33b64f36e0", "f7312395b9b74a")
        server.sendmail(sender, receiver, message)