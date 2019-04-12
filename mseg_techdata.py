#!/usr/bin/env python3

import re
import numpy
import json
import mseg
import copy
import argparse


class EIAData(object):
    """Class of variables naming the EIA data files to be imported.

    Attributes:
        r_nlt_costperf (str): Filename of AEO residential non-lighting
            equipment cost and performance data.
        r_nlt_life (str): Filename of AEO residential non-lighting
            equipment lifetime data.
        r_lt_all (str): Filename for AEO residential lighting
            technology cost, performance, and lifetime data.
    """

    def __init__(self):
        self.r_nlt_costperf = "rsmeqp.txt"
        self.r_nlt_life = "rsclass.txt"
        self.r_lt_all = "rsmlgt.txt"


class UsefulVars(object):
    """Class of variables that would otherwise be global.

    Attributes:
        json_in (str): Filename for empty input JSON with the structure
            to be populated with AEO data.
        json_out (str): Filename for JSON with residential building data added.
        aeo_metadata (str): File name for the custom AEO metadata JSON.
    """

    def __init__(self):
        self.json_in = 'microsegments.json'
        self.json_out = 'cpl_res_cdiv.json'
        self.aeo_metadata = 'metadata.json'


# Pre-specify the numpy field names to be used in importing the EIA
# information on the cost performance, and lifetime of of non-lighting and
# lighting technologies in the residential sector

# Numpy field names for EIA "rsmeqp.txt" file with cost and performance
# information for non-lighting technologies
r_nlt_cp_names = ("ENDUSE", "EQUIP_CLASS", "EQUIP_TYP", "START_EQUIP_YR",
                  "END_EQUIP_YR", "CDIV", "HVAC_POINT", "HP_POINT", "MOD_EF",
                  "WH_LOAD", "BASE_EFF", "INST_COST", "RETAIL_COST",
                  "NA1", "NA2", "NA3", "NA4", "NA5", "NA6",
                  "TECH_MATURE", "COST_TREND",
                  "COST_SHAPE", "COST_PROP", "EFF_CHOICE_P1",
                  "EFF_CHOICE_P2", "EFF_CHOICE_P3", "EFF_CHOICE_MOD",
                  "NAME")

# Numpy field names for EIA "rsclass.txt" file with lifetime information
# for non-lighting technologies
r_nlt_l_names = ("ENDUSE", "EQUIP_CLASS", "EQUIP_POINT", "CLASS_POINT",
                 "REPLACE_CLASS", "FUEL", "FFAN_FLAG",
                 "BASE_EFF", "LIFE_PARAM", "LIFE_MIN", "LIFE_MAX",
                 "FCMOD_P1", "FCMOD_P2", "FCMOD_P3", "FCMOD_P4", "FCMOD_P5",
                 "FCOD_P6", "NAME")

# Numpy field names for EIA "rsmlgt.txt" file with cost, performance, and
# lifetime information for lighting technologies
r_lt_names = ("START_EQUIP_YR", "END_EQUIP_YR", "INST_COST",
              'EE_Sub1', 'EE_Sub2', 'EE_Sub3', 'EE_Sub4', 'EE_Sub5',
              'EE_Sub6', 'EE_Sub7', 'EE_Sub8', 'EE_Sub9',
              "SUB1", "SUB2", "SUB3", "SUB4", "SUB5", "SUB6", "SUB7", "SUB8",
              "SUB9", "BASE_EFF", "BASE_EFF_W", "LIFE_HRS", "CRI", "NAME",
              "BULB_TYPE", 'Beta_1', 'Beta_2')

# Initialize a dict with information needed for filtering EIA cost and
# performance information by the census division being run through in the input
# microsegments JSON (* Note: EIA non-lighting cost and performance information
# is broken down by census division; for lighting technologies, cost and
# performance information can be applied across all census divisions.
# Lifetime information is not broken down by census division)
mseg_cdiv_translate = {"new england": 1, "mid atlantic": 2,
                       "east north central": 3, "west north central": 4,
                       "south atlantic": 5, "east south central": 6,
                       "west south central": 7, "mountain": 8, "pacific": 9
                       }

# Initialize a dict with information needed for filtering EIA cost,
# performance, and lifetime info. by the end use being run through in the input
# microsegments JSON (* Note: EIA non-lighting technology lifetime information
# is broken down by end use)
mseg_enduse_translate = {"heating": 1, "cooling": 2, "clothes washing": 3,
                         "dishwasher": 4, "water heating": 5, "cooking": 6,
                         "drying": 7, "refrigeration": 8, "freezers": 9}

# Create dicts with either:
# a) The information needed to find the cost,
# performance, and lifetime of a given technology in the input microsegment
# JSON from the appropriate EIA .txt file, or
#
# b) Direct information about the
# cost, performance, and lifetime of a given technology in the input
# microsegment.

