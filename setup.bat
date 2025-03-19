@echo off
setlocal

REM Define paths
set SCRIPT_DIR=%~dp0
set BAT_FILE=%SCRIPT_DIR%WOMUpdater.bat
set SHORTCUT_NAME=WOMUpdater.lnk
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set VIRTUAL_ENVIRONMENT=%SCRIPT_DIR%.venv

REM Ensure virtual environment exists
if not exist "%VIRTUAL_ENVIRONMENT%" (
  echo Creating virtual environment...
  py -m venv "%VIRTUAL_ENVIRONMENT%"

  REM Install dependencies if requirements.txt exists
  if exist "%SCRIPT_DIR%requirements.txt" (
    call "%VIRTUAL_ENVIRONMENT%\Scripts\activate"
    pip install -r "%SCRIPT_DIR%requirements.txt"
  )
)

REM Create the batch file to run at startup (overwrite if needed)
(
  echo @echo off
  echo cd /d "%%~dp0src"
  echo call "%%~dp0.venv\Scripts\activate"
  echo py main.py
  echo exit
) > "%BAT_FILE%"

REM Create a shortcut in the Startup folder using PowerShell
setlocal

set "PS_SCRIPT=$WshShell = New-Object -ComObject WScript.Shell; $ShortcutPath = Join-Path -Path '%STARTUP_FOLDER%' -ChildPath '%SHORTCUT_NAME%'; $Shortcut = $WshShell.CreateShortcut($ShortcutPath); $Shortcut.TargetPath = '%BAT_FILE%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Save();"

powershell -NoProfile -ExecutionPolicy Bypass -Command "%PS_SCRIPT%"

endlocal

echo Setup complete! WOM Updater will now run on startup.
pause
