from weapons import weapon_names
from weapons.inventory import item_names

starting_items = {
    "weapons": {weapon_name: 999 for weapon_name in weapon_names},
    "items": {item_name: 9999 for item_name in item_names},
}

spawnpoints = [
    # PLAYER 1
    [
        [750, 360],
        [550, 360],
        [350, 360]
    ],

    # PLAYER 2
    [
        [1200, 360],
        [1400, 360],
        [1600, 360]
    ]
]
