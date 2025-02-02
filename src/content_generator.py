from PIL import Image, ImageDraw, ImageFont
import os
import requests
from pathlib import Path
from typing import Optional
from .config import Config

class ContentGenerator:
    """Handles media generation including screenshots and text-to-speech."""
    
    def __init__(self, config: Optional[Config] = None):
        if config is None:
            config = Config()
            
        # content configuration
        self.base_image_path = config.content.base_image_path
        self.font_path = config.content.font_path
        self.font_size_username = config.content.font_size_username
        self.font_size_title = config.content.font_size_title
        self.username_position = config.content.username_position
        self.title_position = config.content.title_position
        
        # TTS configuration
        self.tts_config = config.tts
        self.chunk_size = config.tts.chunk_size

    def generate_screenshot(self, title: str, subreddit: str, output_path: str) -> bool:
        """
        Generates a screenshot of the post.
        Returns True if successful, False otherwise.
        """
        image = self._load_base_image()
        if not image:
            return False

        image = self._add_subreddit(image, subreddit)
        image = self._add_post_title(image, title)
        return self._save_image(image, output_path)

    def generate_audio(self, 
                      text: str, 
                      filename: str, 
                      output_dir: str,
                      model_id: Optional[str] = None,
                      voice: Optional[str] = None) -> bool:
        """
        Generates audio using ElevenLabs API.
        Returns True if successful, False otherwise.
        """
        model_id = model_id or self.tts_config.model_id
        voice = voice or self.tts_config.voice_id
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/stream"
        
        headers = {
            "Accept": "application/json",
            "xi-api-key": self.tts_config.api_token
        }
        
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": self.tts_config.voice_settings
        }

        try:
            response = requests.post(url, headers=headers, json=data, stream=True)
            if response.ok:
                output_file = os.path.join(output_dir, filename)
                with open(output_file, "wb") as f:
                    for chunk in response.iter_content(chunk_size=self.chunk_size):
                        f.write(chunk)
                print(f"Audio saved successfully in {output_file}")
                return True
            else:
                print(f"Error generating audio: {response.text}")
                return False
        except Exception as e:
            print(f"Exception while generating audio: {e}")
            return False

    def _load_base_image(self) -> Optional[Image.Image]:
        """Loads the base image where the post will be overlaid."""
        try:
            return Image.open(self.base_image_path)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def _load_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Tries to load the font with the specified size."""
        try:
            return ImageFont.truetype(str(self.font_path), size)
        except IOError:
            print("Font file not found, using default font.")
            return ImageFont.load_default()

    def _add_subreddit(self, image: Image.Image, subreddit: str) -> Image.Image:
        """Adds the subreddit to the image."""
        draw = ImageDraw.Draw(image)
        font = self._load_font(self.font_size_username)
        draw.text(self.username_position, subreddit, font=font, fill=(0, 0, 0))
        return image

    def _add_post_title(self, image: Image.Image, post_title: str) -> Image.Image:
        """Adds the post title to the image with text wrapping."""
        draw = ImageDraw.Draw(image)
        font = self._load_font(self.font_size_title)
        
        max_width = image.size[0] - 100
        lines = []
        words = post_title.split()
        
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = text_bbox[2] - text_bbox[0]
            
            if line_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
            
        line_height = (draw.textbbox((0, 0), "Hg", font=font)[3] - 
                      draw.textbbox((0, 0), "Hg", font=font)[1])
        
        for i, line in enumerate(lines):
            draw.text(
                (self.title_position[0], self.title_position[1] + i * line_height),
                line,
                font=font,
                fill=(0, 0, 0)
            )
            
        return image

    def _save_image(self, image: Image.Image, output_path: str) -> bool:
        """
        Saves the modified image to the specified path.
        Returns True if successful, False otherwise.
        """
        try:
            image.save(output_path)
            print(f"Image saved successfully at {output_path}")
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False