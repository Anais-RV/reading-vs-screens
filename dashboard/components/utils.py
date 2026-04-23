"""Utilidades compartidas para las páginas del dashboard."""
from __future__ import annotations

from pathlib import Path

import streamlit as st


@st.cache_data
def _read_css(css_path: str) -> str:
    """Lee y memoiza el contenido CSS para evitar I/O repetido."""
    return Path(css_path).read_text(encoding="utf-8")


def load_css(path: str) -> None:
    """Carga un archivo CSS y lo inyecta en la página actual de Streamlit.

    Args:
        path: Ruta al archivo CSS.
    """
    css_path = Path(path)
    if not css_path.exists():
        st.warning(f"No se encontró el archivo CSS: {css_path}")
        return

    css_content = _read_css(str(css_path.resolve()))
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
