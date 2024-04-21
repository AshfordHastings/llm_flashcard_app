from typing import List

from datetime import datetime 
from sqlalchemy import String, Integer, Column, ForeignKey, Table, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func



from domain.flashcard_manager import Flashcard, Deck


class Base(DeclarativeBase):
    pass

class FlashcardModel(Base):
    __tablename__ = "flashcards"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(nullable=True)
    answer: Mapped[str] = mapped_column(nullable=True)
    deck_id: Mapped[int] = mapped_column(ForeignKey("decks.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    last_updated: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    deck: Mapped['DeckModel'] = relationship(back_populates="flashcards")

    def convert_to_domain(self):
        return Flashcard(
            question=self.question,
            answer=self.answer
        )

class DeckModel(Base):
    __tablename__ = "decks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    summary: Mapped[str]

    flashcards:Mapped[List['FlashcardModel']] = relationship(back_populates="deck", cascade="all, delete-orphan")

    def convert_to_domain(self):
        return Deck(
            name=self.name,
            summary=self.summary,
            flashcards=[flashcard.convert_to_domain() for flashcard in self.flashcards]
        )
    
# class FlashcardOrderModel(Base):
#     __tablename__ = "flashcard_orders"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     flashcard_id: Mapped[int] = mapped_column(ForeignKey("flashcards.id"), nullable=False)
#     deck_id: Mapped[int] = mapped_column(ForeignKey("decks.id"), nullable=False)
#     position: Mapped[float] = mapped_column(Float, nullable=False)

#     flashcard: Mapped['FlashcardModel'] = relationship("FlashcardModel")
