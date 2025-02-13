import aiohttp
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("llm")

class LLMInterface:
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model_name: str = "deepseek-r1:1.5b",
        max_tokens: int = 200,
        temperature: float = 0.7
    ):
        """
        优化后的初始化方法，不再直接创建session
        """
        self.base_url = base_url
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature

    async def generate(self, prompt: str) -> str:
        """通过上下文管理器管理会话生命周期"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": self.temperature,
                            "max_tokens": self.max_tokens
                        }
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["response"].strip()
                    else:
                        error = await response.text()
                        logger.error(f"API请求失败: {error}")
                        return "请求失败，请检查模型服务"
                        
        except Exception as e:
            logger.error(f"生成异常: {str(e)}")
            return "服务不可用，请稍后重试"
