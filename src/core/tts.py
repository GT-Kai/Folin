import edge_tts
import asyncio
from pydub import AudioSegment
from pydub.playback import play
import logging
from pathlib import Path
from typing import Optional
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tts")

def get_text_hash(text: str) -> str:
    """统一哈希生成函数 (必须与测试代码完全一致)"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

class VoiceSynthesizer:
    def __init__(
        self,
        voice: str = "zh-CN-YunxiNeural",
        rate: str = "+0%",
        volume: str = "+0%",
        cache_dir: str = "tts_cache",
        proxy: Optional[str] = None
    ):
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.proxy = proxy
        self._play = play  # 将播放函数作为实例属性

    async def speak(self, text: str, use_cache: bool = True):
        if not text:
            return

        try:
            cache_file = self.cache_dir / f"{get_text_hash(text)}.mp3"
            
            if use_cache and cache_file.exists():
                logger.debug("使用缓存音频")
                audio = AudioSegment.from_mp3(cache_file)
                # 直接调用播放函数，通过 Mock 实例属性来捕获
                await asyncio.get_running_loop().run_in_executor(
                    None, 
                    lambda: self._play(audio)
                )
                return

            communicate = edge_tts.Communicate(
                text,
                self.voice,
                rate=self.rate,
                volume=self.volume,
                proxy=self.proxy
            )
            
            temp_file = self.cache_dir / "temp.mp3"
            await communicate.save(str(temp_file))
            temp_file.rename(cache_file)

            audio = AudioSegment.from_mp3(cache_file)
            await asyncio.get_running_loop().run_in_executor(
                None, 
                lambda: self._play(audio)
            )
            
        except Exception as e:
            logger.error(f"语音合成失败: {str(e)}")
            await self._fallback_tts(text)

    async def _fallback_tts(self, text: str) -> None:
        """离线语音合成备用方案"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            logger.warning(f"离线TTS失败: {str(e)}")
