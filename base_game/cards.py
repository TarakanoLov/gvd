import copy

from . import card_deck
from . import player


class Card:
    def __init__(self, name, cost, func, type_card):
        self.name = name
        self.cost = cost
        self.func = func
        self.type_card = type_card
        self.index = None
        
    def __eq__(self, other):
        return self.func == other.func
        
    def __str__(self):
        return 'Карта: ' + self.name
        
    def __repr__(self):
        return self.__str__()

    def use(self, user, other):
        if self.is_can_use(user):
            if self.type_card == 0:
                user.add_ore(-self.cost)
            elif self.type_card == 1:
                user.add_mana(-self.cost)
            elif self.type_card == 2:
                user.add_squad(-self.cost)
            user.drop(self)
            return self.func(user, other)
            
    def is_can_use(self, user):
        if self.type_card == 0:
            if user.ore >= self.cost:
                return True
            else:
                return False
        elif self.type_card == 1:
            if user.mana >= self.cost:
                return True
            else:
                return False
        elif self.type_card == 2:
            if user.squad >= self.cost:
                return True
            else:
                return False


def cr1(user, other):
    user.add_ore(-8)
    other.add_ore(-8)
    return (False, False)

def cr2(user, other):
    user.add_mine(-1)
    other.add_mine(-1)
    return (False, False)

def cr3(user, other):
    user.add_mine(-1)
    user.add_wall(10)
    user.add_mana(5)
    return (False, False)

def cr4(user, other):
    user.add_ore(2)
    user.add_mana(2)
    return (True, False)
    
def cr5(user, other):
    user.add_wall(1)
    return (True, False)
    
def cr6(user, other):
    user.add_wall(1)
    user.add_tower(1)
    user.add_squad(2)
    return (False, False)

def cr7(user, other):
    user.add_mine(1)
    other.add_mine(1)
    user.add_mana(4)
    return (False, False)
    
def cr8(user, other):
    user.add_wall(3)
    return (False, False)

def cr9(user, other):
    user.add_wall(5)
    user.add_mana(-6)
    return (False, False)

def cr10(user, other):
    user.add_wall(4)
    return (False, False)
    
def cr11(user, other):
    if user.wall == 0:
        user.add_wall(6)
    else:
        user.add_wall(3)
    return (False, False)

def cr12(user, other):
    user.add_mine(1)
    return (False, False)

def cr13(user, other):
    if user.mine < other.mine:
        user.add_mine(2)
    else:
        user.add_mine(1)
    return (False, False)
    
def cr14(user, other):
    other.add_mine(-1)
    return (False, False)
    
def cr15(user, other):
    if user.mine < other.mine:
        user.add_mine(other.mine - user.mine)
    return (False, False)
    
def cr16(user, other):
    user.add_wall(6)
    return (False, False)
    
def cr17(user, other):
    if user.wall < other.wall:
        user.add_barracks(-1)
        user.add_tower(-2)
    elif user.wall > other.wall:
        other.add_barracks(-1)
        other.add_barracks(-2)
    else:
        user.add_barracks(-1)
        user.add_tower(-2)
        other.add_barracks(-1)
        other.add_barracks(-2)
    return (False, False)
    
def cr18(user, other):
    user.add_mine(2)
    return (False, False)
    
def cr19(user, other):
    user.add_wall(4)
    user.add_mine(1)
    return (False, False)

def cr20(user, other):
    user.add_wall(9)
    user.add_squad(-5)
    return (False, False)

def cr21(user, other):
    user.add_wall(-5)
    other.add_wall(-5)
    return (True, False)
    
def cr22(user, other):
    user.add_wall(8)
    return (False, False)
    
def cr23(user, other):
    user.add_monastery(1)
    return (True, False)
    
def cr24(user, other):
    user.add_wall(5)
    user.add_barracks(1)
    return (False, False)
    
def cr25(user, other):
    user.add_wall(7)
    user.add_mana(7)
    return (False, False)
    
def cr26(user, other):
    user.add_squad(6)
    user.add_wall(6)
    if user.barracks < other.barracks:
        user.add_barracks(1)
    return (False, False)
    
    
def cr27(user, other):
    user.add_wall(6)
    user.add_tower(3)
    return (False, False)
    
def cr28(user, other):
    user.add_wall(12)
    return (False, False)
    

def cr29(user, other):
    user.add_wall(7)
    other.make_damage(6)
    return (False, False)
    
def cr30(user, other):
    user.add_wall(8)
    user.add_tower(5)
    return (False, False)
    
    
