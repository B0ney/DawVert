# SPDX-FileCopyrightText: 2023 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from functions import placements
from functions import placement_data
from functions import idvals
from functions import tracks
import plugin_input
import json

ceol_colors = {}
ceol_colors[0] = [0.23, 0.15, 0.93]
ceol_colors[1] = [0.61, 0.04, 0.94]
ceol_colors[2] = [0.82, 0.16, 0.23]
ceol_colors[3] = [0.82, 0.60, 0.16]
ceol_colors[4] = [0.21, 0.84, 0.14]
ceol_colors[5] = [0.07, 0.56, 0.91]

datapos = 0

globalfxname = ['delay','chorus','reverb','distortion','low_boost','compresser','high_pass']

def ceol_read():
    global datapos
    global ceol_data
    output = int(ceol_data[datapos])
    datapos += 1
    return output

def make_fxslot(fx_type, fx_data):
    fxslotdata = {}
    fxslotdata['plugin'] = 'native-boscaceoil'
    fxslotdata['plugindata'] = {}
    fxslotdata['plugindata']['name'] = fx_type
    fxslotdata['plugindata']['data'] = fx_data
    return fxslotdata

class input_ceol(plugin_input.base):
    def __init__(self): pass
    def is_dawvert_plugin(self): return 'input'
    def getshortname(self): return 'ceol'
    def getname(self): return 'Bosca Ceoil'
    def gettype(self): return 'mi'
    def getdawcapabilities(self): 
        return {
        'track_lanes': True
        }
    def supported_autodetect(self): return False
    def parse(self, input_file, extra_param):
        global datapos
        global ceol_data
        
        cvpj_l = {}

        cvpj_l_keynames_data = {}

        idvals_inst_midi = idvals.parse_idvalscsv('data_idvals/midi_inst.csv')
        idvals_inst_bosca = idvals.parse_idvalscsv('data_idvals/boscaceoil_inst.csv')
        idvals_drumkit_midi = idvals.parse_idvalscsv('data_idvals/boscaceoil_drumkit_midi.csv')
        idvals_drumkit_simple = idvals.parse_idvalscsv('data_idvals/boscaceoil_drumkit_simple.csv')
        idvals_drumkit_sion = idvals.parse_idvalscsv('data_idvals/boscaceoil_drumkit_sion.csv')

        cvpj_l_keynames_data['drumkit_midi'] = idvals.idval2drumkeynames(idvals_drumkit_midi)
        cvpj_l_keynames_data['drumkit_simple'] = idvals.idval2drumkeynames(idvals_drumkit_simple)
        cvpj_l_keynames_data['drumkit_sion'] = idvals.idval2drumkeynames(idvals_drumkit_sion)

        bio_mainfile = open(input_file, 'r')
        ceol_data = bio_mainfile.readline().split(',')

        ceol_basic_versionnum = ceol_read()
        print('[input-boscaceoil] Version Number: '+str(ceol_basic_versionnum))
        ceol_basic_swing = ceol_read()
        print('[input-boscaceoil] Swing: '+str(ceol_basic_swing))
        ceol_basic_effect = ceol_read()
        print('[input-boscaceoil] Effect: '+str(ceol_basic_effect))
        ceol_basic_effectvalue = ceol_read()
        print('[input-boscaceoil] Effect Value: '+str(ceol_basic_effectvalue))
        ceol_basic_bpm = ceol_read()
        print('[input-boscaceoil] BPM: '+str(ceol_basic_bpm))
        ceol_basic_patternlength = ceol_read()
        print('[input-boscaceoil] Pattern Length: '+str(ceol_basic_patternlength))
        ceol_basic_barlength = ceol_read()
        print('[input-boscaceoil] Bar Length: '+str(ceol_basic_barlength))

        tracks.a_addtrack_master(cvpj_l, 'Master', 1, [0.31373, 0.39608, 0.41569])
        tracks.add_fxslot(cvpj_l, ['master'], 'audio', make_fxslot(globalfxname[ceol_basic_effect], {'power': ceol_basic_effectvalue}))

        ceol_numinstrument = ceol_read()

        t_key_offset = []

        for instnum in range(ceol_numinstrument):
            cvpj_instid = 'ceol_'+str(instnum).zfill(2)
            print('[input-boscaceoil] Inst '+ str(instnum), end=', ')

            ceol_inst_number = ceol_read()
            ceol_inst_type = ceol_read()
            ceol_inst_palette = ceol_read()
            ceol_inst_cutoff = ceol_read()
            ceol_inst_resonance = ceol_read()
            ceol_inst_volume = ceol_read()

            print('Volume: '+str(ceol_inst_volume/256), end=', ')
            print('Type: '+str(ceol_inst_type), end=', ')
            print('Pal: '+str(ceol_inst_palette), end=', ')
            print('CutRes: '+str(ceol_inst_cutoff)+'/'+str(ceol_inst_resonance))

            initcutoffval = ceol_inst_cutoff
            calc_initcutoffval = pow(initcutoffval, 2)*(925/2048)

            cvpj_instvol = ceol_inst_volume/256

            if ceol_inst_palette in ceol_colors:  cvpj_instcolor = ceol_colors[ceol_inst_palette]
            else: cvpj_instcolor = [0.55, 0.55, 0.55]

            cvpj_instdata = {}

            if ceol_inst_number <= 127:
                cvpj_instname = idvals.get_idval(idvals_inst_midi, str(ceol_inst_number), 'name')
                cvpj_instdata = {'plugin': 'general-midi', 'plugindata': {'bank':0, 'inst':ceol_inst_number}}
            elif ceol_inst_number == 365: 
                cvpj_instname = 'MIDI Drums'
                cvpj_instdata = {'plugin': 'general-midi', 'plugindata': {'bank':128, 'inst':0}}
            else: 
                cvpj_instname = idvals.get_idval(idvals_inst_bosca, str(ceol_inst_number), 'name')
                cvpj_instdata = {'plugin': 'native-boscaceoil', 'plugindata': {'name':'instrument', 'instnum': ceol_inst_number}}

            cvpj_plugindata = cvpj_instdata['plugindata']
            cvpj_plugindata['filter'] = {}
            cvpj_plugindata['filter']['cutoff'] = calc_initcutoffval
            cvpj_plugindata['filter']['reso'] = ceol_inst_resonance
            cvpj_plugindata['filter']['type'] = "lowpass"

            if ceol_inst_number == 363: t_key_offset.append(60)
            if ceol_inst_number == 364: t_key_offset.append(48)
            if ceol_inst_number == 365: t_key_offset.append(24)
            else: t_key_offset.append(0)

            tracks.m_create_inst(cvpj_l, cvpj_instid, cvpj_instdata)
            tracks.m_basicdata_inst(cvpj_l, cvpj_instid, cvpj_instname, cvpj_instcolor, cvpj_instvol, 0.0)

        ceol_numpattern = ceol_read()
        for patnum in range(ceol_numpattern):
            print('[input-boscaceoil] Pattern ' + str(patnum), end=', ')

            cvpj_notelist = []

            t_notepos_table = {}
            for t_notepos in range(ceol_basic_patternlength):
                t_notepos_table[t_notepos] = []

            cvpj_pat_id = 'ceol_'+str(patnum).zfill(3)
            ceol_pat_key = ceol_read()
            ceol_pat_scale = ceol_read()
            ceol_pat_instrument = ceol_read()
            print('Inst:'+str(ceol_pat_instrument), end=', ')
            ceol_pat_palette = ceol_read()
            print('Pal:'+str(ceol_pat_palette), end=', ')
            ceol_numnotes = ceol_read()
            print('#Notes:'+str(ceol_numnotes))

            print_notes = 0
            for _ in range(ceol_numnotes):
                ceol_nl_key = ceol_read()-60 + t_key_offset[ceol_pat_instrument]
                ceol_nl_len = ceol_read()
                ceol_nl_pos = ceol_read()
                ceol_read()
                t_notepos_table[ceol_nl_pos].append({'key': ceol_nl_key, 'instrument': 'ceol_'+str(ceol_pat_instrument).zfill(2), 'duration': ceol_nl_len})
                print_notes += 1

            ceol_recordfilter = ceol_read()
            if ceol_recordfilter == 1:
                for _ in range(32):
                    ceol_read()
                    ceol_read()
                    ceol_read()

            for position in t_notepos_table:
                for note in t_notepos_table[position]:
                    cvpj_notelist.append(note | {'position': position})

            patcolor = {}
            if ceol_pat_palette in ceol_colors: patcolor = ceol_colors[ceol_pat_palette]
            else: patcolor = [0.55, 0.55, 0.55]

            tracks.m_add_nle(cvpj_l, cvpj_pat_id, cvpj_notelist)
            tracks.m_add_nle_info(cvpj_l, cvpj_pat_id, str(patnum), patcolor)

        tracks.m_playlist_pl(cvpj_l, 1, None, [0.43, 0.52, 0.55], None)
        tracks.m_playlist_pl(cvpj_l, 2, None, [0.31, 0.40, 0.42], None)
        tracks.m_playlist_pl(cvpj_l, 3, None, [0.43, 0.52, 0.55], None)
        tracks.m_playlist_pl(cvpj_l, 4, None, [0.31, 0.40, 0.42], None)
        tracks.m_playlist_pl(cvpj_l, 5, None, [0.43, 0.52, 0.55], None)
        tracks.m_playlist_pl(cvpj_l, 6, None, [0.31, 0.40, 0.42], None)
        tracks.m_playlist_pl(cvpj_l, 7, None, [0.43, 0.52, 0.55], None)
        tracks.m_playlist_pl(cvpj_l, 8, None, [0.31, 0.40, 0.42], None)

        ceol_arr_length = ceol_read()
        ceol_arr_loopstart = ceol_read()
        ceol_arr_loopend = ceol_read()

        for plpos in range(ceol_arr_length):
            for plnum in range(8):
                plpatnum = ceol_read()
                if plpatnum != -1:
                    cvpj_l_placement = placement_data.makepl_n_mi(plpos*ceol_basic_patternlength, ceol_basic_patternlength, 'ceol_'+str(plpatnum).zfill(3))
                    tracks.m_playlist_pl_add(cvpj_l, plnum+1, cvpj_l_placement)

        timesig = placements.get_timesig(ceol_basic_patternlength, ceol_basic_barlength)

        cvpj_l['do_addloop'] = True
        
        cvpj_l['use_instrack'] = False
        cvpj_l['use_fxrack'] = False
        
        cvpj_l['keynames_data'] = cvpj_l_keynames_data
        cvpj_l['bpm'] = ceol_basic_bpm
        return json.dumps(cvpj_l)