# The basic structure of a) above for non-lighting technologies is:
#  "microsegments.json" tech. key: [
#   EIA file info.,
#   lifetime filter name,
#  "typical" performance, cost, and tech. adoption parameters filter name,
#  "best" performance and cost filter name,
#   performance units (* Note: cost units are addressed separately)]
tech_eia_nonlt = {"ASHP": ["EIA_EQUIP", "ELEC_HP", "ELEC_HP1", "ELEC_HP4",
                           "COP"],
                  "GSHP": ["EIA_EQUIP", "GEO_HP", "GEO_HP1", "GEO_HP2", "COP"],
                  "NGHP": ["EIA_EQUIP", "NG_HP", "NG_HP", "NG_HP", "COP"],
                  "boiler (NG)": ["EIA_EQUIP", "NG_RAD", "NG_RAD1", "NG_RAD3",
                                  "AFUE"],
                  "boiler (distillate)": ["EIA_EQUIP", "DIST_RAD", "DISTRAD1",
                                          "DISTRAD3", "AFUE"],
                  "resistance heat": ["EIA_EQUIP", "ELEC_RAD", "ELEC_RAD",
                                      "ELEC_RAD", "AFUE"],
                  "furnace (distillate)": ["EIA_EQUIP", "DIST_FA", "DIST_FA1",
                                           "DIST_FA3", "AFUE"],
                  "furnace (kerosene)": ["EIA_EQUIP", "KERO_FA", "KERO_FA1",
                                         "KERO_FA3", "AFUE"],
                  "furnace (LPG)": ["EIA_EQUIP", "LPG_FA", "LPG_FA#1",
                                    "LPG_FA#5", "AFUE"],
                  "furnace (NG)": ["EIA_EQUIP", "NG_FA", "NG_FA#1", "NG_FA#5",
                                   "AFUE"],
                  "stove (wood)": ["EIA_EQUIP", "WOOD_HT", "WOOD_HT",
                                   "WOOD_HT", "COP"],
                  "solar WH": ["EIA_EQUIP", "SOLAR_WH", "SOLR_WH1",
                               "SOLR_WH1", "EF"],
                  "electric WH": ["EIA_EQUIP", "ELEC_WH", "ELEC_WH1",
                                  "ELEC_WH5", "EF"],
                  "central AC": ["EIA_EQUIP", "CENT_AIR", "CT_AIR#1",
                                 "CT_AIR#4", "COP"],
                  "room AC": ["EIA_EQUIP", "ROOM_AIR", "RM_AIR#1", "RM_AIR#3",
                              "COP"],
                  "clothes washing": ["EIA_EQUIP", "CL_WASH", "CW#1", "CW#3",
                                      "kWh/cycle"],
                  "dishwasher": ["EIA_EQUIP", "DS_WASH", "DW#1", "DW#3",
                                 "EF"],
                  "water heating": ["EIA_EQUIP",
                                    ["NG_WH", "LPG_WH"],
                                    ["NG_WH#1", "LPG_WH#1"],
                                    ["NG_WH#4", "LPG_WH#4"],
                                    ["EF", "EF"]],
                  "cooking": ["EIA_EQUIP",
                              ["ELEC_STV", "NG_STV", "LPG_STV"],
                              ["ELECSTV1", "NG_STV1", "LPG_STV1"],
                              ["ELECSTV2", "NG_STV2", "LPG_STV2"],
                              ["kWh/yr", "TEff", "TEff"]],
                  "drying": ["EIA_EQUIP",
                             ["ELEC_DRY", "NG_DRY"], ["ELECDRY1", "NG_DRY1"],
                             ["ELECDRY2", "NG_DRY2"], ["EF", "EF"]],
                  "refrigeration": ["EIA_EQUIP", "REFR",
                                    ["RefBF#1", "RefSF#1", "RefTF#1"],
                                    ["RefBF#2", "RefSF#2", "RefTF#2"],  # Check
                                    "kWh/yr"],
                  "freezers": ["EIA_EQUIP", "FREZ", ["FrzrC#1", "FrzrU#1"],
                               ["FrzrC#2", "FrzrU#2"], "kWh/yr"]}

# The basic structure of a) above for lighting technologies is:
#  "microsegments.json" tech. key: [
#   EIA file info.,
#   performance, cost, and lifetime filter name (light class and bulb type),
#   performance units (* Note: cost units are addressed separately)]
tech_eia_lt = {"linear fluorescent (T-12)": ["EIA_LT", ["LFL", "T12"],
                                             "lm/W"],
               "linear fluorescent (T-8)": ["EIA_LT", ["LFL", "T-8"], "lm/W"],
               "linear fluorescent (LED)": ["EIA_LT", ["LFL", "LED"], "lm/W"],
               "general service (incandescent)": ["EIA_LT", ["GSL", "INC"],
                                                  "lm/W"],
               "general service (CFL)": ["EIA_LT", ["GSL", "CFL"], "lm/W"],
               "general service (LED)": ["EIA_LT", ["GSL", "LED"], "lm/W"],
               "reflector (incandescent)": ["EIA_LT", ["REF", "INC"],
                                            "lm/W"],
               "reflector (CFL)": ["EIA_LT", ["REF", "LED"], "lm/W"],
               "reflector (halogen)": ["EIA_LT", ["REF", "HAL"], "lm/W"],
               "reflector (LED)": ["EIA_LT", ["REF", "LED"], "lm/W"],
               "external (incandescent)": ["EIA_LT", ["EXT", "INC"], "lm/W"],
               "external (CFL)": ["EIA_LT", ["EXT", "CFL"], "lm/W"],
               "external (high pressure sodium)": ["EIA_LT", ["EXT", "HPS"],
                                                   "lm/W"],
               "external (LED)": ["EIA_LT", ["EXT", "LED"], "lm/W"]}

# The basic structure of b) above is:
#  "microsegments.json" tech. key: [
#  average lifetime and range and info. source,
#  "typical" and "best" performance and info. sources,
#  "typical" and "best" cost and info. sources,
#   performance units]

# *** FOR NOW *** do not update any technologies in this routine for which
# there are no EIA cost, performance, and lifetime characteristics
tech_non_eia = {}

