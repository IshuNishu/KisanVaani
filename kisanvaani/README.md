# 🌾 KisanVaani: Voice-first AI assistant for farmers

Hackfest 2026 (OSEN) submission. Farmers speak a question in Hindi or English and hear a spoken answer on crop disease, mandi prices and government schemes.

## Problem
Small farmers in Uttar Pradesh struggle to find timely, trustworthy information. Most apps are text-heavy and English-first, so farmers rely on middlemen and guesswork.

## Features
- Voice input (Hindi / English) and spoken replies
- Grounded advisories for wheat, rice, potato, mustard, sugarcane and tomato, each answer showing its source
- Mandi price tool (sample data for the demo)
- Scheme checker: PM-KISAN, PMFBY, KCC, Soil Health Card
- Safe fallback to Kisan Call Centre (1800-180-1551) / KVK when unsure
- Leaf photo upload that asks for the crop and symptoms
- ElevenLabs text-to-speech via a secure backend proxy, with automatic fallback to the browser voice

## Architecture
```
Browser (HTML/JS, Web Speech STT) -> FastAPI -> ElevenLabs TTS
         |
   Knowledge base retrieval + price tool + scheme checker
```

## Run locally
```bash
pip install -r requirements.txt
cp .env.example .env          # add your ElevenLabs key
export $(cat .env | xargs)    # Windows: set the variables manually
uvicorn backend.main:app --reload
```
Open http://localhost:8000 in Chrome.

## Deploy on Render
Push to GitHub, create a Render Blueprint from this repo (`render.yaml`), and set `ELEVENLABS_API_KEY`.

## Honest limitations
- Mandi prices are sample data; production would use the Agmarknet / data.gov.in API
- Retrieval is keyword matching over a small knowledge base; the roadmap is a vector DB with an LLM
- Leaf photos are not yet classified by a vision model

## Roadmap
Vector-DB RAG with an LLM, real mandi and weather APIs, image-based disease detection, WhatsApp voice notes, IVR for feature phones, more dialects.
