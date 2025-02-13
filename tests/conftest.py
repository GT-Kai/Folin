# tests/conftest.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.main import VoiceAssistant
import asyncio

@pytest.fixture(scope="session")
def event_loop_policy():
    """Windows 兼容性配置"""
    return asyncio.WindowsProactorEventLoopPolicy()

@pytest.fixture(scope="function")
async def assistant():
    """带资源清理的助手实例"""
    assistant = VoiceAssistant()
    yield assistant
    await assistant.shutdown()