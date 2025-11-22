"""
Unified Data Loader for All XR Dimensions
Handles different data formats and provides standardized interfaces
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Union
import sys

# Add dashboard config to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "dashboard" / "config"))
from dimensions import (
    ALL_DIMENSIONS,
    DimensionConfig,
    get_dimension_by_id,
    DATA_ROOT
)


class XRDataLoader:
    """Unified data loader for all XR dimensions"""

    def __init__(self):
        """Initialize the data loader"""
        self.dimensions = ALL_DIMENSIONS
        self.data_cache = {}

    def load_dimension_data(self, dimension_id: str) -> Dict[str, pd.DataFrame]:
        """
        Load all data files for a specific dimension

        Args:
            dimension_id: ID of the dimension ('maturity', 'interoperability', etc.)

        Returns:
            Dictionary mapping file names to DataFrames
        """
        if dimension_id in self.data_cache:
            return self.data_cache[dimension_id]

        dimension = get_dimension_by_id(dimension_id)
        if not dimension:
            raise ValueError(f"Unknown dimension ID: {dimension_id}")

        data = {}
        for file_path in dimension.get_data_paths():
            if not file_path.exists():
                print(f"⚠️  Warning: File not found: {file_path}")
                continue

            file_name = file_path.stem
            try:
                if file_path.suffix == '.csv':
                    data[file_name] = pd.read_csv(file_path)
                elif file_path.suffix == '.txt':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data[file_name] = f.read()
                else:
                    print(f"⚠️  Warning: Unsupported file type: {file_path}")
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")

        self.data_cache[dimension_id] = data
        return data

    def load_dimension_corpus(self, dimension_id: str) -> Union[pd.DataFrame, str]:
        """
        Load the main corpus/data file for a dimension

        Returns:
            DataFrame or string depending on the dimension's primary data format
        """
        data = self.load_dimension_data(dimension_id)

        # Dimension-specific corpus extraction
        corpus_mapping = {
            'maturity': 'XR_present_state_corpus',
            'interoperability': 'xr_interop_clean',
            'scalability': 'XR_06_Scalability_Master_Corpus',
            'ai_alignment': 'XR_Integrated_Master_Corpus',
            'use_cases': 'xr_usecases_corpus'
        }

        corpus_key = corpus_mapping.get(dimension_id)
        if corpus_key and corpus_key in data:
            return data[corpus_key]

        # Fallback: return first available data
        if data:
            return list(data.values())[0]

        return pd.DataFrame()  # Empty DataFrame if nothing found

    def load_dimension_sources(self, dimension_id: str) -> List[str]:
        """
        Load verified source URLs for a dimension

        Returns:
            List of verified article URLs
        """
        import re

        dimension = get_dimension_by_id(dimension_id)
        if not dimension:
            return []

        sources = []

        # Try to load from dedicated source files
        for source_file in dimension.get_source_paths():
            if source_file.exists() and source_file.suffix == '.txt':
                try:
                    with open(source_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract all URLs using regex pattern
                        # Matches http:// or https:// followed by non-whitespace characters
                        urls = re.findall(r'https?://[^\s]+', content)
                        sources.extend(urls)
                except Exception as e:
                    print(f"⚠️  Error reading sources from {source_file}: {e}")

        # If no dedicated source file, extract from CSV files
        if not sources:
            data = self.load_dimension_data(dimension_id)
            for df_name, df in data.items():
                if isinstance(df, pd.DataFrame):
                    # Look for URL columns
                    url_columns = [col for col in df.columns if 'url' in col.lower()]
                    for col in url_columns:
                        urls = df[col].dropna().unique().tolist()
                        sources.extend([str(url) for url in urls if str(url).startswith('http')])

        return list(set(sources))  # Remove duplicates

    def get_text_corpus(self, dimension_id: str) -> str:
        """
        Extract text corpus for NLP analysis

        Returns:
            Combined text string suitable for word cloud, sentiment, topic modeling
        """
        corpus_data = self.load_dimension_corpus(dimension_id)

        # If it's already a string (text file)
        if isinstance(corpus_data, str):
            return corpus_data

        # If it's a DataFrame, extract text from all string columns
        if isinstance(corpus_data, pd.DataFrame):
            text_columns = []

            # Common text column names across dimensions
            text_col_names = ['text', 'content', 'raw_text', 'clean_text', 'description']

            for col in text_col_names:
                if col in corpus_data.columns:
                    text_columns.append(col)

            if text_columns:
                all_text = []
                for col in text_columns:
                    all_text.extend(corpus_data[col].dropna().astype(str).tolist())
                return ' '.join(all_text)

            # Fallback: combine all string columns
            string_cols = corpus_data.select_dtypes(include=['object']).columns
            all_text = []
            for col in string_cols:
                all_text.extend(corpus_data[col].dropna().astype(str).tolist())
            return ' '.join(all_text)

        return ""

    def load_all_dimensions(self) -> Dict[str, Dict]:
        """
        Load data for all dimensions

        Returns:
            Dictionary mapping dimension IDs to their data
        """
        all_data = {}
        for dimension in self.dimensions:
            try:
                all_data[dimension.id] = {
                    'config': dimension,
                    'data': self.load_dimension_data(dimension.id),
                    'corpus': self.load_dimension_corpus(dimension.id),
                    'sources': self.load_dimension_sources(dimension.id),
                    'text': self.get_text_corpus(dimension.id)
                }
                print(f"✅ Loaded {dimension.name}: {len(all_data[dimension.id]['sources'])} sources")
            except Exception as e:
                print(f"❌ Error loading {dimension.name}: {e}")

        return all_data

    def get_dimension_summary(self, dimension_id: str) -> Dict:
        """
        Get summary statistics for a dimension

        Returns:
            Dictionary with counts, sources, readiness info
        """
        dimension = get_dimension_by_id(dimension_id)
        if not dimension:
            return {}

        sources = self.load_dimension_sources(dimension_id)
        corpus = self.load_dimension_corpus(dimension_id)

        entry_count = 0
        if isinstance(corpus, pd.DataFrame):
            entry_count = len(corpus)
        elif isinstance(corpus, str):
            # Rough estimate based on sentences
            entry_count = len([s for s in corpus.split('.') if s.strip()])

        return {
            'id': dimension.id,
            'name': dimension.name,
            'purpose': dimension.purpose,
            'icon': dimension.icon,
            'question': dimension.question,
            'entry_count': entry_count,
            'source_count': len(sources),
            'readiness_score': dimension.readiness_score,
            'readiness_color': dimension.readiness_color,
            'key_finding': dimension.key_finding
        }

    def export_combined_sources(self, output_file: Path):
        """
        Export all verified sources to a single master file

        Args:
            output_file: Path to output CSV file
        """
        all_sources = []

        for dimension in self.dimensions:
            sources = self.load_dimension_sources(dimension.id)
            for url in sources:
                all_sources.append({
                    'dimension_id': dimension.id,
                    'dimension_name': dimension.name,
                    'url': url,
                    'readiness_score': dimension.readiness_score
                })

        df = pd.DataFrame(all_sources)
        df.to_csv(output_file, index=False)
        print(f"✅ Exported {len(all_sources)} sources to {output_file}")

    def validate_all_data(self) -> Dict:
        """
        Validate all data files exist and are accessible

        Returns:
            Validation report with errors and warnings
        """
        report = {
            'total_dimensions': len(self.dimensions),
            'valid_dimensions': 0,
            'missing_files': [],
            'errors': []
        }

        for dimension in self.dimensions:
            try:
                data = self.load_dimension_data(dimension.id)
                if data:
                    report['valid_dimensions'] += 1
                else:
                    report['missing_files'].extend([str(p) for p in dimension.get_data_paths()])
            except Exception as e:
                report['errors'].append(f"{dimension.name}: {str(e)}")

        return report


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

_global_loader = None

def get_loader() -> XRDataLoader:
    """Get global data loader instance (singleton)"""
    global _global_loader
    if _global_loader is None:
        _global_loader = XRDataLoader()
    return _global_loader

def load_dimension(dimension_id: str) -> Dict:
    """Quick load function for a specific dimension"""
    loader = get_loader()
    return {
        'config': get_dimension_by_id(dimension_id),
        'data': loader.load_dimension_data(dimension_id),
        'corpus': loader.load_dimension_corpus(dimension_id),
        'sources': loader.load_dimension_sources(dimension_id),
        'text': loader.get_text_corpus(dimension_id)
    }

def get_all_sources() -> List[str]:
    """Get all verified sources across all dimensions"""
    loader = get_loader()
    all_sources = []
    for dimension in ALL_DIMENSIONS:
        all_sources.extend(loader.load_dimension_sources(dimension.id))
    return list(set(all_sources))


# ============================================================================
# TESTING / VALIDATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("XR DATA LOADER - VALIDATION TEST")
    print("=" * 70)

    loader = XRDataLoader()

    # Test loading all dimensions
    print("\n📊 Loading all dimensions...")
    all_data = loader.load_all_dimensions()

    print("\n" + "=" * 70)
    print("DIMENSION SUMMARIES")
    print("=" * 70)

    for dim_id in all_data:
        summary = loader.get_dimension_summary(dim_id)
        print(f"\n{summary['icon']} {summary['name']}")
        print(f"   Purpose: {summary['purpose']}")
        print(f"   Entries: {summary['entry_count']}")
        print(f"   Sources: {summary['source_count']} verified URLs")
        print(f"   Readiness: {summary['readiness_color']} {summary['readiness_score']}%")

    # Validation report
    print("\n" + "=" * 70)
    print("VALIDATION REPORT")
    print("=" * 70)

    validation = loader.validate_all_data()
    print(f"✅ Valid dimensions: {validation['valid_dimensions']}/{validation['total_dimensions']}")

    if validation['missing_files']:
        print(f"\n⚠️  Missing files ({len(validation['missing_files'])}):")
        for f in validation['missing_files'][:5]:  # Show first 5
            print(f"   - {f}")

    if validation['errors']:
        print(f"\n❌ Errors ({len(validation['errors'])}):")
        for err in validation['errors']:
            print(f"   - {err}")

    # Total sources
    all_sources = get_all_sources()
    print(f"\n📚 Total verified sources: {len(all_sources)}")

    print("\n" + "=" * 70)
    print("✅ DATA LOADER READY FOR DASHBOARD")
    print("=" * 70)
