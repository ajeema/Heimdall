from typing import Optional, Any
from sqlmodel import Field, Session, SQLModel, create_engine
from sqlmodel import create_engine, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.Configuration.config import Config
import logging
from datetime import datetime

"""
TODO: The tag check should be a BM25 search, it's just a simple equality check now.
"""
logger = logging.getLogger(__name__)


class Knowledge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tag: str = Field(index=True)
    contents: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class KnowledgeBase:
    def __init__(self):
        config = Config()
        sqlite_path = config.get_sqlite_db()
        self.engine = create_engine(f"sqlite+aiosqlite:///{sqlite_path}")
        SQLModel.metadata.create_all(self.engine)

    async def get_knowledge_async(self, tag: str) -> str:
        async with AsyncSession(self.engine) as session:
            result = await session.execute(select(Knowledge).where(Knowledge.tag == tag))
            knowledge = result.scalars().first()
            return knowledge.contents if knowledge else None

    def get_knowledge(self, tag: str) -> Any | None:
        with Session(self.engine) as session:
            knowledge = session.query(Knowledge).filter(Knowledge.tag == tag).first()
            if knowledge:
                return knowledge.contents
            return None

    def add_knowledge(self, tag: str, contents: str):
        try:
            knowledge = Knowledge(tag=tag, contents=contents)
            with Session(self.engine) as session:
                session.add(knowledge)
                session.commit()
        except Exception as e:
            logger.error(f"Failed to add knowledge: {e}")