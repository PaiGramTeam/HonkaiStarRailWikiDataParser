from decimal import Decimal
from typing import Optional, Dict

from pydantic import model_validator, BaseModel

from .enums import RelicAffix, RelicPosition


class SingleRelicAffix(BaseModel):
    id: int
    property: RelicAffix
    base_value: float
    level_value: Optional[float] = None
    step_value: Optional[float] = None
    is_main: bool
    max_step: Optional[int] = None

    def get_value(self, level_or_step: int, cnt: int = 1) -> float:
        base_value = Decimal(self.base_value) * Decimal(cnt)
        add_value = Decimal(self.level_value if self.is_main else self.step_value)
        return float(base_value + add_value * Decimal(level_or_step))


class RelicAffixAll(BaseModel):
    id: int
    set_id: int
    """ 套装ID """
    type: RelicPosition
    """ 遗器类型 """
    rarity: int
    """ 星级 """
    main_affix_group: int
    sub_affix_group: int
    max_level: int
    """ 最大等级 """
    main_affix: Dict[str, SingleRelicAffix]
    """ 主词条 """
    sub_affix: Dict[str, SingleRelicAffix]
    """ 副词条 """

    @model_validator(mode="before")
    @classmethod
    def transform_dicts(cls, values):
        for data in ["main_affix", "sub_affix"]:
            affix = values.get(data)
            if affix:
                new_affix = {}
                for key, value in affix.items():
                    if isinstance(value, dict):
                        new_affix[key] = SingleRelicAffix(**value)
                    else:
                        new_affix[key] = value
                values[data] = new_affix
        return values
