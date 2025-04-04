# [ Imports ]
import os
import json
import xmltodict

# [ Constants ]
DEFAULT_SAVE_LOCATION = os.path.join(os.getenv('APPDATA'), 'StardewValley', 'Saves')
XML_IDENTIFIER = '<?xml version="1.0" encoding="utf-8"?>'

# [ Global Variables ]

# [ Functions ]

"""
check_default_save_location()
Preconditions: None
Desc: Uses the constant DEFAULT_SAVE_LOCATION to determine if that path exists on the user's OS.
Returns: boolean
"""
def check_default_save_location() -> bool:
    default_exists = os.path.exists(DEFAULT_SAVE_LOCATION)
    return default_exists


"""
get_save_location()
Preconditions: None
Desc: Checks if the default save location exists on the user's OS, if it does it asks the user if that's where they want to check.
        If neither condition is met, the user is infinitely prompted to enter a path on the OS until they enter a path that exists.
Returns: string value of the save location path
"""
def get_save_location() -> str:
    default_exists = check_default_save_location()
    
    if default_exists:
        print(f'Default Save Location Detected:\n{DEFAULT_SAVE_LOCATION}\n')
        correct_path = input('Is this the correct path to the saves directory? (Y/N): ')
        if correct_path.lower().strip() == "y":
            return DEFAULT_SAVE_LOCATION
        else:
            print('Please enter the correct path to the saves directory.')
    else:
        print('No Default Save Location Detected.')
        print('If they\'re saved elsewhere, please enter path to the saves directory.\n')
    
    location = ""
    while not os.path.exists(location):
        location = input('> ')
        
    return location

"""
get_save(save_location: str)
Preconditions: save_location exists on the system
Desc: Iterates through the path passed through the save_location argument and verifies if it is a save based on whether or not it is save
    based on the following conditions:
        1. The folder contains a file of the exact same name
        2. The folder contains a file named 'SavedGameInfo'
        3(and 4). Both files are XML file
Returns: string containing the path to the save the user wants to analyze
"""
def get_save(save_location: str) -> str: # returns path to specific save
    # list saves from saves location
    directory = os.fsencode(save_location)
    directory_files = os.listdir(directory)
    
    saves = []
    print('\nSave file names may either start with the farmer name or farm name depending on the game version.')
    print('Found Saves:')
    for file in directory_files:
        # Verify that the file/folder is a save
        file_name = os.fsdecode(file)
        file_path = os.path.join(save_location, file_name)
        if os.path.isdir(file_path): # is a save directory
            # check if save exists
            # name of save file is same as save directory
            folder_path = os.path.join(save_location, file_name)
            save_path = os.path.join(folder_path, file_name)
            save_game_info_path = os.path.join(folder_path, 'SaveGameInfo')
            
            contains_save_file = os.path.exists(save_path)
            contains_save_game_info = os.path.exists(save_game_info_path)
            files_are_xml = is_xml(save_path) & is_xml(save_game_info_path)
            
            
            # Debug print string
            debug = False
            if debug:
                print(f'Folder Path: {folder_path}\nSave Path: {save_path}\nSaveGameInfo Path: {save_game_info_path}\n')
                print(f'Contains Save Path: {contains_save_file}\nContains SaveGameInfo: {contains_save_game_info}')
                print(f'Files Are XML: {files_are_xml}')
            
            save_parts = file_name.split('_') # Farmer/Farm Name is index 0, seed is index 1
            
            if contains_save_file and contains_save_game_info and files_are_xml:
                saves.append(os.path.join(save_location, file_name))
                print(f'{len(saves)}. {save_parts[0]} (Seed: {save_parts[1]})')
    
    # return nothing if there are no saves in the specified location
    if len(saves) == 0:
        print('No saves found.')
        return ""
    
    # ask user for save
    save: int = -1
    valid_option: bool = False
    while not valid_option:
        try:
            save = int(input(f'Which save would you like to select? (1-{len(saves)})> '))
            if 1 <= save <= len(saves):
                valid_option = True
            else:
                print(f"Please enter a number between 1 and {len(saves)}.")
        except ValueError:
            print(f"Please enter a valid number (1-{len(saves)}).")

    
    print(f'Selected save: {saves[save-1]}')
    return saves[save-1]


"""
is_xml(path: str) -> bool:
Preconditions: path exists
Desc: Checks to see if the file at the given path starts with an XML identifier
Returns: bool
"""
def is_xml(path: str) -> bool:
    # no point in checking if the path is invalid
    if not os.path.exists(path):
        return False
    
    # ENCODE WITH utf-8-sig BECAUSE OF THAT GODDAMN BYTE ORDER MARKER
    # actually sent me in a debugging spiral for 20 minutes
    with open(path, 'r', encoding='utf-8-sig') as file:
        content = file.read()
        file.close() # GOODBYE
        return content.startswith(XML_IDENTIFIER)


