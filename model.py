import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB
import pickle
import warnings

warnings.filterwarnings('ignore')
filepath = "HeartDataSet.csv"
data = pd.read_csv(filepath)
x = data.iloc[:, :-1]
y = data.iloc[:, -1]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)
model = GaussianNB()
model.fit(x_train, y_train)
y_predict1 = model.predict(x_test) # get y predictions
print(classification_report(y_test, y_predict1))

pickle.dump(model, open('naive_model.pkl', 'wb'))
model = pickle.load(open('naive_model.pkl', 'rb'))
