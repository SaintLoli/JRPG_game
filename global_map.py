GLOBAL_MAP = {'house':              {'S': ['footpath', (12, 0)], 'tiles': [30, 247, 300, 67, 228]},
              'footpath':           {'N': ['house', (12, 30)], 'W': ('city', (29, 24)), 'tiles': [228, 72, 65]},
              'city':               {'E': ['footpath', (0, 16)], 'tiles': [30, 72, 67], 'S': ['footpath2', (15, 0)]},
              'castle':             {'S': ['city', (15, 11), (300, 280)], 'tiles': [511, 510, 441, 693, 694], 'coord': (14, 29)},
              'footpath2':          {'N': ['city', (7, 29)], 'S': ['road_to_the_cave', (15, 0)],'tiles': [32, 30]},
              'road_to_the_cave':   {'N': ['footpath2', (15, 29)], 'tiles': [68, 30]}}