"""
Preconditions: path exist
Desc: Converts the XML save data into a readable dictionary
Returns: dictionary of the save info
"""
def read_save(file_path) -> dict:
    if not os.path.exists(file_path):
        print('Could not read save file.')
        return {}
    else:
        # read save and convert to dict
        with open (os.path.join(file_path, 'SaveGameInfo'), 'r', encoding='utf-8-sig') as save_game_info:
            xml_contents = save_game_info.read() # read save contents
            save_game_info.close() # close the file
            save_contents = xmltodict.parse(xml_contents)
            check_completion(save_contents)

"""
Preconditions: Save Data exists
Desc: Checks the contents of the user's save data to see where they stand with the game's defined perfection goals
Returns: Dictionary of the user's progress towards perfection (categories and completion percentages)
"""
def check_completion(save_data) -> dict:
    # Completion Critiera:
    # Produce & Forage
        # Missing crops to sell
    # Player has all obelisks
        # Missing obelisks
    # Player has golden clock
    # Monster slayer hero
        # All missing monsters
    # Great Friends
        # 8 hearts for non-dateable, 10 hearts for dateable
    # Level 10 in every skill
    # All stardrops found
        # Missing stardrops
    # Cooked every recipe
        # Missing recipes
    # Crafted all recipes
        # Missing crafted items
        # Missing recipes if need be
    # All fish caught
        # Missing fish
    # All golden walnuts found
        # Missing walnuts
    # ==== [ Code Below ] ====
    farmer_data: dict = save_data['Farmer']

    # Farm Info
    game_version: str = farmer_data['gameVersion']
    name: str = farmer_data['name']
    farm_name: str = farmer_data['farmName']
    favorite_thing: str = farmer_data['favoriteThing']
    year: str = farmer_data['yearForSaveGame']
    dayOfMonth: str = farmer_data['dayOfMonthForSaveGame']
    season_id: int = int(farmer_data['seasonForSaveGame'])
    season: str = ''
    if season_id == 0:
        season = 'Spring'
    elif season_id == 1:
        season = 'Summer'
    elif season_id == 2:
        season = 'Fall'
    elif season_id == 3:
        season = 'Winter'
    
    # Stats
    money: str = farmer_data['money']
    total_money_earned: str = farmer_data['totalMoneyEarned']
    stamina: str = farmer_data['stamina']
    max_stamina: str = farmer_data['maxStamina']
    health: str = farmer_data['health']
    max_health: str = farmer_data['maxHealth']
    qi_gems: str = farmer_data['qiGems']
    position: str = ", ".join([farmer_data['Position']['X'], farmer_data['Position']['Y']])
    time_played: float = float(farmer_data['millisecondsPlayed'])
    time_played_formatted: str = f"{time_played // 1000 // 60} minutes"
    backpack_level: str = int(farmer_data['maxItems']) / 12
    
    # Skills
    farming_level: str = farmer_data['farmingLevel']
    mining_level: str = farmer_data['miningLevel']
    combat_level: str = farmer_data['combatLevel']
    foraging_level: str = farmer_data['foragingLevel']
    fishing_level: str = farmer_data['fishingLevel']

    # Luck Stats

    # Professions

    # Mastery

    # Display Info
    print('\n[ Save Data ]')
    print('============================')
    print(f'Game Version: {game_version}')
    print(f'Farmer Name: {name}')
    print(f'Farm Name: {farm_name} Farm')
    print(f'Favorite Thing: {favorite_thing}')
    print(f'Year {year} {season} {dayOfMonth}')
    print(f'Money: {money} | Total Money Earned: {total_money_earned}')
    print(f'Qi Gems: {qi_gems}')
    print(f'Stamina: {stamina} | Max Stamina: {max_stamina}')
    print(f'Health: {health} | Max Health: {max_health}')
    print(f'Position: {position}')
    print(f'Time Played: {time_played_formatted}')
    print(f'Backpack Level: {backpack_level:.0f} ({(backpack_level * 12):.0f} slots)')

    print('\n[ Skills Progress ]')
    print('============================')
    print(f'Farming Level: {farming_level} / 15 ({int(farming_level) * 100 / 15:.2f}%)')
    print(f'Mining Level: {mining_level} / 15 ({int(mining_level) * 100 / 15:.2f}%)')
    print(f'Combat Level: {combat_level} / 15 ({int(combat_level) * 100 / 15:.2f}%)')
    print(f'Foraging Level: {foraging_level} / 15 ({int(foraging_level) * 100 / 15:.2f}%)')
    print(f'Fishing Level: {fishing_level} / 15 ({int(fishing_level) * 100 / 15:.2f}%)')


# [ Program Entry ]
def main():
    saves_location = get_save_location()
    save = get_save(saves_location)

    # now that we have the proper save selected, we can store it into a dictionary
    save_data: dict = read_save(save)

if __name__ == "__main__":
    main()