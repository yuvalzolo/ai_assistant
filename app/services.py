import os
from typing import Sequence, TypedDict

import google.generativeai as genai
from anyio import to_thread
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class ChatMessage(TypedDict):
    role: str     # "user" or "assistant"
    content: str

async def run_chat(system_prompt: str, history: Sequence[ChatMessage]) -> str:
    """Return Gemini reply given a system prompt + chat history."""

    def _call() -> str:
        # ➊   Pass the system prompt via system_instruction=
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=system_prompt,    # <- THIS is the right place
        )

        # ➋   Start an *empty* chat (no system role in history)
        chat = model.start_chat()

        # ➌   Re-send only user / assistant turns
        for msg in history:
            if msg["role"] != "system":
                chat.send_message(
                    {"role": msg["role"], "parts": [msg["content"]]}
                )

        return chat.last.text   # latest assistant reply

    return await to_thread.run_sync(_call)
