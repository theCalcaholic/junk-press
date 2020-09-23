import pandas as pd
from imapclient import response_types


class MessageDataSet:
    def __init__(self):
        self.data_frame = pd.DataFrame(columns=['uid', 'from', 'to', 'subject', 'body', 'class',
                                                'class_num'])

    def _append(self, msg_uid, data, class_num):
        # print(data)
        envelope: response_types.Envelope = data[b'ENVELOPE']
        try:
            body: response_types.BodyData = data[b'BODY[TEXT]'].decode()
        except UnicodeDecodeError as e:
            print("Error decoding message body: ", e)
            return
        self.data_frame = self.data_frame.append({
            'uid': msg_uid,
            'from': envelope.sender,
            'to': envelope.to,
            'subject': envelope.subject.decode(),
            'body': body,
            'class': 'spam' if class_num == 1 else 'ham',
            'class_num': class_num},
            ignore_index=True)

    def append_spam(self, msg_uid, data):
        self._append(msg_uid, data, 1)

    def append_ham(self, msg_uid, data):
        self._append(msg_uid, data, 0)

    def __repr__(self):
        return "Contents:\n" + self.data_frame.__repr__()
