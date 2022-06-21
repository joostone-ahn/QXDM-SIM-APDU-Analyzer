



# def process(start, end, msg_all):
#     File_name = ''
#     File_id = ''
#     for m in range(start,end):
#         if 'File ID:' in msg_all[m]:
#             if '/' in msg_all[m]:
#                 File_name = msg_all[m].split('/')[-1].replace(' ', '')
#                 if '0x' in File_name:
#                     File_id = '0x' + msg_all[m].split('0x')[-1].replace(')', '').replace(' ', '')
#                     if '(' in File_name:
#                         File_name = File_name.split('(')[0]
#                     else:
#                         File_name = '???'  # No file name
#                 else:
#                     File_name += ' ADF'
#             else:  # MF (0x3F00)
#                 File_name = msg_all[m].split(': ')[1].split(' (')[0]
#                 File_id = msg_all[m].split('(')[1].replace(')', '').replace(' ', '')
#             if 'Unknown App' in msg_all[m]:
#                 File_name = '???? ADF'
#         if 'AID:' in msg_all[m]: # 'File ID:'+1줄 AID 있음
#             if '0x' in msg_all[m]:
#                 File_id = '0x' + msg_all[m].split('{ ')[1].replace('0x', '').replace(' ', '')
#                 if 'Status' not in msg_all[m+1]: # AID 한 줄
#                     File_id += msg_all[m + 1].replace('0x', '').replace(' ', '')
#         if 'AID ' in msg_all[m]: # 'File ID:'+1줄 AID 없음
#             if File_name != '???? ADF':
#                 File_id = '0x' + msg_all[m + 1].split(':')[1].replace(' ', '')
#     return File_name, File_id
#
# def rst(msg_sum, Time, Command, File_name, File_id, SW_code):
#     if len(File_id) > 6:
#         msg_sum.append(Time + '  ' + Command + ' (' + File_name + ', ' + File_id + ')')
#     else:
#         msg_sum.append(Time + '  ' + Command + ' (' + File_id + ', ' + File_name + ')')
#     if SW_code == '6A82':
#         msg_sum[-1] += ' *Not found'
#     return msg_sum