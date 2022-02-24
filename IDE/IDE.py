import json
import subprocess, os

class IDE():
    def __init__(self) -> None:
        self.file = None
        self.config = None
        self.outDir = False
        self.srcDir = False
        self.cnf = False
        self.__configEnv()
        
    #private
    def __fetchConfig(self)->dict:
        file = open('config.json')
        data = json.loads(file.read())
        self.config = data
        file.close()
        return self.config
        
    def checkDir(self,dir=None) -> list:
        env_list = subprocess.run(["ls"], stdout=subprocess.PIPE, text=True)
        env_list = env_list.stdout.split('\n')
        env_list.pop()
        if(dir != None):
            cmd = "cd {} && ls".format(dir)
            for i in env_list:
                if(i == dir):
                    dst_file = subprocess.run(cmd, capture_output=True, shell=True)   
                    dst_file = dst_file.stdout.decode().split('\n')
                    dst_file.pop()
                    return dst_file
        return env_list
    
    def run(self)->None:
        self.__fetchConfig()
        source = self.config['srcDir']
        entryFile = self.config['entryFile']
        file_n = entryFile.split(".")
        file_n = file_n[0]
        output = self.config['outDir']
        os.system(f"cd {source} && nasm -f elf {entryFile}")
        os.system(f"ld -m elf_i386 -s -o {source}/{file_n} {source}/{file_n}.o")
        os.system(f"mv {source}/{file_n}.o {output}/")
        os.system(f"mv {source}/{file_n} {output}/")
        os.system(f"./{output}/{file_n}")
        
    # private
    def __envCheck(self)->None:
        env_list = self.checkDir()
        for i in env_list:
            if(i == "out"):
                self.outDir = True
            if(i == "src"):
                self.srcDir = True
            if(i == "config.json"):
                self.cnf = True
                
    # private        
    def __defaultMain(self) -> None:
        default_file = open("src/main.asm", "w")
        file_data = "section .data\nmsg db 'hello world!', 0xa;\nlen equ $ - msg\n\nsection .text\n\tglobal _start\n\n_start:\n\tmov edx,len \n\tmov ecx, msg\n\tmov ebx, 1\n\tmov eax, 4\n\tint 0x80\n\n\tmov eax, 1\n\tint 0x80"
        default_file.write(file_data.strip())
        default_file.close()
        
    # private
    def __defaultConfig(self) -> None:
        config_file = open("config.json", "w")
        file_content = '{\n"outDir": "out",\n"srcDir": "src",\n"entryFile": "main.asm"\n}'
        config_file.write(file_content)
        config_file.close()
        
    # private
    def __printDefaultMessage(self):
        print("\n\t\t\t\tTHINK OUT OF THE BOX\n")
        print("\t\t===========================================================")
        print("\t\t     =====         ==       ===============   =============")
        print("\t\t     ======        ==       ====   -   ====   ===== - =====")
        print("\t\t     ==   ==       ==       ====   -   ====   ===== - =====")
        print("\t\t     ==    ==      ==       ====   -   ====   ===== - =====")
        print("\t\t     ==     ==     ==       ====   -   ====   = --------- =")
        print("\t\t     ==      ==    ==       ====   -   ====   ===== - =====")
        print("\t\t     ==       ==   ==       ====   -   ====   ===== - =====")
        print("\t\t     ==        ==  ==       ====   -   ====   ===== - =====")
        print("\t\t    ===         =====       ===============   =============")
        print("\t\t===========================================================")
        
    # private      
    def __configEnv(self)->None:
        self.__envCheck()
        self.__printDefaultMessage()
        if(not(self.outDir)):
            subprocess.run(["mkdir", "out"], stdout=subprocess.DEVNULL)
        if(not(self.srcDir)):
            subprocess.run(['mkdir', "src"], stdout=subprocess.DEVNULL)
            self.__defaultMain()
        else:
            d = self.checkDir('src')
            if(d == 0):
                self.__defaultMain()
        if(not(self.cnf)):
            self.__defaultConfig()
        
        
        
        