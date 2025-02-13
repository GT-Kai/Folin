import pytest

@pytest.mark.asyncio
async def test_full_interaction(mock_assistant):
    # 配置 Mock 返回值
    mock_assistant.asr_engine.recognize.return_value = "现在几点钟"
    mock_assistant.llm_engine.generate.return_value = "当前时间是上午10点"
    
    # 执行单次交互
    await mock_assistant.main_loop()
    
    # 验证调用顺序
    mock_assistant.asr_engine.recognize.assert_awaited_once()
    mock_assistant.llm_engine.generate.assert_awaited_with("现在几点钟")
    mock_assistant.tts_engine.speak.assert_awaited_with("当前时间是上午10点")
