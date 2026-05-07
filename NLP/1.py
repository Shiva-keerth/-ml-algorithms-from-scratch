import pandas
import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

nltk.download('stopwords')
df=pd.read_csv("sentiment analysis.csv")

df=df[["review_text","sentiment_label"]]
df.dropna(inplace=True)
le=LabelEncoder()
df["sentiment_label"]=le.fit_transform(df["sentiment_label"])

print("Label Mapping:", dict(zip(le.classes_, le.transform(le.classes_))))
stop_words=set(stopwords.words('english'))

def clean_text(text):
    text=re.sub(r'[^a-zA-Z]','',text)
    text=text.lower()
    tokens=text.split()
    tokens=[word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

df["clean_text"] =df["review_text"].apply(clean_text)


vectorizer = TfidfVectorizer(max_features=8000,ngram_range=(1,2),min_df=2)

x=vectorizer.fit_transform(df["clean_text"])
y=df["Sentiment_label"]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
model =SVC(kernel='linear',C=1.5,random_state=42)
model.fit(x_train,y_train)

y_pred=model.predict(x_test)
print("\nAccuracy:", accuracy_score(y_test,y_pred))
print("\nClassification Report:\n", classification_report(y_test,y_pred))

def predict_sentiment(user_input):
    text=user_input.lower()
    test =re.sub(r'[^a-zA-Z]','',text)
    words = test.split()
    words = [word for word in words if word not in stop_words]
    text = ' '.join(words)
    vectorized=vectorizer.transform([text])
    pred =model.predict(vectorized)[0]
    return le.inverse_transform([pred])[0]

while True:
    user_input=input("\nEnter a review (or 'exit' to quit): ")
    if user_input.lower() == 'exit':

      print("Exiting Program...")
      break
    prediction = predict_sentiment(user_input)
    print(f"Predicted Sentiment: {prediction}")