# tech_non_eia = {"secondary heating (electric)": [["NA", "NA", "NA"],
#                                                  ["NA", "NA", "NA"],
#                                                  ["NA", "NA", "NA"], "COP"],
#                 "secondary heating (natural gas)": [["NA", "NA", "NA"],
#                                                     ["NA", "NA", "NA"],
#                                                     ["NA", "NA", "NA"],
#                                                     "AFUE"],
#                 "secondary heating (kerosene)": [["NA", "NA", "NA"],
#                                                  ["NA", "NA", "NA"],
#                                                  ["NA", "NA", "NA"], "AFUE"],
#                 "secondary heating (wood)": [["NA", "NA", "NA"],
#                                              ["NA", "NA", "NA"],
#                                              ["NA", "NA", "NA"], "AFUE"],
#                 "secondary heating (LPG)": [["NA", "NA", "NA"],
#                                             ["NA", "NA", "NA"],
#                                             ["NA", "NA", "NA"], "AFUE"],
#                 "secondary heating (coal)": [["NA", "NA", "NA"],
#                                              ["NA", "NA", "NA"],
#                                              ["NA", "NA", "NA"], "AFUE"],
#                 "TV": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                        ["NA", "NA", "NA"], "W"],
#                 "set top box": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                                 ["NA", "NA", "NA"], "W"],
#                 "DVD": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                         ["NA", "NA", "NA"], "W"],
#                 "home theater & audio": [["NA", "NA", "NA"],
#                                          ["NA", "NA", "NA"],
#                                          ["NA", "NA", "NA"], "W"],
#                 "video game consoles": [["NA", "NA", "NA"],
#                                         ["NA", "NA", "NA"],
#                                         ["NA", "NA", "NA"], "W"],
#                 "desktop PC": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                                ["NA", "NA", "NA"], "W"],
#                 "laptop PC": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                               ["NA", "NA", "NA"], "W"],
#                 "monitors": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                              ["NA", "NA", "NA"], "W"],
#                 "network equipment": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                                       ["NA", "NA", "NA"], "W"],
#                 "fans & pumps": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                                  ["NA", "NA", "NA"], "HP/W"],
#                 "ceiling fan": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                                 ["NA", "NA", "NA"], "W"],
#                 "resistance": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                                ["NA", "NA", "NA"], "NA"],
#                 "other MELs": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                                ["NA", "NA", "NA"], "NA"],
#                 "windows conduction": [[30, 30, "Legacy P-Tool"],
#                                        [1.6, 1.6, "Legacy P-Tool"],
#                                        [12, 12, "RS Means"], "R Value"],
#                 "windows solar": [[30, 30, "Legacy P-Tool"],
#                                   [0.30, 0.30, "NREL Efficiency DB"],
#                                   [12, 12, "RS Means"], "SHGC"],
#                 "wall": [[30, 30, "Legacy P-Tool"],
#                          [11.1, 11.1, "Legacy P-Tool"],
#                          [1.48, 1.48, "Legacy P-Tool"], "R Value"],
#                 "roof": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                          ["NA", "NA", "NA"], "R Value"],
#                 "ground": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                            ["NA", "NA", "NA"], "R Value"],
#                 "infiltration": [[30, 30, "Legacy P-Tool"],
#                                  [13, 1, "Legacy P-Tool, NREL " +
#                                   "Residential Efficiency DB"],
#                                  [0, 0, "Legacy P-Tool"], "ACH"],
#                 "people gain": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                                 ["NA", "NA", "NA"], "NA"],
#                 "equipment gain": [["NA", "NA", "NA"], ["NA", "NA", "NA"],
#                                    ["NA", "NA", "NA"], "NA"]}


def walk_techdata(eia_nlt_cp, eia_nlt_l, eia_lt, eia_lt_choice,
                  tech_eia_nonlt, tech_eia_lt,
                  tech_non_eia, json_dict, project_dict, key_list=[]):
    """ Proceed recursively through data stored in dict-type structure
    and perform calculations at each leaf/terminal node in the data. In
    this case, the function is running through the input microsegments
    JSON levels and updating the values at each of the technology-level leaf
    nodes to the correct cost, performance, and lifetime information for that
    technology """

    for key, item in json_dict.items():
        # If there are additional levels in the dict, call the function
        # again to advance another level deeper into the data structure
        if isinstance(item, dict):
            walk_techdata(eia_nlt_cp, eia_nlt_l, eia_lt, eia_lt_choice,
                          tech_eia_nonlt, tech_eia_lt,
                          tech_non_eia, item, project_dict, key_list + [key])
        # If a leaf node has been reached, finish constructing the key
        # list for the current location and update the data in the dict
        else:
            # Confirm that the building type is one of the residential
            # building types in mseg.bldgtypedict before attempting to
            # proceed with processing the input data
            if key_list[1] in mseg.bldgtypedict.keys():
                leaf_node_keys = key_list + [key]
                # Update data unless the leaf node is describing square
                # footage information, which is not relevant to the
                # mseg_techdata.py routine; in this case, skip the node
                if leaf_node_keys[-1] not in [
                   "total square footage", "new homes", "total homes"]:
                    data_dict = \
                        list_generator_techdata(eia_nlt_cp, eia_nlt_l,
                                                eia_lt, eia_lt_choice,
                                                tech_eia_nonlt,
                                                tech_eia_lt, tech_non_eia,
                                                leaf_node_keys, project_dict)
                    # Set dict key to extracted data
                    json_dict[key] = data_dict

    # Return updated dict
    return json_dict


