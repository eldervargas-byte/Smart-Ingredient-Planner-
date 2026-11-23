# Smart-Ingredient-Planner-

A Unit Final project for the Modern Technology online course. The **"Smart" Ingredient Planner** is an AI-driven web application that allows users to list the food products they currently own, track expiration dates, manage a weekly grocery budget, and generate personalized meal plans with ingredient substitutions to reduce food waste and avoid overspending.

## Problem & Solution

* **Problem:** Students struggle to plan meals around what they already have, resulting in wasted groceries and overspending on takeout.
* **Solution:** A smart food and budget planning app that prioritizes soon-to-expire pantry ingredients and builds cost-conscious meal plans within a user's remaining weekly budget.

## Current Project Status (Unit 12 MVP)

* **Authentication:** Email and password registration and login with input validation and session navigation.
* **Home Dashboard:** Displays a live summary of total listed ingredients and remaining weekly grocery budget.
* **Smart Pantry Management:** Users can add, view, and delete ingredients with quantities and expiration dates (automatically sorted so items expiring soonest appear first).
* **Weekly Budget Structure:** Users can set a weekly grocery limit, log spending, and view their real-time remaining balance.
* **AI Meal Plan Generator:** Connects to the Gemini API to generate multi-day meal plans maximizing current pantry inventory while respecting dietary notes and remaining budget.
* **Containerization:** Packaged with Docker for local testing and Google Cloud Run deployment.

## Technology Stack

* **Backend:** Python 3.11 & FastAPI
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Single-Page UI)
* **AI Integration:** Google Gemini API (`google-genai` / `gemini-2.5-flash`)
* **Containerization & Deployment:** Docker & Google Cloud Run

## Project Structure

```text
Smart-Ingredient-Planner-/
├── Dockerfile          # Container configuration for Cloud Run
├── README.md           # Project documentation
├── index.html          # Frontend UI (Auth, Home, Pantry, Budget, Meal Planner)
├── main.py             # FastAPI backend & Gemini AI integration
└── requirements.txt    # Python dependencies
```

## Getting Started

### Option 1: Run Locally with Python

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd Smart-Ingredient-Planner-
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set your Gemini API key:**
   ```bash
   export GEMINI_API_KEY="your_api_key_here"  # On Windows PowerShell: \$env:GEMINI_API_KEY="your_api_key_here"
   ```

4. **Start the application:**
   ```bash
   uvicorn main:app --reload --port 8080
   ```
   Open `http://localhost:8080` in your browser.


### Option 2: Run with Docker

1. **Build the Docker image:**
   ```bash
   docker build -t smart-meal-planner .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8080:8080 -e GEMINI_API_KEY="your_api_key_here" smart-meal-planner
   ```
   Open `http://localhost:8080` in your browser (or `http://localhost:8080/docs` to view the interactive API documentation).


## AI Tool Usage Documentation

AI tools were used during Sprint 1 development in two ways:
1. **In-App AI Feature:** Integrated the **Google Gemini API (`gemini-2.5-flash`)** to analyze user pantry inventories, prioritize ingredients nearing expiration, and generate budget-aware meal plans.
2. **Development Assistance:** Used AI coding assistants to scaffold the FastAPI endpoints, build the responsive single-page frontend (`index.html`), write the `Dockerfile`, and structure Git feature branch workflows. All generated code was reviewed, tested locally, and verified against Sprint 1 user story acceptance criteria.
