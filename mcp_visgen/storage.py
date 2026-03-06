import base64
import os
import re
from datetime import datetime, timezone
from pathlib import Path


def get_output_dir(working_directory: str | None = None) -> Path:
    base = working_directory or os.getcwd()
    output = os.environ.get("OUTPUT_DIR") or os.path.join(base, "generated-images")
    return Path(output)


def save_image(
    data_url: str,
    filename: str | None = None,
    working_directory: str | None = None,
) -> Path:
    """Save a data URL image to disk. Returns the absolute path."""
    match = re.match(r"data:image/(\w+);base64,(.+)", data_url)
    if not match:
        raise ValueError("Invalid data URL format")

    fmt = match.group(1)
    b64 = match.group(2)

    output_dir = get_output_dir(working_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not filename:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        rand = os.urandom(3).hex()
        filename = f"visgen-{ts}-{rand}"

    filepath = output_dir / f"{filename}.{fmt}"
    filepath.write_bytes(base64.b64decode(b64))
    return filepath


def list_images(working_directory: str | None = None) -> list[dict]:
    """List all generated images in the output directory."""
    output_dir = get_output_dir(working_directory)
    if not output_dir.exists():
        return []

    results = []
    for f in sorted(output_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            stat = f.stat()
            results.append({
                "name": f.name,
                "path": str(f.absolute()),
                "size_kb": round(stat.st_size / 1024, 2),
                "created": datetime.fromtimestamp(stat.st_birthtime, tz=timezone.utc).isoformat(),
            })
    return results
