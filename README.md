## Pehchaan-TIFR

## Touchless two factor authentication based Attendance System

Pehchaan-TIFR is an automated face recognition-based attendance system designed for Tata Institute of Fundamental Research (TIFR). The system leverages deep learning, OpenCV, and real-time image processing to accurately identify individuals and log attendance efficiently.

## Dataset

The system is designed to work with custom face datasets collected from the institution. It processes facial images and extracts unique facial features for recognition.

## Theory

#### Facial Feature Extraction

Facial recognition relies on deep learning-based feature extraction to ensure accurate identification. The process involves:
	1.	Face Detection
	•	Detect faces in images using Haar cascades or CNN-based models.
	2.	Feature Encoding
	•	Extract facial embeddings using Dlib’s FaceNet or OpenFace models.
	3.	Face Matching
	•	Compare new images with stored embeddings using Euclidean distance-based matching.

#### Face Recognition Model

The system employs a pre-trained deep learning model for facial recognition. It follows these steps:
	1.	Train on labeled facial images to create unique feature encodings.
	2.	Store these encodings in a database for real-time comparison.
	3.	Identify individuals by matching new face data with stored embeddings.

The model is optimized to handle variations in lighting, angles, and facial expressions.

#### Workflow Graph

1️⃣ Image Capture  →  2️⃣ Face Detection  →  3️⃣ Feature Extraction  
    →  4️⃣ Face Recognition  →  5️⃣ Attendance Logging  

## Dependencies

This project requires the following Python libraries:
	1.	OpenCV (Face Detection & Processing)
	2.	Dlib (Facial Feature Extraction)
	3.	Face Recognition Library (Deep Learning-based Face Matching)
	4.	Flask/FastAPI (Backend API)
	5.	SQLite/MySQL (Database for attendance storage)

## Results

The system was evaluated on a dataset of 100+ individuals, achieving:
	1.	Face Recognition Accuracy: 96.8%
	2.	Response Time: < 1.5 seconds per face
	3.	False Positives: < 2%

## Installation & Usage
	1.	Clone the repository
		```
		git clone https://github.com/hegdeshreya23/Pehchaan-TIFR.git
		cd Pehchaan-TIFR
		```

	2.	Install dependencies
		```
		pip install -r requirements.txt
		
		```
	3.	Run the application
		```
		python app.py
		
		```
	4.	Register Faces
	•	Upload images through the web interface.
	•	The system extracts and stores facial encodings.
	5.	Start Attendance Recognition
	•	The system captures faces via webcam and recognizes individuals.
	•	Attendance is logged automatically.
