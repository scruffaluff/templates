//! Application entrypoint and command line parsers.

use clap::Parser;

#[derive(Debug, Parser)]
#[command(about, version)]
struct Cli {}

fn main() {
    Cli::parse();
}
