# tests/test_llm.py
import pytest
from src.core.llm import DeepSeekEngine

@pytest.mark.asyncio
async def test_ollama_integration():
    # 先确认Ollama服务已运行
    llm = DeepSeekEngine()
    response = await llm.generate("你好")
    assert len(response) > 0
    print(f"测试响应: {response}")