def list_generator_techdata(eia_nlt_cp, eia_nlt_l, eia_lt, eia_lt_choice,
                            tech_eia_nonlt, tech_eia_lt,
                            tech_non_eia, leaf_node_keys, project_dict):
    """ Given an empty leaf node for a specific technology in the microsegments
    JSON, as well as projected technology costs, performance, and lifetimes
    from EIA and internal BTO analysis, find the appropriate data for the
    specific technology, record it in a performance/cost/lifetime
    dict, and update the leaf node value to this dict """

    # Check to ensure that the dict key hierarchy is generally valid
    # (>= 4 levels: census division, building type, fuel type, and end use)
    if len(leaf_node_keys) < 4:
        raise KeyError("Invalid microsegment key chain structure!")

    # Initialize a dict with performance, cost, lifetime, and consumer choice
    # information to be updated for a given technology in the microsegments
    # JSON input.  Consumer choice information will be used to determine
    # a) the size of the competed market for efficient alternatives to a
    # baseline technology in a given microsegment and year (expected to be
    # determined via COBAM outputs), and b) how much of that competed market
    # each competing efficiency measure is able to capture
    data_dict = {"performance": None,
                 "installed cost": None,
                 "lifetime": None,
                 "consumer choice": {
                      "competed market share": {
                          "model type": "logistic regression",
                          "parameters": {"b1": None, "b2": None},
                          "source": None}}}

    # The census division name to be used in filtering EIA data is the
    # first level in the dict key hierarchy of the input microsegments JSON.
    cdiv = leaf_node_keys[0]

    # Check that the census division name can be translated to the
    # filtering information needed by this routine; if not, set census
    # division to None
    if cdiv not in mseg_cdiv_translate.keys():
        cdiv = None

    # Set the fuel type to be used in filtering EIA data as the
    # third level in the dict key hierarchy of the input microsegments JSON
    fuel_type = leaf_node_keys[2]

    # The end use name to be used in filtering EIA data is the fourth or fifth
    # level in the dict key hierarchy of the input microsegments JSON.
    # To set the end use, check for a special case where the end use is grouped
    # into a larger category (i.e., "freezers" grouped into "other (grid
    # electric)"). If it is a part of this larger grouping, move one more level
    # down the key hierarchy (to the fifth level) to set the specific end use
    # name; if it is not, set the end use name as the fourth level in the key
    # hierarchy.
    if leaf_node_keys[3] in ["other", "TVs", "computers"]:
        end_use = leaf_node_keys[4]
    else:
        end_use = leaf_node_keys[3]

    # Check that the end use name can be translated to the filtering
    # information needed by this routine; if not, set end use to None
    if end_use not in mseg_enduse_translate.keys() and \
       end_use not in \
       ["lighting", "secondary heating", "other"] and \
       end_use not in tech_non_eia:
        end_use = None

    # Identify the technology to be used in filtering EIA data as the last
    # level in the dict key hierarchy of the input microsegments JSON
    tech_dict_key = leaf_node_keys[-1]

    # Flag a special case of a "secondary heater" technology type, which is
    # unique to the secondary heating end use.  Identify which type of
    # secondary heating technology is being filtered for based on the
    # fuel type of the microsegment as defined above.  Note that
    # a "secondary heater" technology type only applies to electric and natural
    # gas secondary heating in the microsegments JSON
    if tech_dict_key == "secondary heater":
        if fuel_type == "electricity":
            tech_dict_key = "secondary heating (electric)"
        else:
            tech_dict_key = "secondary heating (natural gas)"

    # Determine which technology dict from the beginning of the script
    # to use in determining filtering information; if no matching dict
    # exists, set this variable to None
    if tech_dict_key in tech_eia_nonlt.keys():
        tech_dict = tech_eia_nonlt
    elif tech_dict_key in tech_eia_lt.keys():
        tech_dict = tech_eia_lt
    elif tech_dict_key in tech_non_eia.keys():
        tech_dict = tech_non_eia
    else:
        tech_dict = None

    # Access the correct technology characteristics filtering information based
    # on the census division, end use, and technology information from the
    # above few lines. First screen to make sure that none of these variables
    # are set to None; if any are None, technology characteristics data are
    # not available for the given combination of variables; accordingly, set
    # the technology filtering information to zero
    if all([x is not None for x in [cdiv, end_use, tech_dict]]):
        filter_info = tech_dict[tech_dict_key]

        # Update dict values given filtering information

        # In first case (EIA non-lighting technology), run through technology
        # info. found in EIA "rsmeqp.txt" and "rsclass.txt" files via
        # tech_eia_nonlt dict
        if filter_info[0] == "EIA_EQUIP":

            # Initialize matched row lists for "typical" and "best"
            # performance, cost, and consumer choice information for the non-
            # lighting technology in the EIA files
            match_list_typ_perfcost = []
            match_list_best_perfcost = []
            # Loop through the EIA non-lighting technology performance, cost,
            # and consumer choice data array, searching for a match with the
            # desired technology
            for (idx, row) in enumerate(eia_nlt_cp):
                # Check whether the looped row concerns the census division
                # and end use currently being updated in the microsegments
                # JSON; if it does, proceed further (note that EIA non-lighting
                # technology cost/performance/choice info. is broken down by
                # both census div. and end use); otherwise, loop to next row
                if row["CDIV"] == mseg_cdiv_translate[cdiv] and \
                      row["ENDUSE"] == mseg_enduse_translate[end_use]:

                    # Set up each row in the array as a "compareto" string for
                    # use in a regex comparison below
                    compareto = str(row)

                    # In some cases in the EIA non-lighting technology
                    # performance cost/choice data, a technology will have
                    # multiple variants. These variants may be based on a)
                    # technology configuration (i.e. "FrzrC#1" (chest),
                    # "FrzrU#1" (upright)) or b) fuel type (i.e., "ELEC_STV"
                    # (electric stove), "NG_STV" (natural gas stove) for
                    # cooking).  In case a), all tech. configurations
                    # will be included in the filter, and single performance,
                    # cost, and consumer choice values will be averaged across
                    # these configurations. In case b), the filtering info.
                    # for cost, performance, and consumer choice will be each
                    # comprised of multiple elements (i.e., cost will be
                    # specified as [cost electric, cost natural gas, cost
                    # other fuel]). Note that these elements are ordered by
                    # fuel type: electric, then natural gas, then "other" fuel

                    # Determine performance/cost/consumer choice filtering
                    # names and performance units for case a) in comment above
                    if tech_dict_key == "refrigeration" or \
                       tech_dict_key == "freezers":
                        # Note: refrigeration has three technology config.
                        # variants for filtering (bottom freezer, side freezer,
                        # top freezer)
                        if tech_dict_key == "refrigeration":
                            typ_filter_name = "(" + filter_info[2][0] + "|" + \
                                filter_info[2][1] + "|" + \
                                filter_info[2][2] + ")"
                            best_filter_name = "(" + \
                                filter_info[3][0] + "|" + \
                                filter_info[3][1] + "|" + \
                                filter_info[3][2] + ")"
                        # Note: refrigeration has two technology configuration
                        # variants for filtering (chest, upright)
                        else:
                            typ_filter_name = "(" + filter_info[2][0] + "|" + \
                                filter_info[2][1] + ")"
                            best_filter_name = "(" + filter_info[3][0] + \
                                "|" + filter_info[3][1] + ")"
                        # Update performance units (cost units set later)
                        perf_units = filter_info[4]
                    # Determine performance/cost/consumer choice filtering
                    # names and performance units for case b) in comment above
                    elif isinstance(filter_info[2], list):
                        # Filter names determined by fuel type (electricity,
                        # natural gas, and distillate/"other")
                        if fuel_type == "electricity":
                            typ_filter_name = filter_info[2][0]
                            best_filter_name = filter_info[3][0]
                            # Update performance units (cost units set later)
                            perf_units = filter_info[4][0]
                        # In a water heating technology case, electric/solar
                        # water heater filtering information is handled
                        # separately from the natural gas and "other" fuel
                        # filtering information (see tech_eia_nonlt above)
                        elif fuel_type == "natural gas":
                            # Water heating case, natural gas fuel
                            if end_use == "water heating":
                                typ_filter_name = filter_info[2][0]
                                best_filter_name = filter_info[3][0]
                                # Update performance units (cost units set
                                # later)
                                perf_units = filter_info[4][0]
                            # Non water heating case, natural gas
                            else:
                                typ_filter_name = filter_info[2][1]
                                best_filter_name = filter_info[3][1]
                                # Update performance units (cost units set
                                # later)
                                perf_units = filter_info[4][1]
                        else:
                            # Water heating case, distillate or "other" fuel
                            if end_use == "water heating":
                                typ_filter_name = filter_info[2][1]
                                best_filter_name = filter_info[3][1]
                                # Update performance units (cost units set
                                # later)
                                perf_units = filter_info[4][1]
                            # Non water heating case, distillate/"other"
                            else:
                                typ_filter_name = filter_info[2][2]
                                best_filter_name = filter_info[3][2]
                                # Update performance units (cost units set
                                # later)
                                perf_units = filter_info[4][2]

                    # Determine performance/cost/consumer choice filter names
                    # and performance units for a non-lighting technology with
                    # only one configuration/fuel type
                    else:
                        typ_filter_name = filter_info[2]
                        best_filter_name = filter_info[3]
                        # Update performance units for technologies with only
                        # one configuration/fuel type (cost units set later)
                        perf_units = filter_info[4]

                    # Construct the full non-lighting technology performance,
                    # cost, and consumer choice filtering info. to compare
                    # against the current numpy row in a regex for "typical"
                    # and "best" performance/cost/choice cases
                    comparefrom_typ = ".+" + typ_filter_name
                    comparefrom_best = ".+" + best_filter_name

                    # Check for a match between the "typical" performance,
                    # cost, and consumer choice filtering information and the
                    # row
                    match_typ = re.search(comparefrom_typ, compareto,
                                          re.IGNORECASE)
                    # If there is no match for the "typical" performance/cost/
                    # consumer choice case, check for a "best" case performance
                    # and cost match
                    match_best = re.search(comparefrom_best, compareto,
                                           re.IGNORECASE)

                    # If there was a match for the "typical" performance, cost,
                    # and consumer choice cases, append the row to the match
                    # lists initialized for non-lighting technologies above.
                    # Do the same if there was a match for the "best"
                    # performance, cost, and consumer choice case
                    if match_typ:
                        match_list_typ_perfcost.append(row)
                    if match_best:
                        match_list_best_perfcost.append(row)

            # After search through EIA non-lighting technology performance/cost
            # and consumer choice array is complete:

            # If the matched "typical" and "best" performance, cost, and
            # consumer choice parameter lists are populated, convert them back
            # to numpy arrays for later operations; otherwise, yield an error
            if len(match_list_typ_perfcost) > 0 and \
               len(match_list_best_perfcost) > 0:
                match_list_typ_perfcost = numpy.array(
                    match_list_typ_perfcost, dtype=eia_nlt_cp.dtype)
                match_list_best_perfcost = numpy.array(
                    match_list_best_perfcost, dtype=eia_nlt_cp.dtype)
            else:
                raise ValueError("No EIA performance/cost data match for" +
                                 " non-lighting technology!")

            # Once matched "typical" and "best" performance, cost, and consumer
            # choice arrays are finalized for the given non-lighting
            # technology, rearrange the projection year info. for these data in
            # the array to be consistent with the "mseg.py" microsegment
            # projection years (i.e., {"2009": XXX, "2010": XXX, etc.}) using
            # the "fill_years_nlt" function
            [perf_typ, cost_typ, b1, b2] = fill_years_nlt(
                match_list_typ_perfcost, project_dict, tech_dict_key)
            [perf_best, cost_best, b1_best, b2_best] = fill_years_nlt(
                match_list_best_perfcost, project_dict, tech_dict_key)

            # Initialize a count of the number of matched lifetime data rows
            life_match_ct = 0

            # Loop through the EIA non-lighting technology lifetime
            # data, searching for a match with the desired technology
            for (idx, row) in enumerate(eia_nlt_l):

                # Check whether the looped row concerns the end use currently
                # being updated in the microsegments JSON; if it does, proceed
                # further (note that EIA non-lighting technology lifetime info.
                # is broken down by end use); otherwise, loop to next row
                if row["ENDUSE"] == mseg_enduse_translate[end_use]:

                    # Set up each row in the array as a "compareto" string for
                    # use in a regex comparison below
                    compareto = str(row)

                    # In some cases in the EIA non-lighting lifetime data, a
                    # technology will have multiple variants.  These variants
                    # are based on fuel type (i.e., "ELEC_STV" (elec. stove),
                    # "NG_STV" (natural gas stove) for cooking).  In this case,
                    # the filtering information for lifetime will be comprised
                    # of multiple elements (i.e., lifetime will be specified as
                    # [lifetime electric, lifetime natural gas, lifetime other
                    # fuel]). Note again that these elements are ordered by
                    # fuel type: electric, then natural gas, then "other" fuel

                    # Determine lifetime filtering names for a non-lighting
                    # technology with multiple fuel types
                    if isinstance(filter_info[1], list):
                        if fuel_type == "electricity":
                            filter_name = filter_info[1][0]
                        elif fuel_type == "natural gas":
                            if end_use == "water heating":
                                filter_name = filter_info[1][0]
                            else:
                                filter_name = filter_info[1][1]
                        elif fuel_type in ["distillate", "other fuel"]:
                            if end_use == "water heating":
                                filter_name = filter_info[1][1]
                            else:
                                filter_name = filter_info[1][2]
                        else:
                            raise ValueError(
                              "Invalid fuel type in microsegment!")
                    # Determine lifetime filtering names for a non-lighting
                    # technology with only one fuel type
                    else:
                        filter_name = filter_info[1]

                    # Construct the full non-lighting technology lifetime
                    # filtering information to compare against current numpy
                    # row in a regex
                    comparefrom = ".+" + filter_name

                    # Check for a match between the filtering information and
                    # row
                    match = re.search(comparefrom, compareto, re.IGNORECASE)
                    # If there was a match, draw the final technology lifetime
                    # info. (average and range) from the appropriate column in
                    # row
                    if match:
                        # Update matched rows count
                        life_match_ct += 1
                        # Establish single values for avg. life and range (EIA
                        # does not break out life by year for non-lighting
                        # technologies)
                        life_avg_set = (row["LIFE_MAX"] + row["LIFE_MIN"]) / 2
                        life_range_set = row["LIFE_MAX"] - life_avg_set
                        # Extend single lifetime values across each year in the
                        # modeling time horizon
                        [life_avg, life_range] = [dict.fromkeys(
                                                  project_dict.keys(), n)
                                                  for n in [life_avg_set,
                                                            life_range_set]]

            # If there were no matches for lifetime data on the technology,
            # yield an error
            if life_match_ct == 0:
                raise ValueError(
                  "No EIA lifetime data match for non-lighting technology!")

            # Set source to EIA AEO for these non-lighting technologies
            [perf_source, cost_source, life_source, tech_choice_source] = \
                ["EIA AEO" for n in range(4)]

        # In second case (EIA lighting technology), run through technology
        # info. found in EIA "rsmlgt.txt" and "rsclass.txt" files via
        # tech_eia_lt dict
        elif filter_info[0] == "EIA_LT":

            # Initialize matched row list for performance, cost, and lifetime
            # information for the lighting technology in the EIA files
            match_list = []

            # Loop through the EIA lighting technology performance, cost, and
            # lifetime data, searching for a match with the desired technology
            for (idx, row) in enumerate(eia_lt):

                # Set up each row in the array as a "compareto" string for use
                # in a regex comparison below
                compareto = str(row)
                # Construct the full lighting technology performance, cost, and
                # lifetime filtering info. to compare against current numpy row
                # in a regex
                comparefrom = ".+" + filter_info[1][0] + ".+" + \
                    filter_info[1][1]

                # Check for a match between the filtering information and row
                match = re.search(comparefrom, compareto, re.IGNORECASE)
                # If there was a match, append the row to the match list
                # initialized for lighting technologies above
                if match:
                    match_list.append(row)

            # If the matched performance, cost, and lifetime list is
            # populated, convert it back to a numpy array for later operations;
            # otherwise, yield an error

            # Convert matched performance, cost, and lifetime list back to
            # numpy array for later operations
            if len(match_list) > 0:
                match_list = numpy.array(match_list, dtype=eia_lt.dtype)
            else:
                raise ValueError(
                  "No performance/cost/lifetime data match for" +
                  " lighting technology!")

            # Once the performance, cost, and lifetime arrays have been
            # constructed for the given lighting technology, rearrange the
            # projection year information for these data in the array to be
            # consistent with the "mseg.py" microsegment projection years
            # (i.e., {"2009": XXX, "2010": XXX, etc.}) using the
            # "fill_years_lt" function
            [perf_typ, cost_typ, life_avg] = fill_years_lt(match_list,
                                                           project_dict)

            # No "best" technology performance or cost data are available from
            # EIA for lighting technologies, so set these variables to zero.
            # Also set lifetime range to zero for lighting techologies, since
            # only a single lifetime number is provided by EIA (* presumably an
            # average lifetime)
            [perf_best, cost_best, life_range] = [0 for n in range(3)]

            # Set lighting technology consumer choice parameters to universal
            # values specified at bottom of EIA 'rsmlgt.txt' file
            b1 = copy.deepcopy(eia_lt_choice["b1"])
            b2 = copy.deepcopy(eia_lt_choice["b2"])

            # Set lighting performance units(cost units set later)
            perf_units = filter_info[2]

            # Set sources to EIA AEO for these lighting technologies
            [perf_source, cost_source, life_source, tech_choice_source] = \
                ["EIA AEO" for n in range(4)]

        # In third case (BTO-defined technology), run through technology info.
        # directly specified in tech_non_eia above
        else:
            # Set all performance, cost, and lifetime information to that
            # specified in "tech_non_eia" towards the beginning of this script.
            # Note that there are only single values specified for performance,
            # cost, and lifetime here (for now), so the below code extends
            # these values across each year in the modeling time horizon
            [perf_typ, perf_best, cost_typ, cost_best,
             life_avg, life_range] = [
                dict.fromkeys(project_dict.keys(), n) for n in [
                    filter_info[1][0], filter_info[1][1], filter_info[2][0],
                    filter_info[2][1], filter_info[0][0], filter_info[0][1]]]
            # Set performance units and performance, cost, and lifetime sources
            [perf_units, perf_source, cost_source, life_source] = [
                filter_info[3], filter_info[1][2], filter_info[2][2],
                filter_info[0][2]]

        # Based on above search results, update the dict with performance,
        # cost, lifetime, and consumer choice information for the given
        # technology if 'demand' not in leaf_node_keys:
        # Update performance information
        data_dict["performance"] = {"typical": perf_typ, "best": perf_best,
                                    "units": perf_units, "source": perf_source}
        # Update cost information
        data_dict["installed cost"] = {"typical": cost_typ, "best": cost_best,
                                       "units": "2013$/unit",
                                       "source": cost_source}
        # Update lifetime information
        data_dict["lifetime"] = {"average": life_avg, "range": life_range,
                                 "units": "years", "source": life_source}
        # Update consumer choice information
        data_dict["consumer choice"]["competed market share"][
            "parameters"]["b1"] = b1
        data_dict["consumer choice"]["competed market share"][
            "parameters"]["b2"] = b2
        data_dict["consumer choice"]["competed market share"][
            "source"] = tech_choice_source
    else:
        data_dict = 0

    # Return updated technology performance, cost, and lifetime information
    # as well as reduced EIA non-lighting technology data array with matched
    # rows removed
    return data_dict


