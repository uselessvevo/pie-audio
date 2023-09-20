from pathlib import Path

folder = Path(r"pieapp/assets/themes/choco/icons/")
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
        file.rename(new_filename)
