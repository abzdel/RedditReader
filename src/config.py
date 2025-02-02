import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RedditConfig:
    client_id: str = os.environ.get("client_id")
    client_secret: str = os.environ.get("client_secret")
    user_agent: str = os.environ.get("user_agent")
    username: str = os.environ.get("reddit_user")
    password: str = os.environ.get("reddit_password")
    comment_limit: int = 5  # number of "more comments" to load
    include_nsfw: bool = False  # whether to include NSFW posts


@dataclass
class TTSConfig:
    api_token: str = os.environ.get("ELEVEN_LABS_API_TOKEN")
    model_id: str = "eleven_multilingual_v2"
    voice_id: str = "pqHfZKP75CvOlQylNhV4"
    chunk_size: int = 1024
    voice_settings: dict = None

    def __post_init__(self):
        if self.voice_settings is None:
            self.voice_settings = {
                "stability": 0.8,
                "similarity_boost": 0.8,
                "style": 0.3,
                "use_speaker_boost": True,
            }


@dataclass
class ContentConfig:
    base_image_path: Path = Path("assets/templates/reddit_template.png")
    font_path: Path = Path("assets/fonts/dejavu-sans-bold.ttf")
    font_size_username: int = 30
    font_size_title: int = 36
    username_position: tuple = (165, 35)
    title_position: tuple = (65, 150)


@dataclass
class ProcessingConfig:
    max_characters: int = 300
    num_comments: int = 3  # number of top comments to process
    batch_delay: float = 2.0  # delay between processing posts
    posts_buffer_factor: int = 2  # factor to multiply requested posts by to account for skips


class Config:
    def __init__(self, include_nsfw: bool = False):
        self.reddit = RedditConfig(include_nsfw=include_nsfw)
        self.tts = TTSConfig()
        self.content = ContentConfig()
        self.processing = ProcessingConfig()
        self.base_output_dir: Path = Path("outputs")