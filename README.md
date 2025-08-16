# Car Price Prediction System - User Guide

## Overview
This project provides a car price prediction website that estimates prices based on user inputs. It uses machine leaning model, called Quantile Regression Forest (QRF), which offers a range of possible price outcomes. It helps users understand the potential range in car prices.

The following sections give informations about the system architecture, user flow, repository structure, and instructions for building and testing the app.

## System Architecture
- **Frontend**: HTML + CSS + Alpine.js
- **Backend**: FastAPI
- **ML Service**: Quantile Regression Forest (QRF) model for price prediction
- **Load Management**: Traffic handling with Nginx rate limiting function

## User Flow

### 1. Website Access

#### **Successful Scenario** ✅
- Navigate to the website's URL
- Main car specification form loads immediately
- You'll see input fields for car details

#### **Error Scenario: Website Busy** ❌
- **Cause**: High traffic volume exceeds server capacity
- **What You'll See**: Friendly error page displays with message "Site is Busy"
- **What Should You Do?**: Wait and refresh the page after a few minutes

### 2. Form Input

#### **Successful Scenario** ✅
- Select or enter valid data for all required fields
- Form validation will check your input in real-time
- All fields remain in valid state (no red highlighting)
- Submit button becomes active and clickable

#### **Error Scenario: Invalid Input Data** ❌
- **Cause**: You enter invalid or incomplete data
- **What You'll See**:
  - Invalid fields turn red
  - Error messages appear below affected fields
  - Submit button still disabled
- **What Should You Do?**: Correct the highlighted fields with valid data

### 3. Form Submission

#### **Successful Scenario** ✅
- Click the submit button
- Form data passes server-side validation
- Backend send prediction request to QRF Model
- QRF model processes the prediction request
- Backend generates price prediction with confidence intervals

#### **Error Scenario: ML Service Busy** ❌
- **Trigger**: ML service is busy
- **What You'll See**: 
  - Prediction box displays "Service is Busy" message
  - Form remains functional for new attempts
  - No data is lost
- **What Should You Do?**: Wait a few moments and resubmit the form

## Repository

### Overview

This repository contains the full-stack application consists of:

* **Frontend**: The UI source code located in the `frontend` directory.
* **Backend**: The API and ML inference logic located in the `api` directory.
* **Experiments**: Machine learning experiments, including Exploratory Data Analysis (EDA), preprocessing, modeling, and logging into MLflow, located in the `experiments` directory.
* **Data**: Raw and preprocessed datasets ready for training, located in the `data` directory.
* **Tests**: Load testing scripts utilizing Grafana's k6, located in the `tests` directory.

### Structure

```
├── api/               # Backend API, and ML inference logic
├── data/              # Raw and preprocessed datasets
├── experiments/       # ML experiments and logs
├── frontend/          # Frontend application
└── tests/             # Load testing scripts
```

## Build & Test the App

### Build the App

Docker and Docker Compose has to be installed on your machine. To deploy the application using pre-built images:

```bash
docker compose up -d
```

To build the application from source code for local development:

```bash
docker compose -f docker-compose-local.yaml up --build -d
```

### Running Tests

You can run the Grafana's k6 load tests by using the provided test scenario on `tests/load-test.js`:

```bash
docker run --rm -i grafana/k6 run - < tests/load-test.js
```

For more information on k6 scenarios, refer to the [official documentation](https://grafana.com/docs/k6/latest/using-k6/scenarios/).