import re
import argparse
from pathlib import Path
import textwrap as tw


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Full path to icons folder")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        raise FileExistsError(f"Folder doesn't exists: {args.path}")

    fields = []
    seen = []
    for file in path.iterdir():
        if file.stem in seen:
            continue
        file_name_list = re.split(r"[_-]+", file.stem)
        if file_name_list:
            file_name_list = list(map(str.capitalize, file_name_list))
            field_name = "".join(file_name_list)
            fields.append(f"\t{field_name} = \"icons/{file.name}\"")

        seen.append(file.stem)

    with open("models.py", "w", encoding="utf-8") as output:
        text = tw.dedent("""
        import dataclasses as dt
        
        
        @dt.dataclass(eq=False, frozen=True)
        class Icons:
        """)
        for field in fields:
            text += f"{field}\n"

        output.write(text)