def fill_years_nlt(match_list, project_dict, tech_dict_key):
    """ Reconstruct EIA performance, cost, and consumer choice parameter
    projections for non-lighting technologies into a list of dicts containing
    information for each projection year for microsegments in "mseg.py" """

    # For the special non-lighting technology cases of refrigeration and
    # freezers, any given year will have multiple technology configurations.
    # The next few lines average the performance and cost figures across those
    # configurations to yield just one number for each year
    if tech_dict_key == "refrigeration" or tech_dict_key == "freezers":

        # Register number of refrigerator/freezer technology sub-types
        ntypes = len(tech_eia_nonlt[tech_dict_key][2])

        # Initialize a new list to append averaged performance/cost/consumer
        # choice information to
        match_list_new = []

        # Loop through all the rows in the match_list array and average
        # performance, cost, and consumer choice data by year; then append
        # to match_list_new
        for x in sorted(numpy.unique(match_list["START_EQUIP_YR"])):

            # Check for year bin consistency across the multiple refrigeration/
            # freezer technology sub-types being averaged
            if len(numpy.where(match_list["START_EQUIP_YR"] == x)[0]) == \
               ntypes:
                match_list_new.append(
                    (x, numpy.average(
                        match_list[numpy.where(
                            match_list["START_EQUIP_YR"] == x)][
                            "BASE_EFF"]),
                        numpy.average(
                        match_list[numpy.where(
                            match_list["START_EQUIP_YR"] == x)][
                            "INST_COST"]),
                        numpy.average(
                        match_list[numpy.where(
                            match_list["START_EQUIP_YR"] == x)]
                            ["EFF_CHOICE_P1"]),
                        numpy.average(
                        match_list[numpy.where(
                            match_list["START_EQUIP_YR"] == x)]
                            ["EFF_CHOICE_P2"])))
            else:
                raise ValueError('Technology sub-type year bins inconsistent!')

        # Once all the averaged figures are available, reconstruct this
        # information into a numpy array with named columns for later use
        # (* NOTE: it may be possible to perform the above averaging on the
        # initial match_list array above without converting it to a list; this
        # should be investigated further)
        match_list = numpy.array(match_list_new,
                                 dtype=[("START_EQUIP_YR", "<i8"),
                                        ("BASE_EFF", "<f8"),
                                        ("INST_COST", "<f8"),
                                        ("EFF_CHOICE_P1", "<f8"),
                                        ("EFF_CHOICE_P2", "<f8")])
    # Update performance information for projection years
    perf = stitch(match_list, project_dict, "BASE_EFF")
    # Update cost information for projection years
    cost = stitch(match_list, project_dict, "INST_COST")
    # Update consumer choice parameters for projection years
    b1 = stitch(match_list, project_dict, "EFF_CHOICE_P1")
    b2 = stitch(match_list, project_dict, "EFF_CHOICE_P2")

    # Return updated EIA performance, cost, and consumer choice information for
    # non-lighting technologies
    return [perf, cost, b1, b2]


