import sys
from os import (getcwd,
                environ,
                makedirs)
from os.path import (join,
                     exists,
                     isfile)
from sqlite3 import connect


USER_ARGS = {'user': 'TEXT',
             'cache': 'TEXT',
             'nfes': 'BLOB',
             'cls': 'TEXT',
             'product': 'TEXT',
             'types': 'TEXT',
             'sort': 'INTEGER',
             'prev_sort': 'INTEGER',
             'reverse': 'INTEGER',
             'cart': 'BLOB',
             'cart_size': 'INTEGER',
             'snum': 'INTEGER',
             'report_info': 'BLOB',
             'orders': 'BLOB',
             'order_num': 'INTEGER',
             'lists': 'BLOB'}


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = getcwd()
    return join(base_path, relative_path)


def make_directory_for_user_db():
    dir_path = join(environ['APPDATA'], 'FireSale')
    if not exists(dir_path):
         makedirs(dir_path)
    file_path = join(dir_path, 'USER_INFO.db')
    if not isfile(file_path):
        conn = connect(file_path)
        cur = conn.cursor()
        sql = f"""CREATE TABLE users
                  ({', '.join([f'{key} {USER_ARGS[key]}' for key in USER_ARGS])}, PRIMARY KEY (user));"""
        cur.execute(sql)
        conn.commit()
        conn.close()
    return file_path


DB = resource_path('NFES_ITEMS.db')

SEARCH_HEADER = ['', 'NFES #', 'DESCRIPTION', 'ITEM CLASS', 'ITEM PRODUCT', 'ITEM TYPE', 'PRICE', 'U/I', 'STD PACKAGE', 'CACHES AVAILABLE']
SQL_SEARCH_HEADER = ['NFES NO SHORT', 'DESCRIPTION', 'CLASS', 'PROD LINE', 'TYPE', '2021 PRICE', 'U/I', 'STD PK', 'CACHES STOCKING']

EXCEL_SQL_HEADER = [['"NFES NO SHORT"', 2], ['"TYPE"', 7], ['"NSN (IF ANY)"', 8], ['"DESCRIPTION"', 6], ['"U/I"', 4], ['"2021 PRICE"', 9],
                    ['"PROD LINE"', 10], ['"CLASS"', 11], ['"WT (LB)"', 12], ['"HT (IN)"', 13], ['"LN (IN)"', 14], ['"WD (IN)"', 15],
                    ['"CUBIC FT"', 16], ['"STD PK"', 17], ['"REMARKS"', 18], ['"CACHES STOCKING"', 19]]

EXCEL_FILL = [['S #', 1], ['QUANTITY', 3], ['PRICE TOTAL', 5]]

ITEM_COLS = {'NFES NO SHORT': 'NFES #',
             'TYPE': 'TYPE',
             'DESCRIPTION': 'DESCRIPTION',
             'U/I': 'U/I',
             '2021 PRICE': 'PRICE',
             'PROD LINE': 'PRODUCT',
             'CLASS': 'CLASS',
             'WT (LB)': 'WEIGHT (lb)',
             'HT (IN)': 'HEIGHT (in)',
             'LN (IN)': 'LENGTH (in)',
             'WD (IN)': 'WIDTH (in)',
             'CUBIC FT': 'CUBIC FEET',
             'STD PK': 'STANDARD PACK',
             'REMARKS': 'REMARKS',
             'CACHES STOCKING': 'CACHES STOCKED'}

CART_COLS = {'NFES NO SHORT': 'NFES #',
             'TYPE': 'TYPE',
             'DESCRIPTION': 'DESCRIPTION',
             'U/I': 'U/I',
             '2021 PRICE': 'PRICE PER ITEM',
             'STD PK': 'STANDARD PACK'}

CART_HEADER = ['S #', 'NFES #', 'TYPE', 'DESCRIPTION', 'U/I', 'PRICE PER ITEM', 'PRICE TOTAL', 'STANDARD PACK', 'QUANTITY']

ORDERS_HEADER = ['ORDER #', 'DATE ORDERED', 'TOTAL PRICE', 'TOTAL ITEM QTY']

LISTS_HEADER = ['LIST NAME', 'DATE CREATED', 'TOTAL PRICE', 'TOTAL ITEM QTY']

REPORT_HEADER = [['S #', 15], ['NFES #', 15], ['QUANTITY', 15], ['U/I', 15], ['DESCRIPTION', 130]]

CACHES = ['AKK', 'BFK', 'CDK', 'GBK', 'LGK', 'LSK', 'NCK', 'NEK', 'NRK', 'NWK', 'PFK', 'RMK', 'SAK', 'SFK', 'WFK']

CACHE_NAMES = {"AKK": "Alaska",
               "BFK": "Billings",
               "CDK": "Coeur d'Alene",
               "GBK": "Great Basin",
               "LGK": "La Grande",
               "LSK": "Southern California",
               "NCK": "Northern California",
               "NEK": "Northeast",
               "NRK": "Northern Rockies",
               "NWK": "Northwest",
               "PFK": "Southwest Prescott",
               "RMK": "Rocky Mountain",
               "SAK": "Southern",
               "SFK": "Southwest Silver City",
               "WFK": "Wenatchee"}


