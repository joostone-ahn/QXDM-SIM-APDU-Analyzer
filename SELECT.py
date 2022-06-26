import file_system
debug_mode = 0

def process(data, log_ch, log_ch_id):
    if data[-1][-4:] != '9000' and data[-1][-4:-2] != '91':
        log_ch_prev_0 = log_ch[log_ch_id][0]
        log_ch_prev_1 = log_ch[log_ch_id][1]

    file_id = data[2]
    if file_id[0:2] == 'A0':
        log_ch[log_ch_id][0] = file_id
        log_ch[log_ch_id][1] = ''
    else:
        if len(file_id) <= 4:
            if file_id in file_system.DF_name: # MF or DF(7F10)
                log_ch[log_ch_id][0] = file_id
                log_ch[log_ch_id][1] = ''
            elif file_id in file_system.EF_name['3F00']: # MF's child EF
                log_ch[log_ch_id][0] = '3F00'
                log_ch[log_ch_id][1] = file_id
            elif file_id == '7FFF':
                log_ch[log_ch_id][1] = ''
                if len(log_ch[log_ch_id]) == 3:
                    log_ch[log_ch_id][0] = log_ch[log_ch_id][2]
                else:
                    log_ch[log_ch_id][0] = '' # Last selected AID not decided
            else:
                log_ch[log_ch_id][0] = file_id
                log_ch[log_ch_id][1] = file_id
        else: # len(file_id) > 4
            if file_id[0:4] == '7F10':
                if file_id[4:6] == '5F':
                    log_ch[log_ch_id][0] = file_id[0:8]
                    if len(file_id) > 8:
                        log_ch[log_ch_id][1] = file_id[8:]
                    else:
                        log_ch[log_ch_id][1] = ''
                else:
                    log_ch[log_ch_id][0] = file_id[0:4]
                    log_ch[log_ch_id][1] = file_id[4:]
            elif file_id[0:4] == '7FFF':
                if file_id[4:6] == '5F':
                    log_ch[log_ch_id][0] = file_id[0:8]
                    if len(file_id) > 8:
                        log_ch[log_ch_id][1] = file_id[8:]
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
                            if log_ch[log_ch_id][1] in file_system.USIM_EF_list:
                                if log_ch[log_ch_id][1] in file_system.ISIM_EF_list:
                                    log_ch[log_ch_id][0] = '' # Last selected AID not decided
                                else: # USIM ADF decided
                                    log_ch[log_ch_id][0] = 'A0000000871002FF82FFFF89010000FF'
                            else:
                                if log_ch[log_ch_id][1] in file_system.ISIM_EF_list: # ISIM ADF decided
                                    log_ch[log_ch_id][0] = 'A0000000871004FF82FFFF89010000FF'
                                else:
                                    log_ch[log_ch_id][0] = '' # Last selected AID not decided

    if log_ch[log_ch_id][0][0:2] == 'A0':
        if len(log_ch[log_ch_id]) < 3:
            log_ch[log_ch_id].append(log_ch[log_ch_id][0])

    abnormal_msg = ''
    if log_ch[log_ch_id][1]:
        if log_ch[log_ch_id][0]:
            if log_ch[log_ch_id][0] in file_system.DF_name:
                if log_ch[log_ch_id][1] in file_system.EF_name[log_ch[log_ch_id][0]]:
                    file_name = file_system.EF_name[log_ch[log_ch_id][0]][log_ch[log_ch_id][1]]
                else:
                    file_name = file_id
                    abnormal_msg = '(1) Non-standard'
            else:
                file_name = file_id
                abnormal_msg = '(1) Non-standard'
        else:
            file_name = file_id #'7FFFXXXX'
            abnormal_msg = '(2) Last selected AID not decided'
    else:
        if log_ch[log_ch_id][0]:
            if log_ch[log_ch_id][0] in file_system.DF_name:
                file_name = file_system.DF_name[log_ch[log_ch_id][0]]
            else:
                file_name = file_id
                abnormal_msg = '(1) Non-standard'
        else:
            file_name = file_id #'7FFF'
            abnormal_msg = '(2) Last selected AID not decided'

    if debug_mode == 1:
        print('prot_data    :', data[0][0:2], data[2])
        print('log_ch       :', log_ch)
        print('DF_file_id   :', log_ch[log_ch_id][0])
        print('EF_file_id   :', log_ch[log_ch_id][1])
        print('file_name    :', file_name)

    if data[-1][-4:] != '9000' and data[-1][-4:-2] != '91':
        log_ch[log_ch_id][0] = log_ch_prev_0
        log_ch[log_ch_id][1] = log_ch_prev_1
        abnormal_msg = '(SW:' + data[-1][-4:] + ') ' + abnormal_msg

    if debug_mode == 1:
        print('abnormal_msg :', abnormal_msg)
        print()

    file_name = '[' + file_name + ']'

    return log_ch, file_name, abnormal_msg
