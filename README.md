
### Alternate Subnautica APworld

This apworld is meant to be used with (Archipelago)[https://github.com/ArchipelagoMW/Archipelago] and a custom (SubnauticMod)[https://github.com/kedNalatacId/ArchipelagoSubnauticaModSrc].

This apworld can generate "classic" options so that it works with classic subnautica mod which allows playing the custom and non-custom subnautica side by side inside the same archipelago instance.

### Using this alternate apworld

For the moment, the way to use this apworld is as follows:
  - clone a copy of this repo
  - zip the contents of the repo as subnautica.apworld
  - move the apworld into the archipelago custom_worlds folder
    - if a custom_worlds folder doesn't exist, create one or run `python3 Generate.py -h` and it should be created automatically
    - this will make it have precedence over the built-in

### Disabling this alternate apworld

To stop using the alternate, simply delete the subnautica.apworld from the custom_worlds folder.

