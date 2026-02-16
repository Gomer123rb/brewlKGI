import csv
import os

# Folder containing your TSV files
INPUT_FOLDER = "tsv"

# Output folder for PKGi files
OUTPUT_FOLDER = "outputtxt"

# Map filename keywords → PKGi type + output filename
CATEGORY_MAP = {
    "GAME":   (1, "pkgi_games.txt"),
    "GAMES":  (1, "pkgi_games.txt"),
    "DLC":    (2, "pkgi_dlcs.txt"),
    "THEME":  (3, "pkgi_themes.txt"),
    "AVATAR": (4, "pkgi_avatars.txt"),
    "DEMO":   (5, "pkgi_demos.txt"),
    "UPDATE": (6, "pkgi_updates.txt"),
    "EMULATOR": (7, "pkgi_emulators.txt"),
    "APP":    (8, "pkgi_apps.txt"),
    "TOOL":   (9, "pkgi_tools.txt"),
}

def convert_row(row, type_id):
    contentid = row.get("Content ID", "")
    name = row.get("Name", "")
    url = row.get("PKG direct link", "")
    rap = row.get("RAP", "")
    size = row.get("File Size", "0")
    checksum = row.get("SHA256", "")

    # PKGi format:
    # contentid,type,name,description,rap,url,size,checksum
    return f"{contentid},{type_id},{name},,{rap},{url},{size},{checksum}"

def process_tsv(file_path, type_id, output_file):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        with open(output_file, "a", encoding="utf-8") as out:
            for row in reader:
                line = convert_row(row, type_id)
                out.write(line + "\n")

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for filename in os.listdir(INPUT_FOLDER):
        if not filename.lower().endswith(".tsv"):
            continue

        file_upper = filename.upper()

        for key, (type_id, output_name) in CATEGORY_MAP.items():
            if key in file_upper:
                input_path = os.path.join(INPUT_FOLDER, filename)
                output_path = os.path.join(OUTPUT_FOLDER, output_name)

                print(f"Converting {filename} → {output_name}")
                process_tsv(input_path, type_id, output_path)

    print("\nAll done! PKGi files saved in:", OUTPUT_FOLDER)

if __name__ == "__main__":
    main()