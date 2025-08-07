#!/usr/bin/env python3
"""
StickerMe - Discord AI Image Generator Bot
A Discord bot that generates images using Stability AI's API through slash commands.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Fix for Python 3.13 compatibility with discord.py
try:
    import audioop
except ImportError:
    # Create a dummy audioop module for Python 3.13+
    import types
    audioop = types.ModuleType('audioop')
    # Add dummy functions that discord.py might need
    audioop.avg = lambda *args: 0
    audioop.maxpp = lambda *args: 0
    audioop.minmax = lambda *args: (0, 0)
    audioop.rms = lambda *args: 0
    sys.modules['audioop'] = audioop

import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import asyncio
import io
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables")
if not STABILITY_API_KEY:
    raise ValueError("STABILITY_API_KEY not found in environment variables")

# Create images directory if it doesn't exist
IMAGES_DIR = Path("images")
IMAGES_DIR.mkdir(exist_ok=True)

class DownloadView(discord.ui.View):
    def __init__(self, image_data: bytes, filename: str):
        super().__init__(timeout=None)
        self.image_data = image_data
        self.filename = filename

    @discord.ui.button(label="Download Image", style=discord.ButtonStyle.primary, emoji="⬇️")
    async def download_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle download button click"""
        try:
            # Create a file object from the stored image data
            image_file = discord.File(io.BytesIO(self.image_data), filename=self.filename)
            
            # Send the file as a direct download
            await interaction.response.send_message(
                "Here's your generated image:",
                file=image_file,
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Failed to download image: {str(e)}",
                ephemeral=True
            )

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

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

class ImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = f"https://api.stability.ai/v1/generation/{DEFAULT_CONFIG['model']}/text-to-image"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def generate_image(self, prompt: str, width: int = 1024, height: int = 1024, 
                           cfg_scale: int = 7, steps: int = 30, style: str = None) -> bytes:
        """Generate an image using Stability AI API"""
        
        # Apply style preset if specified
        if style and style in STYLE_PRESETS:
            prompt = f"{prompt}, {STYLE_PRESETS[style]}"
        
        payload = {
            "text_prompts": [
                {
                    "text": prompt,
                    "weight": 1
                }
            ],
            "cfg_scale": cfg_scale,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": steps,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                headers=self.headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if "artifacts" in data and len(data["artifacts"]) > 0:
                        image_data = data["artifacts"][0]["base64"]
                        return base64.b64decode(image_data)
                    else:
                        raise Exception("No image generated")
                else:
                    error_text = await response.text()
                    raise Exception(f"API request failed with status {response.status}: {error_text}")

    def save_image(self, image_data: bytes, prompt: str, user_id: str) -> str:
        """Save image to disk with prompt as filename"""
        # Clean prompt for filename
        safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_prompt = safe_prompt[:50]  # Limit length
        
        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename
        filename = f"{timestamp}_{user_id}_{safe_prompt}.png"
        filepath = IMAGES_DIR / filename
        
        # Save image
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return str(filepath)

# Initialize image generator
image_generator = ImageGenerator(STABILITY_API_KEY)

@bot.event
async def on_ready():
    """Called when the bot is ready"""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')
    
    # Set bot activity
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="AI image generation with /generate"
    )
    await bot.change_presence(activity=activity)
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="generate", description="Generate an AI image with advanced parameters")
@app_commands.describe(
    prompt="The image description/prompt",
    aspect_ratio="Aspect ratio preset",
    quality="Quality preset",
    style="Style preset",
    width="Custom width (512-1536)",
    height="Custom height (512-1536)",
    cfg_scale="CFG scale (1-20, higher = more prompt adherence)",
    steps="Number of steps (10-150, higher = better quality but slower)"
)
@app_commands.choices(
    aspect_ratio=[
        app_commands.Choice(name="Square (1024x1024)", value="square"),
        app_commands.Choice(name="Portrait (832x1216)", value="portrait"),
        app_commands.Choice(name="Landscape (1216x832)", value="landscape"),
        app_commands.Choice(name="Wide (1344x768)", value="wide"),
        app_commands.Choice(name="Tall (768x1344)", value="tall"),
        app_commands.Choice(name="Ultra Wide (1536x640)", value="ultrawide"),
        app_commands.Choice(name="Ultra Tall (640x1536)", value="ultratall"),
    ],
    quality=[
        app_commands.Choice(name="Fast (20 steps)", value="fast"),
        app_commands.Choice(name="Standard (30 steps)", value="standard"),
        app_commands.Choice(name="High (50 steps)", value="high"),
        app_commands.Choice(name="Ultra (75 steps)", value="ultra"),
    ],
    style=[
        app_commands.Choice(name="None", value="none"),
        app_commands.Choice(name="Photographic", value="photographic"),
        app_commands.Choice(name="Artistic", value="artistic"),
        app_commands.Choice(name="Cinematic", value="cinematic"),
        app_commands.Choice(name="Anime", value="anime"),
        app_commands.Choice(name="Oil Painting", value="oil_painting"),
        app_commands.Choice(name="Watercolor", value="watercolor"),
        app_commands.Choice(name="Digital Art", value="digital_art"),
        app_commands.Choice(name="Sketch", value="sketch"),
    ]
)
async def generate(
    interaction: discord.Interaction, 
    prompt: str,
    aspect_ratio: app_commands.Choice[str] = None,
    quality: app_commands.Choice[str] = None,
    style: app_commands.Choice[str] = None,
    width: int = None,
    height: int = None,
    cfg_scale: int = None,
    steps: int = None
):
    """Generate an AI image using Stability AI with advanced parameters"""
    
    if not prompt:
        await interaction.response.send_message("Please provide a prompt for image generation.", ephemeral=True)
        return

    # Defer the response since image generation might take time
    await interaction.response.defer()

    try:
        # Get aspect ratio value
        aspect_ratio_value = aspect_ratio.value if aspect_ratio else "square"
        
        # Validate aspect ratio
        if aspect_ratio_value not in ASPECT_RATIOS:
            await interaction.followup.send(f"❌ Invalid aspect ratio. Choose from: {', '.join(ASPECT_RATIOS.keys())}", ephemeral=True)
            return

        # Get dimensions
        if width and height:
            # Custom dimensions
            if not (512 <= width <= 1536 and 512 <= height <= 1536):
                await interaction.followup.send("❌ Width and height must be between 512 and 1536", ephemeral=True)
                return
            img_width, img_height = width, height
        else:
            # Use aspect ratio preset
            img_width, img_height = ASPECT_RATIOS[aspect_ratio_value]

        # Get quality value
        quality_value = quality.value if quality else "standard"
        
        # Get quality settings
        if quality_value not in QUALITY_PRESETS:
            await interaction.followup.send(f"❌ Invalid quality. Choose from: {', '.join(QUALITY_PRESETS.keys())}", ephemeral=True)
            return
        
        quality_settings = QUALITY_PRESETS[quality_value]
        final_cfg_scale = cfg_scale if cfg_scale is not None else quality_settings["cfg_scale"]
        final_steps = steps if steps is not None else quality_settings["steps"]

        # Get style value
        style_value = style.value if style and style.value != "none" else None

        # Validate custom parameters
        if final_cfg_scale and not (1 <= final_cfg_scale <= 20):
            await interaction.followup.send("❌ CFG scale must be between 1 and 20", ephemeral=True)
            return
        
        if final_steps and not (10 <= final_steps <= 150):
            await interaction.followup.send("❌ Steps must be between 10 and 150", ephemeral=True)
            return

        # Generate the image
        image_data = await image_generator.generate_image(
            prompt=prompt,
            width=img_width,
            height=img_height,
            cfg_scale=final_cfg_scale,
            steps=final_steps,
            style=style_value
        )
        
        # Save the image
        saved_path = image_generator.save_image(image_data, prompt, str(interaction.user.id))
        
        # Create a file object from the image data
        image_file = discord.File(io.BytesIO(image_data), filename="generated_image.png")
        
        # Create an embed to display the image
        embed = discord.Embed(
            title="AI Generated Image",
            description=f"**Prompt:** {prompt}",
            color=discord.Color.blue()
        )
        embed.set_image(url="attachment://generated_image.png")
        embed.set_footer(text=f"Generated by {interaction.user.display_name} | Powered by Stability AI")
        
        # Add fields with generation details
        embed.add_field(name="Dimensions", value=f"{img_width}x{img_height}", inline=True)
        embed.add_field(name="Quality", value=quality_value.title(), inline=True)
        embed.add_field(name="Style", value=style_value.title() if style_value else "None", inline=True)
        embed.add_field(name="CFG Scale", value=str(final_cfg_scale), inline=True)
        embed.add_field(name="Steps", value=str(final_steps), inline=True)
        
        # Create a descriptive filename for download
        safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_prompt = safe_prompt[:30]  # Limit length for filename
        download_filename = f"{safe_prompt}.png" if safe_prompt else "generated_image.png"
        
        # Create download view with the image data
        download_view = DownloadView(image_data, download_filename)
        
        # Send the image with download button
        await interaction.followup.send(embed=embed, file=image_file, view=download_view)
        
    except Exception as e:
        error_message = f"❌ Failed to generate image: {str(e)}"
        print(f"Error generating image: {e}")
        await interaction.followup.send(error_message, ephemeral=True)

