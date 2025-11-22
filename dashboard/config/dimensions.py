"""
XR Analysis Dimensions Configuration
Defines metadata, paths, and properties for all 5 analytical dimensions
"""
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "Alignment to Data Intelligence" / "extracted_xr_files"

# Color scheme for dashboard
COLORS = {
    'primary_blue': '#0066CC',
    'accent_teal': '#00C9A7',
    'success_green': '#28A745',
    'warning_amber': '#FFC107',
    'alert_red': '#DC3545',
    'neutral_gray': '#6C757D'
}

@dataclass
class DimensionConfig:
    """Configuration for a single dimension"""
    id: str
    name: str
    purpose: str
    icon: str
    question: str
    data_files: List[Path]
    source_files: List[Path]
    entry_count: int
    readiness_score: int  # 0-100
    readiness_color: str  # 🟢 🟡 🔴
    key_finding: str

    def get_data_paths(self) -> List[Path]:
        """Get absolute paths to data files"""
        return [DATA_ROOT / path for path in self.data_files]

    def get_source_paths(self) -> List[Path]:
        """Get absolute paths to source files"""
        return [DATA_ROOT / path for path in self.source_files]


# ============================================================================
# DIMENSION 1: PRESENT STATE OF MATURITY
# ============================================================================
DIMENSION_1_MATURITY = DimensionConfig(
    id="maturity",
    name="Present State of Maturity",
    purpose="How widely the technology has progressed from lab to market",
    icon="📍",
    question="Where does XR stand on the adoption curve—lab prototype, enterprise pilot, or mainstream deployment?",
    data_files=[
        Path("xr_present_state_maturity_outputs/XR_present_state_corpus.txt"),
        Path("xr_present_state_maturity_outputs/XR_present_state_VERBATIM_raw_EXPANDED.txt"),
        Path("xr_present_state_maturity_outputs/xr_sentences_sentiment.csv"),
        Path("xr_present_state_maturity_outputs/xr_topics.csv"),
    ],
    source_files=[
        Path("xr_present_state_maturity_outputs/XR_Present_State_Maturity_LINKS_VERIFIED.txt"),
    ],
    entry_count=157,
    readiness_score=75,
    readiness_color="🟡",
    key_finding="Market transitioning from pilot to scale (17 verified sources): 70% positive sentiment, enterprise adoption accelerating despite hardware/content barriers"
)

# ============================================================================
# DIMENSION 2: INTEROPERABILITY
# ============================================================================
DIMENSION_2_INTEROP = DimensionConfig(
    id="interoperability",
    name="Interoperability",
    purpose="Compatibility with existing business and data ecosystems",
    icon="🔗",
    question="Can XR integrate seamlessly with current enterprise systems, platforms, and workflows?",
    data_files=[
        Path("xr_interop_submission/xr_interop_raw.csv"),
        Path("xr_interop_submission/xr_interop_clean.csv"),
        Path("xr_interop_submission/xr_interop_sentiment.csv"),
        Path("xr_interop_submission/xr_interop_topics.csv"),
    ],
    source_files=[
        # URLs are embedded in xr_interop_raw.csv (source_url column)
    ],
    entry_count=19,
    readiness_score=70,
    readiness_color="🟡",
    key_finding="OpenXR adoption growing (70%+ support), but cross-platform challenges remain across runtimes"
)

