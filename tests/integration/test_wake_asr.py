# tests/integration/test_wake_asr.py
import pytest
from unittest.mock import patch, AsyncMock
from wake_words.wake_detector import WakeWordDetector

@pytest.mark.asyncio
async def test_detect_success():
    """测试成功检测唤醒词"""
    with patch("sounddevice.InputStream"), \
         patch("pvporcupine.Porcupine.process", return_value=1):
        
        detector = WakeWordDetector()
        async with detector:
            assert await detector.detect(timeout=1) is True

@pytest.mark.asyncio
async def test_detect_timeout():
    """测试超时未检测到"""
    with patch("sounddevice.InputStream"):
        detector = WakeWordDetector()
        async with detector:
            assert await detector.detect(timeout=0.1) is False