def cr31(user, other):
    user.add_wall(15)
    return (False, False)
    
def cr32(user, other):
    user.wall, other.wall = other.wall, user.wall
    return (False, False)
    
def cr33(user, other):
    user.add_wall(6)
    other.make_damage(10)
    return (False, False)
    
def cr34(user, other):
    user.add_wall(20)
    user.add_tower(8)
    return (False, False)
    
def cr35(user, other):
    if user.tower < other.tower:
        user.add_tower(2)
    else:
        user.add_tower(1)
    return (False, False)
    
def cr36(user, other):
    user.add_tower(1)
    other.add_tower(1)
    user.add_mana(3)
    return (False, False)
    
def cr37(user, other):
    user.add_tower(1)
    return (True, False)

def cr38(user, other):
    # призма Сдать 1 карту, сбросить одну карту, играем снова
    return (False, False)
    
def cr39(user, other):
    user.add_tower(3)
    return (False, False)
    
    
def cr40(user, other):
    other.add_tower(-1)
    return (True, False)
    
def cr41(user, other):
    other.add_tower(-3)
    return (False, False)
    
def cr42(user, other):
    user.add_tower(-5)
    user.add_monastery(2)
    return (False, False)
    
def cr43(user, other):
    user.add_tower(5)
    return (False, False)
    
    
def cr44(user, other):
    user.add_monastery(1)
    return (False, False)
    
def cr45(user, other):
    user.add_tower(2)
    other.add_tower(-2)
    return (False, False)

def cr46(user, other):
    other.add_tower(-5)
    return (False, False)

def cr47(user, other):
    user.add_tower(7)
    user.add_ore(-10)
    return (False, False)
    
def cr48(user, other):
    user.add_tower(4)
    user.add_squad(-3)
    other.add_tower(-2)
    return (False, False)
    
def cr49(user, other):
    user.add_tower(-7)
    other.add_tower(-7)
    user.add_monastery(-1)
    other.add_monastery(-1)
    return (False, False)
    
def cr50(user, other):
    user.add_tower(8)
    return (False, False)
    
def cr51(user, other):
    user.add_monastery(1)
    user.add_tower(3)
    other.add_tower(1)
    return (False, False)
    
def cr52(user, other):
    user.add_tower(8)
    return (False, False)

def cr53(user, other):
    user.add_monastery(1)
    user.add_tower(3)
    user.add_wall(3)
    return (False, False)
    
def cr54(user, other):
    user.add_tower(5)
    other.add_ore(-6)
    return (False, False)
    
def cr55(user, other):
    max_mon = max(user.monastery, other.monastery)
    user.monastery = max_mon
    other.monastery = max_mon
    return (False, False)

def cr56(user, other):
    user.add_monastery(-1)
    other.add_tower(-9)
    return (False, False)
    
def cr57(user, other):
    user.add_tower(11)
    other.add_wall(-6)
    return (False, False)
    
def cr58(user, other):
    user.add_tower(5)
    user.add_monastery(1)
    return (False, False)
    
def cr59(user, other):
    user.add_tower(11)
    return (False, False)

def cr60(user, other):
    if user.tower > other.wall:
        other.add_tower(-8)
    else:
        user.make_damage(8)
        other.make_damage(8)
    return (False, False)
    
def cr61(user, other):
    user.add_tower(8)
    user.add_wall(3)
    return (False, False)
    
def cr62(user, other):
    user.add_tower(6)
    other.add_tower(-4)
    return (False, False)
    
def cr63(user, other):
    user.add_tower(8)
    user.add_barracks(1)
    return (False, False)
    
def cr64(user, other):
    user.add_tower(10)
    user.add_wall(5)
    user.add_squad(5)
    return (False, False)

def cr65(user, other):
    user.add_tower(15)
    return (False, False)
    
def cr66(user, other):
    user.add_tower(12)
    other.make_damage(6)
    return (False, False)
    
def cr67(user, other):
    user.add_tower(13)
    user.add_squad(6)
    user.add_ore(6)
    return (False, False)
    
def cr68(user, other):
    user.add_tower(20)
    return (False, False)

def cr69(user, other):
    user.add_squad(-6)
    other.add_squad(-6)
    return (False, False)
    
def cr70(user, other):
    user.add_barracks(1)
    other.add_barracks(1)
    user.add_squad(3)
    return (False, False)
    
def cr71(user, other):
    other.make_damage(4)
    user.add_mana(-3)
    return (False, False)
    
def cr72(user, other):
    other.make_damage(2)
    return (True, False)
    
