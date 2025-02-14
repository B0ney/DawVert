# SPDX-FileCopyrightText: 2023 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

import xml.etree.ElementTree as ET

# -------------------- magical8bitplug --------------------
def shape_m8bp(pluginname, plugindata):
	m8p_root = ET.Element("root")
	m8p_params = ET.SubElement(m8p_root, "Params")
	m8bp_addvalue(m8p_params, "arpeggioDirection", 0.0)
	m8bp_addvalue(m8p_params, "arpeggioTime", 0.02999999932944775)
	m8bp_addvalue(m8p_params, "attack", 0.0)
	m8bp_addvalue(m8p_params, "bendRange", 12.0)
	m8bp_addvalue(m8p_params, "colorScheme", 1.0)
	m8bp_addvalue(m8p_params, "decay", 0.0)
	m8bp_addvalue(m8p_params, "duty", 0.0)
	m8bp_addvalue(m8p_params, "gain", 0.5)
	m8bp_addvalue(m8p_params, "isAdvancedPanelOpen_raw", 1.0)
	m8bp_addvalue(m8p_params, "isArpeggioEnabled_raw", 0.0)
	m8bp_addvalue(m8p_params, "isDutySequenceEnabled_raw", 0.0)
	m8bp_addvalue(m8p_params, "isVolumeSequenceEnabled_raw", 0.0)
	m8bp_addvalue(m8p_params, "maxPoly", 8.0)
	m8bp_addvalue(m8p_params, "noiseAlgorithm_raw", 0.0)
	if pluginname == 'shape-square':
		m8bp_addvalue(m8p_params, "osc", 0.0)
		m8bp_addvalue(m8p_params, "duty", 2.0)
	elif pluginname == 'shape-pulse':
		m8bp_addvalue(m8p_params, "osc", 0.0)
		if 'duty' in plugindata:
			if plugindata['duty'] == 0.25: m8bp_addvalue(m8p_params, "duty", 1.0)
			elif plugindata['duty'] == 0.125: m8bp_addvalue(m8p_params, "duty", 0.0)
			else: m8bp_addvalue(m8p_params, "duty", 0.0)
		else: m8bp_addvalue(m8p_params, "duty", 1.0)
	elif pluginname == 'shape-triangle':
		m8bp_addvalue(m8p_params, "osc", 1.0)
		m8bp_addvalue(m8p_params, "duty", 0.0)
	elif pluginname == 'retro-noise':
		m8bp_addvalue(m8p_params, "osc", 2.0)
		if 'type' in plugindata:
			if plugindata['type'] == '4bit': m8bp_addvalue(m8p_params, "duty", 0.0)
			elif plugindata['type'] == '1bit_long': m8bp_addvalue(m8p_params, "duty", 1.0)
			elif plugindata['type'] == '1bit_short': m8bp_addvalue(m8p_params, "duty", 2.0)
			else: m8bp_addvalue(m8p_params, "duty", 0.0)
		else: m8bp_addvalue(m8p_params, "duty", 0.0)
	else: m8bp_addvalue(m8p_params, "osc", 0.0)
	m8bp_addvalue(m8p_params, "pitchSequenceMode_raw", 0.0)
	m8bp_addvalue(m8p_params, "release", 0.0)
	m8bp_addvalue(m8p_params, "restrictsToNESFrequency_raw", 0.0)
	m8bp_addvalue(m8p_params, "suslevel", 1.0)
	m8bp_addvalue(m8p_params, "sweepInitialPitch", 0.0)
	m8bp_addvalue(m8p_params, "sweepTime", 0.1000000014901161)
	m8bp_addvalue(m8p_params, "vibratoDelay", 0.2999999821186066)
	m8bp_addvalue(m8p_params, "vibratoDepth", 0.0)
	m8bp_addvalue(m8p_params, "vibratoIgnoresWheel_raw", 1.0)
	m8bp_addvalue(m8p_params, "vibratoRate", 0.1500000059604645)
	return m8p_root

