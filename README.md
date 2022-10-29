# aseprite-export-watcher
Watch aseprite files for changes and export them in another folder. For example export them to a Godot project.

Project with aseprite examples : [Aseprite examples](https://github.com/mraiur/aseprite-export-watcher-examples)

# Setup

## Create python environment  

```
python3 -m venv venv
```

## Install dependencies

```
source ./venv/bin/activate

pip3 install -r requirements.txt
```


## Example config ( Linux )

```
{
  "layer": {
    "Layer/**": {
      "layer": "tile"
    }
  },
  "multi-layered-grouped": {
    "MutliLayerGrouped/**" : {
      "groups" : ["normal", "hover"]
    }
  },
  "multi-layered": [
    "MutliLayer/**"
  ],
  "split-layers": [
    "SplitLayers/**"
  ],
  "standard": [
    "Standard/**"
  ],
  "aseprite-project-path": "/home/nivanov/work/aseprite-export-watcher-examples",
  "project-path": "/home/nivanov/work/aseprite-export-watcher/temp",
  "aseprite-executable": "/mnt/store/SteamLibrary/steamapps/common/Aseprite/aseprite"
}
```


# Start

## Single export 
```
source ./venv/bin/activate
python3 src/export.py
```


## Export and start watching for changes

On aseprite file save will autoexport

```
source ./venv/bin/activate
python3 src/export.py --watch
```