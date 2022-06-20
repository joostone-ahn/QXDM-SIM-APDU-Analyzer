# QXDM-SIM-APDU-Analyzer

eSIM device supporting DSDS(Dual SIM Dual Standby) has following limitations.
 - The interface between eSIM and ME(Mobile Equipment) can not be traced with contact-based SIM tracer alike Minimove (COMPRION) 
 - ME's logs includes mixed APDU logs from pSIM and eSIM.

This tool helps you to overcome the above limits.
 - APDU logs can be analyzed on application-level and protocol-leved similarly to contact-based SIM tracer.
 - APDU logs from pSIM or eSIM can be sorted by user's selection.

[Guide]
1) run main.py
2) click 'Open file'
 ※ file_sample : filtered with 'UIM APDU [0x19B7]' from QXDM or QCAT logs and saved as a text file(.txt).

![image](https://user-images.githubusercontent.com/98713651/174545149-abb382ec-b148-4d33-b738-31386c6d097c.png)
