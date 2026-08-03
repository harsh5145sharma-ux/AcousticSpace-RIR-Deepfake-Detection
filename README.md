# 🎧 AcousticSpace – Frontend Module

<div align="center">

### AI-Powered Audio Deepfake Detection System

**Frontend Development | Member 4**

*A modern React.js interface for AI-based Audio Deepfake Detection*

</div>

---

## 📖 Overview

The **Frontend Module** of **AcousticSpace** provides a responsive and user-friendly interface for an AI-powered Audio Deepfake Detection System.

Developed using **React.js**, this module allows users to securely authenticate, upload audio files, visualize waveforms, and view prediction results. It communicates seamlessly with the **FastAPI Backend** through REST APIs to deliver an efficient and interactive user experience.

---

## 🎯 Objectives

The primary objectives of this module are:

- Develop a responsive user interface
- Implement secure user authentication
- Enable audio file upload and validation
- Visualize uploaded audio using waveforms
- Display AI prediction results with confidence score
- Maintain prediction history
- Integrate the frontend with FastAPI backend APIs

---

## ✨ Features

### Authentication

- User Registration
- User Login
- JWT Authentication
- Protected Routes
- Logout Functionality

### Dashboard

The dashboard provides:

- Selected Audio File
- Detection Status
- Confidence Score
- Detection Time
- Uploaded File Information

### Audio Upload

Supported audio formats:

- WAV
- MP3

Displayed Information:

- File Name
- File Size
- File Type
- Audio Duration

### Waveform Visualization

Implemented using **WaveSurfer.js**

Features include:

- Audio Playback
- Waveform Visualization
- Better Audio Representation

### Detection Result

Displays:

- Real / Fake Prediction
- Confidence Score
- Detection Time
- Uploaded File Name

### Prediction History

Stores previous predictions including:

- Prediction Result
- Confidence Score
- Date & Time
- Uploaded Audio Details

### Report Download

Users can download a prediction report containing:

- File Name
- Prediction Result
- Confidence Score
- Detection Time

---

## 🔄 Frontend Workflow

```text
User Opens Application
        │
        ▼
  Login / Signup
        │
        ▼
JWT Authentication
        │
        ▼
    Dashboard
        │
        ▼
 Select Audio File
        │
        ▼
   Upload Audio
        │
        ▼
 REST API Request
        │
        ▼
FastAPI Backend
        │
        ▼
AI Model Prediction
        │
        ▼
Receive Prediction Result
        │
        ▼
  Display Result
        │
        ▼
Save Prediction History
        │
        ▼
  Download Report
```

---

## 🛠 Technologies Used

### Frontend

- React.js
- JavaScript (ES6)
- HTML5
- CSS3

### Libraries

- React Router DOM
- Axios
- WaveSurfer.js

### Authentication

- JWT Token
- Local Storage

### Backend Communication

- REST APIs

---

## 📂 Project Structure

```text
acousticspace-frontend
│
├── public
│
├── src
│   ├── api
│   ├── assets
│   ├── components
│   │   ├── AudioUpload.jsx
│   │   ├── Navbar.jsx
│   │   ├── ResultCard.jsx
│   │   └── WaveformViewer.jsx
│   │
│   ├── data
│   ├── pages
│   │   ├── Dashboard.jsx
│   │   ├── History.jsx
│   │   ├── Login.jsx
│   │   └── Signup.jsx
│   │
│   ├── styles
│   ├── utils
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
│
├── package.json
├── package-lock.json
└── README.md
```

---

## ⚛ React Concepts Used

- Functional Components
- useState()
- useEffect()
- useRef()
- React Router DOM
- Props
- Conditional Rendering
- Local Storage
- Axios

---

## 🔗 API Integration

The frontend communicates with the backend through REST APIs.

Integrated APIs:

- Login API
- Signup API
- Prediction API
- History API

---

## 📦 Components Developed

- Navbar
- AudioUpload
- WaveformViewer
- ResultCard
- Dashboard
- Login
- Signup
- History

---

## 📊 Development Status

| Module | Status |
|---------|--------|
| Login | ✅ Completed |
| Signup | ✅ Completed |
| Dashboard | ✅ Completed |
| Audio Upload | ✅ Completed |
| Waveform Viewer | ✅ Completed |
| API Integration | ✅ Completed |
| Result Display | ✅ Completed |
| Prediction History | ✅ Completed |
| JWT Authentication | ✅ Completed |
| Report Download | ✅ Completed |

---

## 🚀 Future Enhancements

- Dark Mode
- Drag & Drop Audio Upload
- Better Loading Animation
- Mobile Responsiveness
- Cloud Deployment
- Real-Time Audio Detection

---

## 👩‍💻 Member 4 Contribution

As the **Frontend Developer**, I contributed to the following:

- Designed the complete frontend architecture
- Developed Login and Signup pages
- Built the Dashboard interface
- Implemented the Audio Upload module
- Integrated WaveSurfer.js for waveform visualization
- Connected React frontend with FastAPI backend APIs
- Implemented JWT Authentication
- Developed the Prediction History page
- Created the Detection Result module
- Implemented Report Download functionality
- Improved UI responsiveness and overall user experience

---

## 🏆 Conclusion

The **Frontend Module** of **AcousticSpace** provides a secure, responsive, and user-friendly platform for AI-powered audio deepfake detection. It enables users to authenticate, upload audio files, visualize waveforms, receive prediction results, manage prediction history, and download reports while ensuring seamless communication with the FastAPI backend.

---

<div align="center">

### AcousticSpace – Audio Deepfake Detection System

**Frontend Module | Member 4**

Developed using **React.js**

</div>
