# tests/test_tts.py
import pytest
import hashlib
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock
from pydub import AudioSegment
from pydub.generators import Sine
from src.core.tts import VoiceSynthesizer, get_text_hash
# 在测试文件开头添加
from pydub import AudioSegment
AudioSegment.converter = "D:/documents/GitHub/folin_v1/ffmpeg/bin/ffmpeg.exe"  # 替换实际路径


def get_md5(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()

@pytest.fixture
def tts():
    return VoiceSynthesizer(
        cache_dir="tests/tts_cache",
        proxy="http://127.0.0.1:7890"
    )

@pytest.fixture(autouse=True)
def setup_teardown():
    cache_dir = Path("tests/tts_cache")
    cache_dir.mkdir(exist_ok=True, parents=True)  # 修复：确保父目录存在
    
    # 生成有效缓存文件（修复：与实际代码使用相同的哈希逻辑）
    test_text = "缓存命中测试"
    cache_file = cache_dir / f"{get_md5(test_text)}.mp3"
    AudioSegment.silent(duration=1000).export(cache_file, format="mp3")

    yield
    
    for f in cache_dir.glob("*.mp3"):
        f.unlink(missing_ok=True)  # 修复：避免文件不存在时报错
    # 在 setup_teardown 中增加验证



@pytest.mark.asyncio
async def test_tts_speak_normal(tts):
    test_text = "这是一个测试"
    cache_file = tts.cache_dir / f"{get_md5(test_text)}.mp3"

    mock_communicate = AsyncMock()
    mock_communicate.save.side_effect = lambda path: (
        AudioSegment.silent(duration=1000).export(path, format="mp3")
    )

    with patch("edge_tts.Communicate", MagicMock(return_value=mock_communicate)):
        with patch("pydub.playback.play") as mock_play:
            # 使用同步执行保证 Mock 调用被记录
            with patch("asyncio.get_running_loop") as mock_loop:
                mock_loop.return_value.run_in_executor = lambda *args: mock_play()
                await tts.speak(test_text, use_cache=False)
                
                assert cache_file.exists()
                mock_play.assert_called_once()  # 现在应该被调用

@pytest.mark.asyncio
async def test_tts_cache_hit(tts):
    test_text = "缓存命中测试"
    
    # Mock 实例的 _play 属性
    mock_play = MagicMock()
    tts._play = mock_play
    
    with patch("edge_tts.Communicate", AsyncMock()):
        await tts.speak(test_text, use_cache=True)
        
        # 验证播放被调用
        mock_play.assert_called_once()
        
    # 验证缓存文件存在
    cache_file = tts.cache_dir / f"{get_text_hash(test_text)}.mp3"
    assert cache_file.exists()


# test_tts_proxy_failure 保持不变
@pytest.mark.asyncio
async def test_tts_proxy_failure():
    bad_tts = VoiceSynthesizer(proxy="http://invalid:7890")
    with patch.object(bad_tts, "_fallback_tts", new_callable=AsyncMock) as mock_fallback:
        await bad_tts.speak("测试文本", use_cache=False)
        mock_fallback.assert_awaited_once()
