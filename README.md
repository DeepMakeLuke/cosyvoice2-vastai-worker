# CosyVoice2 Vast.ai Worker

PyWorker configuration for running CosyVoice2-0.5B on Vast.ai Serverless.

## Usage

Set this repo as `PYWORKER_REPO` in your Vast.ai template:

```bash
PYWORKER_REPO=https://github.com/DeepMakeLuke/cosyvoice2-vastai-worker
```

## API

### POST /generate

Generate TTS audio from text.

**Request:**
```json
{
  "text": "Hello, world!",
  "mode": "sft",
  "speaker": "english_female"
}
```

**Zero-shot voice cloning:**
```json
{
  "text": "Text to synthesize",
  "mode": "zero_shot",
  "prompt_audio_base64": "<base64-encoded-wav>",
  "prompt_text": "Transcription of the prompt audio"
}
```

**Response:**
```json
{
  "audio_base64": "<base64-encoded-wav>",
  "sample_rate": 22050,
  "duration": 1.5,
  "format": "wav"
}
```

### Available Speakers (SFT mode)

- `english_female`
- `english_male`
- `chinese_female`
- `chinese_male`
- `japanese_male`
- `cantonese_female`
- `korean_female`

## Docker Image

This worker is designed to work with: `dragontamer80085/cosyvoice2-serverless:v1`
