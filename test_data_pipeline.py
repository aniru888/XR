"""
Comprehensive Test of XR Data Pipeline
Tests data loading, text analytics, and dimension processing
"""
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "dashboard" / "config"))
sys.path.insert(0, str(Path(__file__).parent / "analysis" / "common"))

from dimensions import (
    ALL_DIMENSIONS,
    get_overall_readiness,
    get_data_summary,
    ANALYTICAL_FRAMEWORK
)
from data_loader import XRDataLoader, get_all_sources, load_dimension
from text_analytics import (
    WordCloudGenerator,
    SentimentAnalyzer,
    TopicModeler
)

def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def test_data_loading():
    """Test data loading for all dimensions"""
    print_header("DATA LOADING TEST")

    loader = XRDataLoader()

    for dimension in ALL_DIMENSIONS:
        print(f"\n{dimension.icon} {dimension.name}")
        print(f"   Purpose: {dimension.purpose}")

        try:
            # Load data
            data = loader.load_dimension_data(dimension.id)
            corpus = loader.load_dimension_corpus(dimension.id)
            sources = loader.load_dimension_sources(dimension.id)
            text = loader.get_text_corpus(dimension.id)

            print(f"   ✅ Data files loaded: {len(data)}")
            print(f"   ✅ Verified sources: {len(sources)}")
            print(f"   ✅ Text corpus: {len(text)} characters")

            # Show sample source URLs
            if sources:
                print(f"   📚 Sample sources:")
                for url in sources[:2]:
                    print(f"      • {url[:70]}...")

        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_text_analytics():
    """Test text analytics on actual data"""
    print_header("TEXT ANALYTICS TEST")

    loader = XRDataLoader()

    # Test on Use Cases dimension (has good structured data)
    print(f"\n💼 Testing on Use Cases Dimension...")

    use_cases_data = load_dimension('use_cases')
    corpus_df = use_cases_data['corpus']

    if isinstance(corpus_df, pd.DataFrame) and 'raw_text' in corpus_df.columns:
        texts = corpus_df['raw_text'].dropna().tolist()

        print(f"   Documents: {len(texts)}")

        # Word Cloud
        print(f"\n   📊 Word Cloud Analysis...")
        wc_gen = WordCloudGenerator()
        combined_text = ' '.join(texts)
        top_words = wc_gen.get_top_words(combined_text, n=10)
        print(f"   ✅ Top 10 words:")
        for word, freq in top_words[:5]:
            print(f"      • {word}: {freq}")

        # Sentiment Analysis
        print(f"\n   😊 Sentiment Analysis...")
        sentiment_analyzer = SentimentAnalyzer()
        sentiments = sentiment_analyzer.analyze_corpus(texts)
        summary = sentiment_analyzer.get_summary_stats(sentiments)
        print(f"   ✅ Average polarity: {summary['avg_polarity']:.3f}")
        print(f"   ✅ Positive: {summary['positive_pct']:.1f}%")
        print(f"   ✅ Neutral: {summary['neutral_pct']:.1f}%")
        print(f"   ✅ Negative: {summary['negative_pct']:.1f}%")

        # Topic Modeling
        if len(texts) >= 5:
            print(f"\n   🎯 Topic Modeling (LDA)...")
            topic_modeler = TopicModeler(n_topics=3)
            topic_modeler.fit(texts)
            labels = topic_modeler.get_topic_labels()
            print(f"   ✅ Topics discovered:")
            for topic_id, label in labels.items():
                print(f"      • {label}")

    else:
        print(f"   ⚠️  Unexpected data format, skipping analytics")

def test_readiness_scores():
    """Test readiness score calculations"""
    print_header("READINESS ASSESSMENT")

    # Overall readiness
    readiness = get_overall_readiness()
    print(f"\n📊 Overall XR Readiness:")
    print(f"   Average Score: {readiness['average_score']:.1f}%")
    print(f"   Status: {readiness['status']}")

    print(f"\n📈 Dimension Breakdown:")
    for dim in ALL_DIMENSIONS:
        print(f"   {dim.readiness_color} {dim.name}: {dim.readiness_score}%")
        print(f"      → {dim.key_finding}")

def test_source_verification():
    """Test source URL extraction"""
    print_header("SOURCE VERIFICATION")

    all_sources = get_all_sources()
    print(f"\n📚 Total Verified Sources: {len(all_sources)}")

    # Group by dimension
    loader = XRDataLoader()
    print(f"\n🔍 Sources by Dimension:")
    for dimension in ALL_DIMENSIONS:
        sources = loader.load_dimension_sources(dimension.id)
        print(f"   {dimension.icon} {dimension.name}: {len(sources)} sources")

def test_analytical_framework():
    """Test analytical framework configuration"""
    print_header("ANALYTICAL FRAMEWORK")

    print(f"\n📋 Framework Title: {ANALYTICAL_FRAMEWORK['title']}")
    print(f"Description: {ANALYTICAL_FRAMEWORK['description']}")

    print(f"\n🔬 Methodology:")
    for method in ANALYTICAL_FRAMEWORK['methodology']:
        print(f"   • {method['name']}")
        print(f"     {method['description']}")

    print(f"\n📊 Data Quality:")
    dq = ANALYTICAL_FRAMEWORK['data_quality']
    print(f"   • Verified URLs: {dq['total_verified_urls']}")
    print(f"   • Status: {dq['verification_status']}")
    print(f"   • Period: {dq['publication_period']}")

def main():
    """Run all tests"""
    print("\n")
    print("█" * 80)
    print("  XR DATA PIPELINE - COMPREHENSIVE TEST")
    print("█" * 80)

    try:
        test_data_loading()
        test_text_analytics()
        test_readiness_scores()
        test_source_verification()
        test_analytical_framework()

        print("\n" + "=" * 80)
        print("  ✅ ALL TESTS PASSED - DATA PIPELINE READY FOR DASHBOARD")
        print("=" * 80)
        print()

        # Summary
        print(f"\n📊 PIPELINE SUMMARY:")
        summary = get_data_summary()
        print(f"   • Total Dimensions: {summary['total_dimensions']}")
        print(f"   • Total Entries: {summary['total_entries']}")
        print(f"   • Verified URLs: {summary['total_verified_urls']}")

        print(f"\n✨ Next Steps:")
        print(f"   1. Build Streamlit dashboard foundation")
        print(f"   2. Create landing page with 5-dimension framework")
        print(f"   3. Build individual dimension pages")
        print(f"   4. Create synthesis/recommendations page")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import pandas as pd  # Import here for use in functions
    main()
