# encoding: utf-8
# Auther: zhoubowen.929
# Created At: Tue 17 January 2023 15:12:09 CST
# MagIc C0de: a1f3c4534099

"""
在一个每时刻都会随机给出相同数额硬币的世界
1. 会出现马太效应吗
2. 税收与福利会让世界变得更好吗

游戏规则：
基本规则
1. 初始X个玩家，每个玩家拥有Z个金币（coin），初始金币数量可以不相等
2. 每个时刻ti，每个玩家必须拿出ni个硬币，并随机递给另一位玩家
3. 直到最顶尖的20%玩家占有了80%的财富为止

一号世界：
游戏不停止，且可以负债

二号世界：
如果手中没有硬币，则不会再给出硬币，但可以接收

三号世界：
如果手中没有硬币，则退出游戏

四号世界：
增加税收，税金不会返回

五号世界：
增加税收与福利，税金以福利的形式发放
"""
import logging
LOG_FORMAT = '%(asctime)s - %(levelname)s : %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
import random
import copy
from tqdm import tqdm
import pickle

class Persion(object):
    def __init__(self, coins=0) -> None:
        self._coins = 0
        self._life = "alive" 
        
        self._id = self.random_dec(10)

    def gain_coins(self, num):
        if isinstance(num, int):
            self._coins += num
        else:
            raise ValueError("gain coin number must be integer!")
    
    def loss_coins(self, num):
        if isinstance(num, int):
            self._coins -= num
        else:
            raise ValueError("loss coin number must be integer!")
        
    @staticmethod
    def random_dec(length):
        result = str(random.randint(0, 10 ** length))
        if (len(result)<length):
            result = '0' * (length - len(result)) + result
        return int(result)

    @property 
    def id(self):
        return self._id
    
    @property
    def coins(self):
        return self._coins
    
    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, life_status):
        if life_status in ["alive", 'dead']:
            self._life = life_status
        else:
            raise ValueError("life status must be 'alive' or 'dead")
    
    def __str__(self) -> str:
        return "A player, with {} coins, {}".format(self._coins, self._life)
    
    def __hash__(self) -> int:
        return self._id

    def __eq__(self, __o: object) -> bool:
        if self._id == __o._id:
            return True
        return False
    
class WorldBase(object):
    def __init__(
            self,
            population = 1000,
            avg_wealth = 1000,
        ):
        self._total_wealth = population * avg_wealth
        self._population = population
    
        # 递归构建世界居民, 防止id重复
        self._citizen_dict = self._generate_citizens()
        self._turn = 0
        self._history = list()
        
    def __new__(cls, *args, **kwargs):
        raise AttributeError("该类不可实例化")

    def _generate_citizens(self):
        citizen_dict = dict()
        for _ in range(self._population):
            while True:
                new_born = Persion()
                if new_born.id not in citizen_dict:
                    citizen_dict[new_born.id] = new_born
                    break

        return citizen_dict

    def _distribute_wealth(self):
        pass
    
    @staticmethod
    def get_wealth_distribute(citizen_dict, matthew_count = None):
        """
        获取财富分配情况
        :param : citizen_dict: dict of citizens, {id: persion} 
        :param : matthew_count: 马太数量，来查验哪些头部玩家的财富
        return : 
        """
        wealth_leaderboard = list()
        for persion in citizen_dict.values():
            wealth_leaderboard.append((persion.id, persion.coins))
        
        sorted_list_of_tuple = sorted(wealth_leaderboard, key=lambda x: x[-1])
        
        if matthew_count is not None:
            total_population = len(citizen_dict)
            if matthew_count >= (total_population >> 1):
                raise ValueError("Error: matthew count must be little than half of total population!")

            sorted_array = np.array(sorted_list_of_tuple)
            top_wealth = np.sum(sorted_array[-matthew_count:, 1])
            total_wealth = np.sum(sorted_array[:, 1])
            
            return sorted_list_of_tuple, top_wealth / total_wealth
        else :
            return sorted_list_of_tuple
    
    @property
    def last_snapshot(self):
        try:
            return self._history[-1][-1]
        except:
            return None

    @property
    def year(self):
        return self._turn
    
    @property
    def population(self):
        return len(self._citizen_dict)
    
    def run_one_time_particles(self):
        self.run_x_time_particles(1, if_show_bar = False)
        return 
    
    def save_snapshot_gif(self, world_name):
        fig = plt.figure()
        
        ims = list()
        for turn, snapshot in tqdm(self._history):
            leaderborad = self.get_wealth_distribute(snapshot)
            wealth_distribute = np.array(leaderborad)[:, 1]
            ann = plt.annotate(text = turn, xy=(0.9, 0.9), xycoords='figure fraction')
            im = plt.bar(range(len(wealth_distribute)), wealth_distribute, color='b')
            ims.append(list(im) + [ann])

        historty_gif_data = ani.ArtistAnimation(fig, ims, interval=40, repeat=False)
        historty_gif_data.save(world_name + ".gif", writer='pillow')
        return 

    def save_history_data(self, world_name):
        with open(world_name + ".pkl", 'wb') as fo:
            pickle.dump(self._history, fo)
        return 

    def load_history_data(self, world_file):
        with open(world_file, 'rb') as fo:
            history_restored = pickle.load(fo)

        last_snapshot = history_restored[-1]
    
        self._citizen_dict = last_snapshot[1]
        self._turn = last_snapshot[0]
        self._history = history_restored

        self._total_wealth = sum([persion.coins for persion in self._citizen_dict.values()])
        self._population = len(self._citizen_dict)
        return 
            