def cr73(user, other):
    # Эльфы-скауты	Сдать 1 карту, сбросить одну карту, играем снова
    return (True, True)
    
    
def cr74(user, other):
    other.make_damage(3)
    user.add_mana(1)
    return (False, False)
    
def cr75(user, other):
    if user.wall > other.wall:
        other.make_damage(3)
    else:
        other.make_damage(2)
    return (False, False)

def cr76(user, other):
    other.make_damage(6)
    user.make_damage(3)
    return (False, False)

def cr77(user, other):
    user.add_barracks(1)
    return (False, False)
    
def cr78(user, other):
    other.make_damage(5)
    return (False, False)
    
    
def cr79(user, other):
    other.make_damage(8)
    user.add_tower(-3)
    return (False, False)
    
def cr80(user, other):
    other.add_tower(-3)
    user.make_damage(1)
    return (False, False)
    
def cr81(user, other):
    other.make_damage(4)
    user.add_wall(3)
    return (False, False)
    
def cr82(user, other):
    other.make_damage(6)
    return (False, False)

def cr83(user, other):
    other.make_damage(6)
    user.add_ore(-5)
    user.add_mana(-5)
    user.add_squad(-5)
    other.add_ore(-5)
    other.add_mana(-5)
    other.add_squad(-5)
    return (False, False)
    
def cr84(user, other):
    other.make_damage(6)
    other.add_squad(-3)
    return (False, False)
    
def cr85(user, other):
    other.add_tower(-4)
    return (False, False)
    

def cr86(user, other):
    other.make_damage(7)
    return (False, False)
    
def cr87(user, other):
    other.add_tower(-2)
    return (True, False)
    
    
def cr88(user, other):
    user.add_barracks(2)
    return (False, False)

def cr89(user, other):
    other.make_damage(2)
    user.add_wall(4)
    user.add_tower(2)
    return (False, False)
    
def cr90(user, other):
    if other.tower == 0:
        other.make_damage(10)
    else:
        other.make_damage(6)
    return (False, False)
    
def cr91(user, other):
    if user.monastery > other.monastery:
        other.make_damage(12)
    else:
        other.make_damage(8)
    return (False, False)
    
    
def cr92(user, other):
    other.make_damage(9)
    return (False, False)
    
def cr93(user, other):
    if user.wall > other.wall:
        other.add_tower(-6)
    else:
        other.make_damage(6)
    return (False, False)
    
def cr94(user, other):
    if other.wall > 10:
        other.make_damage(10)
    else:
        other.make_damage(7)
    return (False, False)

def cr95(user, other):
    other.make_damage(8)
    other.add_mine(-1)
    return (False, False)
    
def cr96(user, other):
    mana, ore = other.mana // 2, other.ore // 2
    other.add_mana(-mana)
    other.add_ore(-ore)
    user.add_mana(mana)
    user.add_ore(ore)
    return (False, False)
    
def cr97(user, other):
    other.make_damage(13)
    user.add_mana(-3)
    return (False, False)
    
def cr98(user, other):
    other.add_tower(-5)
    other.add_squad(-8)
    return (False, False)
    
def cr99(user, other):
    other.make_damage(10)
    user.add_wall(4)
    return (False, False)
    
def cr100(user, other):
    other.make_damage(10)
    other.add_squad(-5)
    other.add_barracks(-1)
    return (False, False)
    
    
def cr101(user, other):
    other.add_tower(-12)
    return (False, False)
    
def cr102(user, other):
    other.make_damage(20)
    other.add_mana(-10)
    other.add_barracks(-1)
    return (False, False)