def m8bp_init():
	global m8bp_params
	global m8bp_params_env

	m8bp_params_env = {}
	m8bp_params_env["duty"] = None
	m8bp_params_env["pitch"] = None
	m8bp_params_env["volume"] = None

	m8bp_params = {}
	m8bp_params["arpeggioDirection"] = 0.0
	m8bp_params["arpeggioTime"] = 0.02999999932944775
	m8bp_params["attack"] = 0.0
	m8bp_params["bendRange"] = 12.0
	m8bp_params["colorScheme"] = 1.0
	m8bp_params["decay"] = 0.0
	m8bp_params["duty"] = 0.0
	m8bp_params["gain"] = 0.5
	m8bp_params["isAdvancedPanelOpen_raw"] = 1.0
	m8bp_params["isArpeggioEnabled_raw"] = 0.0
	m8bp_params["isPitchSequenceEnabled_raw"] = 0.0
	m8bp_params["isDutySequenceEnabled_raw"] = 0.0
	m8bp_params["isVolumeSequenceEnabled_raw"] = 0.0
	m8bp_params["maxPoly"] = 8.0
	m8bp_params["noiseAlgorithm_raw"] = 0.0
	m8bp_params["osc"] = 0.0
	m8bp_params["duty"] = 2.0
	m8bp_params["pitchSequenceMode_raw"] = 0.0
	m8bp_params["release"] = 0.0
	m8bp_params["restrictsToNESFrequency_raw"] = 0.0
	m8bp_params["suslevel"] = 1.0
	m8bp_params["sweepInitialPitch"] = 0.0
	m8bp_params["sweepTime"] = 0.1000000014901161
	m8bp_params["vibratoDelay"] = 0.2999999821186066
	m8bp_params["vibratoDepth"] = 0.0
	m8bp_params["vibratoIgnoresWheel_raw"] = 1.0
	m8bp_params["vibratoRate"] = 0.1500000059604645

def m8bp_setvalue(name, value):
	global m8bp_params
	m8bp_params[name] = value

def m8bp_setenv(name, value):
	global m8bp_params_env
	m8bp_params_env[name] = value

def m8bp_addvalue(xmltag, name, value):
	temp_xml = ET.SubElement(xmltag, 'PARAM')
	temp_xml.set('id', str(name))
	temp_xml.set('value', str(value))

def m8bp_out():
	global m8bp_params
	global m8bp_params_env
	xml_m8p_root = ET.Element("root")
	xml_m8p_params = ET.SubElement(xml_m8p_root, "Params")
	for m8bp_param in m8bp_params:
		m8bp_addvalue(xml_m8p_params, m8bp_param, str(m8bp_params[m8bp_param]))

	m8p_dutyEnv = ET.SubElement(xml_m8p_root, "dutyEnv")
	m8p_pitchEnv = ET.SubElement(xml_m8p_root, "pitchEnv")
	m8p_volumeEnv = ET.SubElement(xml_m8p_root, "volumeEnv")

	if m8bp_params_env["duty"] != None: m8p_dutyEnv.text = ','.join(str(item) for item in m8bp_params_env["duty"])
	if m8bp_params_env["pitch"] != None: m8p_pitchEnv.text = ','.join(str(item) for item in m8bp_params_env["pitch"])
	if m8bp_params_env["volume"] != None: m8p_volumeEnv.text = ','.join(str(item) for item in m8bp_params_env["volume"])

	return xml_m8p_root

# -------------------- juicysfplugin --------------------
def juicysfplugin_create(bank, patch, filename):
	jsfp_xml = ET.Element("MYPLUGINSETTINGS")
	jsfp_params = ET.SubElement(jsfp_xml, "params")
	jsfp_uiState = ET.SubElement(jsfp_xml, "uiState")
	jsfp_soundFont = ET.SubElement(jsfp_xml, "soundFont")
	if 'bank' != None: jsfp_params.set('bank', str(bank/128))
	else: jsfp_params.set('bank', "0")
	if 'patch' != None: jsfp_params.set('preset', str(patch/128))
	else: jsfp_params.set('preset', "0")
	jsfp_params.set('attack', "0.0")
	jsfp_params.set('decay', "0.0")
	jsfp_params.set('sustain', "0.0")
	jsfp_params.set('release', "0.0")
	jsfp_params.set('filterCutOff', "0.0")
	jsfp_params.set('filterResonance', "0.0")
	jsfp_uiState.set('width', "500.0")
	jsfp_uiState.set('height', "300.0")
	if 'file' != None: jsfp_soundFont.set('path', filename)
	else: jsfp_soundFont.set('path', '')
	return jsfp_xml


# -------------------- opn2 > opnplug --------------------

def opnplug_addvalue(xmltag, name, value):
	temp_xml = ET.SubElement(xmltag, 'VALUE')
	temp_xml.set('name', str(name))
	temp_xml.set('val', str(value))

