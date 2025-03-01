Lynx buildroot
=======
Buildroot is a GN toolset that optimizes parameters and expands features based on [Chromium/build](https://chromium.googlesource.com/chromium/src/build), specifically tailored for the management and construction of the Lynx project. It offers a comprehensive set of GN multi-platform build configurations and tools, enabling developers to efficiently build and deploy the Lynx project.

## Contents
1. `//build/[android/apple/fuchsia/ios/linux/mac/win]`: GN templates and Python build scripts specific to the corresponding system platforms.
2. `//build/config`: Common GN templates and default configurations for builtin templates.
3. `//build/config/BUILDCONFIG.gn`: All `BUILD.gn` files will include this file by setting `buildconfig = "//build/config/BUILDCONFIG.gn"` in the `.gn` file.
4. `//build/toolchain`: Definitions of GN compilation toolchains.
5. `//build/secondary`: An overlay for BUILD.gn files. Enables adding BUILD.gn to directories that live in sub-repositories by setting `secondary_source = "//build/secondary/"` in the .gn file.
6. Other `.py` files: Some are used by GN/Ninja. Some are used by gclient hooks, and some are just random utilities.

## Quick Start
1. Pull this repository into a subdirectory of the project.
    ```shell
    cd path/to/project
    git clone git@github.com:lynx-infra/buildroot.git build
    
    # You will get the following directory structure
    project
    ├── build               # buildroot directory
    ├── .gn
    ├── BUILD.gn
    └── ...
    ```
2. Configure the .gn file in the root directory.
    ```gn
    # project/.gn file 
    script_executable = "python3"
    buildconfig = "//build/config/BUILDCONFIG.gn"
    secondary_source = "//build/secondary/"
    ```
3. Then you can enjoy the default compilation configurations and tools provided by buildroot.

## Contributing
1. Fork the [repository](https://github.com/lynx-infra/buildroot.git) and clone it to your local machine.
2. Create a new branch: `git checkout -b name-of-your-branch`.
3. Make your changes.
4. Once you have finished the necessary tests and verification locally, you can commit the changes with a commit message in the following format to you branch.
    ```shell
    [Label] Title of the commit message(one line)

    Summary of change:
    Longer description of change addressing as appropriate: why the change
    is made, context if it is part of many changes, description of previous
    behavior and newly introduced differences, etc.

    ```
    The title should start with at least one label, and the first label should be one of the following: `Feature`, `BugFix`, `Refactor`, `Optimize`, `Infra`, `Testing`, `Doc`. The format should be: `[Label]`, e.g., `[BugFix]`, `[Feature]`, `[BugFix][Tools]`. Please choose an appropriate label according to your changes.
5. Push the changes to your remote branch and start a pull request to the `main` branch of the original repository.