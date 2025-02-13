import asyncio
from src.core.asr import SpeechRecognizer
from src.core.llm import LLMInterface
from src.core.tts import VoiceSynthesizer
from wake_words.wake_detector import WakeWordDetector

class VoiceAssistant:
    def __init__(self):
        self.wake_detector = WakeWordDetector()
        self.asr_engine = SpeechRecognizer()
        self.llm_engine = LLMInterface()
        self.tts_engine = VoiceSynthesizer()
        self._running = False

    async def main_loop(self):
        """带中断检测的主循环"""
        self._running = True
        try:
            while self._running:
                await self._process_cycle()
        finally:
            await self.shutdown()

    async def _process_cycle(self):
        try:
            await self.wake_detector.detect()
            transcript = await self.asr_engine.recognize()
            response = await self.llm_engine.generate(transcript)
            await self.tts_engine.speak(response)
        except asyncio.CancelledError:
            self._running = False
            raise

    async def shutdown(self):
        """安全关闭所有组件"""
        shutdown_tasks = [
            self.llm_engine.close(),
            self.wake_detector.close(),
            self.tts_engine.close()
        ]
        await asyncio.gather(*shutdown_tasks, return_exceptions=True)