# ============================================================================
# DIMENSION 3: SCALABILITY
# ============================================================================
DIMENSION_3_SCALABILITY = DimensionConfig(
    id="scalability",
    name="Scalability",
    purpose="Capacity to deliver enterprise-grade solutions",
    icon="⚡",
    question="Can XR infrastructure scale from 10 users to 10,000 users without performance degradation?",
    data_files=[
        Path("XR scalability/XR_01_5G_6G_Connectivity_Data.csv"),
        Path("XR scalability/XR_02_Edge_Computing_Data.csv"),
        Path("XR scalability/XR_03_Cloud_Rendering_Data.csv"),
        Path("XR scalability/XR_04_Mobile_Device_Management_Data.csv"),
        Path("XR scalability/XR_05_Infrastructure_Scaling_Data.csv"),
        Path("XR scalability/XR_06_Scalability_Master_Corpus.csv"),
        Path("XR scalability/XR_Sentiment_Analysis_Results.csv"),
        Path("XR scalability/XR_LDA_Topic_Distribution.csv"),
    ],
    source_files=[
        Path("XR scalability/XR_07_Sources_5G_6G_Connectivity.txt"),
        Path("XR scalability/XR_08_Sources_Edge_Computing.txt"),
        Path("XR scalability/XR_09_Sources_Cloud_Rendering.txt"),
        Path("XR scalability/XR_10_Sources_Mobile_Device_Management.txt"),
        Path("XR scalability/XR_11_Sources_Infrastructure_Scaling.txt"),
    ],
    entry_count=600,
    readiness_score=85,
    readiness_color="🟢",
    key_finding="Infrastructure ready with 5G/edge computing (136 verified sources), cloud rendering enables scale"
)

# ============================================================================
# DIMENSION 4: ALIGNMENT TO DATA INTELLIGENCE
# ============================================================================
DIMENSION_4_AI_ALIGNMENT = DimensionConfig(
    id="ai_alignment",
    name="Alignment to Data Intelligence",
    purpose="Synergy with AI, analytics, and decision systems",
    icon="🤖",
    question="How does XR amplify data-driven decision-making through AI integration and intelligent insights?",
    data_files=[
        Path("Alignment to Data Intelligence/XR_Integrated_Master_Corpus.csv"),
        Path("Alignment to Data Intelligence/XR_Cleaned_Data.csv"),
        Path("Alignment to Data Intelligence/xr_ai_alignment_sentiment.csv"),
        Path("Alignment to Data Intelligence/xr_ai_alignment_topics.csv"),
    ],
    source_files=[
        Path("Alignment to Data Intelligence/Sources_Tech_Blogs.txt"),
        Path("Alignment to Data Intelligence/Sources_Social_Media.txt"),
        Path("Alignment to Data Intelligence/Sources_Research_Forums.txt"),
        Path("Alignment to Data Intelligence/Sources_Policy_Briefs.txt"),
        Path("Alignment to Data Intelligence/Sources_Professional_Networks.txt"),
    ],
    entry_count=65,
    readiness_score=65,
    readiness_color="🟡",
    key_finding="Emerging convergence: World models & digital twins dominate AI-XR integration (55% positive sentiment)"
)

# ============================================================================
# DIMENSION 5: USE CASES
# ============================================================================
DIMENSION_5_USE_CASES = DimensionConfig(
    id="use_cases",
    name="Use Cases",
    purpose="Breadth and diversity of industry applications",
    icon="💼",
    question="Across how many industries and job functions can XR deliver measurable business value?",
    data_files=[
        Path("XR_use_cases/XR_Submission/xr_usecases_corpus_VERIFIED.csv"),
    ],
    source_files=[
        Path("XR_use_cases/XR_Submission/xr_usecases_links_UPDATED_2025.txt"),
    ],
    entry_count=20,
    readiness_score=85,
    readiness_color="🟢",
    key_finding="Proven ROI: Boeing 30% faster assembly, DHL 25% efficiency, Mayo Clinic 25% skill boost"
)

# ============================================================================
# ALL DIMENSIONS REGISTRY
# ============================================================================
ALL_DIMENSIONS = [
    DIMENSION_1_MATURITY,
    DIMENSION_2_INTEROP,
    DIMENSION_3_SCALABILITY,
    DIMENSION_4_AI_ALIGNMENT,
    DIMENSION_5_USE_CASES,
]

DIMENSIONS_BY_ID = {dim.id: dim for dim in ALL_DIMENSIONS}

