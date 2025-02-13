# src/config.py
"""
性能优化配置
"""
import os

# 线程池配置
MAX_WORKERS = int(os.cpu_count() * 0.8)  # 80% CPU核心数

# ASR配置
ASR_CONFIG = {
    "sample_rate": 16000,
    "buffer_size": 4096,
    "hotword": "models/wake_words/activate.pmdl"  # 唤醒词模型
}

# TTS缓存策略
TTS_CACHE_POLICY = {
    "max_size": 100,  # 最大缓存文件数
    "ttl": 86400      # 缓存有效期(秒)
}

# 资源监控
RESOURCE_MONITOR = {
    "cpu_warning": 80,  # CPU使用率告警阈值
    "mem_warning": 70   # 内存使用率告警阈值
}

# src/config.py
LLM_CONFIG = {
    "base_url": "http://localhost:11434",  # Ollama 服务地址
    "model_name": "deepseek-r1:1.5b",      # 实际部署的模型名称
    "max_tokens": 200,
    "temperature": 0.7
}
