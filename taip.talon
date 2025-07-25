# TODO: add option to clear latest (could have separate commands for Git and VSCode)?

# Put tape instead of taip since sometimes Talon didn't recognize commands

tape customize git:                             user.taip_edit_text_file("taip_git.talon-list")
tape customize code:                            user.taip_edit_text_file("taip_vscode.talon-list")

tape print latest:
    user.taip_print_latest()
    menu.open_log()

tape print all:
    user.taip_print_all()
    menu.open_log()

tape install latest:
    user.taip_install_latest()
    menu.open_log()

tape install all:
    user.taip_install_all()
    menu.open_log()
