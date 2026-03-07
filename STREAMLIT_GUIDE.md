# 🚀 Streamlit Web App Guide

## 💻 Running the Fitness Tracker Web App

The project now has **TWO interfaces**:
1. **CLI Version**
2. **Web App**

---

## 📦 Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web framework
- `plotly` - Interactive charts
- `pandas` - Data manipulation
- `watchdog` - File system monitoring

### Step 2: Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## 🎨 Features of the Web App

### 📊 Dashboard
- Real-time statistics overview
- Interactive charts (calories over time, workout distribution)
- Weekly activity breakdown
- Current streak tracker

### 💪 Add Workout
- Easy form to log workouts
- Date/time picker
- Automatic calorie calculation
- Success notifications
- Goal completion alerts

### 📋 Workout History
- Searchable and filterable table
- Sort by date, calories, or duration
- Date range filters (This Week, This Month, Last 7/30 Days)
- Summary statistics

### 🎯 Goals
- Create custom goals
- Progress bars for each goal
- Deadline tracking
- Automatic completion detection
- Separate views for active and completed goals

### 📈 Advanced Analytics
- Monthly comparison charts
- Intensity distribution
- Performance by workout type
- Trend analysis

### 👤 Profile
- BMI calculator
- Weight tracking
- Profile management
- BMI category indicator

---

## 💡 Tips for Using the Web App

### First Time Setup
1. Go to **Profile** page first
2. Fill in your details
3. Start adding workouts

### Best Practices
- Log workouts immediately after finishing
- Set weekly/monthly goals to stay motivated
- Check Dashboard daily for progress
- Use Analytics to identify patterns

### Data Persistence
- All data is saved to `streamlit_fitness_data.json`
- Separate from CLI data (`fitness_data.json`)
- Backup this file regularly

---

```

### Key Features to Highlight

✅ **Full-Stack Development** - Backend logic + Frontend UI
✅ **Data Visualization** - Interactive charts and graphs
✅ **Real-time Updates** - Instant feedback and recalculation
✅ **Responsive Design** - Works on desktop and mobile
✅ **Cloud Deployment** - Production-ready application
✅ **User Experience** - Intuitive interface with form validation

---

## 🔧 Customization

### Change Theme/Colors

Edit the color scheme in `app.py`:
```python
st.set_page_config(
    page_title="Your App Name",
    page_icon="🏋️",  # Change emoji
    ...
)
```

### Add New Features

Easy to extend:
- Add nutrition tracking page
- Create workout plans
- Add social sharing
- Integrate with fitness APIs

---

## 📊 Comparison: CLI vs Web App

| Feature | CLI (main.py) | Web App (app.py) |
|---------|---------------|------------------|
| **Interface** | Command-line | Web browser |
| **Charts** | Text-based | Interactive graphs |
| **User Experience** | Technical | Visual & intuitive |
| **Deployment** | Run locally | Deploy to cloud |
| **Mobile** | Not suitable | Responsive |
| **Best For** | Course requirements | Portfolio/CV |

**Both use the same `models.py` backend!**

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Module Not Found
```bash
pip install -r requirements.txt --upgrade
```

### Data Not Saving
Check file permissions in your directory

### Charts Not Showing
Update plotly:
```bash
pip install plotly --upgrade
```

---

## 🎓 Learning Resources

Want to customize more?
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Charts](https://plotly.com/python/)
- [Pandas Tutorial](https://pandas.pydata.org/docs/)

---