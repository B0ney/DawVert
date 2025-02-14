# SPDX-FileCopyrightText: 2023 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

import plugin_input
import json
from mido import MidiFile
from functions import format_midi_in
from functions import midi_exdata
from functions import colors
from functions import song

def setinfo(cvpj_l, textin):
    global author
    global titlefound
    # ------------------------ copyright + year ------------------------
    copyrightdatefound = False
    if '(c)' in textin:
        copyrightpart = textin.split('(c)', 1)
        copyrightdatefound = True
    elif '(C)' in textin:
        copyrightpart = textin.split('(C)', 1)
        copyrightdatefound = True
    elif '©' in textin:
        copyrightpart = textin.split('©', 1)
        copyrightdatefound = True
    elif 'copyright' in textin:
        copyrightpart = textin.split('copyright', 1)
        copyrightdatefound = True
    elif 'Copyright' in textin:
        copyrightpart = textin.split('Copyright', 1)
        copyrightdatefound = True
    elif 'Copyright (c)' in textin:
        copyrightpart = textin.split('Copyright (c)', 1)
        copyrightdatefound = True

    if 'Composed by' in textin:
        authorpart = textin.split('Composed by', 1)
        if len(authorpart) != 1: author = authorpart[1]
    if 'by ' in textin:
        authorpart = textin.split('by ', 1)
        if len(authorpart) != 1: author = authorpart[1]
    if 'By ' in textin:
        authorpart = textin.split('By ', 1)
        if len(authorpart) != 1: author = authorpart[1]

    if copyrightdatefound == True:
        copyrightmsg_len = len(copyrightpart)
        if copyrightmsg_len >= 2:
            copyrightisyear = copyrightpart[1].lstrip().split(' ', 1)
            if copyrightisyear[0].isnumeric() == True:
                song.add_info(cvpj_l, 'year', int(copyrightisyear[0]))
                if len(copyrightisyear) == 2: song.add_info(cvpj_l, 'author', copyrightisyear[1])
            else:
                song.add_info(cvpj_l, 'author', copyrightisyear[0])

    # ------------------------ URL ------------------------
    if 'http://' in textin:
        urlparts = textin.split('"')
        for urlpart in urlparts:
            if 'http://' in urlpart: song.add_info(cvpj_l, 'url', urlpart)

    # ------------------------ title ------------------------
    if textin.count('"') == 2 and titlefound == False:
        titlefound = True
        song.add_info(cvpj_l, 'title', textin.split('"')[1::2][0])

    # ------------------------ email ------------------------
    if '.' in textin and '@' in textin:
        emailparts = textin.split('"')
        for emailpart in emailparts:
            if '.' in emailpart and '@' in emailpart: song.add_info(cvpj_l, 'email', emailpart)

class input_midi(plugin_input.base):
    def __init__(self): pass
    def is_dawvert_plugin(self): return 'input'
    def getshortname(self): return 'midi'
    def getname(self): return 'MIDI'
    def gettype(self): return 'm'
    def getdawcapabilities(self): 
        return {'fxrack': True,'track_lanes': True,'auto_nopl': True,'track_nopl': True}
    def supported_autodetect(self): return True
    def detect(self, input_file):
        bytestream = open(input_file, 'rb')
        bytestream.seek(0)
        bytesdata = bytestream.read(4)
        if bytesdata == b'MThd': return True
        else: return False
    def parse(self, input_file, extra_param):
        global author
        global titlefound

        midifile = MidiFile(input_file, clip=True)
        ppq = midifile.ticks_per_beat
        print("[input-midi] PPQ: " + str(ppq))

        num_tracks = len(midifile.tracks)
        songdescline = []
        midi_copyright = None

        format_midi_in.song_start(16, ppq)

        s_tempo = 120
        s_timesig = [4,4]

        t_tracknames = []

        for track in midifile.tracks:
            format_midi_in.track_start(16, 0)
            midi_trackname = None

            timepos = 0

            for msg in track:
                timepos += msg.time
                format_midi_in.resttime(msg.time)


                if msg.type == 'note_on':
                    if msg.velocity != 0: format_midi_in.note_on(msg.note, msg.channel, msg.velocity)
                    else: format_midi_in.note_off(msg.note, msg.channel)
                if msg.type == 'note_off': format_midi_in.note_off(msg.note, msg.channel)

                if msg.type == 'pitchwheel': format_midi_in.pitchwheel(msg.channel, (msg.pitch/8192)*24)
                if msg.type == 'program_change': format_midi_in.program_change(msg.channel, msg.program)
                if msg.type == 'control_change': format_midi_in.control_change(msg.channel, msg.control, msg.value)
                if msg.type == 'set_tempo': 
                    if timepos == 0: s_tempo = 60000000/msg.tempo
                    format_midi_in.tempo(timepos, 60000000/msg.tempo)

                if msg.type == 'time_signature': 
                    if timepos == 0: s_timesig = [msg.numerator, msg.denominator]
                    format_midi_in.time_signature(timepos, msg.numerator, msg.denominator)

                if msg.type == 'marker': format_midi_in.marker(timepos, msg.text)

                if msg.type == 'track_name': 
                    print("[input-midi] Track Name:", msg.name)
                    format_midi_in.track_name(msg.name)
                    midi_trackname = msg.name

                if msg.type == 'sequencer_specific': 
                    exdata = midi_exdata.decode_exdata(msg.data, True)
                    if exdata[0] == [83]:
                        if exdata[1][0:5] == b'ign\x01\xff':
                            print("[input-midi] Track Color (from Signal)")
                            format_midi_in.track_color(colors.rgb_int_to_rgb_float(exdata[1][5:8]))

                if msg.type == 'copyright': 
                    midi_copyright = msg.text
            format_midi_in.track_end(16)

            usedinsts = format_midi_in.getusedinsts(16)

            for usedinst in usedinsts:
                format_midi_in.make_inst(usedinst[0], usedinst[1], usedinst[2])

            if midi_trackname != None:
                if format_midi_in.get_hasnotes() == False: songdescline.append(midi_trackname)
                t_tracknames.append(midi_trackname)

        song_message = ""

        cvpj_l = format_midi_in.song_end(16)

        cvpj_l['do_addloop'] = True
        cvpj_l['do_singlenotelistcut'] = True
        
        cvpj_l['timesig_numerator'] = s_timesig[0]
        cvpj_l['timesig_denominator'] = s_timesig[1]
        cvpj_l['bpm'] = s_tempo

        author = None
        titlefound = False

        if midi_copyright != None:
            song.add_info(cvpj_l, 'author', midi_copyright)
            setinfo(cvpj_l, midi_copyright)

        for t_trackname in t_tracknames:
            setinfo(cvpj_l, t_trackname)

        for songdesc in songdescline:
            song_message = song_message+songdesc+'\n'

        if num_tracks != 1: song.add_info_msg(cvpj_l, 'text', song_message)
        elif midi_trackname != None: song.add_info(cvpj_l, 'title', midi_trackname)

        return json.dumps(cvpj_l)
