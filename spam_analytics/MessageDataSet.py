import pandas as pd
from imapclient import response_types


class MessageDataSet:
    def __init__(self):
        self.data_frame = pd.DataFrame(columns=['UID', 'From', 'To', 'Subject', 'Body', 'Class',
                                                'ClassNum'])

    def _append(self, msg_uid, data, class_num):
        print(data)
        envelope: response_types.Envelope = data[b'ENVELOPE']
        body: response_types.BodyData = data[b'BODY[TEXT]']
        self.data_frame = self.data_frame.append({
            'UID': msg_uid,
            'From': envelope.sender,
            'To': envelope.to,
            'Subject': envelope.subject,
            'Body': body,
            'Class': 'spam' if class_num == 1 else 'ham',
            'ClassNum': class_num},
            ignore_index=True)

    def append_spam(self, msg_uid, data):
        self._append(msg_uid, data, 1)

    def append_ham(self, msg_uid, data):
        self._append(msg_uid, data, 0)

    def __repr__(self):
        return "Contents:\n" + self.data_frame.__repr__()
