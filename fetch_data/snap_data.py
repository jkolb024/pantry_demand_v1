import re, requests, zipfile, io, os, pandas as pd

# Finds the latest USDA SNAP ZIP link from the main SNAP data page.
def get_latest_snap_zip_url():
    
    url = "https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap"
    response = requests.get(url)
    response.raise_for_status()

    # Make case-insensitive
    html = response.text.lower()

    # Look for any link that contains snap and ends in .zip
    possible_links = re.findall(r'href="([^"]+\.zip)"', html)

    for link in possible_links:
        if "snap" in link and "fy69" in link and "zip" in link:
            # Fix relative links (if missing https://)
            if not link.startswith("http"):
                link = "https://www.fns.usda.gov" + link
            return link
    # Raise an error if the link cannot be found
    raise ValueError("Could not find SNAP ZIP link on USDA page.")


def get_latest_snap_zip(out_dir = "data_downloads"):
    # Create the output directory if it doesn't already exist
    os.makedirs(out_dir, exist_ok=True)

    # Get the URL to the latest SNAP ZIP file
    zip_url = get_latest_snap_zip_url()
    
    # Send an HTTP GET request to download the ZIP from the latest URL
    response = requests.get(zip_url)

    # Raise an error if the request fails
    response.raise_for_status()

    # Open the ZIP file and extract all the contents into the output directory
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Use BytesIO to allow zipfile to work with contents
        z.extractall(out_dir)
