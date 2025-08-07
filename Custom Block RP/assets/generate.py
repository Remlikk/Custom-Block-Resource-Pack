import sys
import os
import json
import shutil

homePath = os.getcwd()

def get_pack_namespace():
    lastDir = os.curdir
    os.chdir(os.path.abspath(homePath))
    
    for file in os.listdir('.'):
        if os.path.isdir(file) and file != 'minecraft':
            os.chdir(lastDir)
            return file
        raise Exception("No valid namespace found. Please ensure you have a valid resource pack structure.")

ITEM_TEMPLATE = {
    "model": {
        "type": "model",
        "model": None # to be filled with block model path
    }
}

MODEL_TEMPLATE = {
    "parent": f"{get_pack_namespace()}:block/spawner",
    "textures": {
        "all": None # to be filled with texture path
    }
}

COMMAND_TEMPLATE = "give @p minecraft:spawner[minecraft:item_name='$1', minecraft:item_model='$2', minecraft:block_entity_data={id:'minecraft:mob_spawner', RequiredPlayerRange:0s, SpawnData:{entity:{id:'minecraft:armor_stand',equipment:{head:{id:'minecraft:stick', components:{\"minecraft:item_model\":'$2'}}}}}}, minecraft:tooltip_display={hidden_components:[block_entity_data]}]"

def validate_model_name(name):
    # Add validation logic for model names
    for char in name:
        if not char.isalnum() and char not in ['_', '-'] or char != char.lower():
            return False
    return True

def generate_block(texturePath):
    while True:
        modelName = input('Enter block name: ')
        if validate_model_name(modelName):
            print(f"Generating block for model: {modelName}")
            break
        else:
            print("Block name contains invalid characters. Please try again. (Allowed characters are letters, numbers, underscores (_), and hyphens (-).)")

    namespace = get_pack_namespace()
    
    # Item definition
    os.chdir('block/items')
    with open(f'{modelName}.json', 'w') as file:
        template = ITEM_TEMPLATE.copy()
        template['model']['model'] = f'{namespace}:block/{modelName}'
        json.dump(template, file, indent=4)
    print(f"Block item JSON for '{modelName}' created successfully.")
    
    # Model definition
    os.chdir(homePath)
    os.chdir(f'{namespace}/models/block')
    
    textureName = os.path.basename(texturePath)
    
    with open(f'{modelName}.json', 'w') as file:
        template = MODEL_TEMPLATE.copy()
        template['textures']['all'] = f'{namespace}:block/{textureName.split(".")[0]}'
        json.dump(template, file, indent=4)
    print(f"Block model JSON for '{modelName}' created successfully.")
    
    # Copy texture
    os.chdir(homePath)
    os.chdir('block/textures')
    shutil.copy(texturePath, os.curdir + '/block/' + textureName)

    print(f"Texture '{textureName}' copied successfully to the block textures directory.")
    
    # Generate item display name
    itemDisplayName = f"{modelName.replace('_', ' ').title()} Block"
    
    print("Generating command...\n")
    print('-' * 64)
    print()
    print(COMMAND_TEMPLATE.replace('$1', itemDisplayName).replace('$2', f'{namespace}:{modelName}'))



def get_block_command():
    os.chdir(get_pack_namespace() + '/items')
    for num, file in enumerate(os.listdir()):
        if file.endswith('.json'):
            print(f"{num + 1} - {file}")
        
        type_choice = input("\nSelect a block by number: ")
        try:
            type_choice = int(type_choice) - 1
            if 0 <= type_choice < len(os.listdir()):
                selected_file = os.listdir()[type_choice]
                model_name = selected_file.replace('.json', '')
                namespace = get_pack_namespace()
                item_display_name = f"{model_name.replace('_', ' ').title()} Block"
                
                print("Generating command...\n")
                print('-' * 64)
                print()
                print(COMMAND_TEMPLATE.replace('$1', item_display_name).replace('$2', f'{namespace}:{model_name}'))
                return
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Main program start
def get_mode():
    if len(sys.argv) > 1:
        generate_block(sys.argv[1])
    else:
        get_block_command()

if __name__ == "__main__":
    get_mode()
    
input("\n\nPress Enter to exit...")