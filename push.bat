@echo off
echo ==========================================
echo   PUSHING ULTIMATE PLAYER S13 TO GITHUB   
echo ==========================================
git add .
git commit -m "Auto-update bracket scorelines & dynamic fixtures"
git push origin main
echo ==========================================
echo   DEPLOYMENT COMPLETE! REFRESH YOUR PAGE.
echo ==========================================
pause
