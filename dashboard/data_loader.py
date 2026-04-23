"""
data_loader.py
Carga y validación de los datasets procesados para el dashboard.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

_DATA_DIR = Path(__file__).parent.parent / "data" / "processed"

# ── Esquemas de columnas ──────────────────────────────────────────────────────

_SCREEN_COLS: dict[str, type] = {
    "country": str,
    "avg_daily_social_media_min": float,
    "avg_daily_tv_min": float,
    "avg_daily_total_screen_min": float,
    "year": int,
    "source": str,
}

_READING_COLS: dict[str, type] = {
    "country": str,
    "pct_reads_regularly": float,
    "avg_books_per_year": float,
    "avg_daily_reading_min": float,
    "year": int,
    "source": str,
}

_COGNITIVE_COLS: dict[str, type] = {
    "study_id": str,
    "institution": str,
    "year": int,
    "metric": str,
    "reading_group_value": float,
    "control_group_value": float,
    "unit": str,
    "sample_size": int,
    "doi": str,
}

_SLEEP_COLS: dict[str, type] = {
    "study_id": str,
    "institution": str,
    "year": int,
    "domain": str,
    "metric": str,
    "screen_value": float,
    "reading_value": float,
    "unit": str,
    "sample_size": int,
    "doi": str,
    "description": str,
}

_ATTENTION_COLS: dict[str, type] = {
    "study_id": str,
    "institution": str,
    "year": int,
    "domain": str,
    "metric": str,
    "multitasker_value": float,
    "focused_value": float,
    "unit": str,
    "sample_size": int,
    "doi": str,
    "description": str,
}

_GENERATION_COLS: dict[str, type] = {
    "generation_label": str,
    "age_range": str,
    "country": str,
    "pct_reads_regularly": float,
    "avg_books_per_year": float,
    "avg_daily_reading_min": float,
    "avg_daily_social_media_min": float,
    "year": int,
    "source": str,
}


# ── Helpers de validación ─────────────────────────────────────────────────────

def _validate_columns(df: pd.DataFrame, required: dict[str, type], name: str) -> None:
    """Verifica que el DataFrame tenga todas las columnas requeridas."""
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(
            f"Dataset '{name}' le faltan columnas obligatorias: {missing}. "
            f"Columnas presentes: {list(df.columns)}"
        )


def _cast_dtypes(df: pd.DataFrame, schema: dict[str, type]) -> pd.DataFrame:
    """Convierte las columnas al tipo de dato correcto según el esquema."""
    df = df.copy()
    for col, dtype in schema.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype)
    return df


def _validate_screen_quality(df: pd.DataFrame) -> None:
    checks = [
        (df["source"].notna() & (df["source"].str.strip() != "")).all(),
        df["avg_daily_social_media_min"].between(0, 600).all(),
        df["avg_daily_tv_min"].between(0, 600).all(),
        df["avg_daily_total_screen_min"].between(0, 1440).all(),
        (df["avg_daily_total_screen_min"] >= df["avg_daily_social_media_min"]).all(),
        (df["avg_daily_total_screen_min"] >= df["avg_daily_tv_min"]).all(),
    ]
    if not all(checks):
        raise ValueError("screen_time contiene valores fuera de rango o inconsistentes")


def _validate_reading_quality(df: pd.DataFrame) -> None:
    checks = [
        (df["source"].notna() & (df["source"].str.strip() != "")).all(),
        df["pct_reads_regularly"].between(0, 100).all(),
        df["avg_books_per_year"].between(0, 300).all(),
        df["avg_daily_reading_min"].between(0, 600).all(),
    ]
    if not all(checks):
        raise ValueError("reading_habits contiene valores fuera de rango o inconsistentes")


def _validate_cognitive_quality(df: pd.DataFrame) -> None:
    checks = [
        df["sample_size"].gt(0).all(),
        df["year"].between(1900, 2100).all(),
        (df["doi"].notna() & (df["doi"].str.strip() != "")).all(),
    ]
    if not all(checks):
        raise ValueError("cognitive_studies contiene valores fuera de rango o incompletos")


def _validate_sleep_quality(df: pd.DataFrame) -> None:
    checks = [
        df["sample_size"].gt(0).all(),
        df["year"].between(1900, 2100).all(),
        (df["doi"].notna() & (df["doi"].str.strip() != "")).all(),
        (df["description"].notna() & (df["description"].str.strip() != "")).all(),
    ]
    if not all(checks):
        raise ValueError("sleep_studies contiene valores fuera de rango o incompletos")


def _validate_attention_quality(df: pd.DataFrame) -> None:
    checks = [
        df["sample_size"].gt(0).all(),
        df["year"].between(1900, 2100).all(),
        (df["doi"].notna() & (df["doi"].str.strip() != "")).all(),
    ]
    if not all(checks):
        raise ValueError("attention_studies contiene valores fuera de rango o incompletos")


def _validate_generation_quality(df: pd.DataFrame) -> None:
    checks = [
        (df["source"].notna() & (df["source"].str.strip() != "")).all(),
        df["pct_reads_regularly"].between(0, 100).all(),
        df["avg_books_per_year"].between(0, 300).all(),
        df["avg_daily_social_media_min"].between(0, 600).all(),
    ]
    if not all(checks):
        raise ValueError("reading_by_generation contiene valores fuera de rango o inconsistentes")


# ── Loaders públicos ──────────────────────────────────────────────────────────

@st.cache_data
def load_screen_time() -> pd.DataFrame:
    """Carga y valida el dataset de tiempo en pantallas."""
    path = _DATA_DIR / "screen_time.csv"
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    df = pd.read_csv(path)
    _validate_columns(df, _SCREEN_COLS, "screen_time")
    df = _cast_dtypes(df, _SCREEN_COLS)
    _validate_screen_quality(df)
    return df


@st.cache_data
def load_reading_habits() -> pd.DataFrame:
    """Carga y valida el dataset de hábitos de lectura."""
    path = _DATA_DIR / "reading_habits.csv"
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    df = pd.read_csv(path)
    _validate_columns(df, _READING_COLS, "reading_habits")
    df = _cast_dtypes(df, _READING_COLS)
    _validate_reading_quality(df)
    return df


@st.cache_data
def load_cognitive_studies() -> pd.DataFrame:
    """Carga y valida el dataset de estudios cognitivos."""
    path = _DATA_DIR / "cognitive_studies.csv"
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    df = pd.read_csv(path)
    _validate_columns(df, _COGNITIVE_COLS, "cognitive_studies")
    df = _cast_dtypes(df, _COGNITIVE_COLS)
    _validate_cognitive_quality(df)
    return df


@st.cache_data
def load_sleep_studies() -> pd.DataFrame:
    """Carga y valida el dataset de estudios sobre sueño y scroll nocturno.

    Returns
    -------
    pd.DataFrame
        Columnas: study_id, institution, year, domain, metric,
        screen_value, reading_value, unit, sample_size, doi, description.
    """
    path = _DATA_DIR / "sleep_studies.csv"
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    df = pd.read_csv(path)
    _validate_columns(df, _SLEEP_COLS, "sleep_studies")
    df = _cast_dtypes(df, _SLEEP_COLS)
    _validate_sleep_quality(df)
    return df


@st.cache_data
def load_attention_studies() -> pd.DataFrame:
    """Carga y valida el dataset de estudios sobre atención sostenida.

    Returns
    -------
    pd.DataFrame
        Columnas: study_id, institution, year, domain, metric,
        multitasker_value, focused_value, unit, sample_size, doi, description.
    """
    path = _DATA_DIR / "attention_studies.csv"
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    df = pd.read_csv(path)
    _validate_columns(df, _ATTENTION_COLS, "attention_studies")
    df = _cast_dtypes(df, _ATTENTION_COLS)
    _validate_attention_quality(df)
    return df


@st.cache_data
def load_reading_by_generation() -> pd.DataFrame:
    """Carga y valida el dataset de hábitos de lectura por generación.

    Returns
    -------
    pd.DataFrame
        Columnas: generation_label, age_range, country, pct_reads_regularly,
        avg_books_per_year, avg_daily_reading_min, avg_daily_social_media_min,
        year, source.
    """
    path = _DATA_DIR / "reading_by_generation.csv"
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    df = pd.read_csv(path)
    _validate_columns(df, _GENERATION_COLS, "reading_by_generation")
    df = _cast_dtypes(df, _GENERATION_COLS)
    _validate_generation_quality(df)
    return df


@st.cache_data
def _load_dataset_lazy_cached(dataset_name: str) -> pd.DataFrame | None:
    """Resuelve y carga un dataset por nombre para lazy loading."""
    loader_map = {
        "screen_time": load_screen_time,
        "reading_habits": load_reading_habits,
        "cognitive_studies": load_cognitive_studies,
        "sleep_studies": load_sleep_studies,
        "attention_studies": load_attention_studies,
        "reading_by_generation": load_reading_by_generation,
    }
    loader = loader_map.get(dataset_name)
    if loader is None:
        return None

    try:
        return loader()
    except (FileNotFoundError, ValueError):
        return None


def load_dataset_lazy(dataset_name: str) -> pd.DataFrame | None:
    """Carga un dataset solo cuando se necesita y lo persiste en session_state.

    Si el dataset no existe o falla su validación, devuelve ``None`` sin bloquear
    la app para preservar compatibilidad entre páginas.
    """
    cached_data = st.session_state.get(dataset_name)
    if cached_data is not None:
        return cached_data

    data = _load_dataset_lazy_cached(dataset_name)
    st.session_state[dataset_name] = data
    return data
