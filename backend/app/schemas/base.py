from pydantic import BaseModel, ConfigDict

class BaseModelConfig(BaseModel):
    # Model config untuk mengizinkan loading dari ORM (SQLAlchemy)
    # serta memetakan otomatis snake_case ke camelCase untuk JSON API.
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        alias_generator=lambda s: "".join(
            word if i == 0 else word.capitalize()
            for i, word in enumerate(s.split("_"))
        )
    )
