!include "MUI.nsh"

!define MUI_ABORTWARNING # This will warn the user if they exit from the installer.

!insertmacro MUI_PAGE_WELCOME # Welcome to the installer page.
!insertmacro MUI_PAGE_LICENSE "C:\AllFiles\MaxPyCharm\NSIS-Code-Maker\License.rtf"
!insertmacro MUI_PAGE_INSTFILES # Installing page.
!insertmacro MUI_PAGE_FINISH # Finished installation page.

!insertmacro MUI_LANGUAGE "English"

Name "J* Package Manager" # Name of the installer (usually the name of the application to install).
OutFile "JStarPackageManagerInstaller.exe" # Name of the installer's file.
InstallDir "C:\jpm" # Default installing folder
RequestExecutionLevel admin

# start default section
Section

    # set the installation directory as the destination for the following actions
    SetOutPath $INSTDIR

    File /r "C:\AllFiles\python\JStar\jpm\exe\exe\*"

SectionEnd