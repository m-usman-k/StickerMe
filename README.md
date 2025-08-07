# StickerMe - Discord AI Image Generator Bot

A feature-rich Discord bot that generates images using Stability AI's API through slash commands, inspired by Midjourney's imagine command.

## Features

- 🎨 Generate AI images using Stability AI's Stable Diffusion XL model
- ⚡ Fast and responsive Discord slash commands
- 🔒 Secure API key management using environment variables
- 📝 Rich embed responses with generated images
- 🛡️ Error handling and user-friendly messages
- 🐍 Python 3.13 compatibility included
- 🎯 Advanced parameters (aspect ratio, quality, style, custom dimensions)
- 💾 Automatic image storage with prompt-based naming
- 📐 Multiple aspect ratio presets
- 🎨 Style presets for different artistic styles
- ⚙️ Quality presets for different generation speeds/quality
- ⬇️ Download button for easy image downloads

## Prerequisites

- Python 3.8 or higher (including Python 3.13)
- Discord Bot Token
- Stability AI API Key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StickerMe
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root and add your API keys:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   STABILITY_API_KEY=your_stability_ai_api_key_here
   ```

## Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the bot token and add it to your `.env` file
5. Enable the following bot permissions:
   - Send Messages
   - Use Slash Commands
   - Attach Files
   - Embed Links
6. Invite the bot to your server using the OAuth2 URL generator

## Stability AI API Setup

1. Sign up for a Stability AI account at [platform.stability.ai](https://platform.stability.ai)
2. Generate an API key from your account dashboard
3. Add the API key to your `.env` file

## Usage

### Running the Bot

```bash
python main.py
```

### Commands

#### 🎨 `/generate` - Generate AI Images
The main command with advanced parameters like Midjourney's imagine command:

**Basic usage:**
```
/generate prompt:a beautiful sunset over mountains
```

**Advanced usage with all parameters:**
```
/generate prompt:a futuristic cityscape aspect_ratio:landscape quality:high style:cinematic
```

**Parameters:**
- `prompt` (required) - The image description/prompt
- `aspect_ratio` (optional) - Aspect ratio preset (dropdown selection):
  - `Square (1024x1024)` - Default
  - `Portrait (832x1216)` - Tall vertical
  - `Landscape (1216x832)` - Wide horizontal
  - `Wide (1344x768)` - Extra wide
  - `Tall (768x1344)` - Extra tall
  - `Ultra Wide (1536x640)` - Ultra wide
  - `Ultra Tall (640x1536)` - Ultra tall
- `quality` (optional) - Quality preset (dropdown selection):
  - `Fast (20 steps)` - Quick generation
  - `Standard (30 steps)` - Default
  - `High (50 steps)` - Better quality
  - `Ultra (75 steps)` - Highest quality
- `style` (optional) - Style preset (dropdown selection):
  - `None` - No style applied
  - `Photographic` - Realistic, detailed
  - `Artistic` - Creative, stylized
  - `Cinematic` - Dramatic lighting, movie-like
  - `Anime` - Anime/manga style
  - `Oil Painting` - Traditional oil painting
  - `Watercolor` - Soft, flowing watercolor
  - `Digital Art` - Clean, modern digital art
  - `Sketch` - Pencil drawing style
- `width` (optional) - Custom width (512-1536)
- `height` (optional) - Custom height (512-1536)
- `cfg_scale` (optional) - CFG scale (1-20, higher = more prompt adherence)
- `steps` (optional) - Number of steps (10-150, higher = better quality but slower)

#### 🎨 `/styles` - Show Available Styles
Displays all available style presets with descriptions.

#### 📐 `/aspects` - Show Aspect Ratios
Displays all available aspect ratio presets with dimensions.

#### ⚙️ `/qualities` - Show Quality Presets
Displays all available quality presets with their settings.

## Image Download

Every generated image includes a **Download Image** button that allows users to:
- Download the image directly from Discord
- Get a descriptive filename based on the prompt
- Access the image privately (ephemeral response)
- No need to right-click and save manually

## Examples

### Basic Image Generation
```
/generate prompt:a cute cat playing with yarn
```

### High-Quality Cinematic Style
```
/generate prompt:a dramatic sunset over a cyberpunk city quality:high style:cinematic aspect_ratio:landscape
```
*Note: Select "High (50 steps)" from quality dropdown, "Cinematic" from style dropdown, and "Landscape (1216x832)" from aspect_ratio dropdown*

### Custom Dimensions
```
/generate prompt:an oil painting of a medieval castle width:1200 height:800 style:oil_painting
```
*Note: Select "Oil Painting" from style dropdown, then enter custom width and height*

### Anime Style Portrait
```
/generate prompt:a beautiful anime character with flowing hair style:anime aspect_ratio:portrait quality:ultra
```
*Note: Select "Anime" from style dropdown, "Portrait (832x1216)" from aspect_ratio dropdown, and "Ultra (75 steps)" from quality dropdown*

## Image Storage

All generated images are automatically saved to the `generated_images/` directory with the following naming convention:
```
YYYYMMDD_HHMMSS_userid_prompt.png
```

Example: `20241201_143022_123456789_a beautiful sunset over mountains.png`

## Configuration

The bot uses the following configuration options (can be modified in `main.py`):

- **Default dimensions**: 1024x1024 (square)
- **Default quality**: Standard (30 steps, CFG 7)
- **Model**: Stable Diffusion XL 1024 v1.0
- **Image storage**: `generated_images/` directory

## Project Structure

```
StickerMe/
├── main.py                 # Main bot implementation
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
├── generated_images/       # Generated images storage
└── README.md              # This file
```

## Error Handling

The bot includes comprehensive error handling for:
- Missing API keys
- Invalid prompts
- API request failures
- Network issues
- Discord API errors
- Invalid parameters
- File system errors

## Security Best Practices

- ✅ API keys stored in environment variables
- ✅ `.env` file excluded from version control
- ✅ Error messages don't expose sensitive information
- ✅ Input validation for user prompts
- ✅ Safe filename generation for stored images

## Troubleshooting

### Common Issues

1. **"Missing required dependency" error**
   - Run: `pip install -r requirements.txt`

2. **"DISCORD_TOKEN not found" error**
   - Make sure you've created a `.env` file
   - Verify your Discord token is correct

3. **"STABILITY_API_KEY not found" error**
   - Make sure you've added your Stability AI API key to `.env`

4. **Bot not responding to commands**
   - Check that the bot has the necessary permissions
   - Verify the bot is online in your server

5. **Image generation fails**
   - Check your Stability AI API key
   - Verify you have sufficient credits
   - Check the console for detailed error messages

6. **Python 3.13 compatibility issues**
   - The bot includes automatic fixes for Python 3.13
   - If you encounter audioop-related errors, the bot will handle them automatically

7. **Invalid parameters error**
   - Use `/aspects`, `/styles`, or `/qualities` to see valid options
   - Check parameter ranges (width/height: 512-1536, CFG: 1-20, steps: 10-150)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues:
1. Check that all environment variables are set correctly
2. Ensure your Discord bot has the necessary permissions
3. Verify your Stability AI API key is valid
4. Check the console output for error messages
5. Use the help commands (`/styles`, `/aspects`, `/qualities`) to see valid options

## Changelog

### v2.0.0
- ✨ Advanced `/generate` command with multiple parameters
- 🎨 Style presets (photographic, artistic, cinematic, anime, etc.)
- 📐 Aspect ratio presets (square, portrait, landscape, wide, tall, etc.)
- ⚙️ Quality presets (fast, standard, high, ultra)
- 💾 Automatic image storage with prompt-based naming
- 🆕 Help commands (`/styles`, `/aspects`, `/qualities`)
- 🎯 Custom dimensions support
- 📊 Rich embed responses with generation details

### v1.0.0
- Initial release
- Basic image generation functionality
- Discord slash command integration
- Stability AI API integration
- Simplified single-file structure
- Python 3.13 compatibility fixes
