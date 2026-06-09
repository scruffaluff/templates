// Application entrypoint and command line parsers.

#include <argparse/argparse.hpp>
#include <iostream>

#include "lib.hpp"

int main(int argc, char **argv) {
    argparse::ArgumentParser program("{{ cookiecutter.__project_package }}", "0.1.0");

    try {
        program.parse_args(argc, argv);
    } catch (const std::exception &err) {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        return 1;
    }

    return 0;
}
