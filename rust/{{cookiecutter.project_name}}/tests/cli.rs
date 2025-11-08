//! Application tests.

use assert_cmd::{Command, cargo};

#[test]
fn version() {
    let mut cmd = Command::new(cargo::cargo_bin!());
    cmd.args(&["--version"]);
    cmd.assert().success();
}
