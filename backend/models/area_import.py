from enum import Enum

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    func,
    Boolean,
    Enum as ColEnum,
    CheckConstraint,
)

from backend.database.base import Base


class ResultStatus(Enum):
    SUCCESS = 'success'
    DOWNLOADING_ERROR = 'downloading_error'
    PARSING_ERROR = 'parsing_error'
    EMPTY_DATA_ERROR = 'empty_data_error'


class AreaImport(Base):
    __tablename__ = 'area_imports'
    __table_args__ = (
        CheckConstraint('end_at > start_at'),
        CheckConstraint('building_count >= 0'),
    )

    id = Column(BigInteger, primary_key=True)
    teryt = Column(String(8), nullable=False)

    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, default=func.now(), nullable=False)
    result_status = Column(ColEnum(ResultStatus), nullable=False)

    building_count = Column(BigInteger, nullable=False)

    has_building_type = Column(Boolean, nullable=False)
    has_building_levels = Column(Boolean, nullable=False)
    has_building_levels_undg = Column(Boolean, nullable=False)
