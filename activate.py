
from IDE.IDE import IDE
from IDE.watcher import Watcher

if __name__ == "__main__":
    ide = IDE()
    watcher = Watcher('src',ide.run)
    watcher.watch()