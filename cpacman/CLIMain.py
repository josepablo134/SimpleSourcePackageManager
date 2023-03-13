import sys

from PackageManager import PackageManager

from CLIEnvFactory import cli_factory_command_list
from CLIEnvFactory import cli_factory_populate
from CLIEnvFactory import cli_factory

from CLIEnv import SimpleCLI
from CLIEnv import Installer

MODULE_CMD=0
MODULE_CLASS=1
module_list = [
        [Installer.cli_module_names, Installer.Installer ],
]

class CLIMain(SimpleCLI.SimpleCLI):
    def __init__( self ) -> None:
        super().__init__()
        self.context_save["pacman"] = PackageManager()

        for module in module_list:
            cli_factory_populate( module[MODULE_CMD] , module[MODULE_CLASS] )

    def process( self, argv:list=[] ) -> int:
        if( len( argv ) < 1 ):
            return self.help()

        cmd = argv[0]
        if( cmd in SimpleCLI.default_help_command ):
            return self.help()

        cli_cmd = cli_factory( cmd )
        if( cli_cmd == None ):
            print( f"Invalid command \"{cmd}\"" , file=sys.stderr )
            return self.help()
        else:
            if( len( argv ) < 2 ):
                return cli_cmd.process( )
            else:
                return cli_cmd.process( argv[1:] )

    def help(self, argv:list=[] ) -> int:
        print( f"\ncpacman [command] <arg1> <arg2>" )
        print( "\nCommand list:\n" )
        for command in cli_factory_command_list():
            print( f"\t{command}" )
        print( "\n[command] --help/-h: to show specific command help" )
        print( "\n--help: Shows this message" )
        return 0

cli_module_names=[
]

