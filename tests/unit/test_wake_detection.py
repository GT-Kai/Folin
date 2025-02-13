import pytest
from src.main import VoiceAssistant

@pytest.mark.asyncio
async def test_wake_word_detection(mock_assistant):
    # 模拟唤醒词检测成功
    mock_assistant.wake_detector.detect.side_effect = [None, KeyboardInterrupt]
    
    try:
        await mock_assistant.main_loop()
    except KeyboardInterrupt:
        pass
    
    # 验证检测方法被调用
    mock_assistant.wake_detector.detect.assert_awaited()
