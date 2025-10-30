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
    activity: Optional[str] = None
) -> Generator[Dict, None, None]:
    """Gửi request tới backend và đọc stream JSON."""
    api_url = build_url("/chat/stream")

    # Chỉ trả danh sách model
    if not message and not model_choice:
        return ["gpt-5-mini", "gpt-4-turbo", "gemini-1.5-pro"]

    session = st.session_state
    if "session_id" not in session:
        session.session_id = str(uuid.uuid4())
    conversation_id = session.get("current_chat_id") or session.session_id

    payload = {
        "message": message or "",
        "conversation_id": conversation_id,
        "model_choice": model_choice,
        "activity": activity,
    }

    log_ai_activity("🔁 Gửi request streaming tới backend", str(payload))

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
                    metadata = data.get("metadata", {})

                    if event == "message" and msg.get("type") == "AIMessageChunk":
                        chunk = msg["data"]
                        content_chunk = chunk.get("content", "")
                        model_name = metadata.get("ls_model_name")

                        if metadata:
                            log_ai_activity(
                                "📡 Nhận stream chunk",
                                f"Node {metadata.get('langgraph_node')}, Step {metadata.get('langgraph_step')}",
                                metadata=metadata,
                            )

                        yield {
                            "content_chunk": content_chunk,
                            "ls_model_name": model_name,
                            "metadata": metadata,
                        }

                    elif event in ("close", "end"):
                        break

                except json.JSONDecodeError:
                    log_ai_activity("⚠️ JSON decode lỗi", str(line))

        log_ai_activity("✅ Hoàn tất phản hồi", f"Session: {session.session_id}")

    except Exception as e:
        err = f"❌ Lỗi stream từ backend: {e}"
        log_ai_activity("Lỗi stream backend", err)
        yield {"content_chunk": err, "ls_model_name": None, "metadata": {}}
