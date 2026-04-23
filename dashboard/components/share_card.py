"""Share cards estilo Wrapped para @anaisentrelineas.

Dos cards principales generadas con Pillow:
  - share_card        → "Tus libros recuperables" (calculadora)
  - profile_share_card → "Tu perfil lector" (quiz)

Ambas usan editorial.py para paleta, tipografía e ilustraciones.
La misma firma pública se mantiene para que 02_tiempo.py no cambie
excepto en el método de visualización (st.image en lugar de st.plotly_chart).
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

# Permite importar desde tests (raíz) y desde Streamlit (pages/)
sys.path.insert(0, str(Path(__file__).parent))

from editorial import (
    AMBER,
    CORAL,
    INK,
    INK_SOFT,
    PAPER,
    PURPLE,
    RULE,
    TEAL,
    FEED,
    STORY,
    CardSize,
    canvas,
    draw_centered,
    draw_header,
    draw_mini_book,
    draw_mini_bookmark,
    draw_mini_cup,
    draw_remite,
    editorial_border,
    font_sans,
    font_sans_bold,
    font_serif,
    font_serif_bold,
    font_serif_italic,
    paper_texture,
    text_size,
    to_png_bytes,
    wrap_centered,
)

HANDLE = "@anaisentrelineas"
_DASHBOARD_URL_CLEAN = "reading-vs-screens.streamlit.app"


# ── Helpers internos ──────────────────────────────────────────────────────────

def _message_for_books(books_per_year: float) -> str:
    """Devuelve un mensaje personalizado según el rango de libros al año."""
    books = int(books_per_year)
    if books <= 6:
        return "Cada página cuenta. Lo importante es ganar continuidad."
    if books <= 12:
        return "Un libro al mes ya cambia tu relación con el tiempo."
    if books <= 24:
        return "Hábito lector sólido. Constancia antes que intensidad."
    if books <= 50:
        return "Lectura muy frecuente. Ese tiempo acumulado se nota."
    return "Un ritmo extraordinario para todo un año lector."


def _clean_url(url: str) -> str:
    return url.replace("https://", "").replace("http://", "").rstrip("/")


# ── Card 1: Tus libros recuperables ──────────────────────────────────────────

def render_share_card(
    minutes_saved: int,
    books_per_year: float,
    dashboard_url: str,
    size: CardSize = FEED,
) -> Image.Image:
    """Genera la share card 'Tus libros recuperables' como imagen Pillow.

    Args:
        minutes_saved:   Minutos diarios de pantalla reducidos.
        books_per_year:  Libros estimados que se leerían en un año.
        dashboard_url:   URL a mostrar en el pie de la tarjeta.
        size:            CardSize.FEED (1080×1080) o CardSize.STORY (1080×1920).

    Returns:
        PIL.Image.Image lista para st.image() / to_png_bytes().

    Raises:
        ValueError: Si los minutos son menores o iguales a cero.
    """
    if minutes_saved <= 0:
        raise ValueError("Los minutos deben ser positivos")

    books = int(books_per_year)
    message = _message_for_books(books_per_year)

    img = canvas(size)
    img = paper_texture(img)
    draw = ImageDraw.Draw(img)
    w, h = size.width, size.height

    # Borde editorial doble
    editorial_border(draw, size)

    # Cabecera con kicker
    header_bottom = draw_header(
        img,
        "Tu año en páginas",
        "¿Cuántos libros podrías leer?",
        kicker_color=TEAL,
    )

    # Cifra central — grande si cabe
    num_size = 210 if books < 100 else 160 if books < 1000 else 120
    big_font = font_serif_bold(num_size)
    center_y = h // 2 - 20
    draw_centered(draw, (w // 2, center_y), str(books), big_font, fill=TEAL)

    # Subtítulo debajo del número
    sub_font = font_serif(48)
    sub_y = center_y + num_size // 2 + 40
    draw_centered(draw, (w // 2, sub_y), "libros este año", sub_font, fill=INK)

    # Línea separadora
    sep_y = sub_y + 50
    draw.line([(w // 2 - 180, sep_y), (w // 2 + 180, sep_y)], fill=RULE, width=2)

    # Mensaje personalizado en cursiva
    msg_font = font_serif_italic(30)
    msg_y = sep_y + 60
    wrap_centered(
        draw,
        (w // 2, msg_y),
        f"\u201c{message}\u201d",
        msg_font,
        max_width=w - 260,
        fill=INK_SOFT,
    )

    # Contexto: tiempo ahorrado
    ctx_font = font_sans(26)
    ctx_y = msg_y + 90
    wrap_centered(
        draw,
        (w // 2, ctx_y),
        f"Si recupero {minutes_saved}\u2009min/día de scroll",
        ctx_font,
        max_width=w - 280,
        fill=INK_SOFT,
    )

    # Ilustración libro en zona neutra (derecha, entre cabecera y número)
    draw_mini_book(img, (w - 240, center_y - num_size // 2 - 160), width=130)

    # Remite final
    draw_remite(img, HANDLE, _clean_url(dashboard_url), qr_size=130)

    return img


def export_share_card(
    minutes_saved: int,
    books_per_year: float,
    dashboard_url: str,
    format: str = "square",
) -> bytes:
    """Exporta la share card en PNG listo para st.download_button.

    Args:
        minutes_saved:  Minutos diarios reducidos.
        books_per_year: Libros estimados por año.
        dashboard_url:  URL del dashboard.
        format:         "square" (1080×1080) o "story" (1080×1920).

    Returns:
        Bytes PNG.

    Raises:
        ValueError: Si los minutos no son positivos o el formato no es válido.
    """
    if minutes_saved <= 0:
        raise ValueError("Los minutos deben ser positivos")
    if format not in {"square", "story"}:
        raise ValueError("Formato debe ser 'square' o 'story'")

    size = FEED if format == "square" else STORY
    img = render_share_card(minutes_saved, books_per_year, dashboard_url, size)
    return to_png_bytes(img)


# ── Card 2: Tu perfil lector ──────────────────────────────────────────────────

def render_profile_share_card(
    profile_name: str,
    profile_message: str,
    minutes_social: int,
    dashboard_url: str,
    size: CardSize = FEED,
) -> Image.Image:
    """Genera la share card 'Tu perfil lector' como imagen Pillow.

    Args:
        profile_name:    Nombre del perfil (p.ej. "Lector en transición").
        profile_message: Descripción narrativa del perfil.
        minutes_social:  Minutos diarios actuales en redes.
        dashboard_url:   URL del dashboard.
        size:            CardSize.FEED o CardSize.STORY.

    Returns:
        PIL.Image.Image lista para st.image() / to_png_bytes().

    Raises:
        ValueError: Si los minutos de redes son negativos.
    """
    if minutes_social < 0:
        raise ValueError("Los minutos de redes no pueden ser negativos")

    img = canvas(size)
    img = paper_texture(img)
    draw = ImageDraw.Draw(img)
    w, h = size.width, size.height

    editorial_border(draw, size)

    draw_header(img, "Tu perfil lector", "Así lees tú", kicker_color=CORAL)

    # Nombre del perfil en grande
    name_font = font_serif_bold(68)
    name_y = h // 2 - 80
    wrap_centered(
        draw,
        (w // 2, name_y),
        profile_name,
        name_font,
        max_width=w - 180,
        fill=CORAL,
    )

    # Separador
    sep_y = name_y + 80
    draw.line([(w // 2 - 220, sep_y), (w // 2 + 220, sep_y)], fill=RULE, width=2)

    # Mensaje del perfil
    msg_font = font_serif_italic(30)
    msg_y = sep_y + 70
    wrap_centered(
        draw,
        (w // 2, msg_y),
        profile_message,
        msg_font,
        max_width=w - 240,
        fill=INK_SOFT,
    )

    # Dato de redes
    ctx_font = font_sans(26)
    ctx_y = msg_y + 110
    draw_centered(
        draw,
        (w // 2, ctx_y),
        f"Hoy tus redes: {minutes_social}\u2009min/día",
        ctx_font,
        fill=INK_SOFT,
    )

    # Ilustración marcapáginas en zona derecha (bajo cabecera, encima del nombre)
    draw_mini_bookmark(img, (w - 190, name_y - 200), width=80)

    # Remite
    draw_remite(img, HANDLE, _clean_url(dashboard_url), qr_size=130)

    return img


def export_profile_share_card(
    profile_name: str,
    profile_message: str,
    minutes_social: int,
    dashboard_url: str,
    format: str = "square",
) -> bytes:
    """Exporta la card de perfil lector en PNG.

    Args:
        profile_name:    Nombre del perfil.
        profile_message: Descripción del perfil.
        minutes_social:  Minutos diarios en redes.
        dashboard_url:   URL del dashboard.
        format:          "square" o "story".

    Returns:
        Bytes PNG.

    Raises:
        ValueError: Si el formato no es válido.
    """
    if format not in {"square", "story"}:
        raise ValueError("Formato debe ser 'square' o 'story'")

    size = FEED if format == "square" else STORY
    img = render_profile_share_card(
        profile_name, profile_message, minutes_social, dashboard_url, size
    )
    return to_png_bytes(img)
