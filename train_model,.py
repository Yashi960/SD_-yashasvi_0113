import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Load the downloaded real dataset
print("📊 Loading real dataset from dataset/reviews.csv...")
df = pd.read_csv('dataset/reviews.csv')

# Look at data structure: 'deceptive' column tells us if it's fake or truthful
# We will convert 'deceptive' to a binary format (1 for fake, 0 for real)
df['label'] = df['deceptive'].apply(lambda x: 1 if x == 'deceptive' else 0)

# 2. Split into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['label'], test_size=0.2, random_state=42
)

# 3. Preprocess text data using TF-IDF
print("🧹 Preprocessing text and converting features...")
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 4. Train the Machine Learning Model
print("🤖 Training the Logistic Regression Model...")
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# 5. Evaluate the model accuracy
predictions = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, predictions)
print(f"📈 Model Evaluation Complete! Current Accuracy: {accuracy * 100:.2f}%")

# 6. Save the newly improved model files
os.makedirs('model', exist_ok=True)
with open('model/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('model/model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("🎉 New high-accuracy model successfully saved inside 'model/'!")