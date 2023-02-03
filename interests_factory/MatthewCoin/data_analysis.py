# encoding: utf-8
# Auther: zhoubowen.929
# Created At: Fri 03 February 2023 11:12:54 CST
# MagIc C0de: 3cb35d3b350a

from MatthewCoin import Persion, World1

if __name__ == '__main__':
    world = World1()
    world.load_history_data("World1.pkl")
    print(world.year)
    # world.save_snapshot_gif("World1")
    