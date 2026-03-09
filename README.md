# mcp-visgen

MCP server for AI vision generation (images, video) via Claude Code. Uses [litellm](https://github.com/BerriAI/litellm) for multi-provider support.

## Install

```bash
claude mcp add visgen \
  --transport stdio \
  -e GEMINI_API_KEY=your-api-key \
  -- uvx --from git+https://github.com/reymondzzzz/mcp-visgen mcp-visgen
```

Add `--scope user` to make it available across all projects.

Verify:

```bash
claude mcp list
```

## Tools

- **generate_image** — Generate an image from a text prompt. Accepts optional `style`, `size`, `model` override, `feedback` (for regeneration), and `reference_image` (file path to use as visual reference).
- **refine_image_prompt** — Craft a better prompt before generating
- **list_generated_images** — List previously generated images

Default model: `gemini/gemini-3.1-flash-image-preview` (Nano Banana 2). Override per-call via the `model` parameter on any generation tool.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes (for Gemini) | — | Google Gemini API key |
| `OUTPUT_DIR` | No | `./generated-images` | Where to save images |

### Other Providers

Pass a different `model` to the tool (e.g. `gpt-image-1`) and set the provider's API key:

```bash
# OpenAI
claude mcp add visgen \
  --transport stdio \
  -e OPENAI_API_KEY=sk-... \
  -- uvx --from git+https://github.com/reymondzzzz/mcp-visgen mcp-visgen
```

See [litellm providers](https://docs.litellm.ai/docs/providers) for all supported models.

## Development

```bash
uv venv --python 3.13 .venv
source .venv/bin/activate
uv pip install -e .
mcp-visgen
```
