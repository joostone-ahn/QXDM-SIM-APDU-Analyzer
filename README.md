# QXDM-SIM-APDU-Analyzer

eSIM devices supporting DSDS(Dual SIM Dual Standby) have the following limitations.
 - The interface between eSIM and ME(Mobile Equipment) can not be traced with contact-based tools alike Minimove (COMPRION) 
 - ME's logs includes mixed APDU logs from pSIM and eSIM.

If you want to analyze eSIM's APDU protocol, you have to analyze it in ME side.
This tool helps you to analyze SIM APDU protocol with QXDM or QCAT logs.
If you load the text file, you can analyze APDU logs on application-level and protocol-level.

[Guide]
1) run main.py
2) click 'Open file'
 ※ file_sample : filtered with 'UIM APDU [0x19B7]' from QXDM or QCAT logs and saved as a text file(.txt).

![image](https://user-images.githubusercontent.com/98713651/174545149-abb382ec-b148-4d33-b738-31386c6d097c.png)
