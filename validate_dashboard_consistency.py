#!/usr/bin/env python3
"""
Comprehensive Dashboard Consistency Validation Script
Verifies all data sources, counts, and configurations are accurate and consistent
"""
import sys
import csv
import re
from pathlib import Path
from collections import defaultdict

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}{text:^80}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    print(f"  {text}")

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_PATH = Path("/home/user/XR")
DATA_PATH = BASE_PATH / "Alignment to Data Intelligence" / "extracted_xr_files"

EXPECTED_TOTALS = {
    "total_verified_urls": 254,
    "total_entries": 861,
    "dimensions": 5
}

DIMENSION_EXPECTED = {
    "Maturity": {"entries": 157, "urls": 17},
    "Interoperability": {"entries": 19, "urls": 19},
    "Scalability": {"entries": 600, "urls": 136},
    "AI Alignment": {"entries": 65, "urls": 59},
    "Use Cases": {"entries": 20, "urls": 25}
}

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_dimensions_config():
    """Validate dimensions.py configuration"""
    print_header("VALIDATING DIMENSIONS.PY CONFIGURATION")

    sys.path.insert(0, str(BASE_PATH / "dashboard" / "config"))
    from dimensions import ALL_DIMENSIONS, ANALYTICAL_FRAMEWORK, get_data_summary

    errors = []
    warnings = []

    # Check number of dimensions
    if len(ALL_DIMENSIONS) == EXPECTED_TOTALS["dimensions"]:
        print_success(f"Correct number of dimensions: {len(ALL_DIMENSIONS)}")
    else:
        errors.append(f"Expected {EXPECTED_TOTALS['dimensions']} dimensions, found {len(ALL_DIMENSIONS)}")

    # Check total entries
    total_entries = sum(dim.entry_count for dim in ALL_DIMENSIONS)
    if total_entries == EXPECTED_TOTALS["total_entries"]:
        print_success(f"Total entries correct: {total_entries}")
    else:
        errors.append(f"Expected {EXPECTED_TOTALS['total_entries']} total entries, calculated {total_entries}")

    # Check verified URLs in ANALYTICAL_FRAMEWORK
    framework_urls = ANALYTICAL_FRAMEWORK['data_quality']['total_verified_urls']
    if framework_urls == EXPECTED_TOTALS["total_verified_urls"]:
        print_success(f"ANALYTICAL_FRAMEWORK verified URLs correct: {framework_urls}")
    else:
        errors.append(f"ANALYTICAL_FRAMEWORK: Expected {EXPECTED_TOTALS['total_verified_urls']}, found {framework_urls}")

    # Check verified URLs in get_data_summary
    summary = get_data_summary()
    summary_urls = summary['total_verified_urls']
    if summary_urls == EXPECTED_TOTALS["total_verified_urls"]:
        print_success(f"get_data_summary() verified URLs correct: {summary_urls}")
    else:
        errors.append(f"get_data_summary(): Expected {EXPECTED_TOTALS['total_verified_urls']}, found {summary_urls}")

    # Check each dimension
    print_info("\nDimension-specific validation:")
    for dim in ALL_DIMENSIONS:
        dim_name = dim.name.split()[-1]  # Get last word (Maturity, Interoperability, etc.)
        if dim_name in DIMENSION_EXPECTED:
            expected = DIMENSION_EXPECTED[dim_name]
            if dim.entry_count == expected["entries"]:
                print_success(f"  {dim.icon} {dim.name}: {dim.entry_count} entries ✓")
            else:
                errors.append(f"{dim.name}: Expected {expected['entries']} entries, found {dim.entry_count}")

    return errors, warnings

