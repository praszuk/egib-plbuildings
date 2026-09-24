from geoalchemy2 import Geometry
from sqlalchemy import JSON, BigInteger, Column, String

from backend.database.base import Base


class Building(Base):
    __tablename__ = 'buildings'

    id = Column(BigInteger, primary_key=True)
    geometry = Column(Geometry(srid=4326, spatial_index=True), nullable=False)
    tags = Column(JSON, nullable=False)
    teryt = Column(String(8), nullable=False)
