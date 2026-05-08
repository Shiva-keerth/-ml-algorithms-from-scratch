import os.path

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import random,re

print("="*60)
print("Loading the whatsapp chats")
csv_path = "whatsapp.csv"
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit()

df =pd.read_csv(csv_path)
print(f"Loaded {len(df)} word with {df['Intent'].nunique()} unique intents.\n")

def clean_text(text):
    text = str(text).lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    return text
df['Clean_Message'] = df["User_Message"].apply(clean_text)
messages = df["Clean_Message"].values
intents =df["Intent"].values

response_map ={}
for _,row in df.iterrows():
    intent = row["Intent"]
    response = row["Bot_Response"]
    if intent not in response_map:
        response_map[intent] = []
    if response not in response_map[intent]:
        response_map[intent].append(response)

print("Tokenizing the messages")

tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(messages)
vocab_size = len(tokenizer.word_index) + 1
print(f"Vocabulary Size: {vocab_size}\n")

sequences = tokenizer.texts_to_sequences(messages)
max_length = max(len(seq) for seq in sequences)
padded = pad_sequences(sequences, maxlen=max_length, padding="post")

label_encoder = LabelEncoder()
encoded_intents = label_encoder.fit_transform(intents)
num_classes = len(label_encoder.classes_)
print(f"Number of unique intents: {num_classes}\n")
print(f"Max sequence length: {max_length}\n")

# build deep learning model

print("="*60)
print("Building the Deep Learning Model")
print("="*60)

model =tf.keras.Sequential([tf.keras.layers.Embedding(vocab_size, 64, input_length=max_length),
                            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
                            tf.keras.layers.Dense(64, activation="relu"),
                            tf.keras.layers.Dropout(0.3),
                            tf.keras.layers.Dense(num_classes, activation="softmax")])

model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.summary()

# training

print("\n"+"="*60)
print("Training the model")
print("="*60)

history = model.fit(padded, encoded_intents, epochs=50, batch_size=16, validation_split=0.1,verbose=1)

final_accuracy = history.history['accuracy'][-1]
print(f"\nFinal Training Accuracy: {final_accuracy*100:.2f}%")

def get_response(user_input):
    cleaned=clean_text(user_input)
    seq = tokenizer.texts_to_sequences([cleaned])
    padded_input = pad_sequences(seq, maxlen=max_length, padding="post")
    prediction = model.predict(padded_input,verbose=0)
    prediction_index = np.argmax(prediction)
    confidence = prediction[0][prediction_index]

    predict_intent = label_encoder.inverse_transform([prediction_index])[0]

    possible_responses = response_map.get(predict_intent, ["Sorry, I don't understand."])
    response = random.choice(possible_responses)

    return response, predict_intent, confidence

while True:
    try:
        user_input = input("\nYou: ")
        if user_input.lower().strip() == "quit":
            print("Goodbye...")
            break
        if not user_input.strip():
            continue
        response,intent,confidence = get_response(user_input)
        print(f"Bot: {response} (Intent: {intent}, Confidence: {confidence:.2f})")

    except KeyboardInterrupt:
        print("\nGoodbye...")
    except Exception as e:
        print(f"An error occurred: {e}")
        break