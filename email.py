import imaplib
import creds

print creds.username

mail.list()
# Out: list of "folders" aka labels in gmail.
#mail.select("inbox") # connect to inbox.

#mail.logout()

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(username, p)

print p
