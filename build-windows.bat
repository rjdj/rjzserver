xcopy . c:\rjzserver\ /D /Y /E
"c:\Program Files\Bazaar\bzr.exe" revno > version
set /p VER= < version
set DEST=/home/rjdj/www/dev_rjdj_me/builds/rjzserver
c:
cd c:\rjzserver

rem delete old files
rmdir /s /q dist
rmdir /s /q rjzserver-%VER%.win

"c:\Program Files\Subversion\bin\svn.exe" co http://svn.makotemplates.org/mako/trunk/lib/mako
c:\Python25\python.exe build-windows.py
copy c:\Python25\Lib\site-packages\wx-2.8-msw-unicode\wx\msvcp71.dll dist\
copy c:\Python25\Lib\site-packages\wx-2.8-msw-unicode\wx\gdiplus.dll dist\
xcopy /D /E /Y media dist\media\
move dist rjzserver-%VER%.win
zip -r rjzserver-%VER%.win.zip rjzserver-%VER%.win
pscp rjzserver-%VER%.win.zip osc.rjdj.me:%DEST%/versions/
@echo "Now do the following in putty:"
@echo "cd %DEST%; rm rjzserver-%VER%.win.zip; ln -s versions/rjzserver-%VER%.win.zip"
putty osc.rjdj.me 
p:
