import asyncio
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig
from src.core.config import settings
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from pydub import AudioSegment

def get_audio_duration(file_path: str) -> float:
    if file_path.lower().endswith(".wav"):
        audio = WAVE(file_path)
    elif file_path.lower().endswith(".mp3"):
        audio = MP3(file_path)
    else:
        raise ValueError("Unsupported audio format")
    return round(audio.info.length, 2)

def pause_metrics(audio_path, min_silence_len=400, silence_thresh=-40):
    audio = AudioSegment.from_file(audio_path)
    pauses = []
    current_pause = 0
    for chunk in audio:
        if chunk.dBFS < silence_thresh:
            current_pause += 1
        else:
            if current_pause >= min_silence_len:
                pauses.append(current_pause / 1000)
            current_pause = 0
    return len(pauses) if pauses else 0

async def perform_pronunciation_assessment(audio_path: str, transcript: str):
    speech_config = SpeechConfig(
        subscription=settings.AZURE_SPEECH_KEY,
        region=settings.AZURE_SPEECH_REGION
    )

    pronunciation_config = speechsdk.PronunciationAssessmentConfig(
        reference_text=transcript,
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
        enable_miscue=True
    )

    audio_config = AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    pronunciation_config.apply_to(recognizer)
    result = await asyncio.to_thread(recognizer.recognize_once)
    return speechsdk.PronunciationAssessmentResult(result)

async def analyze_speech(audio_path: str, transcript: str):
    duration_task = asyncio.to_thread(get_audio_duration, audio_path)
    pauses_task = asyncio.to_thread(pause_metrics, audio_path)

    duration, pauses = await asyncio.gather(
        duration_task,
        pauses_task
    )

    if duration > 30:
        return None

    words = len(transcript.split())
    dur_minutes = duration / 60
    words_per_min = round(words / dur_minutes, 2)

    pauses_per_min = round(pauses / dur_minutes, 2)

    pronunciation_result = await perform_pronunciation_assessment(audio_path, transcript)

    return {
        "duration": duration,
        "words_per_min": words_per_min,
        "pauses_per_min": pauses_per_min,
        "pronunciation_score": pronunciation_result.pronunciation_score,
        "accuracy_score": pronunciation_result.accuracy_score,
        "fluency_score": pronunciation_result.fluency_score,
        "word_scores": [
            {
                "word": word.word,
                "accuracy_score": word.accuracy_score,
                "error_type": word.error_type
            }
            for word in pronunciation_result.words
        ]
    }