def fill_years_lt(match_list, project_dict):
    """ Reconstruct EIA performance, cost, and lifetime projections for
    lighting technologies into a list of dicts containing information for each
    projection year used for microsegments in "mseg.py" """

    # Filter out any rows where 9999 is found in lighting life column (invalid)
    match_list = match_list[numpy.where(match_list["LIFE_HRS"] != 9999)]

    # Update performance information for projection years
    perf = stitch(match_list, project_dict, "BASE_EFF")
    # Update cost information for projection years
    cost = stitch(match_list, project_dict, "INST_COST")
    # Update lifetime information for projection years
    life = stitch(match_list, project_dict, "LIFE_HRS")
    # Convert lighting lifetimes from hours to years
    for yr in life.keys():
        life[yr] = life[yr] / 8760

    # Return updated EIA performance, cost, and lifetime information
    # for lighting technologies
    return [perf, cost, life]


def stitch(input_array, project_dict, col_name):
    """ Given EIA performance, cost, and lifetime projections for a technology
    between a series of time periods (i.e. 2010-2014, 2014-2020, 2020-2040),
    reconstruct this information in a dict with annual keys across the
    modeling time horizon used in "mseg.py" (i.e. {"2009": XXX, "2010": XXX,
    ..., "2040": XXX}) """

    # Initialize output dict which will contain EIA performance, cost,
    # or lifetime information continuous across each year of the
    # modeling time horizon
    output_dict = {}

    # Initialize a previous year value indicator to be used
    # in cases where the input array does not contain information
    # for a given year in the modeling time horizon
    prev_yr_val = None

    # Loop through each year of the projection and fill in information
    # from the appropriate row and column from the input array
    for (yr_ind, yr) in enumerate(sorted(project_dict.keys())):
        # Reduce the input array to only the row concerning the year being
        # looped through (if this year exists in the "START_EQUIP_YR" column)
        array_reduce = input_array[input_array["START_EQUIP_YR"] == int(yr)]
        # If a unique row has been discovered for the looped year, draw output
        # information from column in that row keyed by col_name input; if
        # there are multiple rows that match the looped year, yield an error
        if array_reduce.shape[0] > 0:
            if array_reduce.shape[0] == 1:
                output_dict[yr] = float(array_reduce[col_name])
            else:
                raise ValueError("Multiple identical years in filtered array!")
        # If no row has been discovered for the looped year and we are not in
        # the first year of the loop, set output information to that of the
        # previously looped year
        elif yr_ind != 0:
            output_dict[yr] = prev_yr_val
        # If no row has been discovered for the looped year and we are in the
        # first year of the loop, set output information to that of the row
        # with a "START_EQUIP_YR" that is closest to the looped year
        else:
            # Find the row(s) where the absolute difference between the loop
            # year and value for the "START_EQUIP_YR" column is smallest
            array_close_ind = numpy.where(abs(int(yr) -
                                          input_array["START_EQUIP_YR"]) ==
                                          min(abs(int(yr) -
                                              input_array[
                                              "START_EQUIP_YR"])))[0]
            # If only one row has been found above, draw output information
            # from the column in that row keyed by col_name input
            if len(array_close_ind) == 1:
                output_dict[yr] = float(input_array[array_close_ind][col_name])
            # If multiple rows have been found above and each has a unique year
            # value, draw output information from the column in the first of
            # these rows keyed by col_name input; if multiple rows have been
            # found with the same year value, yield an error
            else:
                if len(array_close_ind) > 1 and \
                   len(numpy.unique(array_close_ind)) == len(array_close_ind):
                    output_dict[yr] = float(
                        input_array[array_close_ind][0][col_name])
                else:
                    raise ValueError("Multiple identical years in filtered" +
                                     " array!")

        # Update previous year value indicator to the output information for
        # the current loop
        prev_yr_val = output_dict[yr]

    # Return output dictionary with performance, lifetime, or cost information
    # updated across all projection years
    return output_dict


