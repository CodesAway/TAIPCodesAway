import os.path
import shlex
import subprocess

from talon import (
    Module,
    actions,
    app,  # type: ignore
    cron,  # type: ignore
    registry,
)

mod = Module()

mod.list(
    "taip_git",
    "Git repositories to install via TAIP (Talon Automated Installation Platform)",
)
mod.list(
    "taip_vscode",
    "VSCode extension ids to install via TAIP (Talon Automated Installation Platform)",
)

vscode_extensions = set()


# Reference: https://github.com/talonhub/community/blob/main/plugin/talon_helpers/talon_helpers.py -> talon_get_active_registry_list
def get_active_registry_list(name: str) -> dict[str, str]:
    """Returns a COPY of the active list from the Talon registry"""
    return dict(registry.lists[name][-1])


def verify_valid_git(git_pathname: str) -> bool:
    command_list = [git_pathname, "version"]

    result = subprocess.run(
        command_list,
        shell=True,  # Don't show CMD window popup
    )

    return not result.returncode


def verify_valid_vscode(vscode_pathname: str) -> bool:
    command_list = [vscode_pathname, "--help"]

    result = subprocess.run(
        command_list,
        shell=True,  # Don't show CMD window popup
    )

    if not result.returncode:
        list_extensions_result = subprocess.run(
            [vscode_pathname, "--list-extensions"],
            capture_output=True,
            shell=True,  # Don't show CMD window popup
            text=True,
        )
        vscode_extensions.clear()
        vscode_extensions.update(list_extensions_result.stdout.splitlines())

    return not result.returncode


def validate_item_git(clone_command: str) -> list[str]:
    clone_command_args = shlex.split(clone_command)
    # The directory is the last command
    download_directory = os.path.join(actions.path.talon_user(), clone_command_args[-1])
    if os.path.isdir(download_directory):
        print(f"Skipping `{clone_command}` (already exists: {download_directory})")
        return []

    clone_command_args[-1] = download_directory
    return clone_command_args


def validate_item_vscode(unique_identifier: str) -> bool:
    # Noticed that results from code --list-extensions were all lowercase
    if unique_identifier.lower() in vscode_extensions:
        print(f"Skipping `{unique_identifier}` (already exists)")
        return False

    return True


def print_item_git(clone_command: str, url: str):
    if validate_item_git(clone_command):
        print(f"{clone_command} -> {url}")


def print_item_vscode(unique_identifier: str, url: str):
    if validate_item_vscode(unique_identifier):
        print(f"{unique_identifier} -> {url}")


def install_item_git(git_pathname: str, clone_command: str, url: str) -> bool:
    clone_command_args = validate_item_git(clone_command)

    if not clone_command_args:
        return False

    # Note: --single-branch is implied (since specify --depth) - https://git-scm.com/docs/git-clone#Documentation/git-clone.txt---depthdepth
    command_list = [git_pathname, "clone", url, "--depth", "1"]
    command_list.extend(clone_command_args)

    result = subprocess.run(
        command_list,
        capture_output=True,
        shell=True,  # Don't show CMD window popup
        text=True,
    )

    if result.returncode:
        print(f"Unable to install: {clone_command} -> {url}")

    if result.stdout:
        print("Standard Output:")
        print(result.stdout)

    if result.stderr:
        print("Standard Error:")
        print(result.stderr)

    return not result.returncode


def install_item_vscode(vscode_pathname: str, unique_identifier: str, url: str) -> bool:
    # TODO: currently, url argument is ignored (how should this be used?)
    if not validate_item_vscode(unique_identifier):
        return False

    if unique_identifier.lower() == "pokey.cursorless":
        workaround_missing_vscode_settings_file()

    command_list = [vscode_pathname, "--install-extension", unique_identifier]

    result = subprocess.run(
        command_list,
        capture_output=True,
        shell=True,  # Don't show CMD window popup
        text=True,
    )

    if result.returncode:
        print(f"Unable to install: {unique_identifier} -> {url}")

    if result.stdout:
        print("Standard Output:")
        print(result.stdout)

    if result.stderr:
        print("Standard Error:")
        print(result.stderr)

    if "is already installed." in result.stdout:
        return False

    return not result.returncode


