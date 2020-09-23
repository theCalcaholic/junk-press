from .MessageDataSet import MessageDataSet

training_data_set = MessageDataSet()


from .simple_bayes import train as simple_bayes_train
from .simple_bayes import is_spam as simple_bayes_predict
