"""Utilidades para exportar figuras Plotly a PNG con branding."""
from __future__ import annotations

import io

import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Carga una fuente TrueType común en Windows y cae a la fuente por defecto si falla."""
    candidates = [
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
    ]
    for font_name in candidates:
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def export_figure_with_branding(
    fig: go.Figure,
    filename: str,
    project_name: str = "Tu cerebro cuando lees",
    dashboard_url: str = "https://reading-vs-screens.streamlit.app",
    width: int = 1080,
    height: int = 1080,
) -> bytes:
    """Renderiza una figura Plotly a PNG y añade una franja inferior de branding.

    Args:
        fig: Figura de Plotly a exportar.
        filename: Nombre sugerido del archivo (sin extensión).
        project_name: Texto de branding mostrado a la izquierda.
        dashboard_url: URL del dashboard mostrada a la derecha.
        width: Ancho de salida en píxeles.
        height: Alto de salida en píxeles.

    Returns:
        Imagen PNG como bytes lista para st.download_button.

    Raises:
        ValueError: Si fig es None o si falta kaleido.
    """
    del filename  # El nombre lo usa la página al definir file_name del download button.

    if fig is None:
        raise ValueError("La figura no puede ser None")

    footer_height = 60
    chart_height = max(height - footer_height, 1)

    try:
        chart_bytes = fig.to_image(format="png", width=width, height=chart_height, scale=2)
    except ValueError as exc:
        if "kaleido" in str(exc).lower():
            raise ValueError("Instala kaleido==0.2.1") from exc
        raise

    chart_img = Image.open(io.BytesIO(chart_bytes)).convert("RGB")

    final_img = Image.new("RGB", (width, height), color="white")
    chart_resized = chart_img.resize((width, chart_height))
    final_img.paste(chart_resized, (0, 0))

    draw = ImageDraw.Draw(final_img)
    strip_color = "#1D9E75"
    draw.rectangle([(0, chart_height), (width, height)], fill=strip_color)

    left_font = _load_font(20, bold=True)
    right_font = _load_font(16, bold=False)
    text_color = "white"
    horizontal_padding = 24

    left_bbox = draw.textbbox((0, 0), project_name, font=left_font)
    left_text_h = left_bbox[3] - left_bbox[1]
    left_y = chart_height + (footer_height - left_text_h) // 2

    right_bbox = draw.textbbox((0, 0), dashboard_url, font=right_font)
    right_text_w = right_bbox[2] - right_bbox[0]
    right_text_h = right_bbox[3] - right_bbox[1]
    right_x = width - horizontal_padding - right_text_w
    right_y = chart_height + (footer_height - right_text_h) // 2

    draw.text((horizontal_padding, left_y), project_name, fill=text_color, font=left_font)
    draw.text((right_x, right_y), dashboard_url, fill=text_color, font=right_font)

    output = io.BytesIO()
    final_img.save(output, format="PNG")
    return output.getvalue()
