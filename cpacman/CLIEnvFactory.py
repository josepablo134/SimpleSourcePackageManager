from CLIEnv import SimpleCLI

COMMANDS={
}

def cli_factory_populate( names:list , constructor:any ):
    global COMMANDS
    for name in names:
        COMMANDS[name] = constructor

def cli_factory_command_list() -> list:
    return COMMANDS.keys()

def cli_factory( command: str ) -> SimpleCLI:
    command = command.lower()
    if ( command == None ):
        return None
    cmdConstructor = COMMANDS.get( command )
    if( cmdConstructor == None ):
        return None
    return cmdConstructor()

