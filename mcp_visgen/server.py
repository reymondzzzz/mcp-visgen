import json
from pathlib import Path

import litellm
from mcp.server.fastmcp import FastMCP

from mcp_visgen.prompts import SIZE_DESCRIPTIONS, STYLE_DESCRIPTIONS, build_regeneration_prompt, refine_prompt
from mcp_visgen.storage import list_images, save_image

# Nano Banana 2 (latest), fallback options:
#   gemini/gemini-2.5-flash-image      — Nano Banana (500 free req/day)
#   gemini/gemini-3-pro-image-preview   — Nano Banana Pro (paid only via API)
#   gemini/gemini-3.1-flash-image-preview — Nano Banana 2 (newest, free tier)
DEFAULT_MODEL = "gemini/gemini-3.1-flash-image-preview"

mcp = FastMCP("visgen")


def _get_model() -> str:
    return DEFAULT_MODEL


def _generate(prompt: str, model: str | None = None) -> str:
    """Generate an image and return the data URL string."""
    response = litellm.completion(
        model=model or _get_model(),
        messages=[{"role": "user", "content": prompt}],
        modalities=["image", "text"],
    )
    choice = response.choices[0].message

    # litellm may return image in choice.images or embedded in choice.content
    if hasattr(choice, "images") and choice.images:
        return choice.images[0]["image_url"]["url"]

    content = choice.content or ""
    if content.startswith("data:image"):
        return content

    raise RuntimeError(
        f"No image in response. Model returned text: {content[:200]}"
    )


@mcp.tool()
def generate_image(
    prompt: str,
    style: str | None = None,
    size: str | None = None,
    model: str | None = None,
    filename: str | None = None,
    working_directory: str | None = None,
) -> str:
    """Generate an image from a text prompt.

    Args:
        prompt: Detailed description of the image to generate (be specific).
        style: Optional visual style. One of: modern, minimal, professional, playful, dark, realistic, artistic, flat.
        size: Optional image size/aspect ratio. One of: square, portrait, landscape, wide, 4k, hd.
        model: Optional litellm model string to override the default (e.g. "gemini/gemini-2.5-flash-image", "gpt-image-1").
        filename: Optional custom filename (without extension).
        working_directory: Directory where the image should be saved. Pass your project's working directory.
    """
    used_model = model or _get_model()
    refined = refine_prompt(prompt, style, size)
    data_url = _generate(refined, model=used_model)
    filepath = save_image(data_url, filename=filename, working_directory=working_directory)
    rel_path = _relative_path(filepath, working_directory)

    return json.dumps({
        "status": "ok",
        "file": rel_path,
        "absolute_path": str(filepath),
        "prompt_used": refined,
        "model": used_model,
        "usage": f"<img src=\"{rel_path}\" alt=\"{prompt[:60]}\">",
    })


@mcp.tool()
def regenerate_image(
    original_prompt: str,
    feedback: str,
    size: str | None = None,
    model: str | None = None,
    filename: str | None = None,
    working_directory: str | None = None,
) -> str:
    """Regenerate an image with feedback on what to change.

    Args:
        original_prompt: The prompt that was used for the previous generation.
        feedback: What to change (e.g. "make it darker", "remove the text", "add more contrast").
        size: Optional image size/aspect ratio. One of: square, portrait, landscape, wide, 4k, hd.
        model: Optional litellm model string to override the default.
        filename: Optional custom filename (without extension).
        working_directory: Directory where the image should be saved.
    """
    used_model = model or _get_model()
    new_prompt = build_regeneration_prompt(original_prompt, feedback)
    if size and size in SIZE_DESCRIPTIONS:
        new_prompt += f"\nImage format: {SIZE_DESCRIPTIONS[size]}."
    data_url = _generate(new_prompt, model=used_model)
    filepath = save_image(data_url, filename=filename, working_directory=working_directory)
    rel_path = _relative_path(filepath, working_directory)

    return json.dumps({
        "status": "ok",
        "file": rel_path,
        "absolute_path": str(filepath),
        "prompt_used": new_prompt,
        "model": used_model,
    })


@mcp.tool()
def refine_image_prompt(
    idea: str,
    style: str | None = None,
    size: str | None = None,
) -> str:
    """Take a rough idea and return an optimized image generation prompt.

    Use this before generate_image to craft a better prompt. Returns the refined prompt
    without generating an image.

    Args:
        idea: A rough description of what you want (e.g. "banana logo for my app").
        style: Optional visual style. One of: modern, minimal, professional, playful, dark, realistic, artistic, flat.
        size: Optional image size/aspect ratio. One of: square, portrait, landscape, wide, 4k, hd.
    """
    refined = refine_prompt(idea, style, size)
    return json.dumps({
        "refined_prompt": refined,
        "available_styles": list(STYLE_DESCRIPTIONS.keys()),
        "available_sizes": list(SIZE_DESCRIPTIONS.keys()),
    })


@mcp.tool()
def list_generated_images(
    working_directory: str | None = None,
) -> str:
    """List all previously generated images.

    Args:
        working_directory: Directory to look for generated images.
    """
    images = list_images(working_directory)
    return json.dumps({
        "count": len(images),
        "images": images,
    })


def _relative_path(filepath: Path, working_directory: str | None) -> str:
    base = Path(working_directory) if working_directory else Path.cwd()
    try:
        return str(filepath.relative_to(base))
    except ValueError:
        return str(filepath)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
