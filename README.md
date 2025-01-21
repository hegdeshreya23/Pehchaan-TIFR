## Pehchaan-TIFR

## Touchless two factor authentication based Attendance System

Pehchaan-TIFR is an automated face recognition-based attendance system designed for Tata Institute of Fundamental Research (TIFR).It leverages facial recognition and voice verification to automate attendance tracking, ensuring accuracy and security.

## Dataset

The system processes two types of biometric data:
1️⃣ Facial Data: Images of individuals for face recognition.
2️⃣ Voice Data: Recorded voice samples for speaker verification.

The system uses a custom dataset collected from users during enrollment, extracting unique facial embeddings and voice features for authentication.

## Theory

1️⃣ Facial Feature Extraction
	•	Face Detection: Identify faces using Haar cascades or CNN-based models.
	•	Feature Encoding: Extract unique facial embeddings using Dlib’s FaceNet.
	•	Face Matching: Compare facial embeddings with stored templates using Euclidean distance.

2️⃣ Voice Feature Extraction
	•	Preprocessing: Remove noise and normalize audio signals.
	•	Feature Extraction: Use Mel-Frequency Cepstral Coefficients (MFCCs) to analyze voice patterns.
	•	Speaker Recognition: Identify individuals using a Gaussian Mixture Model (GMM) trained on voice data.

#### Workflow Graph

1️⃣ Image & Voice Capture  
 →  2️⃣ Face & Voice Detection  
   →  3️⃣ Feature Extraction (Facial Embeddings & MFCCs)  
     →  4️⃣ Face & Voice Recognition  
       →  5️⃣ Attendance Logging  

## Dependencies

This project requires the following Python libraries:
	•	OpenCV (Face Detection & Processing)
	•	Dlib (Facial Feature Extraction)
	•	Face Recognition Library (Deep Learning-based Face Matching)
	•	Librosa & Python Speech Features (Voice Processing & Feature Extraction)
	•	Flask/FastAPI (Backend API)
	•	SQLite/MySQL (Attendance Database)

## Results

The system was tested on a dataset of 100+ individuals, achieving:
	•	Face Recognition Accuracy: 96.8%
	•	Voice Recognition Accuracy: 94.5%
	•	Response Time: < 2 seconds per user

## Installation & Usage

	#### 1.	Clone the repository
		```
		git clone https://github.com/hegdeshreya23/Pehchaan-TIFR.git
		cd Pehchaan-TIFR
		```

	#### 2.	Install dependencies
		```
		pip install -r requirements.txt
		
		```
	3.	Run the application
		```
		python app.py
		
		```
	4.	Enroll Users (Face & Voice Registration)
		•	Upload images and record a short speech sample.
		•	The system extracts and stores facial embeddings & voice features.
	5.	Start Attendance Recognition
		•	The system captures a user’s face and voice.
		•	If both match stored data, attendance is logged automatically.
Here’s your GitHub README with improved formatting and proper alignment for better readability:

Pehchaan-TIFR

Touchless Two-Factor Authentication-Based Attendance System

Pehchaan-TIFR is an automated face and voice recognition-based attendance system designed for Tata Institute of Fundamental Research (TIFR). It leverages facial recognition and voice verification to automate attendance tracking, ensuring accuracy and security.

Dataset

The system processes two types of biometric data:

✅ Facial Data: Images of individuals for face recognition.
✅ Voice Data: Recorded voice samples for speaker verification.

The system uses a custom dataset collected from users during enrollment, extracting unique facial embeddings and voice features for authentication.

Theory

1️⃣ Facial Feature Extraction
	•	Face Detection: Identify faces using Haar cascades or CNN-based models.
	•	Feature Encoding: Extract unique facial embeddings using Dlib’s FaceNet.
	•	Face Matching: Compare facial embeddings with stored templates using Euclidean distance.

2️⃣ Voice Feature Extraction
	•	Preprocessing: Remove noise and normalize audio signals.
	•	Feature Extraction: Use Mel-Frequency Cepstral Coefficients (MFCCs) to analyze voice patterns.
	•	Speaker Recognition: Identify individuals using a Gaussian Mixture Model (GMM) trained on voice data.

Workflow Graph

1️⃣ Image & Voice Capture  
 →  2️⃣ Face & Voice Detection  
   →  3️⃣ Feature Extraction (Facial Embeddings & MFCCs)  
     →  4️⃣ Face & Voice Recognition  
       →  5️⃣ Attendance Logging  

Dependencies

This project requires the following Python libraries:
	•	OpenCV (Face Detection & Processing)
	•	Dlib (Facial Feature Extraction)
	•	Face Recognition Library (Deep Learning-based Face Matching)
	•	Librosa & Python Speech Features (Voice Processing & Feature Extraction)
	•	Flask/FastAPI (Backend API)
	•	SQLite/MySQL (Attendance Database)

Results

The system was tested on a dataset of 100+ individuals, achieving:
	•	Face Recognition Accuracy: 96.8%
	•	Voice Recognition Accuracy: 94.5%
	•	Response Time: < 2 seconds per user

Installation & Usage

1️⃣ Clone the repository

git clone https://github.com/hegdeshreya23/Pehchaan-TIFR.git
cd Pehchaan-TIFR

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Run the application

python app.py

4️⃣ Enroll Users (Face & Voice Registration)
	•	Upload images and record a short speech sample.
	•	The system extracts and stores facial embeddings & voice features.

5️⃣ Start Attendance Recognition
	•	The system captures a user’s face and voice.
	•	If both match stored data, attendance is logged automatically.

This formatting ensures a clean and structured README for GitHub. Let me know if you need further refinements! 🚀