# ============================================================================
# ANALYTICAL FRAMEWORK
# ============================================================================
ANALYTICAL_FRAMEWORK = {
    "title": "Five-Dimension Analytical Framework",
    "description": "Analyzing XR technology readiness through social data signals",
    "data_sources": [
        "Technology blogs (Nokia, NVIDIA, Microsoft, etc.)",
        "Professional networks (LinkedIn discussions, industry forums)",
        "Research abstracts (IEEE Xplore, arXiv, academic journals)",
        "Policy briefs & whitepapers (Ericsson, Qualcomm, AWS)",
        "Twitter/X posts and hashtags (#XR, #ExtendedReality, #Metaverse)"
    ],
    "methodology": [
        {
            "name": "Word Cloud Analysis",
            "description": "Statistical word frequency analysis to visualize dominant themes"
        },
        {
            "name": "Sentiment Analysis",
            "description": "VADER-based sentiment scoring to quantify public attitude (optimism, skepticism, controversy)"
        },
        {
            "name": "Topic Modelling (LDA)",
            "description": "Discovering hidden themes through Latent Dirichlet Allocation"
        }
    ],
    "data_quality": {
        "total_verified_urls": 254,
        "verification_status": "All URLs tested: 200 OK (no 404 errors)",
        "publication_period": "2023-2025",
        "source_types": "Market research reports, technical blogs, research papers, professional networks, policy briefs, social media"
    }
}

# ============================================================================
# LEADERSHIP CONTEXT
# ============================================================================
LEADERSHIP_CONTEXT = {
    "question": "In an AI-native enterprise, which emerging technologies deserve strategic investment?",
    "azeem_vision": "We are not just looking for the next tech to bet on. We're trying to understand the ecosystem in which that technology will thrive.",
    "ananya_vision": "Our vision isn't to chase the trend; it's to anticipate convergence. Technologies like Quantum or Edge Computing will only matter if they align with intelligence-driven business transformation.",
    "goal": "Generate a comparative understanding of readiness, perception, and opportunity—not to declare a 'winner' technology."
}

# ============================================================================
# COLOR SCHEME
# ============================================================================
THEME_COLORS = {
    "primary": "#0066CC",      # Professional blue
    "secondary": "#00C9A7",     # Success/growth green
    "warning": "#FFA500",       # Caution orange
    "danger": "#DC3545",        # Risk red
    "neutral": "#6C757D",       # Text/borders
    "background": "#F8F9FA",    # Subtle gray
    "card": "#FFFFFF",          # Clean white
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_dimension_by_id(dimension_id: str) -> Optional[DimensionConfig]:
    """Get dimension configuration by ID"""
    return DIMENSIONS_BY_ID.get(dimension_id)

def get_all_dimension_names() -> List[str]:
    """Get list of all dimension names"""
    return [dim.name for dim in ALL_DIMENSIONS]

def get_overall_readiness() -> Dict:
    """Calculate overall XR readiness score"""
    scores = [dim.readiness_score for dim in ALL_DIMENSIONS]
    avg_score = sum(scores) / len(scores)

    if avg_score >= 80:
        status = "🟢 Ready for Targeted Enterprise Deployment"
    elif avg_score >= 60:
        status = "🟡 Ready for Pilot Programs with Caution"
    else:
        status = "🔴 Not Yet Ready for Enterprise Deployment"

    return {
        "average_score": avg_score,
        "status": status,
        "dimension_scores": {dim.name: dim.readiness_score for dim in ALL_DIMENSIONS}
    }

def get_data_summary() -> Dict:
    """Get summary of all data sources"""
    return {
        "total_dimensions": len(ALL_DIMENSIONS),
        "total_entries": sum(dim.entry_count for dim in ALL_DIMENSIONS),
        "total_verified_urls": 254,
        "dimensions": [
            {
                "name": dim.name,
                "entries": dim.entry_count,
                "readiness": f"{dim.readiness_color} {dim.readiness_score}%"
            }
            for dim in ALL_DIMENSIONS
        ]
    }
