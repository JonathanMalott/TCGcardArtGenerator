import os
import requests
from tcgdexsdk import TCGdex

# ---------------------- PROMPT ---------------------------
# --- vector line art, black lines on white background. ---
# ----------------------------------------------------------

# ==============================
# Configuration
# ==============================

LANG = "en"
SET_ID = "base1"
OUTPUT_DIR = "pokemon_base_set_1999"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# Initialize TCGdex Client
# ==============================

tcgdex = TCGdex(LANG)

# Fetch full set data (includes cards)
pokemon_set = tcgdex.set.getSync(SET_ID)

if not pokemon_set or not pokemon_set.cards:
    raise Exception("No cards found for set.")

total_downloaded = 0

# ==============================
# Download Images
# ==============================

for card_ref in pokemon_set.cards:
    # Fetch full card details
    card = tcgdex.card.getSync(card_ref.id)

    if not card.image:
        continue

    image_url = card.image + "/high.png"  # High resolution

    # Clean filename
    safe_name = "".join(
        c for c in card.name if c.isalnum() or c in (" ", "-", "_")
    ).rstrip()

    filename = f"{card.localId.zfill(3)}_{safe_name}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    print(f"Downloading {filename}...")

    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    total_downloaded += 1

print(f"\nDownload complete. Total cards saved: {total_downloaded}")