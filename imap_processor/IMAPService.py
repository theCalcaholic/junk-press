from datetime import datetime, timedelta
from imapclient import IMAPClient
import time
from imapclient import response_types, IMAPClient


class IMAPService:
    def __init__(self, imap_client: IMAPClient, training_data=None):
        self.imap_client = imap_client
        self.message_processors = []
        self.training_data = training_data

    def listen(self, folder='INBOX'):

        select_info = self.imap_client.select_folder(folder)
        print(f'{select_info[b"EXISTS"]} messages in {folder}')
        # idle_server.select_folder('INBOX')
        #
        # idle_server.idle()

        ref_date = datetime.now() - timedelta(days=3)

        while True:
            try:

                messages = self.imap_client.search([u'SINCE', ref_date])
                print(f'{len(messages)} messages since {ref_date} in INBOX')

                for msg_uid, data in self.imap_client.fetch(messages, ['ENVELOPE']).items():
                    self.process_message(self.imap_client, msg_uid, data)
                ref_date = datetime.now()
                #         messages = idle_server.idle_check(timeout=30)
                #         print("Server sent: ", messages if messages else "nothing")
                time.sleep(30)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)

        # idle_server.idle_done()
        self.imap_client.logout()

    def load_tagged(self, folder='INBOX', max_results=0):
        self.imap_client.select_folder(folder)
        if self.training_data is None:
            return
        messages = self.imap_client.search()
        print(f'{len(messages)} messages in {folder}')

        spam_uids = []
        ham_uids = []
        for msg_uid, data in self.imap_client.fetch(messages[-5000:], ['FLAGS']).items():
            if b'Junk' in data[b'FLAGS']:
                spam_uids.append(msg_uid)
            if b'NonJunk' in data[b'FLAGS']:
                ham_uids.append(msg_uid)

        offset = -max_results if max_results < len(spam_uids) else 0
        for msg_uid, data in self.imap_client.fetch(spam_uids[offset:],
                                                    ['ENVELOPE', 'BODY.PEEK[TEXT]']).items():
            self.training_data.append_spam(msg_uid, data)

        offset = -max_results if max_results < len(ham_uids) else 0
        for msg_uid, data in self.imap_client.fetch(ham_uids[offset:],
                                                    ['ENVELOPE', 'BODY.PEEK[TEXT]']).items():
            self.training_data.append_ham(msg_uid, data)

    def on_message(self, fn):
        self.message_processors.append(fn)

    def process_message(self, msg_uid: int, data: dict):
        envelope: response_types.Envelope = data[b'ENVELOPE']
        print(f'ID {msg_uid}: "{envelope.subject.decode()}" received {envelope.date}')

        for proc in self.message_processors:
            proc(msg_uid, data)

