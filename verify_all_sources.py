#!/usr/bin/env python3
"""
Verify all source URLs are loading correctly across all dimensions
"""
import re
from pathlib import Path

# Define data root
PROJECT_ROOT = Path(__file__).parent
DATA_ROOT = PROJECT_ROOT / "Alignment to Data Intelligence" / "extracted_xr_files"

# Define dimension source file paths
DIMENSIONS = {
    "Maturity": [
        DATA_ROOT / "xr_present_state_maturity_outputs/XR_Present_State_Maturity_LINKS_VERIFIED.txt",
    ],
    "Interoperability": [
        # No dedicated source files - URLs in CSV
    ],
    "Scalability": [
        DATA_ROOT / "XR scalability/XR_07_Sources_5G_6G_Connectivity.txt",
        DATA_ROOT / "XR scalability/XR_08_Sources_Edge_Computing.txt",
        DATA_ROOT / "XR scalability/XR_09_Sources_Cloud_Rendering.txt",
        DATA_ROOT / "XR scalability/XR_10_Sources_Mobile_Device_Management.txt",
        DATA_ROOT / "XR scalability/XR_11_Sources_Infrastructure_Scaling.txt",
    ],
    "AI Alignment": [
        DATA_ROOT / "Alignment to Data Intelligence/Sources_Tech_Blogs.txt",
        DATA_ROOT / "Alignment to Data Intelligence/Sources_Social_Media.txt",
        DATA_ROOT / "Alignment to Data Intelligence/Sources_Research_Forums.txt",
        DATA_ROOT / "Alignment to Data Intelligence/Sources_Policy_Briefs.txt",
        DATA_ROOT / "Alignment to Data Intelligence/Sources_Professional_Networks.txt",
    ],
    "Use Cases": [
        DATA_ROOT / "XR_use_cases/XR_Submission/xr_usecases_links_UPDATED_2025.txt",
    ],
}

def extract_urls_from_file(file_path):
    """Extract all URLs from a text file using regex"""
    if not file_path.exists():
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract all URLs using regex pattern
            urls = re.findall(r'https?://[^\s]+', content)
            return urls
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return []

def main():
    print("=" * 80)
    print("VERIFYING ALL DIMENSION SOURCE URLs")
    print("=" * 80)

    total_urls = 0
    dimension_counts = {}

    for dim_name, source_files in DIMENSIONS.items():
        if not source_files:
            print(f"\n{dim_name}: No dedicated source files (URLs in CSV)")
            continue

        print(f"\n{dim_name}:")
        dim_urls = []

        for source_file in source_files:
            urls = extract_urls_from_file(source_file)
            print(f"  {source_file.name}: {len(urls)} URLs")
            dim_urls.extend(urls)

        # Remove duplicates
        unique_urls = list(set(dim_urls))
        dimension_counts[dim_name] = len(unique_urls)
        total_urls += len(unique_urls)

        print(f"  ✅ Total unique URLs: {len(unique_urls)}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    for dim_name, count in dimension_counts.items():
        print(f"{dim_name}: {count} unique URLs")

    print(f"\n📚 Total URLs (excluding Interoperability): {total_urls}")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