def opnplug_addbank(xmltag, num, name):
	bank_xml = ET.SubElement(xmltag, 'bank')
	opnplug_addvalue(bank_xml, 'bank', num)
	opnplug_addvalue(bank_xml, 'name', name)

def opnplug_op_params(xmltag, opnum, plugindata):
	opdata = plugindata["op"+str(opnum)]
	opnplug_addvalue(xmltag, "op"+str(opnum)+"detune" ,opdata["detune"])
	opnplug_addvalue(xmltag, "op"+str(opnum)+"fmul" ,opdata["freqmul"])
	opnplug_addvalue(xmltag, "op"+str(opnum)+"level" ,opdata["level"])
	opnplug_addvalue(xmltag, "op"+str(opnum)+"ratescale" ,opdata["ratescale"])
	opnplug_addvalue(xmltag, "op"+str(opnum)+"attack" ,opdata["env_attack"])
	opnplug_addvalue(xmltag, "op"+str(opnum)+"am" ,opdata["am"])
	opnplug_addvalue(xmltag, "op"+str(opnum)+"decay1" ,opdata["env_decay"])
	opnplug_addvalue(xmltag, "op"+str(opnum)+"decay2" ,opdata["env_decay2"])
	opnplug_addvalue(xmltag, "op"+str(opnum)+"sustain" ,opdata["env_sustain"])
	opnplug_addvalue(xmltag, "op"+str(opnum)+"release" ,opdata["env_release"])
	opnplug_addvalue(xmltag, "op"+str(opnum)+"ssgenable" ,opdata["ssg_enable"])
	opnplug_addvalue(xmltag, "op"+str(opnum)+"ssgwave" ,opdata["ssg_mode"])

def opnplug_convert(plugindata):
	opnplug_root = ET.Element("ADLMIDI-state")
	opnplug_addbank(opnplug_root, 1, 'DawVert')
	opnplug_params = ET.SubElement(opnplug_root, 'instrument')
	opnplug_addvalue(opnplug_params, "blank" ,0)
	opnplug_addvalue(opnplug_params, "note_offset" ,0)
	opnplug_addvalue(opnplug_params, "feedback" ,plugindata["feedback"])
	opnplug_addvalue(opnplug_params, "algorithm" ,plugindata["algorithm"])
	opnplug_addvalue(opnplug_params, "ams" ,plugindata["ams"])
	opnplug_addvalue(opnplug_params, "fms" ,plugindata["fms"])
	opnplug_addvalue(opnplug_params, "midi_velocity_offset" ,0)
	opnplug_addvalue(opnplug_params, "percussion_key_number" ,0)
	for opnum in range(4):
		opnplug_op_params(opnplug_params, opnum+1, plugindata)

	opnplug_addvalue(opnplug_params, "delay_off_ms" ,120)
	opnplug_addvalue(opnplug_params, "delay_on_ms" ,486)
	opnplug_addvalue(opnplug_params, "bank" ,0)
	opnplug_addvalue(opnplug_params, "program" ,0)
	opnplug_addvalue(opnplug_params, "name" ,'DawVert')

	opnplug_selection = ET.SubElement(opnplug_root, 'selection')
	opnplug_addvalue(opnplug_selection, "part" ,0)
	opnplug_addvalue(opnplug_selection, "bank" ,0)
	opnplug_addvalue(opnplug_selection, "program" ,0)

	opnplug_chip = ET.SubElement(opnplug_root, 'chip')
	opnplug_addvalue(opnplug_chip, "emulator" ,0)
	opnplug_addvalue(opnplug_chip, "chip_count" ,1)
	opnplug_addvalue(opnplug_chip, "chip_type" ,0)

	opnplug_global = ET.SubElement(opnplug_root, 'global')
	opnplug_addvalue(opnplug_global, "volume_model" ,0)
	opnplug_addvalue(opnplug_global, "lfo_enable" ,plugindata["lfo_enable"])
	opnplug_addvalue(opnplug_global, "lfo_frequency" ,plugindata["lfo_frequency"])

	opnplug_common = ET.SubElement(opnplug_root, 'common')
	opnplug_addvalue(opnplug_common, "bank_title" ,'DawVert')
	opnplug_addvalue(opnplug_common, "part" ,0)
	opnplug_addvalue(opnplug_common, "master_volume" ,12.0)

	return opnplug_root
