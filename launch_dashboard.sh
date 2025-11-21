#!/bin/bash
# XR Technology Readiness Dashboard Launcher

echo "=========================================="
echo "  XR Technology Readiness Dashboard"
echo "  Five-Dimension Analytical Framework"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "dashboard/app.py" ]; then
    echo "Error: Please run this script from the XR project root directory"
    exit 1
fi

# Check Python dependencies
echo "Checking dependencies..."
python3 -c "import streamlit, pandas, numpy, matplotlib, wordcloud, textblob, sklearn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "Missing dependencies. Installing..."
    pip install -q streamlit pandas numpy matplotlib wordcloud textblob scikit-learn
    echo "✓ Dependencies installed"
fi

echo "✓ All dependencies ready"
echo ""

# Display dashboard info
echo "Dashboard Information:"
echo "  • Overall Readiness: 77% (Ready for Pilot Programs)"
echo "  • Dimensions: 5 (Maturity, Interoperability, Scalability, AI Alignment, Use Cases)"
echo "  • Verified Sources: 591 URLs"
echo "  • Total Entries: 940 data points"
echo "  • Analysis Period: 2020-2025"
echo ""

echo "Launching dashboard..."
echo "→ The dashboard will open in your browser at http://localhost:8501"
echo "→ Press Ctrl+C to stop the dashboard"
echo ""

cd dashboard
streamlit run app.py
