@echo off
echo ====================================
echo WMGInvent Test Runner
echo ====================================
echo.
echo Step 1: Cleaning Python cache files...
python clean_cache.py
echo.
echo Step 2: Running all tests...
echo ====================================
python -m unittest tests/test_app.py
echo ====================================
echo.
echo Test run complete!
pause 