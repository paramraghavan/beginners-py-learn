from bag import *


bag_item = Bag();

bag_item.add('item1')
bag_item.add('item2')

print(f'repr {bag_item}')
print(f'type {type(bag_item)}')

for item in bag_item:
    print(item)