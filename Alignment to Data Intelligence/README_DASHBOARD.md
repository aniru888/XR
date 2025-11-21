# XR Technology Analysis Dashboard

An interactive Streamlit dashboard for comprehensive XR (Extended Reality) technology analysis across five key dimensions.

## Features

- **Executive Summary**: Overall sentiment and key findings
- **Present State of Maturity**: Market readiness analysis
- **Interoperability**: Platform compatibility insights
- **Scalability**: Enterprise deployment capacity
- **Data Intelligence Alignment**: AI/Analytics integration opportunities
- **Use Cases**: Industry application breadth
- **Integrated Analysis**: Cross-dimensional synthesis
- **Managerial Implications**: Strategic recommendations

## Installation

### Step 1: Install Dependencies

Open a terminal/command prompt in this directory and run:

```bash
pip install -r requirements.txt
```

### Step 2: Run the Dashboard

```bash
streamlit run xr_dashboard.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

## Data Sources

The dashboard loads data from the `extracted_xr_files` folder:

- **Sentiment Analysis**: CSV files with sentiment classifications
- **Word Clouds**: Top term frequencies
- **Topic Modeling**: JSON files with identified themes
- **Integration Summaries**: Cross-analysis results
- **Managerial Implications**: Strategic insights

## Deployment to Streamlit Cloud

### Step 1: Push to GitHub

1. Create a new GitHub repository
2. Add all files:
   ```bash
   git init
   git add xr_dashboard.py requirements.txt extracted_xr_files/
   git commit -m "Add XR analysis dashboard"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file path: `xr_dashboard.py`
6. Click "Deploy"

Your dashboard will be live at: `https://your-app-name.streamlit.app`

## Navigation

Use the sidebar to navigate between different analysis views:

- 📊 Executive Summary - Overall findings
- 🎯 Present State of Maturity - Market readiness
- 🔗 Interoperability - Platform compatibility
- 📈 Scalability - Enterprise capacity
- 🤖 Data Intelligence Alignment - AI integration
- 💼 Use Cases - Industry applications
- 🔬 Integrated Analysis - Cross-dimensional insights
- 💡 Managerial Implications - Strategic recommendations

## Analytical Framework

The dashboard integrates three analytical methods:

1. **Word Cloud Analysis**: Visualizes dominant themes
2. **Sentiment Analysis**: Quantifies attitudes (positive/neutral/negative)
3. **Topic Modeling**: Identifies key discussion themes

## Troubleshooting

### Module Not Found Error
```bash
pip install --upgrade -r requirements.txt
```

### Port Already in Use
```bash
streamlit run xr_dashboard.py --server.port 8502
```

### Data Loading Issues
Ensure the `extracted_xr_files` folder is in the same directory as `xr_dashboard.py`

## Requirements

- Python 3.8 or higher
- All dependencies in requirements.txt
- Internet connection for initial package installation

## Support

For issues or questions, refer to:
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python/)
