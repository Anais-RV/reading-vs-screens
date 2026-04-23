"""Helpers editoriales para componer share cards tipo Wrapped.

Todas las cards comparten:
- Fondo papel crema con borde editorial fino
- Tipografía serif para cifras grandes, sans para copy
- Mini-ilustración SVG rasterizada en la esquina
- Remite: handle + URL + QR al dashboard

La API pública devuelve bytes PNG para `st.image()` / `st.download_button`.
"""
from __future__ import annotations

import io
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import qrcode
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ── Paleta editorial ────────────────────────────────────────────────────────
PAPER = (247, 243, 236)          # #F7F3EC crema cálida
INK = (31, 41, 55)               # #1F2937 casi negro
INK_SOFT = (90, 81, 70)          # #5A5146 gris papel
RULE = (196, 184, 162)           # #C4B8A2 beige oscuro para líneas
TEAL = (29, 158, 117)            # #1D9E75
CORAL = (216, 90, 48)            # #D85A30
AMBER = (239, 159, 39)           # #EF9F27
PURPLE = (127, 119, 221)         # #7F77DD

PALETTE_BY_TONE = {
    "teal": TEAL,
    "coral": CORAL,
    "amber": AMBER,
    "purple": PURPLE,
}

# ── Fuentes ────────────────────────────────────────────────────────────────
_FONT_CANDIDATES_SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "DejaVuSerif-Bold.ttf",
]
_FONT_CANDIDATES_SERIF = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "DejaVuSerif.ttf",
]
_FONT_CANDIDATES_SERIF_ITALIC = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "DejaVuSerif-Italic.ttf",
]
_FONT_CANDIDATES_SANS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "DejaVuSans.ttf",
]
_FONT_CANDIDATES_SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "DejaVuSans-Bold.ttf",
]


def _load(candidates: Iterable[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def font_serif_bold(size: int) -> ImageFont.FreeTypeFont:
    return _load(_FONT_CANDIDATES_SERIF_BOLD, size)


def font_serif(size: int) -> ImageFont.FreeTypeFont:
    return _load(_FONT_CANDIDATES_SERIF, size)


def font_serif_italic(size: int) -> ImageFont.FreeTypeFont:
    return _load(_FONT_CANDIDATES_SERIF_ITALIC, size)


def font_sans(size: int) -> ImageFont.FreeTypeFont:
    return _load(_FONT_CANDIDATES_SANS, size)


def font_sans_bold(size: int) -> ImageFont.FreeTypeFont:
    return _load(_FONT_CANDIDATES_SANS_BOLD, size)


# ── Canvas helpers ─────────────────────────────────────────────────────────
@dataclass(frozen=True)
class CardSize:
    width: int
    height: int

    @property
    def is_story(self) -> bool:
        return self.height > self.width


FEED = CardSize(1080, 1080)
STORY = CardSize(1080, 1920)


def canvas(size: CardSize, color: tuple[int, int, int] = PAPER) -> Image.Image:
    """Devuelve un canvas RGB del tamaño pedido con color de fondo."""
    return Image.new("RGB", (size.width, size.height), color)


def paper_texture(img: Image.Image, strength: int = 8) -> Image.Image:
    """Añade una textura sutil para que el papel no sea plano.

    Usamos ruido suave con leve blur. `strength` en 0..30 aproximadamente.
    """
    import random

    noise = Image.new("L", img.size, 255)
    pix = noise.load()
    for y in range(img.height):
        for x in range(img.width):
            pix[x, y] = 255 - random.randint(0, strength)
    noise = noise.filter(ImageFilter.GaussianBlur(radius=1.2))
    tex = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, tex, alpha=0.06)


def editorial_border(draw: ImageDraw.ImageDraw, size: CardSize, margin: int = 36) -> None:
    """Borde fino exterior + filete interior: aspecto de portada de libro."""
    w, h = size.width, size.height
    # Exterior
    draw.rectangle(
        [(margin, margin), (w - margin, h - margin)],
        outline=INK,
        width=3,
    )
    # Filete interior, 10 px dentro
    inner = margin + 10
    draw.rectangle(
        [(inner, inner), (w - inner, h - inner)],
        outline=RULE,
        width=1,
    )


# ── Tipografía utilitaria ──────────────────────────────────────────────────
def text_size(text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    """Devuelve (ancho, alto) de un texto con un font dado."""
    # Pillow 10+: textbbox es el camino
    dummy = Image.new("RGB", (1, 1))
    bbox = ImageDraw.Draw(dummy).textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int] = INK,
) -> None:
    """Dibuja un texto centrado en la coordenada (x, y)."""
    w, h = text_size(text, font)
    x = xy[0] - w // 2
    y = xy[1] - h // 2
    draw.text((x, y), text, font=font, fill=fill)


