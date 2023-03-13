# Simple Source Package Manager (cpacman)

This is a simple package manager inspired on npm.
Allows the easy installation of source code as packages as long as they have a CMake structure.

The idea behind this little project is enable reusability of my personal repositories as packages for future projects with an easy setup.

# How it works

Right now the project is very basic and unstable. But the idea is to create a `package.json` file containing the reference to the packages as shown:

```.json
{
  "name": "DummyProject",
  "version": "1.0.0",
  "description": "This is a template",
  "author": "Anonymous",
  "license": "ISC",
  "dependencies": [
		{ "name":"microMiddlewares", "uri":"git@github.com:josepablo134/microMiddlewares.git", "type":"git" },
		{ "name":"local_project_source", "uri":"path/to/some/local/project", "type":"path" }
  ]
}
```

Once `package.json` is defined, it is matter of running the package manager:

```.sh
$ cpacman install
```

After the installation, if everything is ok, you will see a new folder `c_modules` with the following content:

 - List of folders with the name of the requested packages.
 - __CMakeLists.txt__ : The CMake file to import the packages.
 - __packages.json__ : A summary file that holds the list of packages installed.

# Import to project's CMake

Just add the sub directory and link with the new libraries:

```.cmake
add_subdirectory( ${PROJECT_SOURCE_DIR}/c_modules )

target_link_libraries( ${EXEC_NAME}
		DummyLib
)
```

# Installation

Simply add the `cpacman` folder to the path and invoke cpacman from the command line. (Linux only)

