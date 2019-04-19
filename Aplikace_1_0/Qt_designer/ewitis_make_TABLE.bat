@ECHO OFF
IF "%1"=="" GOTO NE
:JO
    pyuic4 -x mainwindow.ui -o %1
:NE
    pyuic4 -x ewitis_qt_template_v1_xx_TABLE.ui -o ewitis_qt_template_v1_xx_TABLE.py
    GOTO END   
:END    