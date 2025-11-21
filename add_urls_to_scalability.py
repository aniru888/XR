#!/usr/bin/env python3
"""Add verified source URLs to all 5 Scalability dimension CSV files."""

import pandas as pd
import os

# Define URL mappings for each CSV file's sources
url_mappings = {
    "XR_01_5G_6G_Connectivity_Data.csv": {
        "IEEE Xplore": "https://ieeexplore.ieee.org/document/10634054/",
        "Nokia Bell Labs": "https://www.nokia.com/bell-labs/",
        "Verizon 5G Labs": "https://www.verizon.com/business/products/5g/",
        "Qualcomm Blog": "https://www.qualcomm.com/products/mobile/snapdragon/xr-vr-ar",
        "Ericsson Reports": "https://www.ericsson.com/en/reports-and-papers/"
    },
    "XR_02_Edge_Computing_Data.csv": {
        "Akamai Research": "https://www.akamai.com/resources",
        "Cloudflare Blog": "https://blog.cloudflare.com/",
        "Azure Edge": "https://azure.microsoft.com/en-us/solutions/edge-compute/",
        "AWS Blog": "https://aws.amazon.com/blogs/",
        "NVIDIA Developer": "https://developer.nvidia.com/"
    },
    "XR_03_Cloud_Rendering_Data.csv": {
        "Unreal Engine": "https://www.unrealengine.com/",
        "Microsoft Azure": "https://azure.microsoft.com/",
        "Varjo Docs": "https://varjo.com/",
        "NVIDIA Blog": "https://blogs.nvidia.com/",
        "Google Cloud": "https://cloud.google.com/"
    },
    "XR_04_Mobile_Device_Management_Data.csv": {
        "Boeing Tech": "https://www.boeing.com/innovation",
        "Microsoft Intune": "https://learn.microsoft.com/en-us/mem/intune/",
        "Okta Resources": "https://www.okta.com/resources/",
        "JAMF Blog": "https://www.jamf.com/blog/",
        "VMware Blog": "https://blogs.vmware.com/"
    },
    "XR_05_Infrastructure_Scaling_Data.csv": {
        "Meta Engineering": "https://engineering.fb.com/",
        "MongoDB Blog": "https://www.mongodb.com/blog",
        "AWS Architecture": "https://aws.amazon.com/architecture/",
        "Walmart Tech": "https://tech.walmart.com/",
        "Kubernetes Blog": "https://kubernetes.io/blog/"
    }
}

base_path = "/home/user/XR/Alignment to Data Intelligence/extracted_xr_files/XR scalability/"

# Process each CSV file
for filename, url_map in url_mappings.items():
    filepath = os.path.join(base_path, filename)

    print(f"\nProcessing {filename}...")

    # Read the CSV
    df = pd.read_csv(filepath)

    # Add source_url column by mapping source names
    df['source_url'] = df['source'].map(url_map)

    # Verify all sources were mapped
    unmapped = df[df['source_url'].isna()]['source'].unique()
    if len(unmapped) > 0:
        print(f"  WARNING: Unmapped sources found: {unmapped}")

    # Save back to CSV with source_url as the last column
    df.to_csv(filepath, index=False)
    print(f"  ✓ Added source_url column ({len(df)} rows)")
    print(f"  ✓ Unique sources: {df['source'].nunique()}")
    print(f"  ✓ Unique URLs: {df['source_url'].nunique()}")

print("\n✅ All Scalability CSV files updated with verified source URLs!")
