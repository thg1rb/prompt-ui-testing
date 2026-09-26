#!/usr/bin/env python3
"""Add a redacted active-page URL above an unchanged browser screenshot.

Usage:
    printf '%s' '{"url":"http://localhost:3000/result"}' | \
      python compose_evidence.py --input raw.png --output evidence.png

The URL is read from stdin to avoid putting sensitive query values in process args.
Only metadata provided by the calling browser workflow is rendered; this script
does not navigate or infer a URL from an image.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from PIL import Image, ImageDraw, ImageFont


REDACTED = "[REDACTED]"
SECRET_PATH_LABELS = {
    "access_token", "auth", "authorization", "code", "key", "oauth",
    "password", "reset", "secret", "session", "token", "verify",
}
OPAQUE_SEGMENT = re.compile(r"(?:[A-Fa-f0-9]{16,}|[A-Za-z0-9_-]{24,}|[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)")


def redact_url(raw_url: str) -> str:
    """Keep the active origin and useful path while hiding likely secrets."""
    if any(ord(character) < 32 or ord(character) == 127 for character in raw_url):
        raise ValueError("Active page URL contains control characters")
    parsed = urlsplit(raw_url)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Expected an active http(s) page URL")

    # Rebuild netloc to remove any userinfo without echoing it in an error.
    host = parsed.hostname
    if ":" in host:  # IPv6
        host = f"[{host}]"
    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError("Invalid active page URL port") from exc
    netloc = f"{host}:{port}" if port is not None else host

    segments = parsed.path.split("/")
    previous_is_secret = False
    safe_segments: list[str] = []
    for segment in segments:
        decoded = unquote(segment)
        label = decoded.casefold().replace("-", "_")
        secret_value = previous_is_secret or "@" in decoded or bool(OPAQUE_SEGMENT.fullmatch(decoded))
        safe_segments.append(REDACTED if secret_value and segment else segment)
        previous_is_secret = label in SECRET_PATH_LABELS
    safe_path = "/".join(safe_segments)

    # Query values can contain secrets even when the key sounds harmless.
    query_parts: list[str] = []
    for part in parsed.query.split("&"):
        if not part:
            continue
        key = unquote(part.split("=", 1)[0])
        safe_key = REDACTED if "@" in key or OPAQUE_SEGMENT.fullmatch(key) else quote(key, safe="-._~")
        query_parts.append(f"{safe_key}={REDACTED}")
    safe_query = "&".join(query_parts)
    safe_fragment = REDACTED if parsed.fragment else ""
    return urlunsplit((parsed.scheme.lower(), netloc, safe_path, safe_query, safe_fragment))


def _font() -> ImageFont.ImageFont | ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype("DejaVuSans.ttf", 16)
    except OSError:
        return ImageFont.load_default(size=16)


def _wrap_text(draw: ImageDraw.ImageDraw, value: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    lines: list[str] = []
    remaining = value
    while remaining:
        if draw.textlength(remaining, font=font) <= width:
            lines.append(remaining)
            break
        low, high = 1, len(remaining)
        while low < high:
            middle = (low + high + 1) // 2
            if draw.textlength(remaining[:middle], font=font) <= width:
                low = middle
            else:
                high = middle - 1
        cut = max(low, 1)
        lines.append(remaining[:cut])
        remaining = remaining[cut:]
    return lines or [""]


def compose(raw_path: Path, output_path: Path, active_url: str) -> str:
    if raw_path.resolve() == output_path.resolve():
        raise ValueError("Raw and final screenshot paths must differ")
    displayed_url = redact_url(active_url)
    with Image.open(raw_path) as source:
        raw = source.copy()
    if raw.mode not in {"RGB", "RGBA"}:
        raw = raw.convert("RGBA")
    canvas_width = max(raw.width, 640)
    font = _font()
    scratch = Image.new("RGB", (canvas_width, 1))
    draw = ImageDraw.Draw(scratch)
    lines = _wrap_text(draw, f"URL: {displayed_url}", font, canvas_width - 32)
    line_height = max(22, int(font.getbbox("Ag")[3] - font.getbbox("Ag")[1]) + 6)
    strip_height = 16 + len(lines) * line_height + 16
    canvas = Image.new(raw.mode, (canvas_width, strip_height + raw.height), "#ffffff")
    canvas.paste(raw, (0, strip_height))
    painter = ImageDraw.Draw(canvas)
    painter.rectangle((0, 0, canvas_width, strip_height - 1), fill="#f1f5f9")
    painter.line((0, strip_height - 1, canvas_width, strip_height - 1), fill="#475569", width=1)
    for index, line in enumerate(lines):
        painter.text((16, 16 + index * line_height), line, font=font, fill="#0f172a")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG")
    return displayed_url


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Existing raw browser screenshot")
    parser.add_argument("--output", required=True, type=Path, help="Final URL-visible PNG")
    args = parser.parse_args()
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict) or not isinstance(payload.get("url"), str):
            raise ValueError("stdin JSON must contain a string 'url'")
        displayed_url = compose(args.input, args.output, payload["url"])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Evidence composition failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"output": str(args.output), "displayed_url": displayed_url}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
