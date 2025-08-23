import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Float,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class FoundItem(Base):
    __tablename__ = 'found_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    finder_user_id = Column(UUID(as_uuid=True), nullable=True)
    image_bucket = Column(String(255), nullable=False)
    image_path = Column(String(255), nullable=False)
    caption_text = Column(Text, nullable=False)
    caption_model = Column(String(50), nullable=True)
    found_at = Column(DateTime(timezone=True), nullable=True)
    location_hint = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, server_default='active')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    matches = relationship("Match", back_populates="found_item")

    __table_args__ = (
        CheckConstraint(
            status.in_(['active', 'claimed', 'archived']),
            name='found_items_status_check'
        ),
    )

class LostReport(Base):
    __tablename__ = 'lost_reports'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_user_id = Column(UUID(as_uuid=True), nullable=True)
    description_text = Column(Text, nullable=False)
    lost_at = Column(DateTime(timezone=True), nullable=True)
    location_hint = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, server_default='open')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    matches = relationship("Match", back_populates="lost_report")

    __table_args__ = (
        CheckConstraint(
            status.in_(['open', 'resolved', 'archived']),
            name='lost_reports_status_check'
        ),
    )

class Match(Base):
    __tablename__ = 'matches'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lost_report_id = Column(UUID(as_uuid=True), ForeignKey('lost_reports.id'), nullable=False)
    found_item_id = Column(UUID(as_uuid=True), ForeignKey('found_items.id'), nullable=False)
    score = Column(Float, nullable=False)
    method = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    lost_report = relationship("LostReport", back_populates="matches")
    found_item = relationship("FoundItem", back_populates="matches")