from pathlib import Path
import xml.etree.ElementTree as ET


def rename_material_icons(folder: Path) -> None:
    if not folder.exists():
        raise FileNotFoundError

    for file in folder.iterdir():
        if "FILL0" not in file.name:
            continue

        fn_split = file.name.split("_FILL0")
        new_filename = f"{fn_split[0].replace('_', '-')}.svg"
        new_fn_path = Path(folder / new_filename)

        if new_fn_path.exists():
            print(f"Removing duplicate {file.name}")
            file.unlink()

        else:
            print(f"Renaming {file.name} to {new_filename}")
            try:
                file.rename(folder / new_filename)
            except Exception:
                pass


def change_icons_color(folder: Path, color: str, *exclude) -> None:
    print(f"File color will be \"{color}\"\n===============================")

    for file in folder.iterdir():
        if file.name in exclude:
            print(f"Skip \"{file.name}\"")
            continue

        tree = ET.parse(str(file))
        root = tree.getroot()
        for child in root.iter():
            child.set("fill", color)

        ET.register_namespace("", "http://www.w3.org/2000/svg")
        print(f"Done with \"{file.name}\"")
        tree.write(file)


if __name__ == '__main__':
    # rename_material_icons(Path(r"../pieapp/assets/themes/dark theme/icons/"))
    change_icons_color(Path(r"../pieapp/assets/themes/dark theme/icons/"), "#cccccc", "app.svg")
