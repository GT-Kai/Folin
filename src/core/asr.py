import json
from vosk import Model, KaldiRecognizer
import pyaudio
import logging
import asyncio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("asr")

class SpeechRecognizer:
    def __init__(self, model_path="models/vosk/vosk-model-cn-0.22"):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.pa = pyaudio.PyAudio()
        
        # 打印可用音频设备
        for i in range(self.pa.get_device_count()):
            dev = self.pa.get_device_info_by_index(i)
            logger.debug(f"Device {i}: {dev['name']} (Input channels: {dev['maxInputChannels']})")
        
        # 打开默认设备
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4096,
            input_device_index=None  # 默认设备
        )
    
    async def listen(self, timeout=5):
        """异步语音识别，支持超时"""
        logger.debug("开始接收音频输入")
        try:
            while True:
                data = self.stream.read(2048, exception_on_overflow=False)
                logger.debug(f"收到 {len(data)} 字节音频数据")
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    logger.info(f"识别结果: {result['text']}")
                    return result["text"]
        except asyncio.TimeoutError:
            logger.warning("语音识别超时")
            return ""