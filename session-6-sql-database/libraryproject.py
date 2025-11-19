# models.py
from __future__ import annotations

from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    CheckConstraint,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