class World2(WorldBase):
    """
    不会负债，如果手中没有硬币，则不会再给出硬币，但可以接收
    平均分配初始财富
    """
    def __init__(self, population=1000, avg_wealth=1000):
        super().__init__(population, avg_wealth)
        # 分配财富，财富分配规则每个世界可能不同
        self._distribute_wealth(avg_wealth=avg_wealth)

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def _distribute_wealth(self, *args, **kwargs):
        avg_wealth = kwargs["avg_wealth"]
        for person in self._citizen_dict.values():
            person.gain_coins(avg_wealth)
        return 
    
    def run_x_time_particles(self, turn, if_show_bar = False):
        iterator = range(turn)
        if if_show_bar:
            iterator = tqdm(iterator)

        citizen_list = list(self._citizen_dict.values())
        for _ in iterator:    
            for persion in citizen_list:
                if persion.coins <=0:
                    continue
                persion.loss_coins(1)
                random.choice(citizen_list).gain_coins(1)
            self._turn += 1
        
        self._history.append((self._turn, copy.deepcopy(self._citizen_dict)))
        return 
    
class World2(WorldBase):
    """
    游戏不停止，且可以负债
    平均分配初始财富
    """
    def __init__(self, population=1000, avg_wealth=1000):
        super().__init__(population, avg_wealth)
        # 分配财富，财富分配规则每个世界可能不同
        self._distribute_wealth(avg_wealth=avg_wealth)

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def _distribute_wealth(self, *args, **kwargs):
        avg_wealth = kwargs["avg_wealth"]
        for person in self._citizen_dict.values():
            person.gain_coins(avg_wealth)
        return 
    
    def run_x_time_particles(self, turn, if_show_bar = False):
        iterator = range(turn)
        if if_show_bar:
            iterator = tqdm(iterator)

        citizen_list = list(self._citizen_dict.values())
        for _ in iterator:    
            for persion in citizen_list:
                persion.loss_coins(1)
                random.choice(citizen_list).gain_coins(1)
            self._turn += 1
        
        self._history.append((self._turn, copy.deepcopy(self._citizen_dict)))
        return 

def io_test(data_list, text = None):
    # 绘制变化图
    fig = plt.figure()
    
    # plt.ion()
    for index, data_item in enumerate(data_list):
        fig.clf()
        # print(len(data_item))
        plt.bar(range(len(data_item)), data_item, color = 'b')
        # plt.ylim((990, 1010))    
        if text is not None:
            plt.annotate(text = text[index], xy=(0.9, 0.9), xycoords='figure fraction')
        plt.pause(0.01)
    # plt.ioff()

    plt.show()


if __name__ == '__main__':
    # world = World1()

    # bias_ratio = 0.2
    # while bias_ratio < 0.25:
    #     world.run_x_time_particles(100)
    #     leaderboard, bias_ratio = world.get_wealth_distribute(world.last_snapshot, 200) 
        
    #     if world.year % 1000 == 0:
    #         logging.info("当前是{}年，头部财富已经占据世界财富{:.4f}...".format(world.year, bias_ratio))
        
    # world.save_history_data("test_world")

    # world = World1()
    # world.load_history_data("test_world.pkl")
    # print(world.last_snapshot)
    # print(world.get_wealth_distribute(world.last_snapshot))
    pass