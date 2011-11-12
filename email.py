import imaplib
import creds

# stuff for google spreadsheets
from xml.etree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom

# for timestamp
import datetime

# name of the spreadsheet we're writing to
doc_name = "Email data"

# fetch message count
def get_message_count(search_string):
  result, msgs = mail.search(None,search_string)
  items = msgs[0].split()
  return str(len(items))

# write stuff to the spreadsheet
def write_data(s_id, w_id, type, num_emails):
  dict = {}
  dict['timestamp'] = str(datetime.datetime.now())
  dict['type'] = type
  dict['emails'] = num_emails
  entry = gd_client.InsertRow(dict, s_id, w_id)
  del dict

# get connected to gmail
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(creds.u, creds.p)

# connect to inbox
mail.select("INBOX")
mail.list()

# get messages
# read important external messages
msgs_ext_read = get_message_count('(SEEN NOT FROM "openplans.org" X-GM-LABELS "Important")')

# unread important external messages
msgs_ext_unread = get_message_count('(UNSEEN NOT FROM "openplans.org" X-GM-LABELS "Important")')

# read important messages from openplans
msgs_op_read = get_message_count('(SEEN FROM "openplans.org" X-GM-LABELS "Important")')

# unread important messages from openplans
msgs_op_unread = get_message_count('(UNSEEN FROM "openplans.org" X-GM-LABELS "Important")')

# 
mail.logout()

# now write these discoveries to the spreadsheet!
# thanks, http://www.payne.org/index.php/Reading_Google_Spreadsheets_in_Python
# and this was also handy: http://code.google.com/p/gdata-python-client/issues/detail?id=363

gd_client = gdata.spreadsheet.service.SpreadsheetsService()
gd_client.email = creds.u
gd_client.password = creds.p
gd_client.source = 'a'
gd_client.ProgrammaticLogin()

# work out spreadsheet details
q = gdata.spreadsheet.service.DocumentQuery()
q['title'] = doc_name
q['title-exact'] = 'true'
feed = gd_client.GetSpreadsheetsFeed(query=q)
s_id = feed.entry[0].id.text.rsplit('/',1)[1]
feed = gd_client.GetWorksheetsFeed(s_id)
w_id = feed.entry[0].id.text.rsplit('/',1)[1]
feed = gd_client.GetListFeed(s_id, w_id)

# save something
write_data(s_id, w_id, "Unread External Important", msgs_ext_unread)
write_data(s_id, w_id, "Unread Internal Important", msgs_op_unread)
write_data(s_id, w_id, "Read External Important", msgs_ext_read)
write_data(s_id, w_id, "Read Internal Important", msgs_op_read)
