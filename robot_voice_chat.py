#!/usr/bin/env python3
"""
XIAO 语音机器人大脑 - Python版（Mac上跑）
完整链路：麦克风录音 → STT → AI → TTS → 喇叭播放
"""

import subprocess
import json
import base64
import time
import requests
import wave
import struct
import sys
import os
from gtts import gTTS

# ====== 配置 ======
API_KEY = "sk-slnwhmmuadvnvsmtohpfbtuoapkpfdyuncjjiychfwghewpn"
API_HOST = "https://api.siliconflow.cn/v1"
STT_MODEL = "FunAudioLLM/SenseVoiceSmall"  # SiliconFlow 语音识别
# TTS 用 gTTS（免费，无需API），备选硅基流动 IndexTTS

# 录音参数
CHANNELS = 1
SAMPLE_RATE = 16000
RECORD_SECONDS = 5

# 颜色输出
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'

def log(msg, color=""):
    prefix = {"green": "✅", "yellow": "⏳", "red": "❌", "cyan": "🔵"}.get(color, "ℹ️")
    print(f"{prefix} {msg}{RESET}")

def print_bot(text):
    print(f"\n{GREEN}🤖 AI: {text}{RESET}\n")

def print_listen():
    print(f"{YELLOW}🎤 正在听...{RESET}", end="", flush=True)

