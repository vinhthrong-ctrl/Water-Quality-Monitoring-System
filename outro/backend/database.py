import os
import math
from typing import Any, Dict, Generator, List, Optional
from supabase import create_client, Client
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    import numpy as np
except ImportError:
    np = None


def _is_nan(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, float) and math.isnan(value):
        return True
    if np is not None and isinstance(value, np.generic):
        try:
            return math.isnan(value)
        except TypeError:
            return False
    return False


def clean_sample(sample: Dict[str, Any]) -> Dict[str, Any]:
    cleaned: Dict[str, Any] = {}
    for key, value in sample.items():
        if _is_nan(value):
            cleaned[key] = None
        elif np is not None and isinstance(value, np.generic):
            cleaned[key] = float(value)
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            cleaned[key] = float(value) if isinstance(value, float) else value
        else:
            cleaned[key] = value
    return cleaned


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
