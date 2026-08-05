# AcousticSpace 🎙️
### Deepfake Audio Detection via Room Impulse Response (RIR) Analysis

AcousticSpace ek deepfake audio detection system hai jo traditional voice-artifact-based detectors se hatke kaam karta hai. Ye sirf awaaz ka tone ya pitch check nahi karta — balki audio ke background mein maujood **room acoustics (echo/reverb pattern)** ko analyze karke check karta hai ki woh us jagah se match karta hai jaha se audio record hone ka dawa kiya ja raha hai. Mismatch = fake audio, chahe voice kitni bhi realistic kyun na lage.

---

## 🚩 Problem Statement

AI voice cloning tools itne advanced ho chuke hain ki kisi ki bhi awaaz hubahu copy ki ja sakti hai — fake CEO voice messages, fake celebrity endorsements, banking fraud calls, fake news/political statements. Traditional deepfake detectors sirf voice artifacts (robotic sound, unnatural pauses) dhundte hain, jo naye AI models mein present hi nahi hote — isliye ye detectors easily bypass ho jaate hain.

## 💡 Our Solution

Hum voice content ki jagah **background acoustic environment (RIR)** analyze karte hain:

1. Analyst dashboard pe ek suspicious audio file upload karta hai
2. System audio se do cheezein alag karta hai: **voice content** aur **background acoustic environment (RIR)**
3. Ek AI model — **AST (Audio Spectrogram Transformer)** — check karta hai ki voice ka echo pattern claimed background se match karta hai ya nahi
4. Mismatch milne par system "possible fake" flag karta hai, saath mein **confidence score**

## 🌍 Real-World Impact

| Sector | Use Case |
|---|---|
| **Banks** | Fake voice-authorized transactions rokna |
| **Media / Journalists** | Fake political ya celebrity statements verify karna |
| **Legal Teams** | Court-admissible audio forensic evidence banana |

## 📦 Expected Output

Ek complete web dashboard jahan analyst:
- Audio file upload kare
- Uska waveform dekhe
- System turant bataye "kitna % chance hai ye fake hai"
- Waveform pe suspicious segments highlighted dikhein

---

## 🏗️ System Architecture

```
[Audio Data] → [Feature Extraction] → [AI Model] → [Backend API] → [Dashboard UI]
   (Input)         (Member 1)          (Member 2)     (Member 3)      (Member 4)
```

1. **Audio Data:** Raw audio input, dataset (ASVspoof)
2. **Feature Extraction:** RIR + spectrogram features (Librosa)
3. **AI Model:** Fine-tuned AST model — fake vs real classification
4. **Backend API:** FastAPI server, model serving, auth, database
5. **Dashboard UI:** React frontend — upload, waveform view, confidence score display

---

## 👥 Team & Work Division

### 🔹 Member 1 — ML / Audio Pipeline Lead
Raw audio se RIR aur spectrogram features nikalna (Librosa), ASVspoof dataset prepare karna.
> Foundation layer — bina saaf features ke model accurate result nahi de sakta.

### 🔹 Member 2 — ML Model Engineer
Member 1 ke features lekar AST model fine-tune karna, accuracy validate karna.
> Ye "dimag" hai jo fake vs real ka actual decision leta hai.

### 🔹 Member 3 — Backend / API Engineer
FastAPI server banana jo trained model serve kare, database design, login/authentication system.
> Ye "pul" (bridge) hai jo model ko frontend tak pahunchata hai.

### 🔹 Member 4 — Frontend Engineer
React dashboard banana jaha analyst audio upload kare aur results (waveform + confidence score) dekhe.
> Ye "face" hai project ka — iske bina koi model use hi nahi kar sakta.

---

## 🔗 Dependencies Between Members

| Kaam | Depend Karta Hai |
|---|---|
| Member 2 ka model training | Member 1 ke extracted features pe |
| Member 3 ka backend | Member 2 ke trained model (`.pt` file) pe |
| Member 4 ka dashboard | Member 3 ke API endpoints pe |

### ⚡ Parallel Work Strategy (taaki koi wait na kare)
- **Member 3** shuru mein ek mock/dummy API bana sakta hai (fake data return karne wala) — isse **Member 4** turant UI banana shuru kar sakta hai, real model ka wait kiye bina.
- **Member 1 & 2** ek chhoti sample dataset pe saath-saath kaam kar sakte hain.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Feature Extraction | Python, Librosa, NumPy, SciPy |
| ML Model | AST (Audio Spectrogram Transformer), PyTorch |
| Backend | FastAPI, Database (auth + storage) |
| Frontend | React |
| Dataset | ASVspoof |

---

## 📁 Repository Structure

```
AcousticSpace-RIR-Deepfake-Detection/
├── member1-branch/     # Audio pipeline & feature extraction
├── member2-branch/     # AST model training & fine-tuning
├── member3-branch/     # FastAPI backend & auth
├── member4-branch/     # React dashboard
└── develop             # integrated branch (merged every Friday)
```

---

## 🚀 Getting Started

```bash
git clone https://github.com/harsh5145sharma-ux/AcousticSpace-RIR-Deepfake-Detection.git
cd AcousticSpace-RIR-Deepfake-Detection
```

Har member apni respective branch pe kaam karta hai aur har **Friday** apna kaam `develop` branch mein merge karke ek dusre ka kaam test karta hai, taaki end mein sab kuch smoothly integrate ho.

---

## 📌 Project Goal (Ek Line Mein)

> Deepfake audio ko awaaz sunke nahi, balki **room ki physics** samajhke pakadna.
