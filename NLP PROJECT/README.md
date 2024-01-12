PDF Image Segmentation Project - Readme
Overview
This project aims to perform image segmentation on PDF files, extracting text and relevant information from each page. The process involves converting PDF pages to images, running a segmentation model, and extracting text using OCR (Optical Character Recognition).

Prerequisites
Ensure you have the following installed:

Python and necessary libraries.
Tesseract OCR.
Required Python packages: pdf2image, pytesseract, detect_exp, pandas, cv2.
Usage
Install Pre-requisites:

Install Anaconda for Python.
Push the code to Google Colab Pro Plus.
Mount drive with Colab and install required libraries.
Run Image Segmentation:

Call the rfp_image_segmentation function, passing the PDF file.
The project creates folders for images and predictions, runs the segmentation model, and extracts text.
Output:

The extracted text is saved in CSV files (extracted.csv, ex2.csv).
A folder structure is created for each PDF file, containing images, predictions, and labels.
Folder Structure
segmentation_run_data/rfx_pdf_folder/YYYY-MM-DD/PDF_FILE_NAME/: Contains PDF-related data.
segmentation_run_data/runs/detect/YYYY-MM-DD/PDF_FILE_NAME/: Contains model predictions.
extracted.csv: CSV file containing extracted text and corresponding labels.
ex2.csv: Another CSV file with extracted information.
Result Interpretation
Each PDF page is processed individually.
Bounding boxes are drawn around detected elements.
Text is extracted using OCR, and results are saved in CSV files.
Important Files
rfp_image_segmentation: Python script for the image segmentation process.
detect_exp: Model prediction script.
resp_op.py and video_resp.py: Testing APIs for image and video responses.
Note: This project assumes a specific model (detect_exp) and label dictionary (lab_dict) for segmentation.

Thank you for using the PDF Image Segmentation Project! Feel free to explore the extracted CSV files for detailed information.