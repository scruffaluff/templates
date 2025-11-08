//! Application tests.

use assert_cmd::Command;

#[test]
fn version() {
    let mut cmd = Command::cargo_bin("{{ cookiecutter.project_name }}").unwrap();
    cmd.args(&["--version"]);
    cmd.assert().success();
}
