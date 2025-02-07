from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserActivity(Base):
    __tablename__ = "TEMPO_CANAL"  # Replace with your table name

    id = Column(Integer, primary_key=True)
    member_id = Column(String(255), nullable=False)
    channel_id = Column(String(255), nullable=False)
    time = Column(Integer, nullable=False)  # Auto-populates time

    def __repr__(self):
        return f"<UserActivity(member_id={self.member_id}, channel_id={self.channel_id}, time={self.time})>"