from typing import List

from sqlalchemy import String, Integer, Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from domain.flashcard_manager import Flashcard, Deck


class Base(DeclarativeBase):
    pass

class FlashcardModel(Base):
    __tablename__ = "flashcards"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str]
    answer: Mapped[str]
    deckId: Mapped[int] = mapped_column(ForeignKey("decks.id"), nullable=False)

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
