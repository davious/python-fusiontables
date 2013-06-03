'''
Created on June 2, 2013

@author: davious
'''

import httplib2
import os
# easy_install --upgrade google-api-python-client
import apiclient
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage


if __name__ == "__main__":
  import sys, getpass
  client_id = sys.argv[1]
  redirect_uri = sys.argv[2]
  client_secret = getpass.getpass("Enter your secret: ")
  # https://developers.google.com/api-client-library/python/guide/aaa_oauth#storage
  flow = OAuth2WebServerFlow(client_id=client_id,
                           client_secret=client_secret,
                           scope='https://www.googleapis.com/auth/fusiontables',
                           redirect_uri=redirect_uri)
  storage = Storage(os.path.expanduser("~/oauth_storage.json"))
  credentials = storage.get()
  if not credentials:
    auth_uri = flow.step1_get_authorize_url()
    print "Visit this URL in a browser: ", auth_uri
    code = raw_input("Enter code appended to the redirect url: ")
    credentials = flow.step2_exchange(code)
    storage.put(credentials)

  http = httplib2.Http()
  http.disable_ssl_certificate_validation = True
  http = credentials.authorize(http)
  oauth_client = OAuthFTClient(http, True)

  #show tables
  results = oauth_client.query(SQL().showTables())
  print results
  
  #create a table
  table = {'tablename':{'strings':'STRING', 'numbers':'NUMBER', 'locations':'LOCATION'}}
  tableid = int(oauth_client.query(SQL().createTable(table)).split("\n")[1])
  print tableid
  
  #insert row into table
  rowid = int(oauth_client.query(SQL().insert(tableid, {'strings':'mystring', 'numbers': 12, 'locations':'Palo Alto, CA'})).split("\n")[1])
  print rowid
  
  #show rows
  print oauth_client.query(SQL().select(tableid, None, "numbers=12"))

  
  #delete row
  print oauth_client.query(SQL().delete(tableid, rowid))
  
  #drop table
  print oauth_client.query(SQL().dropTable(tableid))
  
  
  #import a table from CSV file
  tableid = int(CSVImporter(oauth_client).importFile("data.csv"))
  print tableid
  
  #drop table
  print oauth_client.query(SQL().dropTable(tableid))
  
