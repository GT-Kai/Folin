# wake_words/wake_detector.py
from pathlib import Path
import pvporcupine
import sounddevice as sd
import numpy as np
import asyncio
from typing import Optional

class WakeWordDetector:
    def __init__(self):
        # 获取项目根目录
        base_dir = Path(__file__).resolve().parent.parent
        
        # Porcupine 模型配置
        self.keyword_path = str(base_dir / "models/wake_words/hey_folin_en_windows_v3_0_0.ppn")
        self.model_path = str(base_dir / "models/wake_words/porcupine_params.pv")
        
        # 验证文件存在
        self._validate_files()
        
        # 初始化引擎
        self.handle = pvporcupine.create(
            access_key="+hTsE+FalD8GoLHpzTzKVYcs+lKYPhxkRFqNC+2Bt9sQG3ct4hmzXQ==",
            model_path=self.model_path,
            keyword_paths=[self.keyword_path],
            sensitivities=[0.5]
        )
        
        # 音频配置
        self.sample_rate = self.handle.sample_rate
        self.frame_length = self.handle.frame_length
        self._is_detecting = False

    def _validate_files(self):
        """验证必要文件存在"""
        required = {
            "唤醒词文件": self.keyword_path,
            "基础模型文件": self.model_path
        }
        for name, path in required.items():
            if not Path(path).exists():
                raise FileNotFoundError(f"{name}不存在: {path}")

    async def detect(self, timeout: Optional[float] = None):
        """
        异步检测唤醒词
        :param timeout: 超时时间（秒），None表示无限等待
        """
        self._is_detecting = True
        audio_queue = asyncio.Queue()
        
        def audio_callback(indata, frames, time, status):
            if self._is_detecting:
                audio_queue.put_nowait(indata.copy())

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                blocksize=self.frame_length,
                channels=1,
                dtype=np.int16,
                callback=audio_callback
            ):
                while self._is_detecting:
                    try:
                        # 异步获取音频数据
                        indata = await asyncio.wait_for(audio_queue.get(), timeout=timeout)
                        pcm = np.frombuffer(indata, dtype=np.int16)
                        
                        # 处理唤醒词检测
                        result = self.handle.process(pcm)
                        if result >= 0:
                            return True
                    except asyncio.TimeoutError:
                        break
        except Exception as e:
            raise RuntimeError(f"检测失败: {str(e)}")
        finally:
            self._is_detecting = False
        
        return False

    def close(self):
        """释放资源"""
        if hasattr(self, "handle") and self.handle:
            self.handle.delete()
            self.handle = None
        self._is_detecting = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.close()
