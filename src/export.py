import os
import re
import glob
import click
import config
import time
import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

Aseprite = config.data['aseprite-executable']

aseReg = r'(.aseprite|.ase)'

observers = []
fileMap = {}


def metaFile(file):
    return re.sub(aseReg, '.meta', file)


def outFile(file, suffix=''):
    replace = '.png'
    if suffix != '':
        replace = '-' + suffix + '.png'

    outFile = re.sub(config.data['aseprite-project-path'], '', file)
    outFile = re.sub(aseReg, replace, outFile)
    if outFile.startswith('/'):
        outFile = outFile[1:]
    outDir = os.path.dirname(os.path.join(config.data['project-path'], outFile))
    if os.path.exists(outDir) == False:
        os.makedirs(outDir)
    return os.path.join(config.data['project-path'], outFile)


def getAseFiles(folderMatch):
    list = []
    print('getAseFiles', folderMatch)
    matches = glob.glob(folderMatch, recursive=True)
    for file in matches:
        if file.endswith('.aseprite') or file.endswith('.ase'):
            list.append(file)
    return list


def watchFile(file, exportFile, params, watch):
    if watch:
        def handler(event):
            if event.event_type == 'modified':
                exportFile(file, params)

        event_handler = watchdog.events.PatternMatchingEventHandler(patterns=[file],
                                                                    ignore_patterns=[],
                                                                    ignore_directories=True)
        event_handler.on_modified = handler

        observer = Observer()
        observer.schedule(event_handler, file)
        observer.start()
        observers.append(observer)


@click.command()
@click.option('--watch', is_flag=True, help='Watch for changes and automatically export them')
def exportAssets(watch):
    click.echo('export assets')

    if config.data['layer']:
        for key in  config.data['layer']:
            value = config.data['layer'][key]

            folderMatch = config.data['aseprite-project-path'] + "/" + key
            files = getAseFiles(folderMatch)
            for file in files:
                def handleFile(file, params):
                    cmd = Aseprite + " -b --layer " + params['layer'] + ' ' + file + " --save-as " + outFile(
                        file)
                    print('file: layer | ' + file + ' (' + params['layer'] + ') -> ' + outFile(file))
                    os.system(cmd)

                if file not in fileMap:
                    params = {
                        "layer": value['layer']
                    }
                    handleFile(file, params)
                    watchFile(file, handleFile, params, watch)
                    fileMap[file] = {'exporter': 'layerExport'}

    if config.data['multi-layered-grouped']:
        for key in  config.data['multi-layered-grouped']:
            value = config.data['multi-layered-grouped'][key]

            folderMatch = config.data['aseprite-project-path'] + "/" + key
            files = getAseFiles(folderMatch)
            for file in files:
                def handleFile(file, params):
                    for group in value['groups']:
                        resultFile = outFile(file, group)
                        cmd = Aseprite + " -b --all-layers --layer " + group + ' ' + file + " --sheet " + resultFile + " --data " + metaFile(
                            file)
                        print('file: exportMultiLayerGrouped | ' + file + ' -> ' + file)
                        os.system(cmd)

                if file not in fileMap:
                    params = {}
                    handleFile(file, params)
                    watchFile(file, handleFile, params, watch)
                    fileMap[file] = {'exporter': 'multiLayerGrouped', 'params': params}

    if config.data['multi-layered']:
        for value in config.data['multi-layered']:
            folderMatch = config.data['aseprite-project-path'] + "/" + value
            files = getAseFiles(folderMatch)
            for file in files:
                def handleFile(file, params):
                    cmd = Aseprite + " -b --all-layers " + file + " --save-as " + outFile(file) + " --data " + metaFile(
                        file)
                    print('file: multi-layered | ' + file + ' -> ' + file)
                    os.system(cmd)

                if file not in fileMap:
                    params = {}
                    handleFile(file, params)
                    watchFile(file, handleFile, params, watch)
                    fileMap[file] = {'exporter': 'exportMultilayer'}

    if config.data['split-layers']:
        for value in config.data['split-layers']:
            folderMatch = config.data['aseprite-project-path'] + "/" + value
            files = getAseFiles(folderMatch)
            for file in files:
                def handleFile(file, params):
                    cmd = Aseprite + " -b --all-layers --split-layers " + file + " --sheet " + outFile(
                        file) + " --data " + metaFile(file)
                    print('file: split-layers | ' + file + ' -> ' + outFile(file))
                    os.system(cmd)

                if file not in fileMap:
                    params = {}
                    handleFile(file, params)
                    watchFile(file, handleFile, params, watch)
                    fileMap[file] = {'exporter': 'splitLayers'}

    if config.data['standard']:
        def exportFile(file, params):
            cmd = Aseprite + " -b " + file + " --sheet " + outFile(file) + " --data " + metaFile(file)
            print('file: standart | ' + file + ' -> ' + outFile(file))
            os.system(cmd)

        for value in config.data['standard']:
            folderMatch = config.data['aseprite-project-path'] + "/" + value
            asepriteFiles = getAseFiles(folderMatch)
            for file in asepriteFiles:
                if file not in fileMap:
                    params = {}
                    exportFile(file, params)
                    watchFile(file, exportFile, params, watch)
                    fileMap[file] = {'exporter': 'standardExport'}

    if watch:
        click.echo('export assets with watch')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for observer in observers:
                observer.stop()


if __name__ == '__main__':
    exportAssets()
