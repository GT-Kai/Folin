import pytest
from unittest.mock import AsyncMock, MagicMock
import logging

@pytest.mark.asyncio
async def test_asr_failure_recovery(mock_assistant, caplog):
    """
    测试语音识别失败后的错误恢复流程
    """
    # 配置日志捕获级别
    caplog.set_level(logging.ERROR)
    
    # 模拟语音识别抛出异常
    mock_assistant.asr_engine.recognize.side_effect = Exception("ASR Error")
    
    # 限制主循环执行次数
    mock_assistant.wake_detector.detect.side_effect = [
        None,           # 第一次检测到唤醒词
        KeyboardInterrupt  # 强制退出循环
    ]
    
    try:
        await mock_assistant.main_loop()
    except KeyboardInterrupt:
        pass
    
    # 验证错误日志 (关键修复点)
    assert any(
        "语音合成失败: ASR Error" in record.message
        for record in caplog.records
    ), "未找到预期的错误日志"
    
    # 验证流程恢复
    assert mock_assistant.wake_detector.detect.call_count == 2, "未正确恢复监听"
