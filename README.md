# ChefAI 🍳

**ChefAI** is a smart web application designed to turn your available ingredients into delicious meals. Whether you type your ingredients manually or upload a photo of your fridge, ChefAI uses advanced Machine Learning and Large Language Models to suggest the best recipes, highlighting what you have and what is missing.

The live application is deployed and available at: **[cheif-ai.onrender.com](https://cheif-ai.onrender.com)**

---

## 👤 Authors
- **Saliev Yntymak** — Project Manager
- **Baisal Kerimzhanov** — Backend
- **Aizirek Dokturbek kyzy** — AI Engineer
- **Salman Saparaliev** — Frontend
- **Tilek Esenkulov** — Devsecops

---

## 🚀 Key Features

* **Hybrid Recipe Search:** Instantly checks the local database for existing recipes and calculates matched and missing ingredients (`missing_ingredients`) on the fly for frontend visual indicators.
* **AI-Powered Generation (Fallback):** If no direct matches are found in the database, the app seamlessly calls **Groq API** to generate creative new recipes and automatically caches them in the database for future use.
* **Computer Vision Product Detection:** Allows users to upload photos of food. An integrated **YOLOv8m** model detects ingredients and fills the search bar automatically.
* **Modern Responsive UI:** Clean, intuitive, and mobile-friendly interface with visual indicators for missing ingredients.

---

## 🛠️ Tech Stack & Architecture

The project is built following **Domain-Driven Design (DDD)** principles, separating the core business logic from framework-specific infrastructure layers.

### Backend & AI Microservices
- **Core Framework:** Django / Django REST Framework (DRF)
- **LLM Integration:** Groq API (`llama-3.3-70b-versatile`)
- **Computer Vision:** FastAPI microservice + YOLOv8m (trained on Fruits-Vegetables dataset of 4,827 images, achieving **mAP50: 0.848**)
- **Database:** PostgreSQL

### DevOps & Infrastructure
- **Containerization & Orchestration:** Docker & Docker Compose
- **Cloud Hosting:** Render (Web Service + Managed PostgreSQL)
- **CI/CD & Version Control:** GitHub

---

## 📂 Repository Structure

```text
chef-ai/
├── services/
│   └── recipes/
│       ├── templates/main/recipes.html  # Frontend Templates
│       ├── models.py                   # Recipe & Ingredient Models
│       ├── views.py                    # Search & Hybrid Flow Controller (DB + AI)
│       └── serializers.py              # API Serializers
├── storage/
│   ├── domain/                         # DDD: Core Business Entities
│   ├── application/                    # DDD: Recipe & Inference Services
│   └── infrastructure/                 # DDD: Groq API & Repository Implementations
├── ai_microservice/                    # FastAPI + YOLOv8m Service for /detect
└── docker-compose.yml                  # Local Multi-Container Orchestration
```

## 🔧 Project Setup (Local Development)
Follow the steps below to set up and run the entire project ecosystem locally.

### Prerequisites
Before starting, make sure the following tools are installed on your machine:

```
DockerDesktop
```

Also ensure that the following ports are available and not used by other applications:

```
80

5432

8000
```

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/chef-ai.git](https://github.com/your-username/chef-ai.git)
cd chef-ai
```

### 2. Environment Configuration
Copy the example environment file and create your local configuration in the root directory:

``` bash
cp config/env.example config/.env
```
Open the newly created config/.env file and populate your credentials and API keys:

```
DEBUG=True
SECRET_KEY=your_django_secret_key
DATABASE_URL=postgres://postgres:postgres@db:5432/chef_db
GROQ_API_KEY=your_groq_api_key
```

### 3. Build and Run Containers
Run the following command to build the images and start all services in the background:

``` bash
docker-compose up --build
```
*Note: The configuration automatically triggers database migrations upon container startup.*

### 4. Access the Services
-- Frontend/Backend Web App: http://localhost:8000
-- Django Admin Panel: http://localhost:8000/api/admin/

## 📝 API Endpoints Summary
### ***GET /api/recipes/search_by_ingredients/***
Searches recipes based on available ingredients.

-- Query Parameters: ***ingredients*** (comma-separated or space-separated string).

-- Behavior: Returns matched items from DB if found (including the ***missing_ingredients*** array). Otherwise, triggers Groq LLM generation, saves the generated recipe and ingredients into the DB, and returns the response in the exact same structure.

### ***POST /detect*** (AI Microservice)
Accepts an image file (e.g., a photo of a fridge), processes it via the YOLOv8m model, and returns a list of possible recipes.