ORDER_INFO = {'1Incident Order Number': None,
              '1Issue Number': None,
              '2Incident Name': None,
              '2Accounting/Management Code': None,
              '3Agency Billing Address Name': None,
              '3Agency Shipping Address Name': None,
              '4Unit Name': None,
              '4Unit Name_': None,
              '5Billing Address': None,
              '5Address (No PO Box)': None,
              '6City': None,
              '6State': None,
              '6Zip': None,
              '6City_': None,
              '6State_': None,
              '6Zip_': None,
              '7Authorized By': None,
              '7Title': None,
              '7Person Ordering': None,
              '7Title_': None,
              '8Telephone Number': None,
              '8Telephone Number_': None,
              '9Date/Time Ordered': None,
              '9Date/Time Required': None,
              '0Requested Method of Delivery': None,
              }

CACHE_INFO = {'AKK': {'3Agency Shipping Address Name': 'AKK',
                      '4Unit Name_': 'ALASKA INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': 'Bldg. 1544 Gaffney Road',
                      '6City_': 'Fort Wainwright',
                      '6State_': 'Alaska',
                      '6Zip_': '99707',
                      '8Telephone Number_': '907-356-5742'},
              'BFK': {'3Agency Shipping Address Name': 'BFK',
                      '4Unit Name_': 'BILLINGS INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '551 Northview Drive',
                      '6City_': 'Billings',
                      '6State_': 'Montana',
                      '6Zip_': '59105',
                      '8Telephone Number_': '406-896-2870'},
              'CDK': {'3Agency Shipping Address Name': 'CDK',
                      '4Unit Name_': "COEUR D'ALENE INCIDENT SUPPORT CACHE",
                      '5Address (No PO Box)': '3328 W Industrial Loop',
                      '6City_': "Coeur D'Alene",
                      '6State_': 'Idaho',
                      '6Zip_': '83815',
                      '8Telephone Number_': '208-666-8694'},
              'GBK': {'3Agency Shipping Address Name': 'GBK',
                      '4Unit Name_': 'GREAT BASIN AREA INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '3833 S Development Avenue',
                      '6City_': 'Boise',
                      '6State_': 'Idaho',
                      '6Zip_': '83705',
                      '8Telephone Number_': '208-387-5104'},
              'LGK': {'3Agency Shipping Address Name': 'LGK',
                      '4Unit Name_': 'LA GRANDE INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '59973 Downs Road',
                      '6City_': 'La Grande',
                      '6State_': 'Oregon',
                      '6Zip_': '97850',
                      '8Telephone Number_': '541-975-5420'},
              'LSK': {'3Agency Shipping Address Name': 'LSK',
                      '4Unit Name_': 'SOUTHERN CALIFORNIA INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '1310 S Cucamonga Avenue',
                      '6City_': 'Ontario',
                      '6State_': 'California',
                      '6Zip_': '91761',
                      '8Telephone Number_': '909-930-3238'},
              'NCK': {'3Agency Shipping Address Name': 'NCK',
                      '4Unit Name_': 'NORTHERN CALIFORNIA INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '6101 Airport Road',
                      '6City_': 'Redding',
                      '6State_': 'California',
                      '6Zip_': '96002',
                      '8Telephone Number_': '530-226-2850'},
              'NEK': {'3Agency Shipping Address Name': 'NEK',
                      '4Unit Name_': 'NORTHEAST AREA INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '402 11th Street SE',
                      '6City_': 'Grand Rapids',
                      '6State_': 'Minnesota',
                      '6Zip_': '55744',
                      '8Telephone Number_': '218-322-2775'},
              'NRK': {'3Agency Shipping Address Name': 'NRK',
                      '4Unit Name_': 'NORTHERN ROCKIES AREA INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '5765 West Broadway',
                      '6City_': 'Missoula',
                      '6State_': 'Montana',
                      '6Zip_': '59808',
                      '8Telephone Number_': '406-329-4949'},
              'NWK': {'3Agency Shipping Address Name': 'NWK',
                      '4Unit Name_': 'NORTHWEST AREA INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '1740 SE Ochoco Way',
                      '6City_': 'Redmond',
                      '6State_': 'Oregon',
                      '6Zip_': '97756',
                      '8Telephone Number_': '541-504-7234'},
              'PFK': {'3Agency Shipping Address Name': 'PFK',
                      '4Unit Name_': 'SOUTHWEST AREA PRESCOTT INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '2400 Melville Drive',
                      '6City_': 'Prescott',
                      '6State_': 'Arizona',
                      '6Zip_': '86301',
                      '8Telephone Number_': '928-777-5630'},
              'RMK': {'3Agency Shipping Address Name': 'RMK',
                      '4Unit Name_': 'ROCKY MOUNTAIN AREA INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': 'DFC, BLDG 810, Door N27',
                      '6City_': 'Lakewood',
                      '6State_': 'Colorado',
                      '6Zip_': '80225',
                      '8Telephone Number_': '303-202-4940'},
              'SAK': {'3Agency Shipping Address Name': 'SAK',
                      '4Unit Name_': 'SOUTHERN AREA INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '788 Sublimity School Road',
                      '6City_': 'London',
                      '6State_': 'Kentucky',
                      '6Zip_': '40744',
                      '8Telephone Number_': '606-878-7430'},
              'SFK': {'3Agency Shipping Address Name': 'SFK',
                      '4Unit Name_': 'SOUTHWEST AREA SILVER CITY INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '158 Airport Road',
                      '6City_': 'Hurley',
                      '6State_': 'New Mexico',
                      '6Zip_': '88043',
                      '8Telephone Number_': '575-538-5611'},
              'WFK': {'3Agency Shipping Address Name': 'WFK',
                      '4Unit Name_': 'WENATCHEE INCIDENT SUPPORT CACHE',
                      '5Address (No PO Box)': '4890 Contractors Road',
                      '6City_': 'East Wenatchee',
                      '6State_': 'Washington',
                      '6Zip_': '98802',
                      '8Telephone Number_': '575-538-5611'},
              }