# ====== 录音 ======
def record_audio(filename="temp_recording.wav", seconds=5):
    """用ffmpeg录音"""
    log(f"开始录音 {seconds} 秒...", "yellow")
    cmd = [
        "ffmpeg", "-y", "-f", "avfoundation", "-i", ":0",
        "-ar", str(SAMPLE_RATE), "-ac", str(CHANNELS),
        "-t", str(seconds), "-loglevel", "quiet", filename
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and os.path.exists(filename):
            size = os.path.getsize(filename)
            log(f"录音完成！文件大小: {size} 字节", "green")
            return filename
        else:
            log(f"录音失败: {result.stderr}", "red")
            return None
    except FileNotFoundError:
        log("ffmpeg 未安装，请在Arduino IDE中使用ffmpeg命令", "red")
        return None
    except subprocess.TimeoutExpired:
        log("录音超时", "red")
        return None

# ====== STT（语音转文字）======
def speech_to_text(audio_path):
    """调用硅基流动 SenseVoiceSmall STT"""
    log("正在识别语音...", "yellow")
    
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    
    b64_audio = base64.b64encode(audio_data).decode()
    
    payload = {
        "model": STT_MODEL,
        "file": f"data:audio/wav;base64,{b64_audio}"
    }
    
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        resp = requests.post(
            f"{API_HOST}/audio/transcriptions",
            headers=headers,
            data=payload,
            timeout=30
        )
        if resp.status_code == 200:
            result = resp.json()
            text = result.get("text", "").strip()
            if text:
                log(f"识别结果: {text}", "green")
            else:
                log("未识别到文字内容", "red")
            return text
        else:
            log(f"STT错误: {resp.status_code} - {resp.text}", "red")
            return None
    except Exception as e:
        log(f"STT异常: {e}", "red")
        return None

# ====== AI 对话 ======
def chat_with_ai(user_text):
    """调用硅基流动 DeepSeek AI"""
    log(f"正在思考...", "yellow")
    
    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [
            {"role": "system", "content": "你是一个友好的AI机器人，名叫小白。你说话简洁有趣，像朋友聊天一样。你正在运行在一个树莓派控制的机械臂上，有一个机械身体，可以动动手臂做动作。你的回答要简短，适合语音播报，每句不超过20个字。"},
            {"role": "user", "content": user_text}
        ],
        "stream": False
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        resp = requests.post(
            f"{API_HOST}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        if resp.status_code == 200:
            result = resp.json()
            content = result["choices"][0]["message"]["content"]
            log(f"AI回复: {content}", "green")
            return content
        else:
            log(f"AI错误: {resp.status_code} - {resp.text}", "red")
            return "网络出错了，请稍后再试。"
    except Exception as e:
        log(f"AI异常: {e}", "red")
        return "出错了，请检查网络连接。"

# ====== TTS（文字转语音）======
def text_to_speech(text, output_path="response.mp3"):
    """使用 gTTS（免费）生成语音"""
    log("正在生成语音...", "yellow")
    try:
        tts = gTTS(text=text, lang="zh-cn", slow=False)
        tts.save(output_path)
        size = os.path.getsize(output_path)
        log(f"语音生成完成！({size} 字节)", "green")
        return output_path
    except Exception as e:
        log(f"TTS错误: {e}", "red")
        return None

# ====== 播放音频 ======
def play_audio(filepath):
    """用ffplay播放音频"""
    if not filepath or not os.path.exists(filepath):
        log(f"文件不存在: {filepath}", "red")
        return
    
    log("正在播放...", "yellow")
    cmd = ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", filepath]
    try:
        subprocess.run(cmd, timeout=30)
        log("播放完成", "green")
    except subprocess.TimeoutExpired:
        log("播放超时", "red")
    except FileNotFoundError:
        log("ffplay 未安装，尝试用 afplay", "yellow")
        try:
            subprocess.run(["afplay", filepath], timeout=30)
        except:
            log("播放失败，请手动播放", "red")

# ====== VAD（语音活动检测）======
def detect_voice():
    """简单VAD：持续监听直到检测到较大声音"""
    log("启动语音检测...", "yellow")
    log("（提示：此功能需要配置麦克风，输入 q 退出）", "cyan")
    
    try:
        cmd = [
            "ffmpeg", "-f", "avfoundation", "-i", ":0",
            "-ar", "16000", "-ac", "1", "-t", "10",
            "-loglevel", "quiet", "temp_vad.wav"
        ]
        log("正在监听 10 秒，说出你的问题...", "yellow")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and os.path.exists("temp_vad.wav"):
            size = os.path.getsize("temp_vad.wav")
            if size > 5000:  # 大于5KB说明有录音
                log("检测到语音！", "green")
                return "temp_vad.wav"
            else:
                log("未检测到语音，请重试", "red")
                return None
    except Exception as e:
        log(f"VAD异常: {e}", "red")
    return None

# ====== 完整对话流程 ======
def voice_conversation():
    print(f"\n{CYAN}{'='*50}")
    print("  🤖 XIAO 语音机器人大脑 - 语音对话模式")
    print(f"{'='*50}{RESET}\n")
    
    while True:
        print(f"\n{GREEN}▶ 按回车开始说话（输入 q 退出）{RESET}")
        user_input = input()
        if user_input.lower() == 'q':
            print("再见！下次见！👋")
            break
        
        # 方案A：VAD自动检测
        # audio_file = detect_voice()
        # if not audio_file:
        #     continue
        
        # 方案B：固定时长录音
        audio_file = record_audio("temp_voice.wav", RECORD_SECONDS)
        if not audio_file:
            continue
        
        # STT
        text = speech_to_text(audio_file)
        if not text:
            print_bot("我没听清楚，请再说一次！")
            continue
        
        print_bot(f"你说：{text}")
        
        # AI
        response = chat_with_ai(text)
        
        # TTS
        audio_out = text_to_speech(response, "ai_response.mp3")
        
        # 播放
        if audio_out:
            play_audio(audio_out)
        
        # 清理临时文件
        for f in ["temp_voice.wav", "temp_vad.wav"]:
            if os.path.exists(f):
                os.remove(f)

# ====== 测试模式 ======
def test_mode():
    print(f"\n{CYAN}{'='*50}")
    print("  🧪 XIAO 语音机器人 - 测试模式")
    print(f"{'='*50}{RESET}\n")
    
    # 测试录音
    print("1️⃣ 测试录音...")
    audio = record_audio("test_recording.wav", 3)
    if audio:
        play_audio(audio)
    
    # 测试STT
    if audio:
        print("\n2️⃣ 测试语音识别...")
        text = speech_to_text(audio)
    
    # 测试AI
    print("\n3️⃣ 测试AI对话...")
    response = chat_with_ai("你好！请用一句话介绍自己，要简短有趣！")
    
    # 测试TTS
    print("\n4️⃣ 测试语音合成...")
    tts_file = text_to_speech(response, "test_tts.mp3")
    if tts_file:
        play_audio(tts_file)
    
    print(f"\n{GREEN}{'='*50}")
    print("  测试完成！")
    print(f"{'='*50}{RESET}\n")

# ====== 主入口 ======
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_mode()
    else:
        voice_conversation()
