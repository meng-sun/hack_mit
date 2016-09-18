import re
from getMsg import *

#accesses gmail and authenticates
credentials = quickstart.get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)
#results = service.users().labels().list(userId='me').execute()

data = allNewMail(service)
