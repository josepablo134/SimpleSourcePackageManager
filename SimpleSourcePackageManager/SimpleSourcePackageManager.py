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
    def __load_or_create_config_file( self ):
        if( os.path.isfile( self.CNF_MANAGEMENT_FILE ) ):
            with open( self.CNF_MANAGEMENT_FILE , "r+" ) as json_file:
                self.management_dict = json.load( json_file )
        else:
            os.mkdir( self.CNF_LIBS_FOLDER )
            self.management_dict = json.loads( self.CNF_DEFAULT_MANAGEMENT_FILE_CONTENT )

    def __init__( self ):
        self.__load_or_create_config_file()

    def __add_from_local_path( self, package_name, package_path ):
        dest = f"{self.CNF_LIBS_FOLDER}/{package_name}/"
        if( not( os.path.isdir( dest ) ) ):
            print( shutil.copytree( package_path , dest ) )
            self.management_dict["packages"].append( { "name" : package_name } )
        else:
            pass #Assumme already installed

    def add_package( self, package_name : str , package_uri : str ):
        if( os.path.isdir( package_uri ) ):
            self.__add_from_local_path( package_name, package_uri )
        else:
            raise Exception("Install from remote is not ready")
        print( self.management_dict )
        print( package_name )
        print( package_uri )
        pass

    def __prepare_libs_folder( self ):
        if( not( os.path.isdir( "./lib" ) ) ):
            os.mkdir( f"./lib/" )

    def populate_packages( self ):
        pass
    
    def save(self):
        with open( self.CNF_MANAGEMENT_FILE , "w+" ) as json_file:
            json_file.write( json.dumps( self.management_dict ) )
        with open( self.CNF_CMAKE_FILE , "w+") as cmake_file:
            line="add_subdirectory( ${CMAKE_CURRENT_LIST_DIR}/%s )"
            for package in self.management_dict["packages"]:
                cmake_file.write( line % package["name"] )

def create_package( package_name : str ):
    with open( CNF_PACKAGE_CONFIG_FILE , "w+") as package_json:
        package_json.writelines( CNF_DEFAULT_PACKAGE_CONFIG_CONTENT%package_name )

def getArgParser():
    parser = None
    if( parser is None ):
        parser = argparse.ArgumentParser( description="Package Manager", exit_on_error=True)
        parser.add_argument("-i","--install", nargs=1, required=False, help="Package URI" , dest="package_uri")
        parser.add_argument("-n","--name", nargs=1, required=True, help="Package name" , dest="package_name")
        parser.add_argument("-c","--create", nargs=1, required=False, help="Package name" , dest="new_package_name")
    return parser

def main():
    args = getArgParser().parse_args( sys.argv[1:] )
    package_name = args.package_name[0]
    package_uri = args.package_uri
    new_package_name = args.new_package_name
    if( not( package_uri is None ) ):
        pacman = PackageManager()
        pacman.add_package( package_name , package_uri[0] )
        pacman.save()
    elif( not( new_package_name is None ) ):
        create_package( new_package_name[0] )
    else:
        raise Exception("No package URI or package name given")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print( error )

