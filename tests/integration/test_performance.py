import pytest
import asyncio

@pytest.mark.performance
@pytest.mark.asyncio
async def test_concurrent_requests(mock_assistant):
    from concurrent.futures import ThreadPoolExecutor
    
    # 模拟并行请求
    async def simulate_user():
        mock_assistant.asr_engine.recognize.return_value = "测试问题"
        await mock_assistant.main_loop()
    
    # 创建10个并发用户
    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [asyncio.wrap_future(executor.submit(simulate_user)) for _ in range(10)]
        await asyncio.gather(*tasks)
    
    # 验证线程安全
    assert mock_assistant.tts_engine.speak.call_count == 10
