import argparse
import json
import os
import sys
import wave
import contextlib
import numpy as np
from faster_whisper import WhisperModel

def load_audio_16k(audio_path):
    with wave.open(audio_path, 'rb') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)

    if sampwidth == 2:
        audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    elif sampwidth == 4:
        audio = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0
    else:
        audio = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0

    if n_channels > 1:
        audio = audio.reshape(-1, n_channels).mean(axis=1)

    if framerate != 16000:
        target_len = int(len(audio) * 16000 / framerate)
        audio = np.interp(
            np.linspace(0, len(audio), target_len, endpoint=False),
            np.arange(len(audio)),
            audio
        ).astype(np.float32)

    return audio, len(audio) / 16000.0

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio with faster-whisper (Python)")
    parser.add_argument("--audio", required=True, help="Path to input audio file")
    parser.add_argument("--out", default="public/stickman/captions.whisper.json", help="Path to output captions JSON")
    parser.add_argument("--model", default="base", help="Whisper model size (base, small, medium)")
    parser.add_argument("--language", default="id", help="Audio language code (e.g. id)")
    parser.add_argument("--device", default="cpu", help="Device to use (cpu or cuda)")
    parser.add_argument("--compute_type", default="int8", help="Compute type (int8, float16, float32)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.audio):
        print(f"Error: Audio file '{args.audio}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Loading audio '{args.audio}'...")
    audio_data, duration_sec = load_audio_16k(args.audio)
    duration_ms = int(round(duration_sec * 1000))
    print(f"Audio loaded: {duration_sec:.2f}s ({duration_ms} ms)")

    print(f"Loading Whisper model '{args.model}' ({args.device}, {args.compute_type})...")
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    
    print(f"Transcribing (language: {args.language})...")
    segments, info = model.transcribe(
        audio_data,
        language=args.language,
        word_timestamps=True,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500)
    )
    
    captions = []
    for segment in segments:
        if segment.words:
            for word in segment.words:
                w_text = word.word.strip()
                if not w_text:
                    continue
                start_ms = int(round(word.start * 1000))
                end_ms = max(int(round(word.end * 1000)), start_ms + 50)
                mid_ms = int(round((start_ms + end_ms) / 2))
                prob = float(getattr(word, "probability", 1.0))
                
                captions.append({
                    "text": " " + w_text,
                    "startMs": start_ms,
                    "endMs": end_ms,
                    "timestampMs": mid_ms,
                    "confidence": prob
                })
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(captions, f, ensure_ascii=False, indent=2)
        
    print(f"Selesai: {len(captions)} kata token -> {args.out}")
    print(f"DURATION_MS={duration_ms}")

if __name__ == "__main__":
    main()
