import random

class Game:
    def __init__(self):
        self.winner = 0
        self.e1 = 0 # energy of player 1, etc.
        self.e2 = 0
        self.over = False # the game is still on
        self.requires = [0, 0, 0, 1, 1, 0, 1, 3, 2]
        self.text = [0, "攒一个", "盾", "一枪！", "（鄙视）打我呀！", "拜佛", "（爱心）给我吧", "’这是什么呀？‘，鸡！", "大盾秀！"]

    def act(self, action1, action2):
        # 1：攒豆；2：盾；3：枪；4：鄙视；5：拜佛；6：爱心；7：鸡！8：大盾

        # determine if the game is still on
        if self.determine(action1, action2):
            # player 1 wins
            self.over = True
            self.winner = 1
        elif self.determine(action2, action1):
            self.over = True
            self.winner = 2
        if action1 == 1:
            self.e1 += 1
        elif action1 in [3, 4, 6]:
            self.e1 -= 1
        elif action1 == 7:
            self.e1 -= 3
        elif action1 == 8:
            self.e1 -= 2

        if action2 == 1:
            self.e2 += 1
        elif action2 in [3, 4, 6]:
            self.e2 -= 1
        elif action2 == 7:
            self.e2 -= 3
        elif action2 == 8:
            self.e2 -= 2
        # 特判拜佛、爱心
        # 如果有一方拜佛而且没有死，那么对方豆肯定被清空。对拜同理。
        if action1 == 5:
            self.e2 = 0
        if action2 == 5:
            self.e1 = 0
        # 如果双方同时出爱心，则对撞，不产生效果
        if action1==6 and action2==6:
            pass
        if action1==6 and action2!=5:
            self.e1+=self.e2
            self.e2 = 0
        if action2==6 and action1!=5:
            self.e2+=self.e1
            self.e1 = 0

    def determine(self, act1, act2):
        # 不分顺序，看看1是否能将2打死
        if act1 == 2 and act2 == 5: return True # 拜佛拜死
        if act1 == 3 and (act2 in [1, 5, 6, 8]): return True # 开枪打死
        if act1 == 4 and act2 == 3: return True # 反弹
        if act1 == 5 and act2 == 4: return True # 鄙视佛祖
        if act1 == 7 and act2 <= 6: return True # 鸡无敌
        if act1 == 8 and act2 == 5: return True # 大盾秀
        return False


class GameAI(Game):
    def __init__(self):
        super().__init__()
        # 此时机器作为player2
    def act(self, action1):
        actions_available = [i for i in range(1, 9) if self.requires[i]<=self.e2]
        if self.e2 == 0 and self.e1 == 0:
            actions_available.remove(5)
            actions_available.remove(2)
        if self.e1 == 0:
            if 4 in actions_available:
                actions_available.remove(4) # 对方没豆就不鄙视
            if 5 in actions_available:
                actions_available.remove(5) # 同理，也不拜佛
            if 6 in actions_available:
                actions_available.remove(6) # 也不爱心
        if self.e2 >= 3 and self.e1 <= 1:
            actions_available = [7] # 可以鸡、对方无还手之力的时候，直接结束战斗
        act = random.choice(actions_available)   
        super().act(action1, act)
        return act
    
