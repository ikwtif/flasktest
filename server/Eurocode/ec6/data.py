


STONE_DIMENSIONS = ("190x90x40", "190x90x50", "190x90x57", "190x90x65", "190x90x90", "190x90x90", "190x140x140", "190x190x90", "190x190x140",
                    "290x90x90", "290x90x140", "290x90x240", "290x140x90", "290x140x140", "290x140x190", "290x140x240", "290x190x90",
                    "290x190x140", "290x190x190", "29x19x24", "390x70x190", "390x90x190", "390x140x190", "390x190x190", "390x290x190",
                    "490x70x240", "490x90x240", "490x140x240", "490x190x240", "490x240x240", "490x290x240", "600x70x200", "600x90x200",
                    "600x140x200", "600x140x250", "600x190x200", "600x190x250", "600x240x200", "600x290x200")

STONE_KINDS = ('baksteen', 'kalkzandsteen', 'betonsteen', 'cellenbeton')


STONE_GROUPS = ('groep 1', 'groep 2', 'groep 3')


MORTAR_KINDS = ('algemeen', 'lijm')

MORTAR_GROUPS = (2.5, 5, 8, 12, 20)

MASONRY_APPLICATION = ('stenen van categorie I en mortel, beiden met bijkomende productcertificatie',
                'stenen van categorie I zonder bijkomende productcertificatie en willekeurige mortel',
                'stenen van categorie II met willekeurige mortel')

MASONRY_SUPERVISION = ('normaal', 'uitgebreid')

FORMFACTOR = [[40, 0.8, 0.7, '-', '-', '-'],
                [50, 0.85, 0.75, 0.7, '-', '-'],
                [65, 0.95, 0.85, 0.75, 0.7, 0.65],
                [100, 1.15, 1, 0.9, 0.8, 0.75],
                [150, 1.3, 1.2, 1.1, 1, 0.95],
                [200, 1.45, 1.35, 1.25, 1.15, 1.1],
                [250, 1.55, 1.45, 1.35, 1.25, 1.15]
                ]

STONE_CONDITIONINGFACTOR = {'baksteen': 1,
                       'kalkzandsteen': 0.8,
                       'betonsteen': 1,
                       'cellenbeton': 1,
                       'x': 1, 'y': 1.2, 'z': 0.8}

STONE_WEIGHT_DENSITY = {'baksteen': 1900,
                       'kalkzandsteen': 1700,
                       'betonsteen': 1900,
                       'cellenbeton': 800,
                       'x': 1900, 'y': 1900, 'z': 1900}

MORTAR_WEIGHT_DENSITY = {'cementmortel': 2300,
                         'gipsmortel': 1800,
                         'kalk-cementmortel': 2000,
                         'kalkmortel': 1800
                         }