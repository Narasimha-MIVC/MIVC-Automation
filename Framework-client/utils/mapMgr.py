"""
Map files manager class
"""
__author__ = "Vinay HA"

import os
import sys
from map_parser import mapParser

class mapMgr:
    '''
        mapMgr parsers all the map file inside map directory and converts them into dictionary
    '''
    objRepository = {}
    objRepoList = []
    @staticmethod
    def create_maplist(component = "ManhattanComponent"):
        try:
            # Listing all the file in the map directory
            # creating the map directory path
            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            mapdirectory = None
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            if "Manhattan".lower() in component.lower():
                mapdirectory = os.path.join(base_path,"automation-connect-client","Automation/ManhattanLibrary/map",component)
            elif "BOSS".lower() in component.lower():
                mapdirectory = os.path.join(base_path,"automation-boss","map",component)
            elif "Teamwork".lower() in component.lower() and "android" not in component.lower() and "ios" not in component.lower():
                mapdirectory = os.path.join(base_path,"automation-twd","map",component)
            elif "MnM".lower() in component.lower():
                mapdirectory = os.path.join(base_path,"automation-mnm","map",component)
            elif "gsuite" in component.lower():
                mapdirectory = os.path.dirname(os.getcwd()) + "/map/" + component
            elif "AndroidTeamworkComponent".lower() in component.lower():
                mapdirectory = os.path.join(base_path, "android teamwork automation", "map", component)
            else:
                raise Exception("Component %s is not supported!" % component)
                
            if isinstance(component, str):
                if os.path.isdir(mapdirectory):
                    print "Map directory for <%s> is <%s>"%(component, mapdirectory)
                else:
                    raise AssertionError("<%s> Directory not found for <%s>" %(mapdirectory, component))
           
            
            for dirname, dirnames, filenames in os.walk(mapdirectory):
                pass
            filelist = [os.path.join(dirname, filename) for filename in filenames]           
                 
            for file in filelist:
                #Parsing single map file and updating objRepository dictionary
                map_obj = mapParser(file)
                mapMgr.objRepository.update(map_obj.map_dict)
                mapMgr.objRepoList.append(map_obj.map_key_list)
            #print (mapMgr.objRepository)
        except:
            return False
        
    #Method to get objList
    @staticmethod
    def getMapKeyList():
        return mapMgr.objRepoList

    #Method to get objDictionary
    @staticmethod
    def getMapDict():        
        return mapMgr.objRepository

    #Method to get element from objRepository
    @staticmethod
    def __getitem__(key):
        if key in list(mapMgr.objRepository.keys()):
            return mapMgr.objRepository[key]
        else:
            return None


if __name__ == "__main__":
    mapMgr.create_maplist()
    print (mapMgr.__getitem__('Login_Password'))
    print (mapMgr.getMapDict()['Login1_Password'])
