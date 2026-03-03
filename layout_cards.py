import os
import glob
import math
from PIL import Image

def layout_cards_permutations():
    # Constants
    DPI = 300
    CANVAS_WIDTH_IN = 18
    MARGIN_IN = 0.25
    SPACING_IN = 0.125
    CARD_ASPECT_RATIO = 2.5 / 3.5  # Standard card ratio
    
    MAX_HEIGHT_IN = 24.0
    MAX_VACANT = 4

    # Pixel conversions
    width_px = int(CANVAS_WIDTH_IN * DPI)
    margin_px = int(MARGIN_IN * DPI)
    spacing_px = int(SPACING_IN * DPI)
    usable_w = width_px - 2 * margin_px

    # Folders
    input_folder = r'c:\Users\jonathan\Downloads\tcg\pokemon_base_set_1999'
    output_folder = r'c:\Users\jonathan\Downloads\tcg\sheets'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get card images
    card_paths = sorted(glob.glob(os.path.join(input_folder, '*.png')))
    num_cards = len(card_paths)
    
    if num_cards == 0:
        print("No card images found.")
        return

    print(f"Total cards found: {num_cards}")

    valid_permutations = []
    
    # Optimization Logic: Find all possible grids within constraints
    for cols in range(1, 100):
        rows = math.ceil(num_cards / cols)
        vacant = (cols * rows) - num_cards
        
        # Calculate resulting card dimensions to fill the width
        card_w_px = (usable_w - (cols - 1) * spacing_px) / cols
        if card_w_px <= 0:
            break
        card_h_px = card_w_px / CARD_ASPECT_RATIO
        
        # Calculate resulting total height
        total_h_px = 2 * margin_px + rows * card_h_px + (rows - 1) * spacing_px
        total_h_in = total_h_px / DPI
        
        # CONSTRAINTS check
        if vacant <= MAX_VACANT and total_h_in <= MAX_HEIGHT_IN:
            valid_permutations.append({
                'cols': cols,
                'rows': rows,
                'vacant': vacant,
                'card_w_px': int(card_w_px),
                'card_h_px': int(card_h_px),
                'total_h_px': int(total_h_px)
            })

    if not valid_permutations:
        print(f"No permutations found within {MAX_HEIGHT_IN}\" height and {MAX_VACANT} vacant slots.")
        return

    print(f"Found {len(valid_permutations)} valid permutations:")
    print(f"{'Grid':<10} | {'Vacant':<6} | {'Height (in)':<12} | {'Card Size (in)':<15}")
    print("-" * 55)
    
    for p in valid_permutations:
        h_in = p['total_h_px'] / DPI
        w_in = p['card_w_px'] / DPI
        ch_in = p['card_h_px'] / DPI
        print(f"{p['cols']}x{p['rows']:<5} | {p['vacant']:<6} | {h_in:<12.2f} | {w_in:.2f}x{ch_in:.2f}")

    # Generate images for each permutation
    for p in valid_permutations:
        cols = p['cols']
        rows = p['rows']
        card_w_px = p['card_w_px']
        card_h_px = p['card_h_px']
        total_h_px = p['total_h_px']
        
        print(f"Generating sheet: {cols}x{rows}...")
        
        sheet = Image.new('RGB', (width_px, total_h_px), 'white')
        
        for idx, path in enumerate(card_paths):
            if idx >= num_cards: break
            
            r = idx // cols
            c = idx % cols
            
            try:
                card_img = Image.open(path)
                card_resized = card_img.resize((card_w_px, card_h_px), Image.Resampling.LANCZOS)
                
                x = margin_px + c * (card_w_px + spacing_px)
                y = margin_px + r * (card_h_px + spacing_px)
                
                sheet.paste(card_resized, (x, y))
            except Exception as e:
                print(f"Error processing {path}: {e}")
        
        filename = f"sheet_{cols}x{rows}_{p['vacant']}vacant.png"
        output_path = os.path.join(output_folder, filename)
        sheet.save(output_path, dpi=(DPI, DPI))
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    layout_cards_permutations()
