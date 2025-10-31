@echo off
echo ================================================
echo Building Training Q&A Helper Executable
echo ================================================
echo.

echo Installing PyInstaller if needed...
pip install pyinstaller

echo.
echo Building executable...
echo.

pyinstaller --name=TrainingQA-Helper --onefile --windowed --hidden-import=pywinstyles --hidden-import=PIL._tkinter_finder --collect-all=pywinstyles --clean --noconfirm gui.py

echo.
echo ================================================
echo Build Complete!
echo ================================================
echo.
echo Executable location: dist\TrainingQA-Helper.exe
echo.
echo IMPORTANT: Place your .env file in:
echo            Environment-Variables\.env
echo            (relative to the .exe location)
echo.
pause
