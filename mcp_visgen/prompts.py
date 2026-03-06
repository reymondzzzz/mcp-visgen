STYLE_DESCRIPTIONS = {
    "modern": "sleek, contemporary design with clean lines and vibrant colors",
    "minimal": "minimalist design with lots of white space and subtle colors",
    "professional": "professional corporate design with business-appropriate colors",
    "playful": "playful and colorful design with fun elements and bright colors",
    "dark": "dark mode interface with dark background and accent colors",
    "realistic": "photorealistic style with natural lighting and textures",
    "artistic": "artistic and creative style with bold visual choices",
    "flat": "flat design with solid colors, simple shapes, and no gradients",
}


SIZE_DESCRIPTIONS = {
    "square": "square 1:1 aspect ratio",
    "portrait": "vertical portrait 9:16 aspect ratio",
    "landscape": "wide landscape 16:9 aspect ratio",
    "wide": "ultra-wide 21:9 cinematic aspect ratio",
    "4k": "4K ultra high resolution",
    "hd": "1080p HD resolution",
}


def refine_prompt(idea: str, style: str | None = None, size: str | None = None) -> str:
    """Take a rough idea and return an optimized image generation prompt."""
    parts = [idea.strip()]

    if style and style in STYLE_DESCRIPTIONS:
        parts.append(f"Style: {STYLE_DESCRIPTIONS[style]}")

    if size and size in SIZE_DESCRIPTIONS:
        parts.append(f"Image format: {SIZE_DESCRIPTIONS[size]}.")

    parts.append("High quality, detailed, sharp rendering.")
    parts.append("No watermarks, no text artifacts, no blurriness.")

    return " ".join(parts)


def build_regeneration_prompt(original_prompt: str, feedback: str) -> str:
    """Build a new prompt based on original + user feedback."""
    return (
        f"Based on this original prompt: \"{original_prompt}\"\n"
        f"Apply this feedback: \"{feedback}\"\n"
        f"Generate an improved version addressing the feedback."
    )
