import quickstart
import httplib2
import os
import re

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient import errors

#sends out the ids for all the messages in the email
def ListMessagesMatchingQuery(service, user_id, query):
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

#returns ids for all unread messages in email
#returns in format: [{u'id': u'15739b9330f732a7', u'threadId': u'15739b9330f732a7'}]
def listUnreadMessages(service, user_id, label_ids):
  try:
    response = service.users().messages().list(userId=user_id,
                                               labelIds=label_ids).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id,
                                                 labelIds=label_ids,
                                                 pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

#gets text for a particular the message
#format: subject, from address, msgdate, msgbody
def getMessage(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

##    print 'Message snippet: %s' % message['snippet']
##    print 'From: %s' % message['payload']['headers'][19]
##    print 'Subject: %s' % message['payload']['headers'][18]
##    print 'Message date: %s' % message['payload']['headers'][17]
    subject = ''
    frm = ''
    msgdate = ''

    for x in message['payload']['headers']:
      if x['name'] == 'From':
        frm = x['value']
      elif x['name'] == 'Date':
        msgdate = x['value']
      elif x['name'] == 'Subject':
        subject = x['value']
    editMsg = [subject, frm, msgdate, message['snippet']]
    return editMsg
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def getMsgLabelIDs(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    label_ids = message['labelIds']
    updated_label_ids = [x for x in label_ids if label_ids is not 'UNREAD']
    return updated_label_ids
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

#mark as read
def addReadTag(service, user_id, msg_id, msg_labels={'removeLabelIds': ['UNREAD'], 'addLabelIds': []}):
    try:
      message = service.users().messages().modify(userId=user_id, id=msg_id,
                                                body=msg_labels).execute()
      label_ids = message['labelIds']
      print 'Message ID: %s - With Label IDs %s' % (msg_id, label_ids)
    except errors.HttpError, error:
      print 'An error occurred: %s' % error

#do everything
def allNewMail(service):
  user_id = "hackmitcalendar@gmail.com"
  l = listUnreadMessages(service, user_id, 'UNREAD')
  ids = []
  data = []
  for x in l:
    ids.append(x['id'])
  for id in ids:
    data.append(getMessage(service, user_id, id))
    addReadTag(service, user_id, id)
  return data
    
#testing
#print (ListMessagesMatchingQuery(service, 'hackmitcalendar@gmail.com', ''))
#print(getMessage(service, 'hackmitcalendar@gmail.com', '15739b9330f732a7'))
#addReadTag(service, 'hackmitcalendar@gmail.com', '15739b9330f732a7')
#print(listUnreadMessages(service, 'hackmitcalendar@gmail.com', 'INBOX'))





