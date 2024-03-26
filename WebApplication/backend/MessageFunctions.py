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
#           WORK IN PROGRESS            #
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


def send_email(sender, receiver, subject, body):
    message = f"""\
    Subject: {subject}
    To: {receiver}
    From: {sender}

    {body}"""

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("6667900ba5a91f", "1e132628cfc265")
        server.sendmail(sender, receiver, message)