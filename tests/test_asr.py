import pytest
import wave
import os
from unittest.mock import MagicMock
from src.core.asr import SpeechRecognizer

@pytest.mark.asyncio
async def test_asr():
    recognizer = SpeechRecognizer()

    # 模拟音频输入
    test_wav = os.path.join("tests", "data", "test_audio.wav")
    with wave.open(test_wav, "rb") as wf:
        audio_data = wf.readframes(wf.getnframes())

    # 使用 MagicMock 模拟 pyaudio 流
    mock_stream = MagicMock()
    mock_stream.read.return_value = audio_data
    recognizer.stream = mock_stream

    # 调用 listen 方法
    text = await recognizer.listen()

    # 断言
    assert "测试" in text, f"识别结果中未包含'测试'，实际结果为: {text}"