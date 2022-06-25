import file_system
debug_mode = 0
def process(data, cmd, log_ch):
    detail = ''
    if data[0][0] == '4':  # ETSI 102.221 Table 10.4a extended logical channels
        log_ch_id = 16 # excluding 00~0F
    else:
        log_ch_id = int(data[0][1])
    if log_ch_id > len(log_ch) - 1:
        for n in range(log_ch_id - len(log_ch) + 1):
            log_ch.append(['N/A','N/A'])

    if cmd == 'SELECT':
        if len(data) < 3:
            detail = 'Invalid length'
        elif data[-1][-4:] == '9000':
            file_id = data[2]
            if file_id[0:2] == 'A0':
                log_ch[log_ch_id][0] = file_id
                log_ch[log_ch_id][1] = ''
                log_ch[log_ch_id].append(file_id)
                if len(log_ch[log_ch_id])>3: del log_ch[log_ch_id][-1]
            else:
                if len(file_id) <= 4:
                    if file_id == '3F00':
                        log_ch[log_ch_id][0] = file_id
                        log_ch[log_ch_id][1] = ''
                    elif file_id == '7FFF':
                        log_ch[log_ch_id][1] = ''
                        if len(log_ch[log_ch_id]) == 3:
                            log_ch[log_ch_id][0] = log_ch[log_ch_id][2]
                        else: # last selected AID not available
                            log_ch[log_ch_id][0] = 'USIM or ISIM ADF'
                    else:
                        log_ch[log_ch_id][1] = file_id
                else:
                    if file_id[0:4] == '7F10':
                        if file_id[4:6] == '5F':
                            log_ch[log_ch_id][0] = file_id[0:8]
                            if len(file_id) > 8:
                                log_ch[log_ch_id][1] = file_id[8:12]
                            else:
                                log_ch[log_ch_id][1] = ''
                        else:
                            log_ch[log_ch_id][0] = file_id[0:4]
                            if len(file_id) > 4:
                                log_ch[log_ch_id][1] = file_id[4:8]
                            else:
                                log_ch[log_ch_id][1] = ''
                    elif file_id[0:4] == '7FFF':
                        if file_id[4:6] == '5F':
                            log_ch[log_ch_id][0] = file_id[0:8]
                            if len(file_id) > 8:
                                log_ch[log_ch_id][1] = file_id[8:12]
                            else:
                                log_ch[log_ch_id][1] = ''
                        else: # current ADF
                            log_ch[log_ch_id][1] = file_id[4:8]
                            if len(log_ch[log_ch_id]) == 3:
                                log_ch[log_ch_id][0] = log_ch[log_ch_id][2]
                            else:
                                if log_ch[log_ch_id][0] == '3F00' or '7F10' in log_ch[log_ch_id][0] :
                                    log_ch[log_ch_id][0] = 'A0000000871002FF82FFFF89010000FF'
                                    # MF and DF TELECOM use same logical channel with USIM ADF
                                elif '7FFF5F' in log_ch[log_ch_id][0]:
                                    log_ch[log_ch_id][0] = 'A0000000871002FF82FFFF89010000FF'
                                    # child DF not defined in ISIM ADF, select USIM ADF by default
                                else:
                                    log_ch[log_ch_id][0] = 'USIM or ISIM ADF'
                                    # last selected AID not available
                                    # TBD ISIM EF 여부 확인 후 USIM ISIM 결정

            if debug_mode :
                print('=' * 50)
                print('prot_data  :', data[0][0:2], data[2])
                print('current_DF :', log_ch[log_ch_id][0])
                print('current_EF :', log_ch[log_ch_id][1])

    # elif cmd == 'STORE DATA':
    #     if data[-1][-4:] == '9000':
    #         if data[0][0] == '8' : # ETSI 102.221 Table 10.3 Structured as for '0X'
    #             log_ch_id = int(data[0][1])
    #         if log_ch_id > len(log_ch)-1:
    #             for n in range(log_ch_id - len(log_ch)+1):
    #                 log_ch.append(['',''])
    #         if log_ch[log_ch_id][0] == '':
    #             print("OK")
    #             log_ch[log_ch_id][0] = 'A0000005591010FFFFFFFF8900000100'

    return detail, log_ch

cmd_name = dict()

def detail(data, cmd):
    detail = ''
    if cmd == 'SELECT':
        data
    return detail

cmd_name = dict()

# ETSI 102.221
cmd_name['A4'] = 'SELECT'
cmd_name['F2'] = 'STATUS'
cmd_name['B0'] = 'READ BINARY'
cmd_name['D6'] = 'UPDATE BINARY'
cmd_name['B2'] = 'READ RECORD'
cmd_name['DC'] = 'UPDATE RECORD'
cmd_name['A2'] = 'SEARCH RECORD'
cmd_name['32'] = 'INCREASE'
cmd_name['CB'] = 'RETRIEVE DATA'
cmd_name['DB'] = 'SET DATA'
cmd_name['20'] = 'VERIFY PIN'
cmd_name['24'] = 'CHANGE PIN'
cmd_name['26'] = 'DISABLE PIN'
cmd_name['28'] = 'ENABLE PIN'
cmd_name['2C'] = 'UNBLOCK PIN'
cmd_name['04'] = 'DEACTIVATE FILE'
cmd_name['44'] = 'ACTIVATE FILE'
cmd_name['88'] = 'AUTHENTICATE'
cmd_name['89'] = 'AUTHENTICATE'
cmd_name['84'] = 'GET CHALLENGE'
cmd_name['AA'] = 'TERMINAL CAPABILITY'
cmd_name['10'] = 'TERMINAL PROFILE'
cmd_name['C2'] = 'ENVELOPE'
cmd_name['12'] = 'FETCH'
cmd_name['14'] = 'TERMINAL RESPONSE'
cmd_name['70'] = 'MANAGE CHANNEL'
cmd_name['73'] = 'MANAGE SECURE CHANNEL'
cmd_name['75'] = 'TRANSACT DATA'
cmd_name['76'] = 'SUSPEND UICC'
cmd_name['78'] = 'GET IDENTITY'

# Global Platform v2.3.1
cmd_name['E4'] = 'DELETE'
cmd_name['CA'] = 'GET DATA'
cmd_name['CB'] = 'GET DATA'
cmd_name['F2'] = 'GET STATUS'
cmd_name['E6'] = 'INSTALL'
cmd_name['E8'] = 'LOAD'
cmd_name['D8'] = 'PUT KEY'
cmd_name['F0'] = 'SET STATUS'
cmd_name['E2'] = 'STORE DATA'

# # ISO7816-4
# cmd_name['D0'] = 'WRITE BIRARY'
# cmd_name['0E'] = 'ERASE BIRARY'
# cmd_name['D2'] = 'WRITE RECORD'
# cmd_name['E2'] = 'APPEND RECORD'
# cmd_name['CA'] = 'GET DATA'
# cmd_name['DA'] = 'PUT DATA'
# cmd_name['B4'] = 'GET CHALLENGE'
