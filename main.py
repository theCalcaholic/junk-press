import os
from imapclient import IMAPClient
from imap_processor import IMAPService
from spam_analytics import training_data_set


def require_env_var(key):
    if key in os.environ:
        return os.environ[key]
    else:
        raise ValueError(f"Expected environment variable '{key}' but it was not set!")


imap_password = require_env_var('IMAP_PASSWORD')
imap_url = require_env_var('IMAP_URL')
imap_login = require_env_var('IMAP_LOGIN')
training_data_size = 500

# idle_server = IMAPClient(imap_url, ssl=True, use_uid=True)
# idle_server.login(imap_login, imap_password)
server = IMAPClient(imap_url, ssl=True, use_uid=True)
server.login(imap_login, imap_password)

imap = IMAPService(server, training_data_set)

# imap.listen()
imap.load_tagged('INBOX', max_results=training_data_size)
print(training_data_set)
imap.load_tagged('Spam/learn/spam', max_results=training_data_size)

print(training_data_set)

server.logout()
