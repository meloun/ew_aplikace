@ECHO OFF
IF "%1"=="" GOTO NE
:JO
    pyuic4 -x mainwindow.ui -o %1
:NE
    pyuic4 -x tableView.ui -o tableView.py
    GOTO END   
:END    