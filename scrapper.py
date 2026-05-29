from bs4.element import Tag
from pathlib import Path
import csv

def curiosity_extract(soup) -> dict:
    """Parser through the DIVS and collect the curiosities"""
    all_curiosities = {}

    for div in soup.select("div.mw-heading.mw-heading3"):
        h3 = div.find("h3")
        if not h3:
            continue

        h3_id = h3.get("id")
        h3_text = h3.text.strip()

        if not h3_id:
            continue

        pre_curiosity = div.next_siblings
        curiosity = []
        for children in pre_curiosity:
            if isinstance(children, Tag) and children.name == 'ul':
                for li in children.find_all('li'):
                    curiosity.append(li.get_text(strip=False))
                break

        all_curiosities[h3_text] = curiosity

    return all_curiosities

def scrap_input(curiosity: dict, data_path:str | Path, csv_name: str) -> None:
    """Create the .csv file with the content"""
    # Create the dir for scrappers.
    data_path = Path(data_path)
    Path(data_path).mkdir(exist_ok=True)

    # Treat the name
    csv_name = csv_name.strip() + '.csv'

    with open(data_path / Path(csv_name), 'w', newline='', encoding='utf8') as scrap:
        field_names = ['Month', 'Curiosities']
        writer = csv.DictWriter(scrap, fieldnames=field_names)
        writer.writeheader()
        for months in curiosity:
            for item in curiosity[months]:
                writer.writerow({'Month': months, 'Curiosities': item})