def wrap_centered(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
    fill: tuple[int, int, int] = INK,
    line_spacing: int = 10,
) -> int:
    """Dibuja texto con wrap en varias líneas, centrado en (x, y_start). Devuelve alto total."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for w in words:
        candidate = (current + " " + w).strip()
        width, _ = text_size(candidate, font)
        if width <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)

    line_heights = [text_size(l, font)[1] for l in lines]
    total_h = sum(line_heights) + line_spacing * (len(lines) - 1)

    y = xy[1] - total_h // 2
    for line, lh in zip(lines, line_heights):
        lw, _ = text_size(line, font)
        x = xy[0] - lw // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += lh + line_spacing
    return total_h


# ── QR code ────────────────────────────────────────────────────────────────
def make_qr(url: str, size_px: int = 180) -> Image.Image:
    """Genera un QR code en estilo editorial (tinta sobre papel, sin marco)."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=(31, 41, 55), back_color=PAPER).convert("RGB")
    return img.resize((size_px, size_px), Image.LANCZOS)


# ── Remite común: handle + URL + QR ────────────────────────────────────────
def draw_remite(
    base: Image.Image,
    handle: str,
    dashboard_url: str,
    *,
    qr_size: int = 140,
    include_qr: bool = True,
) -> None:
    """Pie de marca idéntico en todas las cards.

    Estructura (de izquierda a derecha):
        [Logo-mark] @handle                       reading-vs-screens.streamlit.app [QR]
        Recupera minutos de lectura
    """
    draw = ImageDraw.Draw(base)
    w, h = base.size
    margin = 90

    # Línea separadora fina
    rule_y = h - (margin + qr_size + 20)
    draw.line([(margin, rule_y), (w - margin, rule_y)], fill=RULE, width=1)

    # Texto a la izquierda: handle + tagline
    handle_font = font_serif_bold(38)
    tagline_font = font_serif_italic(24)

    handle_y = rule_y + 30
    draw.text((margin, handle_y), handle, font=handle_font, fill=INK)

    _, hh = text_size(handle, handle_font)
    tagline_y = handle_y + hh + 10
    draw.text(
        (margin, tagline_y),
        "Recupera minutos de lectura",
        font=tagline_font,
        fill=INK_SOFT,
    )

    # URL pequeña debajo de tagline
    url_font = font_sans(18)
    _, th = text_size("Tg", tagline_font)
    url_y = tagline_y + th + 10
    draw.text((margin, url_y), dashboard_url, font=url_font, fill=INK_SOFT)

    # QR a la derecha
    if include_qr:
        qr = make_qr(f"https://{dashboard_url.lstrip('https://').lstrip('http://')}", qr_size)
        qr_x = w - margin - qr_size
        qr_y = rule_y + 30
        base.paste(qr, (qr_x, qr_y))


