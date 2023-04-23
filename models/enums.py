from aenum import StrEnum


class Quality(StrEnum):
    """ 星级 """
    Five = "五星"
    Four = "四星"
    Three = "三星"
    Two = "二星"
    One = "一星"


class Destiny(StrEnum):
    """ 命途 """
    HuiMie = "毁灭"
    ZhiShi = "智识"
    XunLie = "巡猎"
    CunHu = "存护"
    FengRao = "丰饶"
    TongXie = "同谐"
    XuWu = "虚无"


class Element(StrEnum):
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


class MonsterType(StrEnum):
    """ 怪物种类 """
    Normal = "普通"
    Elite = "精英"
    Leader = "首领"
    Boss = "历战余响"


class Area(StrEnum):
    """ 地区 """
    Herta = "空间站「黑塔」"
    YaLiLuo = "雅利洛-VI"
    LuoFu = "仙舟「罗浮」"
    NULL = "未知"


class MaterialType(StrEnum):
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


class PropType(StrEnum):
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
