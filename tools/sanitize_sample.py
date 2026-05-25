"""
Generates sanitized sample output files for the examples/sample_output/ directory.
Replaces all business-specific names with generic placeholders.
Run once to generate public-safe examples for the repository.

Usage: python tools/sanitize_sample.py <input_dir> <output_dir>
"""

import json
import pathlib
import re
import sys


_REPLACEMENTS = [
    (r"Greenleaf", "Acme"),
    (r"greenleaf", "acme"),
    (r"Tyler", "User"),
    (r"tyler", "user"),
    (r"tlv1231-py", "your-org"),
]


def sanitize_text(text: str) -> str:
    for pattern, replacement in _REPLACEMENTS:
        text = re.sub(pattern, replacement, text)
    return text


def sanitize_json(data):
    if isinstance(data, dict):
        return {sanitize_text(k): sanitize_json(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_json(item) for item in data]
    if isinstance(data, str):
        return sanitize_text(data)
    return data


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python sanitize_sample.py <input_dir> <output_dir>")
        sys.exit(1)

    input_dir = pathlib.Path(sys.argv[1])
    output_dir = pathlib.Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    for file in input_dir.iterdir():
        if not file.is_file():
            continue

        if file.suffix == ".json":
            data = json.loads(file.read_text(encoding="utf-8"))
            sanitized = sanitize_json(data)
            # Truncate large arrays to keep sample size reasonable
            if isinstance(sanitized, dict):
                for key in sanitized:
                    if isinstance(sanitized[key], list) and len(sanitized[key]) > 10:
                        sanitized[key] = sanitized[key][:10]
            out_name = sanitize_text(file.name)
            output_dir.joinpath(out_name).write_text(
                json.dumps(sanitized, indent=2), encoding="utf-8"
            )
            print(f"Sanitized: {file.name} → {out_name}")

        elif file.suffix == ".md":
            text = sanitize_text(file.read_text(encoding="utf-8"))
            out_name = sanitize_text(file.name)
            output_dir.joinpath(out_name).write_text(text, encoding="utf-8")
            print(f"Sanitized: {file.name} → {out_name}")

    print(f"\nSample output written to: {output_dir}")


if __name__ == "__main__":
    main()
