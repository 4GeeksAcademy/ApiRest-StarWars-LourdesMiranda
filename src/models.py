import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(40), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    favorites: Mapped[List["Favourite"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    climate: Mapped[Optional[str]] = mapped_column(String(80))
    terrain: Mapped[Optional[str]] = mapped_column(String(80))

    favorites: Mapped[List["Favourite"]] = relationship(
        back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    hair_color: Mapped[Optional[str]] = mapped_column(String(40))
    eye_color: Mapped[Optional[str]] = mapped_column(String(40))
    gender: Mapped[Optional[str]] = mapped_column(String(20))

    favorites: Mapped[List["Favourite"]] = relationship(
        back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "gender": self.gender
        }


class Favourite(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("planet.id"), nullable=True)
    character_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("character.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    planet: Mapped[Optional["Planet"]] = relationship(
        back_populates="favorites")
    character: Mapped[Optional["Character"]] = relationship(
        back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }
