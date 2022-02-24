
import os,time,sys,glob

        
        
class Watcher():
    running = True
    refresh_delay = 1
    def __init__(self, sourcePath, call_fun_on_change = None) -> None:
        self.sourcePath = sourcePath
        self.source = None
        self.call_fun_on_change = call_fun_on_change
        self.fileList = []
        self.defaultWatch()
        
    def defaultWatch(self) -> None:
        self.source = os.listdir(self.sourcePath)
        fList = []
        for i in glob.glob(f"{self.sourcePath}/*.asm"):
            file = open(i,'r')
            data = file.read()
            fList.append(data)
            file.close()
        self.fileList = fList
        del fList
            
    
    def watchFile(self)->None:
        j = 0
        for i in glob.glob(f"{self.sourcePath}/*.asm"):
            file = open(i,"r")
            data = file.read()
            if(data != self.fileList[j]):
                self.fileList[j] = data
                self.call_fun()
            file.close()
            j += 1
    def watchDir(self):
        src = os.listdir(self.sourcePath)
        if (src != self.source):
            self.source = src
            self.defaultWatch()
            self.watchFile()
            self.call_fun()

    def call_fun(self):
        print("\n\t\tOutput")
        print("\t\t======\n")
        print("--------------------------------------")
        if self.call_fun_on_change is not None:
            self.call_fun_on_change()
            print("--------------------------------------")
            print("\n[+]: Loking for changes....")
    
    def watch(self):
        self.call_fun()
        while self.running:
            try: 
                # Look for changes
                time.sleep(self.refresh_delay)
                self.watchDir()
                self.watchFile()
                      
            except KeyboardInterrupt: 
                print('\nHave a nice Day!') 
                break 
            except FileNotFoundError:
                print('\nFile not found')
                break
            except: 
                print('Unhandled error: %s' % sys.exc_info()[0])



    