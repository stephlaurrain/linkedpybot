import os
import sys
import gc
from linkbot import Bot
from datetime import datetime
import importlib

class Menuitem:
    def __init__(self, command, init_driver, label, nbparams, ret):
        self.command = command
        self.init_driver = init_driver
        self.label = label
        self.nbparams = nbparams
        self.ret = ret

rootApp = os.getcwd()
hardgreen = "\033[32m\033[1m"
normalgreen = "\033[32m\033[2m"
normalcolor = "\033[0m"

def dotail(profil):
    logFilename = "{0}{1}log{1}{3}{2}.log".format(rootApp, os.path.sep, profil, dnow)
    os.system("tail -f {0}".format(logFilename))

def mencol(nb, fonc, comment):
    return "{0}{3} - {4} {1} - {5}{2}".format(hardgreen, normalgreen, normalcolor, nb, fonc, comment)

def drkcol(str):
    return "{0}{2}{1}".format(hardgreen, normalcolor, str)

def clear():
    return os.system('clear')

nb_args = len(sys.argv)
jsonfilefromarg = "default" if (nb_args == 1) else sys.argv[1]
mode_menu = "default" if (nb_args < 3) else sys.argv[2]
clear()

bot = Bot()
bot.init_main(jsonfilefromarg)
while True:
    print(drkcol("\nHi Neo, I'm the Linkedin bot"))
    print(drkcol("Your wish is my order\n"))
    print(drkcol("What I can do for you :\n"))
    menulist = []
    menulist.append(Menuitem("test", False, "test", 0, False))
    menulist.append(Menuitem("simplyconnect", True, "simplyconnect", 0, False))
    menulist.append(Menuitem("search", True, "search", 0, True))
    if mode_menu == "advanced":
        menulist.append(Menuitem("reinit_visited", False, "reinit visited", 0, False))
    menulist.append(Menuitem("get_visited_list", False, "list ", 0, False))
    menulist.append(Menuitem("add_to_keyword", False, "add [keyword]", 1, False))
    menulist.append(Menuitem("get_keyword_list", False, "list keyword table", 0, True))

    for idx, menuitem in enumerate(menulist):
        print (mencol(idx, menuitem.command, menuitem.label))
        if menuitem.ret:
            print(drkcol("#####"))
    print(drkcol("#####"))
    print(mencol("66", "advanced", "advanced menu"))
    print(mencol("93", "editparams", "edit default.json"))
    print(mencol("99", "exit", "exit this menu"))
    dothat = input(drkcol("\n\nReady to rock : "))
    today = datetime.now()
    dnow = today.strftime(r"%y%m%d")
    if dothat == "66":
        mode_menu = "advanced"
    if dothat == "93":
        print(drkcol("\edit params -r\n"))
        os.system("nano data/conf/default.json")    
    if dothat == "99":
        print(drkcol("\nsee you soon, Neo\n"))
        if item.init_driver:
                if bot.driver != None:
                    bot.driver.close()
                    bot.driver.quit()
        del bot
        gc.collect
        quit()
    try:
        if int(dothat) < 50:
            cmdstr = "nop"
            item = menulist[int(dothat)]
            cmd = item.command
            if item.init_driver:
                bot.init_webdriver()                                
            prms = int(item.nbparams)
            prmcmdlist = []
            for i in range(prms):
                prmcmdlist.append(input(drkcol(f"enter param {i} :")))
            prm2 = "" if (len(prmcmdlist) < 1) else prmcmdlist[0]
            prm3 = "" if (len(prmcmdlist) < 2) else prmcmdlist[1]            
            bot.main(cmd, jsonfilefromarg, prm2, prm3)            
    except Exception as e:
        print (e)
        print(f"\n{hardgreen}bad command (something went wrong){normalcolor}\n")
    