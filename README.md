# 💪 Fitness Tracker

A comprehensive fitness tracking application built with Python. Available in two versions: a command-line interface (CLI) for developers and a modern web interface built with Streamlit.

## 🚀 Two Ways to Use

### 1️⃣ Command-Line Interface (CLI)

```bash
python main.py
```

### 2️⃣ Web Application (Streamlit)
Modern, interactive web interface with charts and analytics.
```bash
streamlit run app.py
```

## 🌟 Features

### Core Functionality
- **User Profile Management**: Track personal metrics including BMI, weight history, and body composition
- **Workout Tracking**: Log various workout types with automatic calorie calculation
- **Goal Setting**: Create and track fitness goals with progress monitoring and deadlines
- **Progress Analytics**: View detailed statistics, streaks, and performance trends
- **Data Persistence**: All data automatically saved to JSON format
- **Data Export**: Export workout history to CSV for external analysis

### Supported Workout Types
- 🏃 Running
- 🚴 Cycling
- 🏊 Swimming
- 🏋️ Gym/Strength Training
- 🧘 Yoga
- 🚶 Walking
- 🔥 HIIT
- 💃 Dancing

### Analytics & Insights
- Weekly and monthly summaries
- Workout streak tracking
- Calorie burn analysis
- BMI calculation and tracking
- Personal records and achievements
- Progress visualization

## 📋 Requirements

**For CLI Version (main.py):**
- Python 3.7+
- No external dependencies (uses only Python standard library)

**For Web App (app.py):**
- Python 3.7+
- streamlit
- plotly
- pandas

## 🚀 Installation

### CLI Version (No Installation Needed!)

1. Clone the repository:
```bash
git clone https://github.com/katrinDY/fitness-tracker.git
cd fitness-tracker
```

2. Run the CLI application:
```bash
python main.py
```

### Web App Version

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 💻 Usage

### First Time Setup
When you run the application for the first time, you'll be prompted to create your user profile:
- Enter your name, age, weight, height, and gender
- Your BMI will be automatically calculated
- Data is saved automatically

### Main Menu Options

1. **View/Edit Profile** - View your profile and BMI, update weight
2. **Add Workout** - Log a new workout session
3. **View Workout History** - Browse past workouts with filtering options
4. **View Statistics** - See comprehensive analytics and insights
5. **Manage Goals** - Create, view, and track fitness goals
6. **Weekly Summary** - Detailed breakdown of the current week
7. **Export Data** - Export workouts to CSV format
8. **Exit** - Save and exit the application

### Example Usage

```bash
# Run the fitness tracker
python main.py

# The application will guide you through:
# - Creating your profile
# - Adding workouts
# - Setting goals
# - Viewing your progress
```


## 🎯 Classes Overview

### `User`
Manages user profile and body metrics
- BMI calculation
- Weight tracking history
- Body composition analysis

### `Workout`
Represents individual workout sessions
- Automatic calorie calculation based on MET values
- Intensity level detection
- Multiple workout type support

### `Goal`
Handles fitness goal management
- Progress tracking
- Deadline monitoring
- Automatic completion detection

### `WorkoutTracker`
Main application controller
- Data persistence (JSON)
- Analytics and statistics
- Workout and goal management
- CSV export functionality

## 📊 Technical Highlights

- **Object-Oriented Design**: Clean separation of concerns with SOLID principles
- **Type Hints**: Full type annotation for better code quality
- **Data Validation**: Input validation and error handling throughout
- **Data Persistence**: Automatic JSON serialization/deserialization
- **Extensible Architecture**: Easy to add new workout types or features

## 📝 Example Workflow

1. **Create Profile**: Set up your user profile with personal metrics
2. **Log Workouts**: Add workouts after each session
3. **Set Goals**: Create goals like "20 workouts this month"
4. **Track Progress**: Check your stats and streaks regularly
5. **Review Analytics**: Use weekly/monthly summaries to optimize training

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built as part of a Python programming course project
- Calorie calculations based on MET (Metabolic Equivalent of Task) values
- Designed for learners and fitness enthusiasts

---

**Stay healthy, stay fit! 💪**
