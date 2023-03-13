#! /usr/bin/python3
import json
import sys
import os
import argparse
import shutil

CNF_LIBS_FOLDER="c_modules"
CNF_PACKAGE_CONFIG_FILE="package.json"
CNF_DEFAULT_PACKAGE_CONFIG_CONTENT=\
"""{
  "name": "%s",
  "version": "1.0.0",
  "description": "This is a template",
  "author": "Anonymous",
  "license": "ISC",
  "dependencies": {
  }
}
"""

class PackageManager:
    CNF_LIBS_FOLDER= CNF_LIBS_FOLDER
    CNF_MANAGEMENT_FILE= f"./{CNF_LIBS_FOLDER}/packages.json"
    CNF_CMAKE_FILE= f"./{CNF_LIBS_FOLDER}/CMakeLists.txt"
    CNF_DEFAULT_MANAGEMENT_FILE_CONTENT=\
    """{
        "packages":[
        ]
    }
    """
    URI_TYPES=["git","http","path"]
    def __load_or_create_config_file( self ):
        if( self.config_is_loaded ):
            return

        if( os.path.isfile( self.CNF_MANAGEMENT_FILE ) ):
            with open( self.CNF_MANAGEMENT_FILE , "r+" ) as json_file:
                self.management_dict = json.load( json_file )
        else:
            if( not os.path.isdir( self.CNF_LIBS_FOLDER ) ):
                os.mkdir( self.CNF_LIBS_FOLDER )
            self.management_dict = json.loads( self.CNF_DEFAULT_MANAGEMENT_FILE_CONTENT )

        self.config_is_loaded= True

    def __init__( self ):
        self.config_is_loaded= False

    def __add_from_local_path( self, package_name, package_path ):
        dest = f"{self.CNF_LIBS_FOLDER}/{package_name}/"
        if( not( os.path.isdir( dest ) ) ):
            print( shutil.copytree( package_path , dest ) )
            self.management_dict["packages"].append( package_name )
        else:
            pass #Assumme already installed

    def __add_from_git( self, package_name:str, package_uri:str, package_tag:str ):
        dest = f"{self.CNF_LIBS_FOLDER}/{package_name}/"
        if( not( os.path.isdir( dest ) ) ):
            os.mkdir( dest )
            cmd = f"cd {dest} && git clone {package_uri} . && git checkout {package_tag}"
            print( cmd )
            os.system( cmd )
            self.management_dict["packages"].append( package_name )
        else:
            pass #Assumme already installed

    def add_package_from_path( self, package_name : str , package_uri : str ):
        self.__load_or_create_config_file()
        if( os.path.isdir( package_uri ) ):
            self.__add_from_local_path( package_name, package_uri )
        else:
            raise Exception(f"Invalid source path: \"{package_uri}\"")

    def add_package_from_http( self, package_name : str , package_uri : str ):
        self.__load_or_create_config_file()
        raise Exception("http: Work in progress")

    def add_package_from_git( self, package_name:str, package_uri:str, package_tag:str="master" ):
        self.__load_or_create_config_file()
        self.__add_from_git( package_name, package_uri, package_tag )

    def add_package( self, package_name:str, package_uri:str, package_type:str ):
        self.__load_or_create_config_file()
        if( package_type == "git" ):
            self.add_package_from_git( package_name, package_uri )
        elif( package_type == "path" ):
            self.add_package_from_path( package_name, package_uri )
        elif( package_type == "http" ):
            self.add_package_from_http( package_name, package_uri )
        else:
            pass

    def populate_packages( self ):
        """
        Install what is specified on the "package.json"
        """
        self.__load_or_create_config_file()
        with open( CNF_PACKAGE_CONFIG_FILE , "r+" ) as json_file:
            package_json = json.load( json_file )

        installed_list=[]

        # Check for not repeated packages.
        for package in package_json["dependencies"]:
            package_name = package["name"]
            package_uri = package["uri"]
            package_type = package["type"]
            if( package_name in installed_list ):
                print( f"Warning: ignoring repeated package entry \"{package_name}\"" , file=sys.stderr )
            else:
                installed_list.append( package_name )
                self.add_package( package_name, package_uri, package_type )
    
    def save(self):
        with open( self.CNF_MANAGEMENT_FILE , "w+" ) as json_file:
            json_file.write( json.dumps( self.management_dict ) )
        with open( self.CNF_CMAKE_FILE , "w+") as cmake_file:
            line="add_subdirectory( ${CMAKE_CURRENT_LIST_DIR}/%s )\n"
            for package in self.management_dict["packages"]:
                #cmake_file.write( line % package["name"] )
                cmake_file.write( line % package )

#def create_package( package_name : str ):
#    with open( CNF_PACKAGE_CONFIG_FILE , "w+") as package_json:
#        package_json.writelines( CNF_DEFAULT_PACKAGE_CONFIG_CONTENT%package_name )

