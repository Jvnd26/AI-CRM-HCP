from sqlalchemy import Column, Date, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255), nullable=False, index=True)
    interaction_type = Column(String(100), nullable=False)
    interaction_date = Column(Date, nullable=False)
    interaction_time = Column(String(20), nullable=False)
    attendees = Column(String(500), nullable=True)
    topics_discussed = Column(Text, nullable=True)
    materials_shared = Column(Text, nullable=True)
    outcome = Column(Text, nullable=True)
    follow_up_actions = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
