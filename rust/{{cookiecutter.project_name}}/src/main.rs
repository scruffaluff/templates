//! Application entrypoint and command line parsers.

use clap::{AppSettings, Parser};

#[derive(Parser)]
#[clap(
    about = env!("CARGO_PKG_DESCRIPTION"),
    global_setting = AppSettings::ColorAuto,
    global_setting = AppSettings::ColoredHelp,
    version = env!("CARGO_PKG_VERSION"),
)]
struct Cli {}

fn main() -> eyre::Result<()> {
    Cli::parse();
    Ok(())
}
