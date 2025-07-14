# TAIP - Talon Automated Installation Platform

![Letters T A I P looking like torn tape with another piece of tape across the letters A and I](https://github.com/user-attachments/assets/526a73eb-09f8-49c9-b73f-408495543804)<br/>
The tool doesn't use AI (just the image)

## GOAL!!!

My goal with TAIP (pronounced "tape") is to facilitate setting up voice control for non-technical and technical audiences alike.

**Note**: The below setup steps are what I use for a 100% admin-free Windows install of Talon, `git`, VSCode, and the wonderful world of voice control.

I've included links to install on Mac or Linux. I don't have a Mac or Linux computer, so please submit an issue if TAIP isn't working for you!

## Installation

### (Suggested) Install VSCode

**Note**: VSCode combined with Cursorless and the various Talon related extensions make it enjoyable to create your own custom grammar (no coding required). TAIP is able to install VSCode extensions for you!

1. Open https://code.visualstudio.com/download
2. Click **User Installer x64**
3. Use default install directory `%LocalAppData%\Programs\Microsoft VS Code`
4. Optionally, check **Add "Open with Code" action to Windows Explorer** options
5. Install!

### Install `git`

**Note**: TAIP will use `git` to install the various Talon command sets, which are what define the grammar for the voice commands.

1. Open https://git-scm.com/downloads
2. Download (standalone installer) and run the installer
3. Use default install directory `%LocalAppData%\Programs\Git`
4. Install default selection of components
5. Chose the default editor for `git` (I select Notepad since no external dependencies; I've never had to use this for `git` though)
6. Override the default branch name for new repositories (suggest using the default **main**)
7. Use default options for the rest and let it install

### Install Talon

**Note**: The portable zip doesn't require admin, whereas the **Download for Windows** exe currently does.

1. Open https://talonvoice.com
2. Click **Windows (portable zip)**
3. Extract to a folder of your choice
4. Run **talon.exe**
5. Accept the EULA
6. Talon lives in the system tray
7. Optionally, right click the icon and check **Start on Login**
8. Right click the icon, under **Speech Recognition**, install the latest speech engine (this is used to recognize your voice commands locally)

### Install TAIP

#### Windows
Open a command prompt, paste the following command, and press `Enter` to install TAIP using `git`.

```shell
git clone https://github.com/CodesAway/TAIPCodesAway %AppData%\Talon\user\TAIPCodesAway
```

#### Linux & Mac

Open a terminal, paste the following command, and press `Enter`/`Return` to install TAIP using `git`.

```shell
git clone https://github.com/CodesAway/TAIPCodesAway ~/.talon/user/TAIPCodesAway
```

### Install Talon community command set and other items using TAIP

Customize which items to install
* `tape customize git` - edit `taip_git.talon-list`
* `tape customize code` - edit `taip_vscode.talon-list`

Print and install latest items (typical commands to use)
* `tape print latest` - print latest items to Talon log (useful before installing to verify what will be installed)
* `tape install latest` - install latest items

Print and install all items
* `tape print all` - print all items to Talon log
* `tap install all` - install all items (will skip stuff already installed)

## (Suggested) Install Rango extension

**Note**: Rango is a cross browser extension that helps you interact with web pages using your voice and Talon

Chrome extension
https://chromewebstore.google.com/detail/rango/lnemjdnjjofijemhdogofbpcedhgcpmb

**Reference**: https://github.com/david-tejada/rango?tab=readme-ov-file#installation

Rango Talon command set is included by default in the files installed using TAIP

Enable keyboard clicking (voice command `keyboard switch`)
1. Right click on extension icon
2. Click **Keyboard Clicking**

## Additional resources
* There is an active community of Talon users on Slack to help you along your voice control journey! (https://talonvoice.com/chat)

* Talon wiki (https://talon.wiki)
  * Basic usage (https://talon.wiki/Basic%20Usage/basic_usage)
  * Talon user file set list (https://talon.wiki/integrations/talon_user_file_sets)

* Talon practice (https://chaosparrot.github.io/talon_practice)

* Cursorless (https://www.cursorless.org)
  * Cursorless documentation (https://www.cursorless.org/docs)
  * Cursorless cheatsheet (https://www.cursorless.org/cheatsheet)

* Andreas Talon user scripts (https://github.com/AndreasArvidsson/andreas-talon)