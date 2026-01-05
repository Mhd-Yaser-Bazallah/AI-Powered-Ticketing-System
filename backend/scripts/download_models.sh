#!/usr/bin/env bash
set -euo pipefail

if [ -z "${MODEL_URL:-}" ] || [ -z "${MODEL_DIR:-}" ]; then
  echo "MODEL_URL and MODEL_DIR must be set" >&2
  exit 1
fi

mkdir -p "$MODEL_DIR"

url_path="${MODEL_URL%%\?*}"
filename="$(basename "$url_path")"
if [ -z "$filename" ]; then
  echo "Could not determine filename from MODEL_URL" >&2
  exit 1
fi

output_path="$MODEL_DIR/$filename"

if command -v curl >/dev/null 2>&1; then
  curl -fL "$MODEL_URL" -o "$output_path"
elif command -v wget >/dev/null 2>&1; then
  wget -O "$output_path" "$MODEL_URL"
else
  echo "curl or wget is required to download models." >&2
  exit 1
fi

if [ ! -f "$output_path" ]; then
  echo "Download failed: $output_path not found" >&2
  exit 1
fi

echo "Downloaded model to $output_path"
