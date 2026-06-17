"""
Pluggable AI Service — supports OpenAI (GPT-4) and Google Gemini.
Set AI_PROVIDER=openai or AI_PROVIDER=gemini in .env.
"""
from flask import current_app


class AIService:

    @staticmethod
    def _provider():
        return current_app.config.get('AI_PROVIDER', 'openai').lower()

    @classmethod
    def complete(cls, prompt: str, system: str = '', temperature: float = 0.3) -> str:
        """Single text completion. Returns the response string."""
        if cls._provider() == 'gemini':
            return cls._gemini_complete(prompt, system, temperature)
        return cls._openai_complete(prompt, system, temperature)

    @staticmethod
    def _openai_complete(prompt: str, system: str, temperature: float) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])
        messages = []
        if system:
            messages.append({'role': 'system', 'content': system})
        messages.append({'role': 'user', 'content': prompt})
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    @staticmethod
    def _gemini_complete(prompt: str, system: str, temperature: float) -> str:
        import google.generativeai as genai
        genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
        model = genai.GenerativeModel('gemini-1.5-pro')
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        response = model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(temperature=temperature),
        )
        return response.text.strip()

    @classmethod
    def complete_json(cls, prompt: str, system: str = '') -> dict:
        """Request JSON output and parse it."""
        import json
        raw = cls.complete(prompt, system=system + '\nRespond ONLY with valid JSON.')
        # Strip markdown code fences if present
        raw = raw.replace('```json', '').replace('```', '').strip()
        return json.loads(raw)
