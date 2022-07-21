# QXDM-SIM-APDU-Analyzer

eSIM device supporting DSDS(Dual SIM Dual Standby) has following limitations.
 - The interface between eSIM and ME(Mobile Equipment) can not be traced with contact-based SIM tracer alike Minimove (COMPRION) 
 - ME's logs includes mixed APDU logs from pSIM and eSIM.

This tool helps you to overcome the above limits.
 - APDU logs can be analyzed on application-level and protocol-leved similarly to contact-based SIM tracer.
 - APDU logs from pSIM or eSIM can be sorted by user's selection.


[Guide]
1) run main.py
2) click 'Open file' or 'Clipboard' button
3) select SIM1 or SIM2
4) click 'Execute' button

※ text file(.txt) in 'file_sample' directory, which is filtered with 'UIM APDU [0x19B7]' from QCAT logs

![image](https://user-images.githubusercontent.com/98713651/180137163-67f260c2-a6cb-441e-a972-e892c2eba9f1.png)
