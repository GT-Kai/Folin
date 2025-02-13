from unittest.mock import AsyncMock
import pytest
import asyncio
from src.main import VoiceAssistant

@pytest.mark.integration
@pytest.mark.asyncio
async def test_end_to_end_flow():
    # 使用真实组件（需要提前配置测试模型）
    assistant = VoiceAssistant()
    
    # 覆盖唤醒词检测直接进入交互
    assistant.wake_detector.detect = AsyncMock()
    
    # 启动有限时间运行
    try:
        await asyncio.wait_for(assistant.main_loop(), timeout=10)
    except asyncio.TimeoutError:
        pass
    
    # 验证至少完成一次循环
    assert assistant.asr_engine.recognize.call_count >= 1
