"""Valida calidad y plausibilidad de datasets en data/processed.

Uso:
  python tools/validate_data_quality.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"


def _assert(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_screen_time(df: pd.DataFrame, errors: list[str]) -> None:
    _assert(df["source"].notna().all() and (df["source"].str.strip() != "").all(), "screen_time: source vacio", errors)
    _assert(df["avg_daily_social_media_min"].between(0, 600).all(), "screen_time: social media fuera de rango", errors)
    _assert(df["avg_daily_tv_min"].between(0, 600).all(), "screen_time: tv fuera de rango", errors)
    _assert(df["avg_daily_total_screen_min"].between(0, 1440).all(), "screen_time: total screen fuera de rango", errors)
    _assert((df["avg_daily_total_screen_min"] >= df["avg_daily_social_media_min"]).all(), "screen_time: total < social_media", errors)
    _assert((df["avg_daily_total_screen_min"] >= df["avg_daily_tv_min"]).all(), "screen_time: total < tv", errors)


def validate_reading_habits(df: pd.DataFrame, errors: list[str]) -> None:
    _assert(df["source"].notna().all() and (df["source"].str.strip() != "").all(), "reading_habits: source vacio", errors)
    _assert(df["pct_reads_regularly"].between(0, 100).all(), "reading_habits: pct_reads_regularly fuera de rango", errors)
    _assert(df["avg_books_per_year"].between(0, 300).all(), "reading_habits: avg_books_per_year fuera de rango", errors)
    _assert(df["avg_daily_reading_min"].between(0, 600).all(), "reading_habits: avg_daily_reading_min fuera de rango", errors)


def validate_cognitive_studies(df: pd.DataFrame, errors: list[str]) -> None:
    _assert(df["sample_size"].gt(0).all(), "cognitive_studies: sample_size debe ser > 0", errors)
    _assert(df["year"].between(1900, 2100).all(), "cognitive_studies: year fuera de rango", errors)
    _assert(df["doi"].notna().all() and (df["doi"].str.strip() != "").all(), "cognitive_studies: DOI vacio", errors)


def validate_sleep_studies(df: pd.DataFrame, errors: list[str]) -> None:
    _assert(df["sample_size"].gt(0).all(), "sleep_studies: sample_size debe ser > 0", errors)
    _assert(df["year"].between(1900, 2100).all(), "sleep_studies: year fuera de rango", errors)
    _assert(df["doi"].notna().all() and (df["doi"].str.strip() != "").all(), "sleep_studies: DOI vacio", errors)
    _assert(df["description"].notna().all() and (df["description"].str.strip() != "").all(), "sleep_studies: description vacia", errors)
    _assert(df["screen_value"].notna().all(), "sleep_studies: screen_value con nulos", errors)
    _assert(df["reading_value"].notna().all(), "sleep_studies: reading_value con nulos", errors)


def validate_attention_studies(df: pd.DataFrame, errors: list[str]) -> None:
    _assert(df["sample_size"].gt(0).all(), "attention_studies: sample_size debe ser > 0", errors)
    _assert(df["year"].between(1900, 2100).all(), "attention_studies: year fuera de rango", errors)
    _assert(df["doi"].notna().all() and (df["doi"].str.strip() != "").all(), "attention_studies: DOI vacio", errors)
    _assert(df["multitasker_value"].notna().all(), "attention_studies: multitasker_value con nulos", errors)
    _assert(df["focused_value"].notna().all(), "attention_studies: focused_value con nulos", errors)


def validate_reading_by_generation(df: pd.DataFrame, errors: list[str]) -> None:
    _assert(df["source"].notna().all() and (df["source"].str.strip() != "").all(), "reading_by_generation: source vacio", errors)
    _assert(df["pct_reads_regularly"].between(0, 100).all(), "reading_by_generation: pct_reads_regularly fuera de rango", errors)
    _assert(df["avg_books_per_year"].between(0, 300).all(), "reading_by_generation: avg_books_per_year fuera de rango", errors)
    _assert(df["avg_daily_social_media_min"].between(0, 600).all(), "reading_by_generation: social_media fuera de rango", errors)
    VALID_GENS = {"GenZ", "Millennial", "GenX", "Boomer"}
    invalid_gens = set(df["generation_label"].unique()) - VALID_GENS
    _assert(len(invalid_gens) == 0, f"reading_by_generation: etiquetas de generacion no reconocidas: {invalid_gens}", errors)


def main() -> int:
    errors: list[str] = []

    screen = pd.read_csv(DATA_DIR / "screen_time.csv")
    reading = pd.read_csv(DATA_DIR / "reading_habits.csv")
    cognitive = pd.read_csv(DATA_DIR / "cognitive_studies.csv")
    sleep = pd.read_csv(DATA_DIR / "sleep_studies.csv")
    attention = pd.read_csv(DATA_DIR / "attention_studies.csv")
    generation = pd.read_csv(DATA_DIR / "reading_by_generation.csv")

    validate_screen_time(screen, errors)
    validate_reading_habits(reading, errors)
    validate_cognitive_studies(cognitive, errors)
    validate_sleep_studies(sleep, errors)
    validate_attention_studies(attention, errors)
    validate_reading_by_generation(generation, errors)

    # Duplicados exactos
    for name, df in [
        ("screen_time", screen),
        ("reading_habits", reading),
        ("cognitive_studies", cognitive),
        ("sleep_studies", sleep),
        ("attention_studies", attention),
        ("reading_by_generation", generation),
    ]:
        if df.duplicated().any():
            errors.append(f"{name}: hay filas duplicadas exactas")

    if errors:
        print("VALIDACION FALLIDA")
        for e in errors:
            print(f"- {e}")
        return 1

    print("VALIDACION OK")
    print(f"- screen_time: {len(screen)} filas")
    print(f"- reading_habits: {len(reading)} filas")
    print(f"- cognitive_studies: {len(cognitive)} filas")
    print(f"- sleep_studies: {len(sleep)} filas")
    print(f"- attention_studies: {len(attention)} filas")
    print(f"- reading_by_generation: {len(generation)} filas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
