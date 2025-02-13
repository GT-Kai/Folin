# test_edge_tts.py 更新版
import edge_tts
import asyncio
import os

async def test_connection():
    try:
        # 设置代理（根据实际情况修改）
        os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
        os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
        
        communicate = edge_tts.Communicate(
            "测试连接", 
            "zh-CN-YunxiNeural",
            proxy="http://127.0.0.1:7890"  # 显式指定代理
        )
        await communicate.save("test_connection.mp3")
        print("连接成功！")
    except Exception as e:
        print(f"连接失败: {str(e)}")
    finally:
        # 清理代理设置
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)

asyncio.run(test_connection())
