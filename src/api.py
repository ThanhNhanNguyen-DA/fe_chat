import json
import uuid
import requests
import streamlit as st
from typing import Generator, Dict, Optional
from dataclasses import dataclass
from src.config import build_url, get_stream_timeout
from src.chat_utils import log_ai_activity


@dataclass
class ChatRequest:
    message: str
    conversation_id: str
    model_choice: Optional[str] = None
    activity: Optional[str] = None


def get_ai_response_stream(
    message: Optional[str] = None,
    model_choice: Optional[str] = None,
    activity: Optional[str] = None,
) -> Generator[Dict, None, None]:
    """Gửi request tới backend và đọc stream JSON."""
    api_url = build_url("/chat/stream")

    if not message and not model_choice:
        return ["gpt-5-mini", "gpt-4-turbo", "gemini-1.5-pro"]

    session = st.session_state
    if "session_id" not in session:
        session.session_id = str(uuid.uuid4())

    payload = {
        "message": message or "",
        "conversation_id": session.get("current_chat_id") or session.session_id,
        "model_choice": model_choice,
        "activity": activity,
    }

    log_ai_activity("🔁 Gửi yêu cầu", str(payload))

    try:
        with requests.post(api_url, params=payload, stream=True, timeout=get_stream_timeout()) as res:
            res.raise_for_status()
            for line in res.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line.decode("utf-8"))
                    event = data.get("event")
                    msg = data.get("message", {})
                    meta = data.get("metadata", {})

                    if event == "message" and msg.get("type") == "AIMessageChunk":
                        chunk = msg["data"]
                        yield {
                            "content_chunk": chunk.get("content", ""),
                            "ls_model_name": meta.get("ls_model_name"),
                            "metadata": meta,
                        }
                        log_ai_activity(
                            "📡 Nhận chunk",
                            f"Node {meta.get('langgraph_node')}, Step {meta.get('langgraph_step')}",
                            meta,
                        )

                    elif event in ("close", "end"):
                        break

                except json.JSONDecodeError:
                    log_ai_activity("⚠️ JSON decode lỗi", str(line))

        log_ai_activity("✅ Hoàn tất phản hồi", f"Session: {session.session_id}")

    except Exception as e:
        err = f"❌ Lỗi stream backend: {e}"
        log_ai_activity("Lỗi stream backend", err)
        yield {"content_chunk": err, "ls_model_name": None, "metadata": {}}
