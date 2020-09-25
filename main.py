import os
import numpy as np
from imapclient import IMAPClient
from imap_processor import IMAPService
from spam_analytics import BayesianFilter, MessageDataSet


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

training_data_set = MessageDataSet.get_named_set('training')
imap = IMAPService(server, training_data_set)

# imap.listen()
imap.load_tagged('Spam/learn/ham', max_results=training_data_size)
print(MessageDataSet.get_named_set('training'))
imap.load_tagged('Spam/learn/spam', max_results=training_data_size)

server.logout()

print(training_data_set)

message_filter = BayesianFilter()
message_filter.train()

prediction = message_filter.get_spam_probability("""Dear notanactualuser,

Your Steam account password has been successfully changed.

We are sending this notice to ensure the privacy and security of your Steam account. If you authorized this change, no further action is necessary.

If you did not authorize this change, then please change your Steam password, and consider changing your email password as well to ensure your account security.

If you are unable to access your account, then you may use this account specific recovery link for assistance recovering or self-locking your account.""")

spam_class = np.where(prediction == np.amax(prediction))[0]

print(f"Test message was classified as {'not ' if spam_class == 0 else ''}spam with probabilities "
      f"[ {prediction[0]} (not spam), {prediction[1]} (spam)]")
