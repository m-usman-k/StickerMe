# Image generation settings
DEFAULT_CONFIG = {
    "width": 1024,
    "height": 1024,
    "cfg_scale": 7,
    "steps": 30,
    "samples": 1,
    "model": "stable-diffusion-xl-1024-v1-0"
}

# Aspect ratio presets
ASPECT_RATIOS = {
    "square": (1024, 1024),
    "portrait": (832, 1216),
    "landscape": (1216, 832),
    "wide": (1344, 768),
    "tall": (768, 1344),
    "ultrawide": (1536, 640),
    "ultratall": (640, 1536)
}

# Quality presets
QUALITY_PRESETS = {
    "fast": {"steps": 20, "cfg_scale": 7},
    "standard": {"steps": 30, "cfg_scale": 7},
    "high": {"steps": 50, "cfg_scale": 8},
    "ultra": {"steps": 75, "cfg_scale": 8}
}

# Style presets
STYLE_PRESETS = {
    "photographic": "photographic, realistic, detailed, high quality",
    "artistic": "artistic, creative, stylized, vibrant",
    "cinematic": "cinematic, dramatic lighting, movie still, professional",
    "anime": "anime style, manga, cel shaded, colorful",
    "oil_painting": "oil painting, textured, artistic, traditional",
    "watercolor": "watercolor, soft, flowing, artistic",
    "digital_art": "digital art, clean, modern, professional",
    "sketch": "sketch, pencil drawing, monochrome, artistic"
}