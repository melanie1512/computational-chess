from ..db.database import db
from sqlalchemy.ext.declarative import declared_attr

class ModelMixin:
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Position(db.Model, ModelMixin):
    __tablename__ = "positions"
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        if not self.is_valid():
            raise ValueError("Invalid position coordinates")

    def same_position(self, other_position):
        return self.x == other_position.x and self.y == other_position.y

    def clone(self):
        return Position(x=self.x, y=self.y)

    def is_valid(self):
        if 1 <= self.x <= 8 and 1 <= self.y <= 8:
            return True
        else:
            return False

    @classmethod
    def from_dict(cls, data):
        return cls(x=data["x"], y=data["y"])

