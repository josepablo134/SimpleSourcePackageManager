import argparse
import sys
from .SimpleCLI import SimpleCLI,default_help_command

class Installer(SimpleCLI):
    URI_TYPES=[]
    def __init__( self ) -> None:
        super().__init__( )
        self.parser = self.__getArgParser()

    def __getArgParser( self ):
        self.URI_TYPES = self.context_save["pacman"].URI_TYPES
        parser = None
        if( parser is None ):
            parser = argparse.ArgumentParser( prog="install", description="Installer", exit_on_error=True )
            parser.add_argument("-n","--name", nargs=1, required=True, help="Package name" , dest="package_name")
            parser.add_argument("-u","--URI", nargs=1, required=True, help="Package uri" , dest="package_uri")
            parser.add_argument("-t","--type", nargs=1, required=True, help=f"Package type: {self.URI_TYPES}" , dest="package_type")
        return parser

    def process( self, argv:list=[] ) -> int:
        pacman = self.context_save["pacman"]
        if( len( argv ) == 0 ):
            pacman.populate_packages()
            pacman.save()
            return 0
        else:
            raise Exception("Feature is WIP")
        if( len( argv ) < 2 ):
            self.parser.print_help()
            return -1
        args = self.parser.parse_args( argv )

        package_uri = args.package_uri[0]
        package_name = args.package_name[0]
        package_type = args.package_type[0]

        if( not( package_type in self.URI_TYPES ) ):
            print( f"available types are {self.URI_TYPES}", file=sys.stderr )
            return -1
        pacman.add_package( package_name, package_uri, package_type)
        pacman.save()
        return 0

    def help( self, argv:list=[] ) -> int:
        self.parser.print_help()
        return 0

cli_module_names=[
        "install",
]

