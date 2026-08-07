import os
import numpy as np
import pandas as pd
import librosa
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_model():
    print("Loading metadata...")
    if not os.path.exists("metadata.csv"):
        print("metadata.csv not found!")
        return

    df = pd.read_csv("metadata.csv")
    
    X = []
    y = []

    print("Extracting features from audio files...")
    for idx, row in df.iterrows():
        filename = row['filename']
        label_str = row['label'] # Assuming 'label' column exists ('bonafide'/'spoof' or 0/1)
        
        # Normalize label to binary (0 for bonafide/human, 1 for spoof/ai)
        if isinstance(label_str, str):
            label = 1 if label_str.lower() in ['spoof', 'ai', 'fake', '1'] else 0
        else:
            label = int(label_str)

        audio_path = os.path.join("data", filename)
        if not os.path.exists(audio_path):
            continue

        try:
            audio_data, sr = librosa.load(audio_path, sr=16000)
            mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=40)
            features = np.mean(mfccs.T, axis=0)
            X.append(features)
            y.append(label)
        except Exception as e:
            print(f"Error processing {audio_path}: {e}")

    if len(X) == 0:
        print("No valid audio features extracted. Check your data paths and metadata.csv!")
        return

    X = np.array(X)
    y = np.array(y)

    print(f"Dataset shape: {X.shape}. Training classes: {np.unique(y, return_counts=True)}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest classifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model trained successfully! Test Accuracy: {acc * 100:.2f}%")

    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/checkpoint.pkl")
    print("Saved trained model checkpoint to models/checkpoint.pkl")

if __name__ == "__main__":
    train_model()