import sys
import time

#open() opens file into f1/f2
#.read(numCharacters)

# tick = res * 4 * step
    # 16 step = 48t
    # 24 step = 32t
    # 32 = 24t
    # 48 = 16t
    # 64 = 12t
    # 96 = 8t
    # ...
# tick_to_ms = tick * res / bpm * 60000
# tick_to_s = tick * res / bpm * 600 
#    60000 = milliseconds in a minute

NOTE_HASH = ['G', '-R', '--Y', '---B', '-----O', '*F*', '*T*', '*****']
CHORD_HASH = \
    [ \
    'GR---', 'G-Y--', 'G--B-', 'G---O', '-RY--', '-R-B-', '-R--O', '--YB-', '--Y-O', '---BO', \
    'GRY--', 'GR-B-', 'GR--O', 'G-YB-', 'G-Y-O', 'G--BO', '-RYB-', '-RY-O', '-R-BO', '--YBO', \
    'GRYB-', 'GRY-O', 'GR-BO', 'G-YBO', '-RYBO', \
    'GRYBO' \
    ]
# ---------------  
# NOTES KEY 
        # -------------
        # N [0-4] [DUR] : GRYBO
        # N [2-3][0-A] : 2 NOTE, 3 NOTE CHORDS
        # N 4[0-4] : 4 NOTE CHORDS
        # N 50 0 : 5 NOTE CHORD

# func parse_notes:
#     pararms: Chart file (.chart)
#     return:   - resolution of chart, 
#               - list(s) of bpms, ticks, notes
def parse_notes(chart_file):
    res = 192 # Default res
    bpm = 120.0 # Default BPM
    curr_timestamp = 0 
    tick_diff = 0 # Default to no time passage if error
    
    list_of_bpms = [] # List of any BPM changes, including initial ; ticks at even indicies, bpms are odd indices
    list_of_notes = [] # List of charted notes to append
    list_of_ticks = [] # List of charted notes' ticks (1:1 with list_of_notes)
    timestamps = [] # List of timestamps - number of seconds between notes

    with open(chart_file, "r") as chart: 
        
        isNotes = False
        
        line = chart.readline().strip()
        lineNumber = 1
        while line:
            #- Obtain resolution -#
            if 'Resolution' in line: 
                indexOfEquals = line.find('=')
                res = int(line[indexOfEquals+2:])
                print('Res = ', res)
            
            #- Obtain BPM -#
            elif ' = B ' in line:
                # print('BPM line: ', line)
                index_of_BPM_value = line.find('B')
                tick = int(line[:index_of_BPM_value-3])
                list_of_bpms.append(tick)
                bpm = int(line[index_of_BPM_value+2:]) / 1000
                list_of_bpms.append(bpm)
                print('BPMs = ', list_of_bpms)
            
            #- Read Notes -#
            elif '[ExpertSingle]' in line:
                # print('Line before: ', line)
                line = chart.readline().strip() #read to next line
                isNotes = True
            
            # TODO: add chord logic (v2)
            elif isNotes:
                chord_num = 0
                if line == '}':
                    break
                indexOfEquals = line.find('=')
                current_note = line[indexOfEquals+2:]
                current_tick = line[:indexOfEquals-1]
                list_of_notes.append(current_note)
                list_of_ticks.append(int(current_tick))
                # append to timestamps list
                length_of_tick_list = len(list_of_ticks)
                if length_of_tick_list < 2:
                   tick_diff = int(current_tick) - int(list_of_ticks[0])
                else:
                    tick_diff = int(current_tick) - int(list_of_ticks[-2])
                    curr_timestamp = (int(tick_diff) * res)/ (list_of_bpms[-1] * 600)
                    timestamps.append(curr_timestamp)
            
            line = chart.readline().strip()
            lineNumber = lineNumber + 1
    chart.close()

    with open("all_notes.txt", "w") as txt: 
        for n in list_of_notes:
            txt.write(n)
            txt.write('\n')
    txt.close()
    with open("all_ticks.txt", "w") as txt: 
        for t in list_of_ticks:
            txt.write(str(t))
            txt.write('\n')
    txt.close()
    with open("timestamps.txt", "w") as txt: 
        for t in timestamps:
            txt.write(str(t))
            txt.write('\n')
    txt.close()

    return res, list_of_bpms, list_of_ticks, list_of_notes, timestamps

# Timemap logic

res, bpms, ticks, notes, tstamps = parse_notes('charts/effingchords2.chart') # INSERT CHART HERE
for (timestamp, note) in zip(tstamps, notes):
    note_num = note[2]
    # sus_value = note[4:-1]
    time.sleep(timestamp)
            # - Do something -#
    print(NOTE_HASH[int(note_num)]) 