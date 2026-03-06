# mcp-banana-get Design

## Overview

Python MCP server for AI image generation via Claude Code. Uses litellm as a library for provider abstraction. Distributed via uvx from GitHub.

## Tools

1. **generate_image** — Generate image from prompt via litellm. Saves locally, returns path + base64 preview.
2. **refine_prompt** — Takes rough idea, returns optimized image generation prompt.
3. **regenerate_image** — Takes previous result + feedback, generates improved version.
4. **list_images** — List previously generated images in output directory.

## Stack

- Python 3.13
- mcp SDK (official Python MCP SDK)
- litellm (provider abstraction, library mode)
- Distribution: uvx from GitHub

## v1 Provider

Google Gemini only. Adding more providers = changing model string in litellm.

## Structure

```
src/mcp_banana_get/
├── __init__.py
├── server.py       # MCP server, tool definitions
├── prompts.py      # Prompt crafting/refinement
└── storage.py      # Save/list images, path management
```

## Config

Environment variables:
- GEMINI_API_KEY — required for v1
- IMAGE_MODEL — litellm model string (default: gemini/gemini-2.0-flash-exp)
- OUTPUT_DIR — where to save images (default: ./generated-images)

## Claude Code MCP Config

```json
{
  "mcpServers": {
    "banana-get": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/<user>/mcp-banana-get", "mcp-banana-get"],
      "env": {
        "GEMINI_API_KEY": "..."
      }
    }
  }
}
```

## Future (v2+)

- Video generation via litellm.video_generation()
- LoRA support
- Image editing (inpainting, upscale)
- More providers (OpenAI, Stability, FAL, self-hosted)
