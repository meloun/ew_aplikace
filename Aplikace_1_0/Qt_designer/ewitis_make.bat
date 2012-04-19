@ECHO OFF
IF "%1"=="" GOTO NE
:JO
    pyuic4 -x mainwindow.ui -o %1
:NE
    pyuic4 -x ewitis_qt_template_v0_1.ui -o ewitis_qt_template_v0_1.py
    GOTO END   
:END    