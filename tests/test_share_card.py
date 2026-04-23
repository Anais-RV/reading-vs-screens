"""Tests para share_card.py (implementación Pillow).

Se verifica:
  - Tipo de retorno de render_* (PIL.Image.Image)
  - Tamaño de píxeles correcto para feed (1080×1080) y story (1080×1920)
  - Mensajes de error / validación de inputs
  - Exportación a bytes PNG (cabecera \x89PNG)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "dashboard"))

from PIL import Image

from components.share_card import (
    export_profile_share_card,
    export_share_card,
    render_profile_share_card,
    render_share_card,
)


# ── render_share_card ─────────────────────────────────────────────────────────

def test_render_returns_pil_image() -> None:
    img = render_share_card(20, 12, "share.streamlit.io/x")
    assert isinstance(img, Image.Image)


def test_render_feed_size() -> None:
    img = render_share_card(20, 12, "share.streamlit.io/x")
    assert img.size == (1080, 1080)


def test_render_story_size() -> None:
    from components.editorial import STORY
    img = render_share_card(20, 12, "share.streamlit.io/x", size=STORY)
    assert img.size == (1080, 1920)


def test_render_invalid_minutes_zero() -> None:
    with pytest.raises(ValueError, match="Los minutos deben ser positivos"):
        render_share_card(0, 10, "share.streamlit.io/x")


def test_render_invalid_minutes_negative() -> None:
    with pytest.raises(ValueError, match="Los minutos deben ser positivos"):
        render_share_card(-5, 10, "share.streamlit.io/x")


def test_render_large_books_value() -> None:
    """Sin excepción aunque el número de libros sea muy grande."""
    img = render_share_card(120, 120, "share.streamlit.io/x")
    assert isinstance(img, Image.Image)


# ── export_share_card ─────────────────────────────────────────────────────────

def test_export_returns_bytes() -> None:
    result = export_share_card(15, 10, "share.streamlit.io/x")
    assert isinstance(result, bytes)


def test_export_png_header() -> None:
    result = export_share_card(15, 10, "share.streamlit.io/x")
    # Los primeros 4 bytes de un PNG son \x89PNG
    assert result[:4] == b"\x89PNG"


def test_export_square_generates_1080x1080() -> None:
    result = export_share_card(15, 10, "share.streamlit.io/x", format="square")
    import io
    img = Image.open(io.BytesIO(result))
    assert img.size == (1080, 1080)


def test_export_story_generates_1080x1920() -> None:
    result = export_share_card(15, 10, "share.streamlit.io/x", format="story")
    import io
    img = Image.open(io.BytesIO(result))
    assert img.size == (1080, 1920)


def test_export_invalid_format() -> None:
    with pytest.raises(ValueError, match="Formato debe ser 'square' o 'story'"):
        export_share_card(10, 10, "share.streamlit.io/x", format="pdf")


def test_export_invalid_minutes() -> None:
    with pytest.raises(ValueError, match="Los minutos deben ser positivos"):
        export_share_card(0, 10, "share.streamlit.io/x")


# ── render_profile_share_card ─────────────────────────────────────────────────

def test_profile_render_returns_pil_image() -> None:
    img = render_profile_share_card(
        "Lector en transición",
        "Estás recuperando foco.",
        75,
        "share.streamlit.io/x",
    )
    assert isinstance(img, Image.Image)


def test_profile_render_feed_size() -> None:
    img = render_profile_share_card(
        "Lector en transición", "Mensaje.", 75, "share.streamlit.io/x"
    )
    assert img.size == (1080, 1080)


def test_profile_render_story_size() -> None:
    from components.editorial import STORY
    img = render_profile_share_card(
        "Lector en transición", "Mensaje.", 75, "share.streamlit.io/x", size=STORY
    )
    assert img.size == (1080, 1920)


def test_profile_render_invalid_minutes() -> None:
    with pytest.raises(ValueError, match="no pueden ser negativos"):
        render_profile_share_card("Perfil", "Mensaje", -1, "share.streamlit.io/x")


# ── export_profile_share_card ─────────────────────────────────────────────────

def test_profile_export_returns_bytes() -> None:
    result = export_profile_share_card("Perfil", "Mensaje", 60, "share.streamlit.io/x")
    assert isinstance(result, bytes)


def test_profile_export_png_header() -> None:
    result = export_profile_share_card("Perfil", "Mensaje", 60, "share.streamlit.io/x")
    assert result[:4] == b"\x89PNG"


def test_profile_export_story_size() -> None:
    result = export_profile_share_card(
        "Perfil", "Mensaje", 60, "share.streamlit.io/x", format="story"
    )
    import io
    img = Image.open(io.BytesIO(result))
    assert img.size == (1080, 1920)


def test_profile_export_invalid_format() -> None:
    with pytest.raises(ValueError, match="Formato debe ser 'square' o 'story'"):
        export_profile_share_card("Perfil", "Mensaje", 60, "share.streamlit.io/x", format="jpeg")