NFES_RNG = [['0000', '1000'], ['1001', '2000'], ['2001', '3000'], ['3001', '4000'], ['4001', '5000'],
            ['5001', '6000'], ['6001', '7000'], ['7001', '8000'], ['8001', '9000'], ['9001', '9999']]

CLASS = ['CONSUMABLE', 'DURABLE', 'TRACKABLE']

CATEGORIES = {'all': {'all': {'STAND', 'STAPLES', 'EARPHONE', 'HANDTRUCK', 'VALVE', 'TAPE', 'INSTRUCTIONS',
                              'FLY', 'SPRAY', 'PLUG', 'APPLICATOR', 'BRUSH', 'CARTRIDGE', 'POST',
                              'STEREOSCOPE', 'WATERBAG', 'COMPASS', 'SHELTER', 'GENERATOR', 'LID', 'NOMEX',
                              'CHAPS', 'STONE', 'COT', 'TABLE', 'LEAD LINE', 'GLASSES', 'ANTENNA',
                              'GUARD', 'TOWEL', 'HEATER', 'FILING GUIDE', 'FORM', 'WRENCH', 'TOILET',
                              'HARNESS', 'PLACARD', 'THERMOMETER', 'WASHCLOTH', 'FUEL LINE ASSEMBLY', 'PLATE', 'BERM',
                              'SURGE PROTECTOR', 'BOOKLET', 'PLANS', 'SPOON', 'TANK', 'CHAINSAW', 'GAUGE',
                              'LABELS', 'BLANKET', 'CORD', 'BRIEFCASE', 'SCANNER', 'BOTTLE', 'KIT',
                              'FOOD', 'HOLDER', 'STRAP', 'BANDS', 'REGULATOR', 'GUIDE -INTERAGENCY AVIATION USER POCKET (2015)', 'HELMET',
                              'SHIELD', 'SORTER', 'MAT', 'COUPLER', 'DINING PACKET', 'VISOR LOCK ASSEMBLY', 'VISOR',
                              'MITTS', 'MICROPHONE ELEMENT', 'SANITIZER', 'BOARD', 'CONTAINER', 'LABEL', 'SOCK',
                              'STRAINER', 'NAILS', 'FLASHLIGHT', 'BRACKET', 'TAG', 'EXTENSION', 'CLIPBOARD',
                              'EAR SEALS', 'GLASS', 'CAN', 'ADAPTER', 'DRUM', 'ATLAS', 'FLOODLIGHT',
                              'FAN', 'HOSE ROLLER', 'FILE', 'CLIP', 'MIRROR', 'BULB', 'INCREASER',
                              'GUN', 'REPELLENT', 'CHAIR', 'SUGAR', 'WINDSHIELD', 'CORD ASSEMBLY', 'TIP',
                              'CUTTER', 'ENVELOPE', 'TORCH', 'CLAMP', 'LAUNCHER', 'PAD', 'BEACON',
                              'BOOM SUPPORT', 'CAP', 'SCREWS', 'CREAM', 'SQUARE', 'RACK', 'DISPENSER',
                              'LID REMOVER', 'CALCULATOR', 'VEST', 'FOLDER', 'SPOUT', 'TACK', 'CONE',
                              'PRIMER', 'SWIVEL', 'HIGHLIGHTERS', 'SHEARS', 'RESPIRATOR', 'FLAGGING', 'ROPE',
                              'PUNCH', 'RAKE', 'SPLINT', 'AXE', 'FLIGHT SUIT', 'SOAP', 'HANDLE',
                              'TIE', 'GUIDE', 'PALLET JACK', 'PENCIL', 'HOSE', 'BOX', 'SWATTER',
                              'BINDER', 'PANELS', 'ANEMOMETER', 'PULLER', 'RIBBON', 'PORTFOLIO', 'FLARE',
                              'BLOWER', 'DRIVER', 'BAR', 'COFFEE', 'CHARGER', 'WIRE', 'BAND',
                              'INDICATOR', 'HANDBOOK', 'HAMMER', 'FUSEE', 'BATTERY', 'BOOM', 'SUGAR SUBSTITUTE',
                              'JACKET', 'WRAP', 'CUP', 'SAW', 'DATA PACKAGE', 'SHARPENER', 'SPRAYER',
                              'EARPLUGS', 'PAPER', 'DOT CHART 16', 'MASK', 'PEN', 'NET', 'RUBBER BAND',
                              'REDUCER', 'PIN', 'PSYCHROMETER', 'RAGS', 'SUSPENSION', 'CARTON', 'BASIN',
                              'CLOTH', 'FRAME', 'LANTERN', 'FOAM', 'TRACK', 'FUEL', 'PULASKI',
                              'CLOCK', 'FLASHDRIVE', 'FUNNEL', 'STOVE', 'POUCH', 'MAINFRAME', 'FLATWARE SET',
                              'LAYER ASSEMBLY', 'LITTER', 'MC LEOD', 'JUG', 'FORMS', 'MESS GEAR', 'RAG',
                              'GOGGLES', 'COUNTER', 'RING', 'GASKET', 'KNIFE', 'EASEL', 'STAPLER',
                              'SEAL', 'EARCUP SET', 'SCALE', 'WINDSOCK', 'CALENDAR', 'FILTERS', 'PLIERS',
                              'FITTING', 'OPENER', 'PACK', 'HEADLAMP', 'PACKSACK', 'OIL', 'LIGHTSTICK',
                              'FENCE', 'REMOVER', 'GRID', 'STAKES', 'LEAD', 'CUSHION', 'TRAILER',
                              'SCREWDRIVER', 'LIP BALM', 'PAMPHLET', 'POLE', 'TOOL', 'FOOT POWDER', 'CHEST',
                              'HOE', 'PACKBOARD', 'MAP', 'BELT', 'DISINFECTANT', 'EXTINGUISHER', 'SPILL KIT',
                              'TENT', 'COMPRESS', 'PUMP', 'CASE', 'COUPLING', 'CALIBRATOR', 'WATERBAG ASSEMBLY',
                              'WIPES', 'AERIAL IGNITION DEV', 'TEE', 'SHEATH', 'LADDER', 'WEDGE', 'LINER',
                              'SCALES', 'BLADE', 'BAG', 'SPACER', 'IGNITER', 'PAIL', 'RULER',
                              'SHOVEL', 'CARD', 'CABLE ASSEMBLY', 'MARKER', 'NOZZLE', 'BASKET', 'TUB',
                              'URN', 'SIGN', 'GLOVES', 'COVER', 'CANTEEN', 'SHEETING', 'PLEXIGLASS',
                              'PRINTER/PLOTTER', 'TEST', 'SHROUD', 'TIE WRAPS'},
                      'GENERAL': {'STAND', 'VALVE', 'TAPE', 'FLY', 'SPRAY', 'PLUG', 'CARTRIDGE',
                                  'POST', 'COMPASS', 'LID', 'TABLE', 'TOILET', 'WRENCH', 'HARNESS',
                                  'THERMOMETER', 'SURGE PROTECTOR', 'GAUGE', 'TANK', 'BLANKET', 'CORD', 'BOTTLE',
                                  'KIT', 'HOLDER', 'STRAP', 'BANDS', 'REGULATOR', 'SHIELD', 'MITTS',
                                  'SANITIZER', 'BOARD', 'CONTAINER', 'EXTENSION', 'NAILS', 'BRACKET', 'FLASHLIGHT',
                                  'CAN', 'DRUM', 'FLOODLIGHT', 'HOSE ROLLER', 'MIRROR', 'BULB', 'GUN',
                                  'CHAIR', 'REPELLENT', 'WINDSHIELD', 'TORCH', 'LAUNCHER', 'BEACON', 'SCREWS',
                                  'SQUARE', 'RACK', 'CONE', 'CALCULATOR', 'SPOUT', 'ROPE', 'FLAGGING',
                                  'HANDLE', 'TIE', 'PALLET JACK', 'HOSE', 'FLARE', 'BLOWER', 'BAR',
                                  'WIRE', 'BAND', 'WRAP', 'SPRAYER', 'RUBBER BAND', 'RAGS', 'CARTON',
                                  'CLOTH', 'FRAME', 'FUEL', 'FOAM', 'FLASHDRIVE', 'FUNNEL', 'STOVE',
                                  'POUCH', 'MAINFRAME', 'JUG', 'RAG', 'RING', 'GASKET', 'KNIFE',
                                  'SEAL', 'FILTERS', 'FITTING', 'PACKSACK', 'OIL', 'LIGHTSTICK', 'FENCE',
                                  'STAKES', 'TRAILER', 'CHEST', 'PACKBOARD', 'DISINFECTANT', 'SPILL KIT', 'PUMP',
                                  'CASE', 'LADDER', 'SHEATH', 'WEDGE', 'SCALES', 'BAG', 'IGNITER',
                                  'PAIL', 'MARKER', 'NOZZLE', 'BASKET', 'TUB', 'URN', 'GLOVES',
                                  'COVER', 'PRINTER/PLOTTER', 'TIE WRAPS'},
                      'WATER': {'FITTING', 'VALVE', 'ADAPTER', 'APPLICATOR', 'WATERBAG', 'HOSE ROLLER', 'INCREASER',
                                'TIP', 'REDUCER', 'PUMP', 'WRENCH', 'CLAMP', 'COUPLING', 'WATERBAG ASSEMBLY',
                                'TEE', 'LINER', 'CAP', 'BAG', 'TANK', 'CALCULATOR', 'PAIL',
                                'PRIMER', 'NOZZLE', 'KIT', 'COUPLER', 'GASKET', 'HOSE', 'SOCK',
                                'STRAINER'},
                      'TOOLS': {'PLIERS', 'DRIVER', 'BAR', 'HAMMER', 'FILE', 'SAW', 'STONE',
                                'SCREWDRIVER', 'TOOL', 'HOE', 'CUTTER', 'FILING GUIDE', 'WRENCH', 'FRAME',
                                'SHEATH', 'PULASKI', 'BLADE', 'GAUGE', 'SHOVEL', 'MC LEOD', 'RAKE',
                                'AXE', 'HANDLE', 'GUIDE', 'KNIFE', 'SWATTER', 'PULLER'},
                      'AVIATION': {'EAR SEALS', 'EARPHONE', 'EARCUP SET', 'ADAPTER', 'BOOM', 'CUSHION', 'LEAD LINE',
                                   'CORD ASSEMBLY', 'NET', 'PIN', 'PAD', 'FUEL', 'AERIAL IGNITION DEV', 'TRACK',
                                   'BOOM SUPPORT', 'SCALES', 'SPACER', 'BAG', 'PLANS', 'CABLE ASSEMBLY', 'SCANNER',
                                   'SWIVEL', 'KIT', 'LAYER ASSEMBLY', 'PANELS', 'HOLDER', 'STRAP', 'VISOR LOCK ASSEMBLY',
                                   'HELMET', 'COVER', 'VISOR', 'MICROPHONE ELEMENT', 'BOARD', 'TEST', 'BRACKET',
                                   'WINDSOCK'},
                      'CAMP': {'CAN', 'HANDTRUCK', 'TAPE', 'FLY', 'BRUSH', 'FUSEE', 'FAN',
                               'GENERATOR', 'LID', 'COT', 'POLE', 'PAPER', 'CHEST', 'TOWEL',
                               'EXTINGUISHER', 'TENT', 'HEATER', 'BASIN', 'THERMOMETER', 'WASHCLOTH', 'LANTERN',
                               'BERM', 'BAG', 'LID REMOVER', 'STOVE', 'CORD', 'KIT', 'JUG',
                               'MAT', 'SOAP', 'SHEETING', 'CONTAINER', 'NAILS', 'RIBBON'},
                      'BATTERIES': {'BATTERY'},
                      'OFFICE ': {'STAPLES', 'GLASS', 'TAPE', 'REMOVER', 'ATLAS', 'GRID', 'STEREOSCOPE',
                                  'INDICATOR', 'LEAD', 'FILE', 'JACKET', 'CLIP', 'SHARPENER', 'PAPER',
                                  'MAP', 'PEN', 'PIN', 'ENVELOPE', 'PAD', 'WIPES', 'CLOCK',
                                  'DISPENSER', 'CALCULATOR', 'RULER', 'FOLDER', 'TACK', 'BRIEFCASE', 'MARKER',
                                  'KIT', 'HIGHLIGHTERS', 'SHEARS', 'PUNCH', 'BANDS', 'SORTER', 'COUNTER',
                                  'PENCIL', 'BOX', 'EASEL', 'PLEXIGLASS', 'STAPLER', 'BINDER', 'PORTFOLIO',
                                  'SCALE', 'CLIPBOARD'},
                      'SUBSIST': {'OPENER', 'LIP BALM', 'MESS GEAR', 'PLATE', 'COFFEE', 'FOOT POWDER', 'TOWEL',
                                  'CAP', 'SUGAR', 'DINING PACKET', 'CREAM', 'CANTEEN', 'SPOON', 'SUGAR SUBSTITUTE',
                                  'FLATWARE SET', 'CUP', 'FOOD'},
                      'PPE': {'PACK', 'SHELTER', 'NOMEX', 'CHAPS', 'GLASSES', 'EARPLUGS', 'BELT',
                              'MASK', 'SUSPENSION', 'CASE', 'HARNESS', 'LINER', 'BAG', 'VEST',
                              'RESPIRATOR', 'STRAP', 'HELMET', 'GLOVES', 'GOGGLES', 'FLIGHT SUIT', 'SHROUD',
                              'HEADLAMP'},
                      'MEDICAL': {'PAD', 'SPLINT', 'COMPRESS', 'LITTER', 'KIT', 'CASE'},
                      'PUBLICATION': {'SIGN', 'FORMS', 'PAMPHLET', 'GUIDE -INTERAGENCY AVIATION USER POCKET (2015)', 'INSTRUCTIONS', 'DOT CHART 16', 'GUIDE',
                                      'BOOKLET', 'HANDBOOK', 'CARD', 'FORM', 'CALENDAR'},
                      'PUMP': {'PUMP', 'KIT', 'FUEL LINE ASSEMBLY'},
                      'CHAINSAW': {'FILE', 'GUARD', 'CHAINSAW', 'KIT'},
                      'FORM/SIGN': {'PLACARD', 'LABELS', 'LABEL', 'FORM', 'KIT', 'TAG'},
                      'WEATHER': {'ANEMOMETER', 'CALIBRATOR', 'KIT', 'PSYCHROMETER'},
                      'NIICD': {'KIT'},
                      'COMMUNICATION': {'CHARGER', 'HOLDER', 'DATA PACKAGE', 'ANTENNA'}
                      },

              'DURABLE': {'all': {'STAND', 'HANDTRUCK', 'VALVE', 'TAPE', 'FLY', 'APPLICATOR', 'STEREOSCOPE',
                                  'POST', 'WATERBAG', 'COMPASS', 'SHELTER', 'LID', 'NOMEX', 'CHAPS',
                                  'TABLE', 'COT', 'LEAD LINE', 'ANTENNA', 'GUARD', 'HEATER', 'FILING GUIDE',
                                  'WRENCH', 'TOILET', 'HARNESS', 'THERMOMETER', 'FUEL LINE ASSEMBLY', 'BERM', 'GAUGE',
                                  'TANK', 'BLANKET', 'CORD', 'BRIEFCASE', 'KIT', 'HOLDER', 'STRAP',
                                  'REGULATOR', 'MAT', 'HELMET', 'SHIELD', 'SORTER', 'COUPLER', 'MITTS',
                                  'BOARD', 'CONTAINER', 'SOCK', 'EXTENSION', 'STRAINER', 'FLASHLIGHT', 'BRACKET',
                                  'CLIPBOARD', 'GLASS', 'CAN', 'ADAPTER', 'FLOODLIGHT', 'FAN', 'HOSE ROLLER',
                                  'MIRROR', 'INCREASER', 'CHAIR', 'WINDSHIELD', 'TIP', 'CUTTER', 'TORCH',
                                  'CLAMP', 'BEACON', 'CAP', 'SQUARE', 'RACK', 'CONE', 'VEST',
                                  'SPOUT', 'PRIMER', 'SWIVEL', 'SHEARS', 'PUNCH', 'RAKE', 'SPLINT',
                                  'AXE', 'FLIGHT SUIT', 'GUIDE', 'PALLET JACK', 'HOSE', 'SWATTER', 'BINDER',
                                  'PANELS', 'ANEMOMETER', 'PULLER', 'DRIVER', 'BAR', 'CHARGER', 'INDICATOR',
                                  'HAMMER', 'SAW', 'DATA PACKAGE', 'SPRAYER', 'NET', 'REDUCER', 'PSYCHROMETER',
                                  'FRAME', 'LANTERN', 'PULASKI', 'CLOCK', 'FUNNEL', 'STOVE', 'POUCH',
                                  'MAINFRAME', 'LITTER', 'MC LEOD', 'JUG', 'COUNTER', 'RING', 'GASKET',
                                  'KNIFE', 'EASEL', 'STAPLER', 'SCALE', 'WINDSOCK', 'HEADLAMP', 'PLIERS',
                                  'FITTING', 'OPENER', 'PACK', 'PACKSACK', 'FENCE', 'REMOVER', 'GRID',
                                  'STAKES', 'SCREWDRIVER', 'POLE', 'TOOL', 'HOE', 'CHEST', 'BELT',
                                  'PACKBOARD', 'MAP', 'EXTINGUISHER', 'TENT', 'PUMP', 'CASE', 'COUPLING',
                                  'CALIBRATOR', 'WATERBAG ASSEMBLY', 'TEE', 'SHEATH', 'LADDER', 'SCALES', 'LINER',
                                  'BAG', 'IGNITER', 'PAIL', 'RULER', 'SHOVEL', 'MARKER', 'NOZZLE',
                                  'BASKET', 'TUB', 'URN', 'COVER', 'CANTEEN', 'PLEXIGLASS', 'SHROUD'},
                          'GENERAL': {'STAND', 'FITTING', 'BRACKET', 'PACKSACK', 'CAN', 'BAR', 'VALVE',
                                      'FENCE', 'TAPE', 'FLY', 'CONE', 'FLOODLIGHT', 'STAKES', 'POST',
                                      'COMPASS', 'LID', 'TABLE', 'SPRAYER', 'MIRROR', 'CHAIR', 'CHEST',
                                      'PACKBOARD', 'WINDSHIELD', 'PUMP', 'TORCH', 'TOILET', 'WRENCH', 'CASE',
                                      'HARNESS', 'THERMOMETER', 'FRAME', 'BEACON', 'SHEATH', 'LADDER', 'SCALES',
                                      'BAG', 'SQUARE', 'RACK', 'TANK', 'FUNNEL', 'IGNITER', 'PAIL',
                                      'BLANKET', 'SPOUT', 'MAINFRAME', 'STOVE', 'MARKER', 'CORD', 'KIT',
                                      'NOZZLE', 'POUCH', 'BASKET', 'GAUGE', 'URN', 'HOLDER', 'STRAP',
                                      'JUG', 'REGULATOR', 'TUB', 'SHIELD', 'COVER', 'RING', 'KNIFE',
                                      'MITTS', 'HOSE', 'PALLET JACK', 'BOARD', 'CONTAINER', 'EXTENSION', 'FLASHLIGHT'},
                          'WATER': {'FITTING', 'VALVE', 'ADAPTER', 'APPLICATOR', 'WATERBAG', 'HOSE ROLLER', 'INCREASER',
                                    'TIP', 'REDUCER', 'PUMP', 'WRENCH', 'CLAMP', 'COUPLING', 'WATERBAG ASSEMBLY',
                                    'TEE', 'LINER', 'CAP', 'BAG', 'TANK', 'PAIL', 'PRIMER',
                                    'NOZZLE', 'COUPLER', 'GASKET', 'HOSE', 'SOCK', 'STRAINER'},
                          'TOOLS': {'PLIERS', 'DRIVER', 'BAR', 'HAMMER', 'SAW', 'SCREWDRIVER', 'TOOL',
                                    'HOE', 'CUTTER', 'FILING GUIDE', 'WRENCH', 'FRAME', 'SHEATH', 'PULASKI',
                                    'GAUGE', 'SHOVEL', 'MC LEOD', 'RAKE', 'AXE', 'GUIDE', 'KNIFE',
                                    'SWATTER', 'PULLER'},
                          'CAMP': {'HANDTRUCK', 'CAN', 'TAPE', 'FLY', 'FAN', 'LID', 'COT',
                                   'POLE', 'CHEST', 'EXTINGUISHER', 'TENT', 'HEATER', 'THERMOMETER', 'LANTERN',
                                   'BERM', 'BAG', 'STOVE', 'CORD', 'KIT', 'JUG', 'MAT'},
                          'PPE': {'HARNESS', 'PACK', 'HELMET', 'FLIGHT SUIT', 'HEADLAMP', 'BELT', 'LINER',
                                  'BAG', 'VEST', 'SHELTER', 'SHROUD', 'NOMEX', 'CHAPS', 'CASE'},
                          'PUMP': {'KIT', 'FUEL LINE ASSEMBLY'},
                          'OFFICE ': {'GLASS', 'TAPE', 'REMOVER', 'GRID', 'STEREOSCOPE', 'INDICATOR', 'MAP',
                                      'CLOCK', 'RULER', 'BRIEFCASE', 'SHEARS', 'PUNCH', 'SORTER', 'COUNTER',
                                      'EASEL', 'PLEXIGLASS', 'STAPLER', 'BINDER', 'SCALE', 'CLIPBOARD'},
                          'AVIATION': {'LEAD LINE', 'HELMET', 'ADAPTER', 'SCALES', 'BAG', 'NET', 'PANELS',
                                       'SWIVEL', 'BRACKET', 'KIT', 'WINDSOCK'},
                          'SUBSIST': {'OPENER', 'CANTEEN'},
                          'CHAINSAW': {'GUARD', 'KIT'},
                          'MEDICAL': {'LITTER', 'KIT', 'SPLINT', 'CASE'},
                          'WEATHER': {'ANEMOMETER', 'CALIBRATOR', 'KIT', 'PSYCHROMETER'},
                          'NIICD': {'KIT'},
                          'COMMUNICATION': {'CHARGER', 'HOLDER', 'DATA PACKAGE', 'ANTENNA'}
                          },

              'CONSUMABLE': {'all': {'STAPLES', 'EARPHONE', 'TAPE', 'INSTRUCTIONS', 'SPRAY', 'PLUG', 'BRUSH',
                                     'CARTRIDGE', 'SHELTER', 'STONE', 'GLASSES', 'TOWEL', 'FORM', 'PLACARD',
                                     'WASHCLOTH', 'PLATE', 'SURGE PROTECTOR', 'BOOKLET', 'PLANS', 'SPOON', 'GAUGE',
                                     'LABELS', 'BLANKET', 'CORD', 'BOTTLE', 'KIT', 'FOOD', 'HOLDER',
                                     'STRAP', 'BANDS', 'VISOR LOCK ASSEMBLY', 'GUIDE -INTERAGENCY AVIATION USER POCKET (2015)', 'HELMET', 'DINING PACKET', 'VISOR',
                                     'MICROPHONE ELEMENT', 'SANITIZER', 'BOARD', 'CONTAINER', 'LABEL', 'NAILS', 'TAG',
                                     'EAR SEALS', 'CAN', 'ADAPTER', 'DRUM', 'ATLAS', 'FILE', 'CLIP',
                                     'BULB', 'GUN', 'REPELLENT', 'SUGAR', 'CORD ASSEMBLY', 'ENVELOPE', 'PAD',
                                     'BOOM SUPPORT', 'CAP', 'SCREWS', 'CREAM', 'DISPENSER', 'LID REMOVER', 'CALCULATOR',
                                     'TACK', 'FOLDER', 'VEST', 'SPOUT', 'HIGHLIGHTERS', 'ROPE', 'RESPIRATOR',
                                     'FLAGGING', 'SOAP', 'HANDLE', 'TIE', 'GUIDE', 'PENCIL', 'BOX',
                                     'PORTFOLIO', 'RIBBON', 'FLARE', 'COFFEE', 'WIRE', 'BAND', 'HANDBOOK',
                                     'FUSEE', 'BATTERY', 'BOOM', 'SUGAR SUBSTITUTE', 'JACKET', 'WRAP', 'CUP',
                                     'SHARPENER', 'EARPLUGS', 'PAPER', 'DOT CHART 16', 'MASK', 'PEN', 'RUBBER BAND',
                                     'PIN', 'SUSPENSION', 'RAGS', 'CARTON', 'BASIN', 'CLOTH', 'FUEL',
                                     'FOAM', 'TRACK', 'FLASHDRIVE', 'FLATWARE SET', 'LAYER ASSEMBLY', 'FORMS', 'MESS GEAR',
                                     'RAG', 'GOGGLES', 'GASKET', 'KNIFE', 'SEAL', 'EARCUP SET', 'CALENDAR',
                                     'FILTERS', 'OIL', 'LIGHTSTICK', 'LEAD', 'CUSHION', 'LIP BALM', 'PAMPHLET',
                                     'FOOT POWDER', 'DISINFECTANT', 'SPILL KIT', 'COMPRESS', 'WIPES', 'AERIAL IGNITION DEV', 'WEDGE',
                                     'LINER', 'BLADE', 'SPACER', 'BAG', 'CABLE ASSEMBLY', 'CARD', 'MARKER',
                                     'NOZZLE', 'SIGN', 'GLOVES', 'COVER', 'CANTEEN', 'SHEETING', 'TEST',
                                     'TIE WRAPS'},
                             'AVIATION': {'EAR SEALS', 'EARPHONE', 'ADAPTER', 'BOOM', 'CUSHION', 'CORD ASSEMBLY', 'PIN',
                                          'PAD', 'FUEL', 'AERIAL IGNITION DEV', 'TRACK', 'BOOM SUPPORT', 'SPACER', 'BAG',
                                          'PLANS', 'CABLE ASSEMBLY', 'LAYER ASSEMBLY', 'KIT', 'HOLDER', 'STRAP', 'VISOR LOCK ASSEMBLY',
                                          'COVER', 'VISOR', 'MICROPHONE ELEMENT', 'BOARD', 'TEST', 'EARCUP SET'},
                             'CAMP': {'WASHCLOTH', 'CAN', 'PAPER', 'SOAP', 'TOWEL', 'BAG', 'BRUSH',
                                      'LID REMOVER', 'FUSEE', 'SHEETING', 'CONTAINER', 'NAILS', 'RIBBON', 'KIT',
                                      'BASIN'},
                             'GENERAL': {'CAN', 'OIL', 'LIGHTSTICK', 'TAPE', 'DRUM', 'SPRAY', 'WIRE',
                                         'PLUG', 'BAND', 'CARTRIDGE', 'WRAP', 'BULB', 'GUN', 'REPELLENT',
                                         'DISINFECTANT', 'SPILL KIT', 'RUBBER BAND', 'RAGS', 'CARTON', 'CLOTH', 'FUEL',
                                         'FILTERS', 'FOAM', 'WEDGE', 'SURGE PROTECTOR', 'SCREWS', 'BAG', 'FLASHDRIVE',
                                         'GAUGE', 'CALCULATOR', 'BLANKET', 'SPOUT', 'CORD', 'BOTTLE', 'KIT',
                                         'NOZZLE', 'ROPE', 'FLAGGING', 'BANDS', 'RAG', 'GLOVES', 'COVER',
                                         'HANDLE', 'TIE', 'GASKET', 'KNIFE', 'SANITIZER', 'CONTAINER', 'SEAL',
                                         'NAILS', 'FLARE', 'TIE WRAPS'},
                             'BATTERIES': {'BATTERY'},
                             'OFFICE ': {'STAPLES', 'TAPE', 'ATLAS', 'LEAD', 'FILE', 'JACKET', 'CLIP',
                                         'SHARPENER', 'PAPER', 'PEN', 'PIN', 'ENVELOPE', 'PAD', 'WIPES',
                                         'DISPENSER', 'CALCULATOR', 'TACK', 'FOLDER', 'MARKER', 'KIT', 'HIGHLIGHTERS',
                                         'BANDS', 'PENCIL', 'BOX', 'PORTFOLIO'},
                             'SUBSIST': {'LIP BALM', 'MESS GEAR', 'PLATE', 'COFFEE', 'FOOT POWDER', 'TOWEL', 'CAP',
                                         'SUGAR', 'DINING PACKET', 'CREAM', 'CANTEEN', 'SPOON', 'SUGAR SUBSTITUTE', 'FLATWARE SET',
                                         'CUP', 'FOOD'},
                             'TOOLS': {'FILE', 'BLADE', 'HANDLE', 'STONE'},
                             'MEDICAL': {'COMPRESS', 'PAD', 'KIT'},
                             'PUBLICATION': {'SIGN', 'FORMS', 'PAMPHLET', 'GUIDE -INTERAGENCY AVIATION USER POCKET (2015)', 'INSTRUCTIONS', 'DOT CHART 16', 'GUIDE',
                                             'BOOKLET', 'HANDBOOK', 'CARD', 'FORM', 'CALENDAR'},
                             'PPE': {'STRAP', 'GLASSES', 'EARPLUGS', 'HELMET', 'GLOVES', 'GOGGLES', 'MASK',
                                     'VEST', 'SUSPENSION', 'SHELTER', 'RESPIRATOR'},
                             'FORM/SIGN': {'PLACARD', 'LABELS', 'LABEL', 'FORM', 'KIT', 'TAG'},
                             'WATER': {'ADAPTER', 'LINER', 'BAG', 'GASKET', 'CALCULATOR', 'KIT'},
                             'CHAINSAW': {'FILE'}
                             },

              'TRACKABLE': {'all': {'BLOWER', 'LAUNCHER', 'GENERATOR', 'CHAINSAW', 'PRINTER/PLOTTER', 'HOSE ROLLER', 'PUMP',
                                    'TRAILER', 'SCANNER', 'KIT'},
                            'PUMP': {'PUMP'},
                            'CHAINSAW': {'CHAINSAW'},
                            'GENERAL': {'BLOWER', 'LAUNCHER', 'PRINTER/PLOTTER', 'HOSE ROLLER', 'TRAILER', 'KIT'},
                            'WATER': {'HOSE ROLLER'},
                            'CAMP': {'GENERATOR'},
                            'AVIATION': {'SCANNER'},
                            'NIICD': {'KIT'},
                            'WEATHER': {'KIT'}
                            }
              }