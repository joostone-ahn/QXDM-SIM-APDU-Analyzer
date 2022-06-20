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


