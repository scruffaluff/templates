// End to end tests.

#include <array>
#include <catch2/catch_test_macros.hpp>
#include <reproc++/arguments.hpp>
#include <reproc++/drain.hpp>
#include <reproc++/reproc.hpp>
#include <reproc++/run.hpp>
#include <string>

TEST_CASE("Check project version") {
    reproc::options options;
    options.redirect.out.type = reproc::redirect::pipe;
    options.redirect.err.type = reproc::redirect::parent;
    std::string output;

    const auto args = reproc::arguments(
        std::array<std::string, 2>{"build/Debug/{{ cookiecutter.__project_package }}", "--version"});
    const auto [exit_code, error] = reproc::run(
        args, options, reproc::sink::string(output), reproc::sink::null);
    REQUIRE(!error);
    REQUIRE(exit_code == 0);
    REQUIRE(output == "0.1.0\n");
}
