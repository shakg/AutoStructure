"""
automatically orginazes folders to given structers.
"""

from operator import le
import sys
import time
from typing import Tuple 
from os import listdir, getcwd, mkdir
from os.path import isfile, join
import subprocess




class Organizer:
    """
    version 0.1 :
     - runs in cli 
     - you can create folder extension couples in infinite loop
     - when you done creating couples, choose run command to execute organizer
    """
    def __init__(self, ForceUse:bool = False) -> None:
        # init empty dict for further use.
        self.ExtensionFolderCouples:list = []

        if(ForceUse == False):
            if (sys.platform == "win32" or sys.platform == "win64"):
                raise Exception("This OS is not supported!")


    @classmethod
    def Version()->str:
        return "0.1"

    @staticmethod
    def __Prompt(prompt:str)->str:
        """
        Prompts user with given string
        :returns: user input in string in lowercase and stripped lowercase and stripped format
        """
        user_instruction:str = str(input(prompt))
        return user_instruction.lower().strip()

    @staticmethod
    def __CreateExtensionNameArray(ExtensionNameWithComma:str)->list:
        """
        Takes extention names as array with in comma seperated
        :returns: list of extensions
        """

        SplittedExtentions:list = ExtensionNameWithComma.split(",")

        if(len(SplittedExtentions)<=1):
            return [ExtensionNameWithComma]
        
        return SplittedExtentions
        
    def __AddExtFolderCouple(self)->bool:
        """
        Prompts user for adding extension folder couple names.
        Generates extention-folder couple.
        Adds this tuple object to global array for further use.
        :returns: bool if succesfully appended.
        """

        if(self.ExtensionFolderCouples is None): raise Exception("You need to construct new object from Organizer class.")

        # Prompt for extension name without period
        ExtensionNameWithComma:str = self.__Prompt("Extension name without comma(.) \n And you can input multiple values seperarated with comma(png,jpg,json) : ")
        ExtensionNameArray:list = self.__CreateExtensionNameArray(ExtensionNameWithComma)
        print("\n")
        # Prompt for folder name, Organizer will put files containing this extention to this folder.
        FolderName:str = self.__Prompt("Folder name : ")
        
        for ExtensionName in ExtensionNameArray:
            ExtensionFolderCouple:Tuple = (ExtensionName,FolderName)
            # Adding construted extention-folder couple tuple to global object.
            self.ExtensionFolderCouples.append(ExtensionFolderCouple)
            self.__PrettyPrintCouple()
        
        # TODO : implement return false scenarios
        return True

    def __PrettyPrintCouple(self)->None:
        """
        Beautifully prints extension-folder couple to stdout.
        :returns: None 
        """
        if(len(self.ExtensionFolderCouples)<=0):
            # Raise exception here bc this func can't run without adding extension-folder couple.
            raise Exception("Please contact author of this app. Critical issue happened!")

        print(" -- Added new extension-folder couple.")
        
        # Tuple access 
        #  -- a = (1,2)
        #  -- a[0] == 1 evals to True

        # TODO: Instead of tuples we can use named tuple, json or dict with string field names.

        print(f" -- Extension name : {self.ExtensionFolderCouples[-1][0]}")
        print(f" -- Folder name : {self.ExtensionFolderCouples[-1][1]} \n")

    def __PrettyPrintCoupleAll(self)->None:
        """
        Prints all extension file couples
        :returns: nothing
        """
        for ExtFolderCouple in self.ExtensionFolderCouples:
            print(f" -- Extension name : {ExtFolderCouple[0]}  -- Folder name : {ExtFolderCouple[1]}")

    @staticmethod
    def __MoveFile(FileName:str, FolderName:str)->None:
        """
        Moves given file to desired location
        :returns: None
        """

        BashCommand = f"mv {FileName} {FolderName}"
        print(f" -- Executing command = {BashCommand}")
        subprocess.Popen(BashCommand.split(), stdout=subprocess.PIPE)
        
    def __RunOrganizer(self)->None:
        """
        Creates and orginases new folders for given extension-folder couples 
        :returns: None
        """
        if(len(self.ExtensionFolderCouples)<=0):
            print("You have zero or less extension-folder couple, please configure and try again! \n")
            return

        for ExtFolderCouple in self.ExtensionFolderCouples:
            
            ExtensionName:str = ExtFolderCouple[0]
            FolderName:str = ExtFolderCouple[1]
            
            print(f"FolderName = {FolderName} && FileName = {ExtensionName}")

            # create folder if not exists
            while(FolderName not in listdir(getcwd())):
                try:
                    mkdir(FolderName)
                except Exception as e :
                    print(e)
                time.sleep(1)

            # move files with matching extentions to created folder.
            AllFiles = [f for f in listdir(getcwd()) if isfile(join(getcwd(), f))]
            for File in AllFiles:
                if ExtensionName in File:
                    FullFolderPath = join(getcwd(),FolderName)
                    print(f" -- Moving {File} to {FullFolderPath}")
                    time.sleep(5)
                    self.__MoveFile(File, FullFolderPath)

    def MainLoop(self):
        """
        - run organizer <_______________________
        - enter new extension-folder couple    |
        |___ enter extension name              |
        |___ enter folder name ________________|

        """
        while 1:
            answer:str = self.__Prompt("Run organizer(r), add extension-folder couple(e), write all couples(w) or quit(q) : ")
            if (answer == "r"):
                self.__RunOrganizer()
            elif(answer == "e"):
                # gets user input and creates extension-folder couple.
                AddExtFolderCoupleStatus:bool = self.__AddExtFolderCouple()
                if (AddExtFolderCoupleStatus): continue
                else: raise Exception("Please contact author of this app. Critical issue happened!")
            elif(answer == "q"):
                sys.exit(0)
            elif(answer == "w"):
                self.__PrettyPrintCoupleAll()
            else:
                print("Unkown command please try again! \n")
                continue
                
if __name__ == '__main__':
    organizer = Organizer()
    organizer.MainLoop()