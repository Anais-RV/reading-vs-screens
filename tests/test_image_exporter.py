"""Tests básicos para export_figure_with_branding."""
from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image
from PIL import ImageFont

# Permite importar components desde dashboard/
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "dashboard"))

from components.image_exporter import export_figure_with_branding


class _FakeFigure:
    def __init__(self, payload: bytes | None = None, raises: Exception | None = None) -> None:
        self._payload = payload
        self._raises = raises

    def to_image(self, **_: object) -> bytes:
        if self._raises is not None:
            raise self._raises
        assert self._payload is not None
        return self._payload


def _png_bytes(width: int, height: int, color: str = "white") -> bytes:
    img = Image.new("RGB", (width, height), color=color)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


class TestImageExporter(unittest.TestCase):
    def test_raise_when_fig_none(self) -> None:
        with self.assertRaisesRegex(ValueError, "La figura no puede ser None"):
            export_figure_with_branding(None, filename="x")  # type: ignore[arg-type]

    def test_raise_kaleido_message(self) -> None:
        fig = _FakeFigure(raises=ValueError('Image export using the "kaleido" engine requires the kaleido package'))
        with self.assertRaisesRegex(ValueError, "Instala kaleido==0.2.1"):
            export_figure_with_branding(fig, filename="x")

    @patch("components.image_exporter._load_font")
    def test_returns_png_bytes_with_expected_size(self, mock_load_font) -> None:
        mock_load_font.return_value = ImageFont.load_default()
        fig = _FakeFigure(payload=_png_bytes(1080, 1020))

        result = export_figure_with_branding(
            fig,
            filename="x",
            project_name="Proyecto",
            dashboard_url="https://example.com",
            width=1080,
            height=1080,
        )

        self.assertTrue(result.startswith(b"\x89PNG"))
        out_img = Image.open(io.BytesIO(result))
        self.assertEqual(out_img.size, (1080, 1080))

        # Verifica que la franja inferior tenga el color de branding (muestra en el centro inferior).
        self.assertEqual(out_img.getpixel((540, 1050)), (29, 158, 117))


if __name__ == "__main__":
    unittest.main()