all_cards = [Card('Бракованная руда', 0, cr1, 0), Card('Землетрясение', 0, cr2, 0), Card('Обвал рудника', 0, cr3, 0), Card('Счастливая монетка', 0, cr4, 0),
             Card('Благодатная почва', 1, cr5, 0), Card('Сад камней', 1, cr6, 0), Card('Новшества', 2, cr7, 0), Card('Обычная стена', 2, cr8, 0),
             Card('Сверхурочные', 2, cr9, 0), Card('Большая стена', 3, cr10, 0), Card('Фундамент', 3, cr11, 0), Card('Шахтеры', 3, cr12, 0),
             Card('Большая жила', 4, cr13, 0), Card('Обвал', 4, cr14, 0), Card('Кража технологий', 5, cr15, 0), Card('Усиленная стена', 5, cr16, 0),
             Card('Грунтовые воды', 6, cr17, 0), Card('Новое оборудование', 6, cr18, 0), Card('Гномы-шахтеры', 7, cr19, 0), Card('Рабский труд', 7, cr20, 0),
             Card('Толчки', 7, cr21, 0), Card('Великая стена', 8, cr22, 0), Card('Секретная пещера', 8, cr23, 0), Card('Галереи', 9, cr24, 0),
             Card('Магическая гора', 9, cr25, 0), Card('Казармы', 10, cr26, 0), Card('Поющий уголь', 11, cr27, 0), Card('Бастион', 13, cr28, 0),
             Card('Укрепления', 14, cr29, 0), Card('Новые успехи', 15, cr30, 0), Card('Величайшая стена', 16, cr31, 0), Card('Сдвиг', 17, cr32, 0),
             Card('Скаломет', 18, cr33, 0), Card('Сердце дракона', 24, cr34, 0),
             
             Card('Бижутерия', 0, cr35, 1), Card('Радуга', 0, cr36, 1), Card('Кварц', 1, cr37, 1), Card('Призма', 2, cr38, 1),
             Card('Аметист', 2, cr39, 1), Card('Дымчатый кварц', 2, cr40, 1), Card('Трещина', 2, cr41, 1), Card('Взрыв силы', 3, cr42, 1),
             Card('Рубин', 3, cr43, 1), Card('Ткачи заклинаний', 3, cr44, 1), Card('Затмение', 4, cr45, 1), Card('Копье', 4, cr46, 1),
             Card('Помощь в работе', 4, cr47, 1), Card('Вступление', 5, cr48, 1), Card('Раздоры', 5, cr49, 1), Card('Рудная жила', 5, cr50, 1),
             Card('Матрица', 6, cr51, 1), Card('ЭМЕРАЛЬД', 6, cr52, 1), Card('Гармония', 7, cr53, 1), Card('Мягкий камень', 7, cr54, 1),
             Card('Паритет', 7, cr55, 1), Card('Дробление', 8, cr56, 1), Card('Отвердение', 8, cr57, 1), Card('Жемчуг мудрости', 9, cr58, 1),
             Card('Сапфир', 10, cr59, 1), Card('Молния', 11, cr60, 1), Card('Кристальный щит', 12, cr61, 1), Card('Огненный рубин', 13, cr62, 1),
             Card('Эмпатия', 14, cr63, 1), Card('Монастырь', 15, cr64, 1), Card('Алмаз', 16, cr65, 1), Card('Сияющий камень', 17, cr66, 1),
             Card('Медитация', 18, cr67, 1), Card('Глаз дракона', 21, cr68, 1),
             
             Card('Коровье бешенство', 0, cr69, 2), Card('Полнолуние', 0, cr70, 2), Card('Гоблины', 1, cr71, 2), Card('Фея', 1, cr72, 2),
             Card('Эльфы-скауты', 2, cr73, 2), Card('Карлик', 2, cr74, 2), Card('Копьеносец', 2, cr75, 2), Card('Армия гоблинов', 3, cr76, 2),
             Card('Минотавр', 3, cr77, 2), Card('Орк', 3, cr78, 2), Card('Берсерк', 4, cr79, 2), Card('Гоблины-лучники', 4, cr80, 2),
             Card('Гномы', 5, cr81, 2), Card('Крушитель', 5, cr82, 2), Card('Черт', 5, cr83, 2), Card('Бешеная овца', 6, cr84, 2),
             Card('Маленькие змейки', 6, cr85, 2), Card('Огр', 6, cr86, 2), Card('Призрачная фея', 6, cr87, 2), Card('Тролль-наставник', 7, cr88, 2),
             Card('Гремлин в башне', 8, cr89, 2), Card('Жучара', 8, cr90, 2), Card('Единорог', 9, cr91, 2), Card('Оборотень', 9, cr92, 2),
             Card('Эльфы-лучники', 10, cr93, 2), Card('Едкое облако', 11, cr94, 2), Card('Камнееды', 11, cr95, 2), Card('Вор', 12, cr96, 2),
             Card('Воитель', 13, cr97, 2), Card('Суккубы', 14, cr98, 2), Card('Каменный гигант', 15, cr99, 2), Card('Вампир', 17, cr100, 2),
             Card('Всадник на пегасе', 18, cr101, 2), Card('Дракон', 25, cr102, 2)
             ]
             
map_name_too_card = {card.name.upper() : card for card in all_cards}


for i in range(len(all_cards)):
    all_cards[i].index = i


    
def id_of(card):
    return card.index
