# PokéBuilder: A Full-Stack Pokémon Game & Team Management App

PokéBuilder is a complete, full-stack web application that allows users to catch, collect, and manage Pokémon, build strategic teams, and engage in exciting, AI-powered battle simulations.

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://pokemon-eoue.onrender.com/)
[![Language](https://img.shields.io/badge/Language-Python%20%26%20JS-blue)](.)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688)](https://fastapi.tiangolo.com/)

##  Features

This application is built with a complete game loop, allowing users to progress from a new trainer to a seasoned champion.

* **Full User Authentication:** Secure user registration and login system using JWT tokens.
* **Starter Pokémon Selection:** New trainers begin their journey by choosing one of the three classic starters: Bulbasaur, Charmander, or Squirtle.
* **Safari Zone:** An interactive mini-game where players can explore to find and catch wild, 1st Generation Pokémon.
    * **Timing-Based Catch Mechanic:** Catch success is determined by a fun and challenging timing bar, where the difficulty is based on the Pokémon's official catch rate.
* **Player Progression System:**
    * **Levels & XP:** Earn experience points by playing the PokéStreak game to level up.
    * **Tiered Encounters:** Higher-level trainers unlock the ability to encounter rarer and more powerful Pokémon in the Safari Zone.
* **PokéCoin Economy & Shop:**
    * Earn **PokéCoins** by winning in the PokéStreak game.
    * Spend coins in the **Poké Mart** to buy better Pokéballs (Great Balls, Ultra Balls) to improve catch chances.
* **Personal Pokémon Collection:** Every user has their own collection of caught Pokémon, which is persisted in the database.
* **Advanced Team Builder:**
    * Create, view, update, and delete multiple teams.
    * The team builder **only** allows users to select from Pokémon they have personally caught.
* **PokéStreak Game:**
    * A streak-based prediction game where players test their knowledge against a high-performance **AI Battle Predictor**.
    * Features a global leaderboard to track the top trainers.
* **Kanto Gym Challenge (The Endgame):**
    * Challenge all 8 Kanto Gym Leaders in the correct sequence.
    * Gym Leaders use their authentic, stat-boosted teams.
    * Battles are **turn-by-turn**, with users making strategic commands ("Aggressive", "Standard", "Defensive").
    * A **Live "Power Meter"**, powered by the Battle Predictor AI, shows the real-time win probability after every turn.

##  Tech Stack

### Backend
* **Python 3.11+**
* **FastAPI:** For building the high-performance, asynchronous API.
* **SQLAlchemy:** As the ORM for database interactions.
* **PostgreSQL:** The production-ready SQL database.
* **Pydantic:** For data validation and serialization.
* **Scikit-learn & XGBoost:** For training and serving the machine learning models.
* **JWT (JSON Web Tokens):** For secure user authentication.

### Frontend
* **HTML5**
* **CSS3:** For modern styling and a fully responsive design.
* **Vanilla JavaScript (ES6+):** For all client-side logic, game mechanics, and API communication.

### Deployment
* **Render:** For hosting the live FastAPI application and PostgreSQL database.
* **Gunicorn:** As the production web server.

##  Local Setup and Installation

To run this project on your local machine, please follow these steps.

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

2. Backend Setup
Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install dependencies:

pip install -r requirements.txt

Set up environment variables:

Create a file named .env in the root directory.

Add your database credentials to this file. It should look like this:

DATABASE_URL=postgresql://user:password@hostname/dbname
SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

Run the database migrations:
The application uses SQLAlchemy's create_all to automatically create the necessary tables when it first starts.

Train the ML Models (Optional):
If you want to retrain the models, run the following scripts from the root directory:

python battle_simulator.py
python train_model.py
python generate_catch_data.py
python train_catch_model.py

Run the server:

uvicorn app.main:app --reload

The backend will be running at http://127.0.0.1:8000.

3. Frontend Setup
The frontend is served directly by the FastAPI backend.

Once the backend is running, open your web browser.

Navigate to http://127.0.0.1:8000.



