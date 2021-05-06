from typing import Type, Dict, Callable

from bali.db import db
from bali.schema import model_to_schema
from pydantic import BaseModel
from sqlalchemy.sql.functions import func
from toolz import compose

from consts import ALWAYS_EXCLUDE

__all__ = ["ModelBiz", "clean"]
READONLY_FIELDS = ("id", "uuid", "created_time", "updated_time")


def clear_readonly_fields(data: Dict) -> Dict:
    return {k: v for k, v in data.items() if k not in READONLY_FIELDS}


def flat_data(data: Dict) -> Dict:
    if len(data) == 1 and isinstance(data.get("data"), dict):
        data = data["data"]
    return data


clean_steps = (
    clear_readonly_fields,
    flat_data,
    clear_readonly_fields,
)

clean: Callable[[Dict], Dict] = compose(*reversed(clean_steps))


class ModelBiz:
    model: db.BaseModel = None
    model_schema: Type[BaseModel] = None

    def __init_subclass__(cls, **kwargs):
        assert cls.model is not None, f"{cls.__name__} can not be None"
        if cls.model_schema is None:
            cls.model_schema = model_to_schema(cls.model, exclude=ALWAYS_EXCLUDE)

    def create(self, create: BaseModel) -> db.BaseModel:
        create_data = clean(create.dict(exclude_unset=True))
        model = self.model(**create_data)
        db.session.add(model)
        db.session.commit()
        return model

    def delete(self, uuid: str) -> None:
        model = self.retrieve(uuid)
        db.session.delete(model)
        db.session.commit()

    def patch(self, uuid: str, patch: BaseModel) -> db.BaseModel:
        model = self.retrieve(uuid)
        patch_data = clean(patch.dict(exclude_unset=True))
        for k, v in patch_data.items():
            setattr(model, k, v)
        db.session.add(model)
        db.session.commit()
        db.session.refresh(model)
        return model

    def retrieve(self, uuid: str) -> db.BaseModel:
        return db.session.query(self.model).filter(self.model.uuid == uuid).one()

    def list(self, filters: BaseModel):
        q = db.session.query(self.model)
        filters_data = filters.dict(exclude_defaults=True)
        if filters_data:
            q = q.filter_by(**filters_data)
        return q

    def count(self, filters: BaseModel) -> int:
        q = db.session.query(func.count(self.model.id))
        filters_data = filters.dict(exclude_defaults=True)
        if filters_data:
            q = q.filter_by(**filters_data)
        return q.scalar()
