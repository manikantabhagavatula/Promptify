import os
import json
import re
import httpx
import random
import time
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image

app = FastAPI(title="Promptify API", version="1.0.0")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Node.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CaptionResponse(BaseModel):
    captions: list[str]
    hashtags: list[str]
    image_description: str | None = None

@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "Promptify API is running"}

async def describe_image(upload: UploadFile) -> str:
    """Placeholder image describer. Replace with a call to a vision model / CLIP / Replicate as you scale.
    For MVP this returns simple filename + dimensions when possible."""
    try:
        upload.file.seek(0)
        img = Image.open(upload.file)
        w, h = img.size
        return f"{upload.filename} ({w}×{h}) — photo"
    except Exception:
        return upload.filename or "uploaded media"


async def call_llm(system_prompt: str, user_prompt: str):
    """Simple OpenAI Chat Completions call (HTTP). Expects OPENAI_API_KEY in env."""
    api_key = os.getenv('OPENAI_API_KEY')
    model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY env var is required')

    # Add randomness to prevent caching and increase variability
    random_seed = int(time.time() * 1000) % 10000
    temperature = random.uniform(0.8, 1.2)  # Random temperature between 0.8-1.2

    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        'max_tokens': 200,
        'temperature': temperature,
        'seed': random_seed  # Add seed for more randomness
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post('https://api.openai.com/v1/chat/completions', 
                            headers={'Authorization': f'Bearer {api_key}'}, 
                            json=payload)
        r.raise_for_status()
        j = r.json()
        return j['choices'][0]['message']['content']


@app.post('/api/improve_caption', response_model=CaptionResponse)
async def improve_caption(sentence: str = Form(...), platform: str = Form('instagram'), tone: str = Form('default'), file: UploadFile | None = File(None)):
    image_desc = None
    if file:
        image_desc = await describe_image(file)

    # Add variety to system prompt to prevent caching
    creativity_boosters = [
        "Be creative and think outside the box.",
        "Focus on viral potential and engagement.",
        "Consider current trends and popular culture.",
        "Make it memorable and shareable.",
        "Think about what would make people stop scrolling."
    ]

    system_prompt = (
        f"You are a social media caption expert. Generate 3 engaging captions and 3 relevant hashtags for the given content.\n\n"
        f"{random.choice(creativity_boosters)}\n\n"
        "PLATFORM GUIDELINES:\n"
        "- Instagram: Visual storytelling, emojis, 1-2 sentences max\n"
        "- Twitter: Concise, trending topics, 1-2 sentences max\n"
        "- LinkedIn: Professional, value-driven, 2-3 sentences\n"
        "- TikTok: Trendy, conversational, 1-2 sentences\n"
        "- Facebook: Community-focused, 2-3 sentences\n\n"
        "TONE OPTIONS:\n"
        "- Professional: Formal, business-appropriate\n"
        "- Casual: Friendly, conversational\n"
        "- Funny: Humorous, witty\n"
        "- Inspirational: Motivational, uplifting\n"
        "- Trendy: Current, hip, viral-worthy\n\n"
        "OUTPUT FORMAT: Return ONLY valid JSON in this exact structure:\n"
        "{\"captions\": [\"caption1\", \"caption2\", \"caption3\"], \"hashtags\": [\"#tag1\", \"#tag2\", \"#tag3\"], \"image_description\": \"brief description\"}\n\n"
        "Keep captions under 150 characters. Make hashtags relevant and platform-appropriate."
    )

    # Add variety to prompt structure to prevent caching
    prompt_variations = [
        f"""CONTENT: "{sentence}"
PLATFORM: {platform}
TONE: {tone}
IMAGE: {image_desc or 'No image provided'}

Generate captions and hashtags now.""",

        f"""Create engaging social media content for this:
Content: "{sentence}"
Target Platform: {platform}
Desired Tone: {tone}
Image Context: {image_desc or 'No image provided'}

Please generate 3 captions and 3 hashtags.""",

        f"""Social Media Caption Request:
Post Description: "{sentence}"
Platform: {platform}
Tone: {tone}
Image: {image_desc or 'No image provided'}

Generate creative captions and relevant hashtags."""
    ]

    user_prompt = random.choice(prompt_variations)

    llm_output = await call_llm(system_prompt, user_prompt)

    # Try to parse JSON from LLM. Fall back to best-effort extraction.
    try:
        parsed = json.loads(llm_output)
    except Exception:
        m = re.search(r'\{.*\}', llm_output, re.S)
        if m:
            parsed = json.loads(m.group(0))
        else:
            parsed = {'captions': [llm_output.strip()[:400]], 'hashtags': [], 'image_description': image_desc}

    return {
        'captions': parsed.get('captions', []),
        'hashtags': parsed.get('hashtags', []),
        'image_description': parsed.get('image_description', image_desc)
    }