from enum import Enum


class Quality(str, Enum):
    """ 星级 """
    Five = "五星"
    Four = "四星"
    Three = "三星"
    Two = "二星"
    One = "一星"


class Destiny(str, Enum):
    """ 命途 """
    HuiMie = "毁灭"
    ZhiShi = "智识"
    XunLie = "巡猎"
    CunHu = "存护"
    FengRao = "丰饶"
    TongXie = "同谐"
    XuWu = "虚无"


class Element(str, Enum):
    """ 属性 """
    Physical = "物理"
    Pyro = "火"
    Anemo = "风"
    Electro = "雷"
    Cryo = "冰"
    Nombre = "虚数"
    Quantum = "量子"
    Null = "NULL"
    """无"""


class MonsterType(str, Enum):
    """ 怪物种类 """
    Normal = "普通"
    Elite = "精英"
    Leader = "首领"
    Boss = "历战余响"


class Area(str, Enum):
    """ 地区 """
    Herta = "空间站「黑塔」"
    YaLiLuo = "雅利洛-VI"
    LuoFu = "仙舟「罗浮」"
    NULL = "未知"


class MaterialType(str, Enum):
    """ 材料类型 """
    AvatarUpdate = "角色晋阶材料"
    XingJi = "行迹材料"
    LightConeUpdate = "光锥晋阶材料"
    Exp = "经验材料"
    Grow = "养成材料"
    Synthetic = "合成材料"
    Task = "任务道具"
    Important = "贵重物"
    Consumable = "消耗品"
    TaskMaterial = "任务材料"
    Other = "其他材料"


class PropType(str, Enum):
    """ 遗器套装效果 """
    HP = "基础-生命值"
    Defense = "基础-防御力"
    Attack = "基础-攻击力"
    Critical = "基础-效果命中"
    Physical = "伤害类-物理"
    Pyro = "伤害类-火"
    Anemo = "伤害类-风"
    Electro = "伤害类-雷"
    Cryo = "伤害类-冰"
    Nombre = "伤害类-虚数"
    Quantum = "伤害类-量子"
    Add = "伤害类-追加伤害"
    Heal = "其他-治疗加成"
    OtherCritical = "其他-效果命中"
    Charge = "其他-能量充能效率"


class RelicAffix(str, Enum):
    AttackAddedRatio: str = "AttackAddedRatio"
    """ 攻击力 百分比 """
    AttackDelta: str = "AttackDelta"
    """ 攻击力 """
    BreakDamageAddedRatioBase: str = "BreakDamageAddedRatioBase"
    """ 击破特攻 """
    CriticalChanceBase: str = "CriticalChanceBase"
    """ 暴击率 百分比 """
    CriticalDamageBase: str = "CriticalDamageBase"
    """ 暴击伤害 百分比 """
    DefenceAddedRatio: str = "DefenceAddedRatio"
    """ 防御力 百分比 """
    DefenceDelta: str = "DefenceDelta"
    """ 防御力 """
    FireAddedRatio: str = "FireAddedRatio"
    """ 火属性伤害提高 百分比 """
    HPAddedRatio: str = "HPAddedRatio"
    """ 生命值 百分比 """
    HPDelta: str = "HPDelta"
    """ 生命值 """
    HealRatioBase: str = "HealRatioBase"
    """ 治疗量加成 百分比"""
    IceAddedRatio: str = "IceAddedRatio"
    """ 冰属性伤害提高 百分比 """
    ImaginaryAddedRatio: str = "ImaginaryAddedRatio"
    """ 虚数属性伤害提高 百分比 """
    PhysicalAddedRatio: str = "PhysicalAddedRatio"
    """ 物理属性伤害提高 百分比 """
    QuantumAddedRatio: str = "QuantumAddedRatio"
    """ 量子属性伤害提高 百分比 """
    SpeedDelta: str = "SpeedDelta"
    """ 速度 """
    SPRatioBase: str = "SPRatioBase"
    """ 能量恢复效率 百分比 """
    StatusProbabilityBase: str = "StatusProbabilityBase"
    """ 效果命中 百分比 """
    StatusResistanceBase: str = "StatusResistanceBase"
    """ 效果抵抗 百分比 """
    ThunderAddedRatio: str = "ThunderAddedRatio"
    """ 雷属性伤害提高 百分比 """
    WindAddedRatio: str = "WindAddedRatio"
    """ 风属性伤害提高 百分比 """


class RelicPosition(str, Enum):
    HEAD: str = "HEAD"
    """ 头 """
    HAND: str = "HAND"
    """ 手 """
    BODY: str = "BODY"
    """ 躯干 """
    FOOT: str = "FOOT"
    """ 脚 """
    NECK: str = "NECK"
    """ 位面球 """
    OBJECT: str = "OBJECT"
    """ 连结绳 """

    @property
    def num(self):
        index_map = {
            RelicPosition.HEAD: 0,
            RelicPosition.HAND: 1,
            RelicPosition.BODY: 2,
            RelicPosition.FOOT: 3,
            RelicPosition.NECK: 0,
            RelicPosition.OBJECT: 1,
        }
        return index_map.get(self)
