import os
import shutil
from pathlib import Path
import subprocess
import json


def main():
    with Path("./names.txt").open("r") as f:
        contents = f.readlines()
    contents = [line.strip() for line in contents]

    mainfile = contents[0]
    names = contents[1:]

    # Create directory for files
    d = Path("./files")
    if d.exists():
        shutil.rmtree(d)
    d.mkdir()
    os.chdir(d)

    # Separate into individual pdfs
    subprocess.run(["pdfseparate", f"../{mainfile}.pdf", f"{mainfile}_%d.pdf"])

    meta_data = []
    for i, name in enumerate(names):
        pdf = Path(".", f"{mainfile}_{i + 1}.pdf")
        assert pdf.exists(), f"No page {pdf.name} found"
        filename = name.replace(" ", "_").lower()
        
        # Convert to pdf
        subprocess.run(["pdf2svg", pdf.name, f"{filename}.svg"])

        # Add white background to svg
        with Path(f"{filename}.svg").open("r") as f:
            contents = f.readlines()
        contents.insert(2, "<rect x=\"0\" y=\"0\" width=\"1123.2pt\" height=\"1497.6pt\" style=\"fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;\"/>")
        with Path(f"{filename}.svg").open("w") as f:
            f.writelines(contents)

        # Convert to png
        subprocess.run(["rsvg-convert", "-f", "png", "-o", f"{filename}.png", f"{filename}.svg"])
        
        # Add metadata
        meta_data.append({
            "name": name,
            "filename": filename,
            "iconCode": "\ue98f",
            "categories": ["Gtd"]
        })

    with Path("templates.json").open("w") as f:
        json.dump({"templates": meta_data}, f, indent=2)


if __name__ == "__main__":
    main()