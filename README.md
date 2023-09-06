# BizCardX
# BizCardX: Extracting Business Card Data with OCR

## Table of Contents
- [Project Description](#project-description)
- [Technologies](#technologies)
- [Problem Statement](#problem-statement)
- [Approach](#approach)
- [Results](#results)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Description

BizCardX is a Streamlit application that allows users to upload an image of a business card and extract relevant information using easyOCR. The extracted information includes the company name, cardholder name, designation, mobile number, email address, website URL, area, city, state, and pin code. Users can also save the extracted information and the uploaded image to a database, allowing for multiple entries and data management.

## Technologies

- OCR
- Streamlit GUI
- SQL (Database Management)
- Data Extraction

## Problem Statement

You have been tasked with developing a Streamlit application that addresses the following problem statement:

**Problem Statement**: Create an application that allows users to upload a business card image and extract relevant information, such as company name, cardholder name, and contact details. Additionally, enables users to save this information along with the image to a database. Users should be able to read, update, and delete entries through the Streamlit GUI.

## Approach

To achieve the project's objectives, we follow this approach:

1. **Install Required Packages**: Install Python, Streamlit, easyOCR, and a database management system like SQLite or MySQL.

2. **Design the User Interface**: Create an intuitive Streamlit interface for uploading business card images, extracting information, and managing data.

3. **Implement Image Processing and OCR**: Utilize easyOCR for information extraction, including image preprocessing techniques to enhance OCR accuracy.

4. **Display Extracted Information**: Present extracted information in an organized manner within the Streamlit GUI.

5. **Database Integration**: Implement database functionality for storing extracted information and business card images. This includes CRUD (Create, Read, Update, Delete) operations through the Streamlit UI.

6. **Test the Application**: Thoroughly test the application to ensure functionality as expected.

7. **Continuous Improvement**: Enhance the application by adding new features, optimizing code, and ensuring security with user authentication and authorization.

## Results

The project's outcome is a Streamlit application that fulfills the following objectives:

- Users can upload a business card image and extract relevant information using easyOCR.
- Extracted information includes company name, cardholder name, contact details, and more.
- Extracted data is displayed in an organized Streamlit GUI.
- Users can save extracted information and business card images to a database.
- The database supports multiple entries and CRUD operations through the Streamlit UI.

The project requires expertise in image processing, OCR, GUI development, and database management. It emphasizes scalability, maintainability, and code organization.