def workaround_missing_vscode_settings_file():
    # Workaround for https://github.com/cursorless-dev/cursorless/issues/3030

    # TODO: for now, only handle Windows VSCode, since this is the only one I can confirm has an issue (handle others as needed)
    # Reference: https://github.com/cursorless-dev/cursorless/blob/main/cursorless-talon/src/apps/vscode_settings.py

    if app.platform != "windows":
        return

    settings_directory = os.path.expandvars(r"%APPDATA%\Code\User")
    settings_json_pathname = os.path.join(settings_directory, "settings.json")

    if os.path.exists(settings_json_pathname):
        return

    if os.path.isdir(settings_directory):
        # Since settings.json doesn't exist, create file with empty braces
        with open(settings_json_pathname, "w") as file:
            file.write("{}")


def print_latest():
    taip_handle_items(install=False)


def print_all():
    taip_handle_items(install=False, latest=False)


def install_latest():
    taip_handle_items()


def install_all():
    taip_handle_items(latest=False)


def taip_handle_items(install: bool = True, latest: bool = True):
    """Handle items via TAIP

    Args:
        install (bool, optional): Whether to install (the default) or just print to Talon log
        latest (bool, optional): Whether to handle only the latest (the default) or all items
    """

    handle_items_list = [
        ("user.taip_git", "git", verify_valid_git, install_item_git, print_item_git),
        (
            "user.taip_vscode",
            "code",
            verify_valid_vscode,
            install_item_vscode,
            print_item_vscode,
        ),
    ]

    anything_installed = False
    for handle_items in handle_items_list:
        talon_list, default_command, verify_valid, install_item, print_item = (
            handle_items
        )

        if talon_list not in registry.lists:
            error_message = f"Could not find Talon list: {talon_list}"
            print(error_message)
            app.notify(error_message)
            continue

        taip_items = get_active_registry_list(talon_list)
        program_pathname = taip_items.pop("program_pathname", default_command)
        program_pathname = os.path.expandvars(program_pathname)

        if not verify_valid(program_pathname):
            error_message = (
                f"Could not find program (from {talon_list}): {program_pathname}"
            )
            print(error_message)
            app.notify(
                error_message,
                "Restart Talon if installed while Talon was running",
            )
            continue

        action = "Install" if install else "Print"
        if latest:
            action += " latest"

        print(f"{action} {talon_list} items...\n{program_pathname=}")

        if latest:
            # TODO: populate from database storage
            existing_keys = set()
            for key in existing_keys:
                existing_value = taip_items.pop(key, None)
                if existing_value is None:
                    continue

                print(f"Skipping `{key}` (previously installed)")

        for key, value in taip_items.items():
            if install:
                installed = install_item(program_pathname, key, value)
                if installed:
                    print(f"Installed: {key} -> {value}")
                    anything_installed = True
            else:
                print_item(key, value)

    if install:
        if anything_installed:
            app.notify("TAIP - Please restart Talon")
        else:
            app.notify("TAIP - Nothing was installed")


@mod.action_class
class Actions:
    def taip_print_latest():
        """Use TAIP (Talon Automated Installation Platform) to print latest (to Talon log) without installing anything"""
        cron.after("0ms", print_latest)

    def taip_print_all():
        """Use TAIP (Talon Automated Installation Platform) to print all (to Talon log) without installing anything"""
        cron.after("0ms", print_all)

    def taip_install_latest():
        """Use TAIP (Talon Automated Installation Platform) to install latest"""
        cron.after("0ms", install_latest)

    def taip_install_all():
        """Use TAIP (Talon Automated Installation Platform) to install all"""
        cron.after("0ms", install_all)
