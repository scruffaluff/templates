// Application entrypoint and command line parsers.

#include <argparse/argparse.hpp>
#include <exception>
#include <iostream>

#include "lib.hpp"

int main(int argc, char** argv) {
    argparse::ArgumentParser program("{{ cookiecutter.__project_package }}", "0.1.0");

    try {
        program.parse_args(argc, argv);
    } catch (const std::exception& error) {
        std::cerr << error.what() << "\n";
        std::cerr << program;
        return 1;
    }

    return 0;
}
