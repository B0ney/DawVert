# SPDX-FileCopyrightText: 2022 Colby Ray
# SPDX-License-Identifier: GPL-3.0-or-later

import json

def m2mi(song):
    global cvpj_proj
    cvpj_proj = json.loads(song)
    cvpj_playlist = cvpj_proj['playlist']
    cvpj_notelistindex = {}
    pattern_number = 1
    for cvpj_playlistentry in cvpj_playlist:
        cvpj_playlistentry_data = cvpj_playlist[cvpj_playlistentry]
        cvpj_placements = cvpj_playlistentry_data['placements']
        for cvpj_placement in cvpj_placements:
            if cvpj_placement['type'] == 'instruments':
                cvpj_notelist = cvpj_placement['notelist']
                cvpj_notelistindex['m2mi_' + str(pattern_number)] = {}
                cvpj_notelistindex['m2mi_' + str(pattern_number)]['notelist'] = cvpj_notelist.copy()
                cvpj_placement['fromindex'] = 'm2mi_' + str(pattern_number)
                del cvpj_placement['notelist']
                pattern_number += 1
    cvpj_proj['notelistindex'] = cvpj_notelistindex
    return json.dumps(cvpj_proj)

def r2m(song):
    cvpj_proj = json.loads(song)
    if 'trackordering' not in cvpj_proj:
        print('[error] trackordering not found')

    t_s_trackordering = cvpj_proj['trackordering']
    t_s_trackdata = cvpj_proj['trackdata']
    del cvpj_proj['trackdata']
    del cvpj_proj['trackordering']

    cvpj_proj['instruments'] = {}
    cvpj_proj['instrumentsorder'] = []
    cvpj_proj['playlist'] = {}

    temp_num_playlist = 1
    for trackid in t_s_trackordering:
        if trackid in t_s_trackdata:
            singletrack_data = t_s_trackdata[trackid]
            singletrack_placements = singletrack_data['placements']
            del singletrack_data['placements']

            if singletrack_data['type'] == 'instrument':
                cvpj_proj['instrumentsorder'].append(trackid)
                cvpj_proj['playlist'][str(temp_num_playlist)] = {}
                playlistrow = cvpj_proj['playlist'][str(temp_num_playlist)]
                if 'name' in singletrack_data: playlistrow['name'] = singletrack_data['name']
                if 'color' in singletrack_data: playlistrow['color'] = singletrack_data['color']
                for singletrack_placement in singletrack_placements:
                    singletrack_placement['type'] = 'instruments'
                    if 'notelist' in singletrack_placement:
                        for t_note in singletrack_placement['notelist']:
                            t_note['instrument'] = trackid

                playlistrow['placements'] = singletrack_placements

                cvpj_proj['instruments'][trackid] = singletrack_data
            temp_num_playlist += 1
    return json.dumps(cvpj_proj)