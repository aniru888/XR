#!/usr/bin/env python3
"""
Complete verification of all source URLs including CSV sources
"""
import re
import csv
from pathlib import Path

# Define data root
PROJECT_ROOT = Path(__file__).parent
DATA_ROOT = PROJECT_ROOT / "Alignment to Data Intelligence" / "extracted_xr_files"

def extract_urls_from_txt(file_path):
    """Extract all URLs from a text file using regex"""
    if not file_path.exists():
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            urls = re.findall(r'https?://[^\s]+', content)
            return urls
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return []

def extract_urls_from_csv(file_path, url_column='source_url'):
    """Extract URLs from CSV file"""
    if not file_path.exists():
        return []

    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if url_column in row and row[url_column]:
                    url = row[url_column].strip()
                    if url.startswith('http'):
                        urls.append(url)
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")

    return urls

def main():
    print("=" * 80)
    print("COMPLETE SOURCE URL VERIFICATION")
    print("=" * 80)

    all_sources = {}

    # Maturity
    print("\n1. MATURITY")
    maturity_urls = extract_urls_from_txt(
        DATA_ROOT / "xr_present_state_maturity_outputs/XR_Present_State_Maturity_LINKS_VERIFIED.txt"
    )
    all_sources['Maturity'] = list(set(maturity_urls))
    print(f"   ✅ {len(all_sources['Maturity'])} unique URLs")

    # Interoperability
    print("\n2. INTEROPERABILITY")
    interop_urls = extract_urls_from_csv(
        DATA_ROOT / "xr_interop_submission/xr_interop_raw.csv"
    )
    all_sources['Interoperability'] = list(set(interop_urls))
    print(f"   ✅ {len(all_sources['Interoperability'])} unique URLs (from CSV)")

    # Scalability
    print("\n3. SCALABILITY")
    scalability_files = [
        "XR scalability/XR_07_Sources_5G_6G_Connectivity.txt",
        "XR scalability/XR_08_Sources_Edge_Computing.txt",
        "XR scalability/XR_09_Sources_Cloud_Rendering.txt",
        "XR scalability/XR_10_Sources_Mobile_Device_Management.txt",
        "XR scalability/XR_11_Sources_Infrastructure_Scaling.txt",
    ]
    scalability_urls = []
    for file in scalability_files:
        urls = extract_urls_from_txt(DATA_ROOT / file)
        print(f"   {Path(file).name}: {len(urls)} URLs")
        scalability_urls.extend(urls)
    all_sources['Scalability'] = list(set(scalability_urls))
    print(f"   ✅ {len(all_sources['Scalability'])} unique URLs")

    # AI Alignment
    print("\n4. AI ALIGNMENT")
    ai_files = [
        "Alignment to Data Intelligence/Sources_Tech_Blogs.txt",
        "Alignment to Data Intelligence/Sources_Social_Media.txt",
        "Alignment to Data Intelligence/Sources_Research_Forums.txt",
        "Alignment to Data Intelligence/Sources_Policy_Briefs.txt",
        "Alignment to Data Intelligence/Sources_Professional_Networks.txt",
    ]
    ai_urls = []
    for file in ai_files:
        urls = extract_urls_from_txt(DATA_ROOT / file)
        print(f"   {Path(file).name}: {len(urls)} URLs")
        ai_urls.extend(urls)
    all_sources['AI Alignment'] = list(set(ai_urls))
    print(f"   ✅ {len(all_sources['AI Alignment'])} unique URLs")

    # Use Cases
    print("\n5. USE CASES")
    use_case_urls = extract_urls_from_txt(
        DATA_ROOT / "XR_use_cases/XR_Submission/xr_usecases_links_UPDATED_2025.txt"
    )
    all_sources['Use Cases'] = list(set(use_case_urls))
    print(f"   ✅ {len(all_sources['Use Cases'])} unique URLs")

    # Summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)

    total = 0
    for dim, urls in all_sources.items():
        count = len(urls)
        total += count
        print(f"{dim:20s}: {count:3d} URLs")

    print(f"\n{'TOTAL':20s}: {total:3d} URLs")
    print("=" * 80)

    # Check for overlaps
    all_urls_combined = []
    for urls in all_sources.values():
        all_urls_combined.extend(urls)

    unique_total = len(set(all_urls_combined))
    if unique_total != total:
        print(f"\n⚠️  Note: {total - unique_total} duplicate URLs across dimensions")
        print(f"   Globally unique URLs: {unique_total}")

if __name__ == "__main__":
    main()
