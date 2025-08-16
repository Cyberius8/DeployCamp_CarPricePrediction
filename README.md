# Car Price Prediction System - User Guide

## Overview
This guide documents the complete user journey for the car price prediction system, including successful flows and error scenarios. The system uses a Quantile Regression Forest (QRF) machine learning model to predict car prices based on your provided specifications.

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

---

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

---

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