def main():
    """ Import EIA cost/performance and lifetime files; run through these
    files, using their information to fill in a dict with technology-level
    cost, performance, and lifetime information (where EIA data do not exist
    for a given technology, fill information in with BTO numbers); before
    exporting updated dict to a JSON, translate the dict from a census division
    breakdown to a climate zone breakdown """

    # Set up to support user option to specify the year for the
    # AEO data being imported (default if the option is not used
    # should be current year)
    parser = argparse.ArgumentParser()
    help_string = 'Specify year of AEO data to be imported'
    parser.add_argument('-y', '--year', type=int, help=help_string,
                        choices=[2015, 2017])

    # Get import year specified by user (if any)
    aeo_import_year = parser.parse_args().year

    # Specify the number of header and footer lines to skip based on the
    # optional AEO year indicated by the user when this module is called
    if aeo_import_year == 2015:
        nlt_cp_skip_header = 20
        nlt_l_skip_header = 19
        lt_skip_header = 35
        lt_skip_footer = 54
    else:
        nlt_cp_skip_header = 25
        nlt_l_skip_header = 20
        lt_skip_header = 37
        if aeo_import_year in [2016, 2017]:
            lt_skip_footer = 54
        else:
            lt_skip_footer = 52

    # Instantiate objects that contain useful variables
    handyvars = UsefulVars()
    eiadata = EIAData()

    # Import EIA non-lighting residential cost and performance data
    eia_nlt_cp = numpy.genfromtxt(eiadata.r_nlt_costperf, names=r_nlt_cp_names,
                                  dtype=None, comments=None,
                                  skip_header=nlt_cp_skip_header,
                                  encoding="latin1")

    # Import EIA non-lighting residential lifetime data
    eia_nlt_l = numpy.genfromtxt(eiadata.r_nlt_life, names=r_nlt_l_names,
                                 dtype=None, comments=None,
                                 skip_header=nlt_l_skip_header,
                                 encoding="latin1")

    # Import EIA lighting residential cost, performance and lifetime data
    eia_lt = numpy.genfromtxt(eiadata.r_lt_all, names=r_lt_names,
                              dtype=None, comments=None,
                              skip_header=lt_skip_header,
                              skip_footer=lt_skip_footer,
                              encoding="latin1")

    # Establish the modeling time horizon based on metadata generated
    # from EIA AEO data files
    with open(handyvars.aeo_metadata, 'r') as metadata:
        metajson = json.load(metadata)

    # Define years vector using year data from metadata and convert
    # the resulting list into a dict with the years as keys
    years = list(range(metajson['min year'], metajson['max year'] + 1))
    project_dict = dict.fromkeys(years)

    # Establish residential lighting technology consumer choice parameters for
    # each year in the modeling time horizon (these parameters will later be
    # applied across all residential lighting technologies, and are based on
    # EIA consumer choice data for the residential lighting end use at the
    # bottom of 'rsmlgt.txt') (* HARD CODED, MAY CHANGE IN THE FUTURE *)
    eia_lt_choice = {"b1": {k: -0.95
                            for k in project_dict.keys()},
                     "b2": {k: -0.10
                            for k in project_dict.keys()}}

    # Import microsegments JSON file as a dictionary structure
    with open(handyvars.json_in, "r") as jsi:
        msjson = json.load(jsi)

    # Run through microsegment JSON levels, determine technology leaf node
    # info. to mine from the imported data, and update nodes with this info.
    result = walk_techdata(eia_nlt_cp, eia_nlt_l, eia_lt, eia_lt_choice,
                           tech_eia_nonlt, tech_eia_lt,
                           tech_non_eia, msjson, project_dict)

    # Write the updated dict of data to a new JSON file
    with open(handyvars.json_out, "w") as jso:
        json.dump(result, jso, indent=2)


if __name__ == "__main__":
    main()
