# QXDM-SIM-APDU-Analyzer

eSIM device supporting DSDS(Dual SIM Dual Standby) has following limitations.
 - The interface between eSIM and ME(Mobile Equipment) can not be traced with contact-based SIM tracer alike Minimove (COMPRION) 
 - ME's logs includes mixed APDU logs from pSIM and eSIM.

This tool helps you to overcome the above limits.
 - APDU logs can be analyzed on application-level and protocol-leved similarly to contact-based SIM tracer.
 - APDU logs from pSIM or eSIM can be sorted by user's selection.


[Guide]
1) run main.py
2) click 'Open' button and load a text file(.txt) in 'file_sample' directory
  ※ filtered with 'UIM APDU [0x19B7]' from QXDM or QCAT logs
3) select SIM1 or SIM2
4) click 'Execute' button

![image](https://user-images.githubusercontent.com/98713651/176852087-5609e529-266c-43a7-a2ff-75ae41fba760.png)