@bot.tree.command(name="styles", description="Show available style presets")
async def styles(interaction: discord.Interaction):
    """Show available style presets"""
    embed = discord.Embed(
        title="Available Style Presets",
        description="Use these styles with the `/generate` command (select from dropdown)",
        color=discord.Color.green()
    )
    
    for style, description in STYLE_PRESETS.items():
        embed.add_field(
            name=style.replace('_', ' ').title(),
            value=description,
            inline=False
        )
    
    embed.add_field(
        name="Usage",
        value="When using `/generate`, you can select a style from the dropdown menu in the `style` parameter.",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="aspects", description="Show available aspect ratios")
async def aspects(interaction: discord.Interaction):
    """Show available aspect ratios"""
    embed = discord.Embed(
        title="Available Aspect Ratios",
        description="Use these aspect ratios with the `/generate` command (select from dropdown)",
        color=discord.Color.green()
    )
    
    for aspect, (width, height) in ASPECT_RATIOS.items():
        embed.add_field(
            name=aspect.title(),
            value=f"{width}x{height}",
            inline=True
        )
    
    embed.add_field(
        name="Usage",
        value="When using `/generate`, you can select an aspect ratio from the dropdown menu in the `aspect_ratio` parameter.",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="qualities", description="Show available quality presets")
async def qualities(interaction: discord.Interaction):
    """Show available quality presets"""
    embed = discord.Embed(
        title="Available Quality Presets",
        description="Use these quality settings with the `/generate` command (select from dropdown)",
        color=discord.Color.green()
    )
    
    for quality, settings in QUALITY_PRESETS.items():
        embed.add_field(
            name=quality.title(),
            value=f"Steps: {settings['steps']}, CFG: {settings['cfg_scale']}",
            inline=True
        )
    
    embed.add_field(
        name="Usage",
        value="When using `/generate`, you can select a quality preset from the dropdown menu in the `quality` parameter.",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

def main():
    """Main function to run the bot"""
    print("🤖 StickerMe Discord Bot")
    print("=" * 30)
    print("Starting Discord bot...")
    print("Make sure you have set up your .env file with DISCORD_TOKEN and STABILITY_API_KEY")
    print(f"Images will be saved to: {IMAGES_DIR}")
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main() 