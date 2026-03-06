# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

MCP server for AI image generation via Claude Code. Uses litellm as a library for multi-provider routing. Default provider: Google Gemini (Nano Banana 2). Distributed via `uvx` from GitHub.

## Development

```bash
uv venv --python 3.13 .venv
source .venv/bin/activate
uv pip install -e .
```

Run the server (waits for stdio, use Ctrl+C to stop):
```bash
GEMINI_API_KEY=... mcp-visgen
```

Test image generation directly:
```bash
GEMINI_API_KEY=... python -c "from mcp_visgen.server import generate_image; print(generate_image('a banana', working_directory='.'))"
```

## Architecture

All code is in `mcp_visgen/` package:

- **server.py** — FastMCP server instance, 4 tools (`generate_image`, `regenerate_image`, `refine_image_prompt`, `list_generated_images`), and `_generate()` which calls litellm and extracts the image data URL from the response.
- **prompts.py** — Prompt refinement: appends style descriptions and quality hints. Also builds regeneration prompts from original + feedback.
- **storage.py** — Saves base64 data URL images to disk, lists images in output directory.

The flow: tool receives prompt → `prompts.py` refines it → `_generate()` calls `litellm.completion()` with `modalities=["image", "text"]` → response image extracted as data URL → `storage.py` saves to disk → tool returns JSON with file path.

## Key Details

- litellm returns images either in `choice.images[0]["image_url"]["url"]` or directly in `choice.content` as a data URL string — `_generate()` handles both cases.
- Default model is `gemini/gemini-3.1-flash-image-preview` (Nano Banana 2). Override per-call via the `model` parameter on generation tools.
- Images save to `generated-images/` under the working directory (or `OUTPUT_DIR` env var).
