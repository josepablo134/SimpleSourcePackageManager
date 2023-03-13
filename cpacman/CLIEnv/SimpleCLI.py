default_help_command=[
        "--help","-h"
]

class SimpleCLI:
    context_save = {}
    """
    SimpleCLI command super class
    """
    def __init__( self ) -> None:
        """ Initializing string containers where place error and log messages """

    def process( self, argv:list=[] ) -> int:
        """ Process arguments in form of a list, if fails raises an exception,
            if succeed then returns stdout string.
        """
        pass

    def help( self, argv:list=[] ) -> int:
        """ Returns a generic help message if argv is an empty list,
            or a specific message for the argv list.
        """
        pass

cli_module_names=[]