def draw_header(
    base: Image.Image,
    kicker: str,
    title: str,
    *,
    kicker_color: tuple[int, int, int] = CORAL,
) -> int:
    """Cabecera común: kicker en mayúsculas + título serif.

    Devuelve la coordenada Y donde termina la cabecera.
    """
    draw = ImageDraw.Draw(base)
    w = base.size[0]
    margin_top = 130

    # Kicker (mayúsculas espaciadas)
    kicker_up = " ".join(list(kicker.upper()))
    kicker_font = font_sans_bold(22)
    kw, kh = text_size(kicker_up, kicker_font)
    draw.text(((w - kw) // 2, margin_top), kicker_up, font=kicker_font, fill=kicker_color)

    # Título serif debajo del kicker
    title_font = font_serif_bold(44)
    title_y = margin_top + kh + 20
    wrap_centered(
        draw,
        (w // 2, title_y + 30),
        title,
        title_font,
        max_width=w - 220,
        fill=INK,
    )

    return title_y + 70


# ── Micro-ilustración: libro abierto SVG rasterizado ───────────────────────
def draw_mini_book(base: Image.Image, xy: tuple[int, int], width: int = 140) -> None:
    """Dibuja un libro abierto minimalista (línea fina) en la posición dada."""
    draw = ImageDraw.Draw(base)
    x, y = xy
    h = int(width * 0.72)

    ink = INK
    line_w = 2

    # Páginas (dos trapecios que convergen en el lomo)
    # Página izquierda
    draw.polygon(
        [
            (x, y + h * 0.15),
            (x + width * 0.48, y),
            (x + width * 0.48, y + h),
            (x, y + h * 0.85),
        ],
        outline=ink,
        fill=(255, 255, 255),
        width=line_w,
    )
    # Página derecha
    draw.polygon(
        [
            (x + width * 0.52, y),
            (x + width, y + h * 0.15),
            (x + width, y + h * 0.85),
            (x + width * 0.52, y + h),
        ],
        outline=ink,
        fill=(255, 255, 255),
        width=line_w,
    )
    # Lomo central
    draw.line(
        [(x + width * 0.5, y + h * 0.05), (x + width * 0.5, y + h * 0.95)],
        fill=ink,
        width=line_w,
    )
    # Líneas de texto sugerido en cada página
    for i in range(3):
        ly = y + h * (0.3 + i * 0.15)
        draw.line(
            [(x + width * 0.08, ly), (x + width * 0.42, ly + 1)],
            fill=RULE,
            width=1,
        )
        draw.line(
            [(x + width * 0.58, ly + 1), (x + width * 0.92, ly)],
            fill=RULE,
            width=1,
        )


def draw_mini_cup(base: Image.Image, xy: tuple[int, int], width: int = 120) -> None:
    """Taza de té con vapor."""
    draw = ImageDraw.Draw(base)
    x, y = xy
    h = int(width * 0.85)

    # Cuerpo de la taza
    draw.rounded_rectangle(
        [(x, y + h * 0.35), (x + width * 0.75, y + h)],
        radius=int(width * 0.05),
        outline=INK,
        fill=(255, 255, 255),
        width=2,
    )
    # Asa
    draw.ellipse(
        [(x + width * 0.7, y + h * 0.45), (x + width, y + h * 0.85)],
        outline=INK,
        width=2,
    )
    draw.ellipse(
        [(x + width * 0.76, y + h * 0.52), (x + width * 0.93, y + h * 0.78)],
        fill=PAPER,
        outline=PAPER,
    )
    # Vapor (tres líneas onduladas)
    for off, amp in [(0.18, 4), (0.34, 5), (0.52, 4)]:
        cx = x + width * off
        path = []
        for i in range(8):
            py = y + h * 0.3 - i * (h * 0.04)
            px = cx + (amp if i % 2 == 0 else -amp)
            path.append((px, py))
        for p1, p2 in zip(path, path[1:]):
            draw.line([p1, p2], fill=INK, width=2)


def draw_mini_bookmark(base: Image.Image, xy: tuple[int, int], width: int = 80) -> None:
    """Marcapáginas con borla."""
    draw = ImageDraw.Draw(base)
    x, y = xy
    h = int(width * 2)

    # Cuerpo rectangular
    draw.rectangle(
        [(x, y), (x + width, y + h * 0.82)],
        outline=INK,
        fill=(255, 255, 255),
        width=2,
    )
    # V de corte abajo
    draw.polygon(
        [
            (x, y + h * 0.82),
            (x + width // 2, y + h * 0.92),
            (x + width, y + h * 0.82),
            (x + width, y + h * 0.82),
        ],
        fill=PAPER,
    )
    draw.line([(x, y + h * 0.82), (x + width // 2, y + h * 0.92)], fill=INK, width=2)
    draw.line(
        [(x + width // 2, y + h * 0.92), (x + width, y + h * 0.82)],
        fill=INK,
        width=2,
    )
    # Motivo central
    draw.line(
        [(x + width * 0.3, y + h * 0.15), (x + width * 0.7, y + h * 0.15)],
        fill=INK,
        width=1,
    )
    draw.line(
        [(x + width * 0.3, y + h * 0.72), (x + width * 0.7, y + h * 0.72)],
        fill=INK,
        width=1,
    )


# ── Serializar a bytes PNG ─────────────────────────────────────────────────
def to_png_bytes(img: Image.Image) -> bytes:
    out = io.BytesIO()
    img.save(out, format="PNG", optimize=True)
    return out.getvalue()
