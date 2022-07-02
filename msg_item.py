def process(msg):
    msg_start, msg_end, msg_SN, msg_port, msg_type = [],[],[],[],[]
    for n in range(len(msg)):
        if '0x19B7' in msg[n]:
            msg_start.append(n)
            msg_end.append(n-1)
        if 'Sequence Number' in msg[n]:
            msg_SN.append(int(msg[n].split('= ')[1]))
        if 'Slot Id' in msg[n]:
            msg_port.append(int(msg[n].split('= SLOT_')[1]))
        if 'Message Type' in msg[n]:
            msg_type.append(msg[n].split('= ')[1])
    if msg_end:
        msg_end.remove(msg_start[0]-1)
        msg_end.append(len(msg)-1)

    msg_data = []
    for m in range(len(msg_start)):
        msg_data.append('')
        for n in range(msg_start[m], msg_end[m]+1):
            if 'Data' in msg[n] or 'DATA' in msg[n]:
                if '{' in msg[n]:
                    if msg[n].split('{ ')[1]:
                        msg_data[-1] = msg[n].split('{ ')[1].replace('  }', '').replace(' ','')
                    else:
                        msg_data_item = ''
                        for a in range(n+1, msg_end[m]+1):
                            msg_data_item += msg[a].replace(' ', '')
                            if '}' in msg[a]:
                                msg_data[-1] = msg_data_item.replace('}','').replace(' ','')
                                break
                else:
                    msg_data[-1] = msg[n].split('= ')[1].replace('\x00','').replace(' ', '')
                break
    return msg_start, msg_end, msg_SN, msg_port, msg_type, msg_data

def process2(msg_all):
    msg_start, msg_end, msg_SN, msg_port, msg_type, msg_data = [], [], [], [], [], []

    if '19B7' not in msg_all[0]:
        return [], [], [], [], [], []

    cnt = 0
    CONTINUED = 0
    for n in range(len(msg_all)):
        if msg_all[n] == '': break
        cnt += 1
        if CONTINUED == 0:
            msg_start.append(n)
            msg_end.append(n)
            msg_SN.append(cnt)
            msg_port.append(int(msg_all[n].split("SLOT_")[1].split(" ")[0]))

            type = msg_all[n].split("Type =")[1]
            if type == '':
                msg_type.append("RESET")
                msg_data.append('')
            elif "DATA" in type:
                msg_type.append(type.split(" DATA")[0][1:].replace(' ', '_'))
                msg_data.append(type.split("=")[1].replace(' ', ''))
                if '{' in msg_data[-1]: msg_data[-1] = msg_data[-1].replace('{', '').replace('}', '')
            elif "Data" in type:
                msg_type.append(type.split(" Data")[0][1:])
                msg_data.append(type.split("=")[1].replace(' ', ''))
                if '{' in msg_data[-1]:
                    msg_data[-1] = msg_data[-1].split('{')[1]
                    if msg_data[-1] == '':
                        CONTINUED = 1
                    else:
                        msg_data[-1] = msg_data[-1].replace('}', '')
        else:
            if msg_all[n] != '}':
                msg_data[-1] += msg_all[n].replace(' ','')
            else:
                CONTINUED = 0

        # print(msg_SN[-1], msg_port[-1], msg_type[-1], msg_data[-1])
    return msg_start, msg_end, msg_SN, msg_port, msg_type, msg_data