def count_actual_verified_urls():
    """Count actual verified URLs from source files"""
    print_header("COUNTING ACTUAL VERIFIED URLs FROM SOURCE FILES")

    sys.path.insert(0, str(BASE_PATH / "dashboard" / "config"))
    from dimensions import ALL_DIMENSIONS

    total_urls = set()
    dimension_counts = {}

    for dimension in ALL_DIMENSIONS:
        dim_urls = set()

        # Load from dedicated source files
        for source_file in dimension.get_source_paths():
            if source_file.exists() and source_file.suffix == '.txt':
                try:
                    with open(source_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract URLs from text
                        urls_in_text = re.findall(r'https?://[^\s\),]+', content)
                        for url in urls_in_text:
                            dim_urls.add(url.rstrip(',').rstrip(')'))
                        # Also check for lines starting with http
                        for line in content.split('\n'):
                            stripped = line.strip()
                            if stripped.startswith('http'):
                                dim_urls.add(stripped)
                except Exception as e:
                    print_warning(f"Error reading {source_file}: {e}")

        # If no dedicated source files, check CSV
        if not dim_urls:
            for data_file in dimension.get_data_paths():
                if data_file.exists() and data_file.suffix == '.csv':
                    try:
                        with open(data_file, 'r', encoding='utf-8') as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                for col in ['source_url', 'url', 'link', 'source']:
                                    if col in row and row[col]:
                                        if str(row[col]).startswith('http'):
                                            dim_urls.add(row[col])
                    except Exception as e:
                        pass

        dimension_counts[dimension.name] = len(dim_urls)
        total_urls.update(dim_urls)
        print_info(f"{dimension.icon} {dimension.name}: {len(dim_urls)} URLs")

    total_count = len(total_urls)
    print(f"\n{BLUE}{'─'*80}{RESET}")
    if total_count == EXPECTED_TOTALS["total_verified_urls"]:
        print_success(f"TOTAL VERIFIED URLs: {total_count} ✓")
    else:
        print_error(f"TOTAL VERIFIED URLs: {total_count} (Expected {EXPECTED_TOTALS['total_verified_urls']})")

    return total_count, dimension_counts

def validate_dashboard_files():
    """Validate app.py and synthesis page"""
    print_header("VALIDATING DASHBOARD FILES")

    errors = []

    # Check app.py
    app_file = BASE_PATH / "dashboard" / "app.py"
    with open(app_file, 'r') as f:
        content = f.read()

    # Check for incorrect counts
    if '591' in content:
        errors.append("app.py still contains '591' (should be 254)")
    else:
        print_success("app.py: No references to '591'")

    if '254 verified URLs' in content or '254 Verified URLs' in content:
        print_success("app.py: Contains correct count '254'")
    else:
        print_warning("app.py: May not contain '254' reference")

    # Check for full names
    if 'Azeem Azhar' in content or 'Ananya Srivastava' in content:
        errors.append("app.py still contains full names (should be first names only)")
    else:
        print_success("app.py: Uses first names only")

    # Check synthesis page
    synthesis_file = BASE_PATH / "dashboard" / "pages" / "7_🎯_Synthesis.py"
    with open(synthesis_file, 'r') as f:
        content = f.read()

    if '591' in content:
        errors.append("Synthesis.py still contains '591' (should be 254)")
    else:
        print_success("Synthesis.py: No references to '591'")

    if '254' in content:
        print_success("Synthesis.py: Contains correct count '254'")
    else:
        print_warning("Synthesis.py: May not contain '254' reference")

    return errors

def validate_readme_files():
    """Validate README and documentation"""
    print_header("VALIDATING README & DOCUMENTATION")

    errors = []

    # Check dashboard README
    readme_file = BASE_PATH / "dashboard" / "README.md"
    if readme_file.exists():
        with open(readme_file, 'r') as f:
            content = f.read()

        if '591' in content:
            errors.append("dashboard/README.md still contains '591'")
        else:
            print_success("dashboard/README.md: No references to '591'")

        if '254' in content:
            print_success("dashboard/README.md: Contains correct count '254'")

        if 'Azeem Azhar' in content or 'Ananya Srivastava' in content:
            errors.append("dashboard/README.md contains full names")
        else:
            print_success("dashboard/README.md: Uses first names only")

    # Check DASHBOARD_CONTENT.md
    content_file = BASE_PATH / "DASHBOARD_CONTENT.md"
    if content_file.exists():
        with open(content_file, 'r') as f:
            content = f.read()

        if '591' in content:
            errors.append("DASHBOARD_CONTENT.md still contains '591'")
        else:
            print_success("DASHBOARD_CONTENT.md: No references to '591'")

        if '254' in content:
            print_success("DASHBOARD_CONTENT.md: Contains correct count '254'")

        if 'Azeem Azhar' in content or 'Ananya Srivastava' in content:
            errors.append("DASHBOARD_CONTENT.md contains full names")
        else:
            print_success("DASHBOARD_CONTENT.md: Uses first names only")

    return errors

# ============================================================================
# MAIN VALIDATION
# ============================================================================

def main():
    print(f"\n{BLUE}╔════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║{' '*27}DASHBOARD CONSISTENCY VALIDATION{' '*27}║{RESET}")
    print(f"{BLUE}╚════════════════════════════════════════════════════════════════════════════╝{RESET}")

    all_errors = []
    all_warnings = []

    # 1. Validate dimensions.py
    errors, warnings = validate_dimensions_config()
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    # 2. Count actual URLs
    total_count, dim_counts = count_actual_verified_urls()
    if total_count != EXPECTED_TOTALS["total_verified_urls"]:
        all_errors.append(f"URL count mismatch: {total_count} vs expected {EXPECTED_TOTALS['total_verified_urls']}")

    # 3. Validate dashboard files
    errors = validate_dashboard_files()
    all_errors.extend(errors)

    # 4. Validate README files
    errors = validate_readme_files()
    all_errors.extend(errors)

    # ============================================================================
    # FINAL REPORT
    # ============================================================================

    print_header("VALIDATION SUMMARY")

    if not all_errors and not all_warnings:
        print(f"\n{GREEN}╔════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{GREEN}║{' '*20}✓ ALL VALIDATIONS PASSED - DASHBOARD IS CONSISTENT{' '*20}║{RESET}")
        print(f"{GREEN}╚════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
        print_success(f"Total Verified URLs: {EXPECTED_TOTALS['total_verified_urls']}")
        print_success(f"Total Data Entries: {EXPECTED_TOTALS['total_entries']}")
        print_success("Leadership names: First names only")
        print_success("All files updated consistently")
        return 0
    else:
        if all_errors:
            print(f"\n{RED}╔════════════════════════════════════════════════════════════════════════════╗{RESET}")
            print(f"{RED}║{' '*26}✗ VALIDATION ERRORS FOUND{' '*28}║{RESET}")
            print(f"{RED}╚════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
            for error in all_errors:
                print_error(error)

        if all_warnings:
            print(f"\n{YELLOW}Warnings:{RESET}")
            for warning in all_warnings:
                print_warning(warning)

        return 1

if __name__ == "__main__":
    sys.exit(main())
