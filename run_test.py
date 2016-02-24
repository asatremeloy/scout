#!/usr/bin/env python3

""" Tests for running the engine """

# Import code to be tested
import run

# Import needed packages
import unittest
import numpy
import scipy.stats as ss
import copy

# Define sample residential measure for use in tests below
sample_measure = {
    "name": "sample measure 1",
    "active": 1,
    "market_entry_year": None,
    "market_exit_year": None,
    "structure_type": ["new", "retrofit"],
    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
    "bldg_type": ["single family home"],
    "fuel_type": {"primary": ["electricity (grid)"],
                  "secondary": None},
    "fuel_switch_to": None,
    "end_use": {"primary": ["heating", "cooling"],
                "secondary": None},
    "technology_type": {"primary": "supply",
                        "secondary": None},
    "technology": {"primary": ["boiler (electric)",
                   "ASHP", "GSHP", "room AC"],
                   "secondary": None}}

# Define sample residential measure w/ secondary msegs for use in tests below
sample_measure2 = {
    "name": "sample measure 2",
    "active": 1,
    "market_entry_year": None,
    "market_exit_year": None,
    "structure_type": ["new", "retrofit"],
    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
    "bldg_type": ["single family home"],
    "fuel_type": {"primary": ["electricity (grid)"],
                  "secondary": ["electricity (grid)"]},
    "fuel_switch_to": None,
    "end_use": {"primary": ["heating", "cooling"],
                "secondary": ["lighting"]},
    "technology_type": {"primary": "supply",
                        "secondary": "supply"},
    "technology": {"primary": ["boiler (electric)",
                   "ASHP", "GSHP", "room AC"],
                   "secondary": ["general service (LED)"]}}

# Define sample commercial measure for use in tests below
sample_measure3 = {
    "name": "sample measure 3 (commercial)",
    "active": 1,
    "market_entry_year": None,
    "market_exit_year": None,
    "structure_type": ["new", "retrofit"],
    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
    "bldg_type": ["assembly"],
    "fuel_type": {"primary": ["electricity (grid)"],
                  "secondary": None},
    "fuel_switch_to": None,
    "end_use": {"primary": ["heating", "cooling"],
                "secondary": None},
    "technology_type": {"primary": "supply",
                        "secondary": None},
    "technology": {"primary": ["boiler (electric)",
                   "ASHP", "GSHP", "room AC"],
                   "secondary": None}}

# Define sample residential water heating measure for use in tests of
# measure packaging routine below
sample_measure4 = {
    "name": "sample measure 4",
    "active": 1,
    "market_entry_year": None,
    "market_exit_year": None,
    "structure_type": ["new", "retrofit"],
    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
    "bldg_type": ["single family home"],
    "fuel_type": {"primary": ["natural gas"],
                  "secondary": None},
    "fuel_switch_to": None,
    "end_use": {"primary": ["water heating"],
                "secondary": None},
    "technology_type": {"primary": "supply",
                        "secondary": None},
    "technology": {"primary": None,
                   "secondary": None},
    "mseg_adjust": {
        "contributing mseg keys and values": {
            ("('AIA_CZ1', 'single family home', 'natural gas',"
             "'water heating', None, 'new')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 10, "2010": 10},
                        "measure": {"2009": 6, "2010": 6}},
                    "competed": {
                        "all": {"2009": 5, "2010": 5},
                        "measure": {"2009": 1, "2010": 1}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 12, "2010": 12}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 2, "2010": 2}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 18, "2010": 18}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 3, "2010": 3}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 12, "2010": 12}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 2, "2010": 2}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 3, "2010": 3}}}},
                "lifetime": {
                    "baseline": {"2009": 5, "2010": 5},
                    "measure": 10}},
            ("('AIA_CZ1', 'single family home', 'natural gas',"
             "'water heating', None, 'retrofit')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 10, "2010": 10},
                        "measure": {"2009": 6, "2010": 6}},
                    "competed": {
                        "all": {"2009": 5, "2010": 5},
                        "measure": {"2009": 1, "2010": 1}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 12, "2010": 12}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 2, "2010": 2}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 18, "2010": 18}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 3, "2010": 3}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 12, "2010": 12}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 2, "2010": 2}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 3, "2010": 3}}}},
                "lifetime": {
                    "baseline": {"2009": 5, "2010": 5},
                    "measure": 10}},
            ("('AIA_CZ2', 'single family home', 'natural gas',"
             "'water heating', None, 'new')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 10, "2010": 10},
                        "measure": {"2009": 6, "2010": 6}},
                    "competed": {
                        "all": {"2009": 5, "2010": 5},
                        "measure": {"2009": 1, "2010": 1}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 12, "2010": 12}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 2, "2010": 2}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 18, "2010": 18}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 3, "2010": 3}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 12, "2010": 12}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 2, "2010": 2}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 3, "2010": 3}}}},
                "lifetime": {
                    "baseline": {"2009": 5, "2010": 5},
                    "measure": 10}},
            ("('AIA_CZ2', 'single family home', 'natural gas',"
             "'water heating', None, 'retrofit')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 10, "2010": 10},
                        "measure": {"2009": 6, "2010": 6}},
                    "competed": {
                        "all": {"2009": 5, "2010": 5},
                        "measure": {"2009": 1, "2010": 1}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 12, "2010": 12}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 2, "2010": 2}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 18, "2010": 18}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 3, "2010": 3}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 12, "2010": 12}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 2, "2010": 2}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 3, "2010": 3}}}},
                "lifetime": {
                    "baseline": {"2009": 5, "2010": 5},
                    "measure": 10}}},
        "competed choice parameters": {
            ("('AIA_CZ1', 'single family home', 'natural gas',"
             "'water heating', None, 'new')"): {
                "b1": {"2009": 0.5, "2010": 0.5},
                "b2": {"2009": 0.5, "2010": 0.5}},
            ("('AIA_CZ1', 'single family home', 'natural gas',"
             "'water heating', None, 'retrofit')"): {
                "b1": {"2009": 0.5, "2010": 0.5},
                "b2": {"2009": 0.5, "2010": 0.5}},
            ("('AIA_CZ2', 'single family home', 'natural gas',"
             "'water heating', None, 'new')"): {
                "b1": {"2009": 0.5, "2010": 0.5},
                "b2": {"2009": 0.5, "2010": 0.5}},
            ("('AIA_CZ2', 'single family home', 'natural gas',"
             "'water heating', None, 'retrofit')"): {
                "b1": {"2009": 0.5, "2010": 0.5},
                "b2": {"2009": 0.5, "2010": 0.5}}},
        "supply-demand adjustment": {
            "savings": {},
            "total": {}},
        "savings updated": False}}

# Define sample residential lighting measure for use in tests of
# measure packaging routine below
sample_measure5 = {
    "name": "sample measure 5",
    "active": 1,
    "market_entry_year": None,
    "market_exit_year": None,
    "structure_type": ["retrofit"],
    "climate_zone": ["AIA_CZ1"],
    "bldg_type": ["single family home"],
    "fuel_type": {"primary": ["electricity (grid)"],
                  "secondary": None},
    "fuel_switch_to": None,
    "end_use": {"primary": ["lighting"],
                "secondary": None},
    "technology_type": {"primary": "supply",
                        "secondary": None},
    "technology": {"primary": [
        "reflector (incandescent)",
        "reflector (halogen)"], "secondary": None},
    "mseg_adjust": {
        "contributing mseg keys and values": {
            ("('AIA_CZ1', 'single family home', 'electricity (grid)',"
             "'lighting', 'reflector (incandescent)', 'retrofit')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 100, "2010": 100},
                        "measure": {"2009": 60, "2010": 60}},
                    "competed": {
                        "all": {"2009": 50, "2010": 50},
                        "measure": {"2009": 10, "2010": 10}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 200, "2010": 200},
                        "efficient": {"2009": 120, "2010": 120}},
                    "competed": {
                        "baseline": {"2009": 100, "2010": 100},
                        "efficient": {"2009": 20, "2010": 20}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 300, "2010": 300},
                        "efficient": {"2009": 180, "2010": 180}},
                    "competed": {
                        "baseline": {"2009": 150, "2010": 150},
                        "efficient": {"2009": 30, "2010": 30}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 200, "2010": 200},
                            "efficient": {"2009": 120, "2010": 120}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 20, "2010": 20}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 300, "2010": 300},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 150, "2010": 150},
                            "efficient": {"2009": 30, "2010": 30}}}},
                "lifetime": {
                    "baseline": {"2009": 1, "2010": 1},
                    "measure": 20}},
            ("('AIA_CZ1', 'single family home', 'electricity (grid)',"
             "'lighting', 'reflector (halogen)', 'retrofit')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 100, "2010": 100},
                        "measure": {"2009": 60, "2010": 60}},
                    "competed": {
                        "all": {"2009": 50, "2010": 50},
                        "measure": {"2009": 10, "2010": 10}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 200, "2010": 200},
                        "efficient": {"2009": 120, "2010": 120}},
                    "competed": {
                        "baseline": {"2009": 100, "2010": 100},
                        "efficient": {"2009": 20, "2010": 20}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 300, "2010": 300},
                        "efficient": {"2009": 180, "2010": 180}},
                    "competed": {
                        "baseline": {"2009": 150, "2010": 150},
                        "efficient": {"2009": 30, "2010": 30}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 200, "2010": 200},
                            "efficient": {"2009": 120, "2010": 120}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 20, "2010": 20}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 300, "2010": 300},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 150, "2010": 150},
                            "efficient": {"2009": 30, "2010": 30}}}},
                "lifetime": {
                    "baseline": {"2009": 2, "2010": 2},
                    "measure": 15}}},
        "competed choice parameters": {
            ("('AIA_CZ1', 'single family home', 'electricity (grid)',"
             "'lighting', 'reflector (incandescent)', 'retrofit')"): {
                "b1": {"2009": 0.25, "2010": 0.25},
                "b2": {"2009": 0.25, "2010": 0.25}},
            ("('AIA_CZ1', 'single family home', 'electricity (grid)',"
             "'lighting', 'reflector (halogen)', 'retrofit')"): {
                "b1": {"2009": 0.25, "2010": 0.25},
                "b2": {"2009": 0.25, "2010": 0.25}}},
        "supply-demand adjustment": {
            "savings": {},
            "total": {}},
        "savings updated": False}}

# Define sample residential cooling measure for use in tests of
# measure packaging routine below
sample_measure6 = {
    "name": "sample measure 6",
    "active": 1,
    "market_entry_year": None,
    "market_exit_year": None,
    "structure_type": ["new"],
    "climate_zone": ["AIA_CZ5"],
    "bldg_type": ["multi family home"],
    "fuel_type": {"primary": ["electricity (grid)"],
                  "secondary": None},
    "fuel_switch_to": None,
    "end_use": {"primary": ["cooling"],
                "secondary": None},
    "technology_type": {"primary": "supply",
                        "secondary": None},
    "technology": {"primary": ["ASHP"],
                   "secondary": None},
    "mseg_adjust": {
        "contributing mseg keys and values": {
            ("('AIA_CZ5', 'single family home', 'electricity (grid)',"
             "'cooling', 'supply', 'ASHP', 'new')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 1000, "2010": 1000},
                        "measure": {"2009": 600, "2010": 600}},
                    "competed": {
                        "all": {"2009": 500, "2010": 500},
                        "measure": {"2009": 100, "2010": 100}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 2000, "2010": 2000},
                        "efficient": {"2009": 1200, "2010": 1200}},
                    "competed": {
                        "baseline": {"2009": 1000, "2010": 1000},
                        "efficient": {"2009": 200, "2010": 200}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 3000, "2010": 3000},
                        "efficient": {"2009": 1800, "2010": 1800}},
                    "competed": {
                        "baseline": {"2009": 1500, "2010": 1500},
                        "efficient": {"2009": 300, "2010": 300}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 200, "2010": 200},
                            "efficient": {"2009": 120, "2010": 120}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 20, "2010": 20}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 300, "2010": 300},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 150, "2010": 150},
                            "efficient": {"2009": 30, "2010": 30}}}},
                "lifetime": {
                    "baseline": {"2009": 18, "2010": 18},
                    "measure": 18}}},
        "competed choice parameters": {
            ("('AIA_CZ5', 'single family home', 'electricity (grid)',"
             "'cooling', 'supply', 'ASHP', 'new')"): {
                "b1": {"2009": 0.75, "2010": 0.75},
                "b2": {"2009": 0.75, "2010": 0.75}}},
        "supply-demand adjustment": {
            "savings": {},
            "total": {}},
        "savings updated": False},
    "master_mseg": {
        "stock": {
            "total": {
                "all": {"2009": 1000, "2010": 1000},
                "measure": {"2009": 600, "2010": 600}},
            "competed": {
                "all": {"2009": 500, "2010": 500},
                "measure": {"2009": 100, "2010": 100}}},
        "energy": {
            "total": {
                "baseline": {"2009": 2000, "2010": 2000},
                "efficient": {"2009": 1200, "2010": 1200}},
            "competed": {
                "baseline": {"2009": 1000, "2010": 1000},
                "efficient": {"2009": 200, "2010": 200}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 3000, "2010": 3000},
                "efficient": {"2009": 1800, "2010": 1800}},
            "competed": {
                "baseline": {"2009": 1500, "2010": 1500},
                "efficient": {"2009": 300, "2010": 300}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 180, "2010": 180}},
                "competed": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 180, "2010": 180}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 200, "2010": 200},
                    "efficient": {"2009": 120, "2010": 120}},
                "competed": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 20, "2010": 20}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 300, "2010": 300},
                    "efficient": {"2009": 180, "2010": 180}},
                "competed": {
                    "baseline": {"2009": 150, "2010": 150},
                    "efficient": {"2009": 30, "2010": 30}}}},
        "lifetime": {
            "baseline": {"2009": 18, "2010": 18},
            "measure": 18}}}

# Define sample residential cooling measure for use in tests of
# measure packaging routine below
sample_measure7 = {
    "name": "sample measure 7",
    "active": 1,
    "market_entry_year": None,
    "market_exit_year": None,
    "structure_type": ["new"],
    "climate_zone": ["AIA_CZ5"],
    "bldg_type": ["multi family home"],
    "fuel_type": {"primary": ["electricity (grid)"],
                  "secondary": None},
    "fuel_switch_to": None,
    "end_use": {"primary": ["cooling"],
                "secondary": None},
    "technology_type": {"primary": ["supply"],
                        "secondary": None},
    "technology": {"primary": ["ASHP"],
                   "secondary": None},
    "mseg_adjust": {
        "contributing mseg keys and values": {
            ("('AIA_CZ5', 'single family home', 'electricity (grid)',"
             "'cooling', 'supply', 'ASHP', 'new')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 1000, "2010": 1000},
                        "measure": {"2009": 600, "2010": 600}},
                    "competed": {
                        "all": {"2009": 500, "2010": 500},
                        "measure": {"2009": 100, "2010": 100}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 2000, "2010": 2000},
                        "efficient": {"2009": 1200, "2010": 1200}},
                    "competed": {
                        "baseline": {"2009": 1000, "2010": 1000},
                        "efficient": {"2009": 200, "2010": 200}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 3000, "2010": 3000},
                        "efficient": {"2009": 1800, "2010": 1800}},
                    "competed": {
                        "baseline": {"2009": 1500, "2010": 1500},
                        "efficient": {"2009": 300, "2010": 300}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 200, "2010": 200},
                            "efficient": {"2009": 120, "2010": 120}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 20, "2010": 20}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 300, "2010": 300},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 150, "2010": 150},
                            "efficient": {"2009": 30, "2010": 30}}}},
                "lifetime": {
                    "baseline": {"2009": 18, "2010": 18},
                    "measure": 18}}},
        "competed choice parameters": {
            ("('AIA_CZ5', 'single family home', 'electricity (grid)',"
             "'cooling', 'supply', 'ASHP', 'new')"): {
                "b1": {"2009": 0.75, "2010": 0.75},
                "b2": {"2009": 0.75, "2010": 0.75}}},
        "supply-demand adjustment": {
            "savings": {},
            "total": {}},
        "savings updated": False},
    "master_mseg": {
        "stock": {
            "total": {
                "all": {"2009": 1000, "2010": 1000},
                "measure": {"2009": 600, "2010": 600}},
            "competed": {
                "all": {"2009": 500, "2010": 500},
                "measure": {"2009": 100, "2010": 100}}},
        "energy": {
            "total": {
                "baseline": {"2009": 2000, "2010": 2000},
                "efficient": {"2009": 1200, "2010": 1200}},
            "competed": {
                "baseline": {"2009": 1000, "2010": 1000},
                "efficient": {"2009": 200, "2010": 200}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 3000, "2010": 3000},
                "efficient": {"2009": 1800, "2010": 1800}},
            "competed": {
                "baseline": {"2009": 1500, "2010": 1500},
                "efficient": {"2009": 300, "2010": 300}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 180, "2010": 180}},
                "competed": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 180, "2010": 180}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 200, "2010": 200},
                    "efficient": {"2009": 120, "2010": 120}},
                "competed": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 20, "2010": 20}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 300, "2010": 300},
                    "efficient": {"2009": 180, "2010": 180}},
                "competed": {
                    "baseline": {"2009": 150, "2010": 150},
                    "efficient": {"2009": 30, "2010": 30}}}},
        "lifetime": {
            "baseline": {"2009": 18, "2010": 18},
            "measure": 18}}}


class CommonMethods(object):
    """ Define common methods for use in all tests below """

    # Create a routine for checking equality of a dict with point vals
    def dict_check(self, dict1, dict2, msg=None):
        for (k, i), (k2, i2) in zip(sorted(dict1.items()),
                                    sorted(dict2.items())):
            if isinstance(i, dict):
                self.assertCountEqual(i, i2)
                self.dict_check(i, i2)
            else:
                self.assertAlmostEqual(dict1[k], dict2[k2], places=2)

    # Create a routine for checking equality of a dict with list vals
    def dict_check_list(self, dict1, dict2, msg=None):
        for (k, i), (k2, i2) in zip(sorted(dict1.items()),
                                    sorted(dict2.items())):
            if isinstance(i, dict):
                self.assertCountEqual(i, i2)
                self.dict_check_list(i, i2)
            else:
                # Expect numpy arrays and/or point values
                if type(i) == numpy.ndarray:
                    # Additional check for dict elements in the numpy
                    # array is needed to accomodate the current structure
                    # of measure Annualized Net Present Value information
                    # when distributions are placed on measure inputs
                    # (see ok_out_dist test dicts in PrioritizationMetricsTest
                    # below)
                    if isinstance(i[0], dict):
                        for ind in range(0, len(i)):
                            self.assertCountEqual(i[ind], i2[ind])
                            self.dict_check_list(i[ind], i2[ind])
                    else:
                        numpy.testing.assert_array_almost_equal(
                            i, i2, decimal=2)
                else:
                    self.assertAlmostEqual(dict1[k], dict2[k2],
                                           places=2)


class TestMeasureInit(unittest.TestCase):
    """ Ensure that measure attributes are correctly initiated """

    def test_attributes(self):
        # Create an instance of the object using sample_measure
        measure_instance = run.Measure(**sample_measure)
        # Put object attributes into a dict
        attribute_dict = measure_instance.__dict__
        # Loop through sample measure keys and compare key values
        # to those from the "attribute_dict"
        for key in sample_measure.keys():
            self.assertEqual(attribute_dict[key],
                             sample_measure[key])


class AddKeyValsTest(unittest.TestCase, CommonMethods):
    """ Test the operation of the add_keyvals function to verify it
    adds together dict items correctly """

    # Create a measure instance to use in the testing
    measure_instance = run.Measure(**sample_measure)

    # 1st dict to be entered into the "ok" test of the function
    base_dict1 = {"level 1a":
                  {"level 2aa":
                      {"2009": 2, "2010": 3},
                   "level2ab":
                      {"2009": 4, "2010": 5}},
                  "level 1b":
                  {"level 2ba":
                      {"2009": 6, "2010": 7},
                   "level2bb":
                      {"2009": 8, "2010": 9}}}

    # 1st dict to be entered into the "fail" test of the function
    base_dict2 = copy.deepcopy(base_dict1)

    # 2nd dict to be added to "base_dict1" in the "ok" test of the function
    ok_add_dict2 = {"level 1a":
                    {"level 2aa":
                        {"2009": 2, "2010": 3},
                     "level2ab":
                        {"2009": 4, "2010": 5}},
                    "level 1b":
                    {"level 2ba":
                        {"2009": 6, "2010": 7},
                     "level2bb":
                        {"2009": 8, "2010": 9}}}

    # 2nd dict to be added to "base_dict2" in the "fail" test of the function
    fail_add_dict2 = {"level 1a":
                      {"level 2aa":
                          {"2009": 2, "2010": 3},
                       "level2ab":
                          {"2009": 4, "2010": 5}},
                      "level 1b":
                      {"level 2ba":
                          {"2009": 6, "2010": 7},
                       "level2bb":
                          {"2009": 8, "2011": 9}}}

    # Correct output of the "ok" test to check against
    ok_out = {"level 1a":
              {"level 2aa":
                  {"2009": 4, "2010": 6},
               "level2ab":
                  {"2009": 8, "2010": 10}},
              "level 1b":
              {"level 2ba":
                  {"2009": 12, "2010": 14},
               "level2bb":
                  {"2009": 16, "2010": 18}}}

    # Test the "ok" function output
    def test_ok_add(self):
        dict1 = self.measure_instance.add_keyvals(self.base_dict1,
                                                  self.ok_add_dict2)
        dict2 = self.ok_out
        self.dict_check(dict1, dict2)

    # Test the "fail" function output
    def test_fail_add(self):
        with self.assertRaises(KeyError):
            self.measure_instance.add_keyvals(self.base_dict2,
                                              self.fail_add_dict2)


class ReduceSqftStockCostTest(unittest.TestCase, CommonMethods):
    """ Test the operation of the reduce_sqft function to verify
    that it properly divides dict key values by a given factor (used in special
    case where square footage is used as the microsegment stock) """

    # Create a measure instance to use in the testing
    measure_instance = run.Measure(**sample_measure)

    # Initialize a factor to divide input dict key values by
    test_factor = 4

    # Base input dict to be divided by test_factor in "ok" test
    base_dict = {"stock":
                 {"total":
                     {"2009": 100, "2010": 200},
                  "competed":
                      {"2009": 300, "2010": 400}},
                 "energy":
                 {"total":
                     {"2009": 500, "2010": 600},
                  "competed":
                     {"2009": 700, "2010": 800},
                  "efficient":
                     {"2009": 700, "2010": 800}},
                 "carbon":
                 {"total":
                     {"2009": 500, "2010": 600},
                  "competed":
                     {"2009": 700, "2010": 800},
                  "efficient":
                     {"2009": 700, "2010": 800}},
                 "cost":
                 {"baseline": {
                     "stock": {"2009": 900, "2010": 1000},
                     "energy": {"2009": 900, "2010": 1000},
                     "carbon": {"2009": 900, "2010": 1000}},
                  "measure": {
                     "stock": {"2009": 1100, "2010": 1200},
                     "energy": {"2009": 1100, "2010": 1200},
                     "carbon": {"2009": 1100, "2010": 1200}}}}

    # Correct output of the "ok" test to check against
    ok_out = {"stock":
              {"total":
                  {"2009": 25, "2010": 50},
               "competed":
                   {"2009": 75, "2010": 100}},
              "energy":
              {"total":
                  {"2009": 500, "2010": 600},
               "competed":
                  {"2009": 700, "2010": 800},
               "efficient":
                  {"2009": 700, "2010": 800}},
              "carbon":
              {"total":
                   {"2009": 500, "2010": 600},
               "competed":
                   {"2009": 700, "2010": 800},
               "efficient":
                   {"2009": 700, "2010": 800}},
              "cost":
              {"baseline": {
                  "stock": {"2009": 225, "2010": 250},
                  "energy": {"2009": 900, "2010": 1000},
                  "carbon": {"2009": 900, "2010": 1000}},
               "measure": {
                  "stock": {"2009": 275, "2010": 300},
                  "energy": {"2009": 1100, "2010": 1200},
                  "carbon": {"2009": 1100, "2010": 1200}}}}

    # Test the "ok" function output
    def test_ok_add(self):
        dict1 = self.measure_instance.reduce_sqft(self.base_dict,
                                                  self.test_factor)
        dict2 = self.ok_out
        self.dict_check(dict1, dict2)


# NOT SURE WE NEED THIS TEST

# class RandomSampleTest(unittest.TestCase):
#     """ Test that the "rand_list_gen" yields an output
#     list of sampled values that are correctly distributed """

#     # Create a measure instance to use in the testing
#     measure_instance = run.Measure(**sample_measure)

#     # Set test sampling number
#     test_sample_n = 100

#     # Set of input distribution information that should
#     # yield valid outputs
#     test_ok_in = [["normal", 10, 2], ["weibull", 5, 8],
#                   ["triangular", 3, 7, 10]]

#     # Set of input distribution information that should
#     # yield value errors
#     test_fail_in = [[1, 10, 2], ["triangle", 5, 8, 10],
#                     ["triangular", 3, 7]]

#     # Calls to the scipy fit function that will be used
#     # to check for correct fitted distribution parameters
#     # for sampled values
#     test_fit_calls = ['ss.norm.fit(sample)',
#                       'ss.weibull_min.fit(sample, floc = 0)',
#                       'ss.triang.fit(sample)']

#     # Correct set of outputs for given random sampling seed
#     test_outputs = [numpy.array([10.06, 2.03]),
#                     numpy.array([4.93, 0, 8.02]),
#                     numpy.array([0.51, 3.01, 7.25])]

#     # Test for correct output from "ok" input distribution info.
#     def test_distrib_ok(self):
#         # Seed random number generator to yield repeatable results
#         numpy.random.seed(5423)
#         for idx in range(0, len(self.test_ok_in)):
#             # Sample values based on distribution input info.
#             sample = self.measure_instance.rand_list_gen(self.test_ok_in[idx],
#                                                          self.test_sample_n)
#             # Fit parameters for sampled values and check against
#             # known correct parameter values in "test_outputs" * NOTE:
#             # this adds ~ 0.15 s to test computation
#             for elem in range(0, len(self.test_outputs[idx])):
#                 with numpy.errstate(divide='ignore'):  # Warning for triang
#                     self.assertAlmostEqual(
#                         list(eval(self.test_fit_calls[idx]))[elem],
#                         self.test_outputs[idx][elem], 2)

#     # Test for correct output from "fail" input distribution info.
#     def test_distrib_fail(self):
#         for idx in range(0, len(self.test_fail_in)):
#             with self.assertRaises(ValueError):
#                 self.measure_instance.rand_list_gen(
#                     self.test_fail_in[idx], self.test_sample_n)

class CreateKeyChainTest(unittest.TestCase, CommonMethods):
    """ Test the operation of the create_keychain function to verify that
    it yields proper key chain output given input microsegment information """

    # Create a measure instance to use in the testing
    measure_instance = run.Measure(**sample_measure2)

    # Correct key chain output (primary microsegment)
    ok_out_primary = [('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'heating', 'supply',
                       'boiler (electric)', 'new'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'ASHP',
                       'new'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'GSHP',
                       'new'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'room AC',
                       'new'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'cooling', 'supply',
                       'boiler (electric)', 'new'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'ASHP',
                       'new'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'GSHP',
                       'new'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'room AC',
                       'new'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'heating', 'supply',
                       'boiler (electric)', 'new'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'ASHP',
                       'new'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'GSHP',
                       'new'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'room AC',
                       'new'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'cooling', 'supply',
                       'boiler (electric)', 'new'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'ASHP',
                       'new'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'GSHP',
                       'new'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'room AC',
                       'new'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'heating', 'supply',
                       'boiler (electric)', 'retrofit'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'ASHP',
                       'retrofit'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'GSHP',
                       'retrofit'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'room AC',
                       'retrofit'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'cooling', 'supply',
                       'boiler (electric)', 'retrofit'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'ASHP',
                       'retrofit'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'GSHP',
                       'retrofit'),
                      ('primary', 'AIA_CZ1', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'room AC',
                       'retrofit'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'heating', 'supply',
                       'boiler (electric)', 'retrofit'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'ASHP',
                       'retrofit'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'GSHP',
                       'retrofit'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'heating', 'supply', 'room AC',
                       'retrofit'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'cooling', 'supply',
                       'boiler (electric)', 'retrofit'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'ASHP',
                       'retrofit'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'GSHP',
                       'retrofit'),
                      ('primary', 'AIA_CZ2', 'single family home',
                       'electricity (grid)', 'cooling', 'supply', 'room AC',
                       'retrofit')]

    # Correct key chain output (secondary microsegment)
    ok_out_secondary = [('secondary', 'AIA_CZ1', 'single family home',
                         'electricity (grid)', 'lighting',
                         'general service (LED)', 'new'),
                        ('secondary', 'AIA_CZ2', 'single family home',
                         'electricity (grid)', 'lighting',
                         'general service (LED)', 'new'),
                        ('secondary', 'AIA_CZ1', 'single family home',
                         'electricity (grid)', 'lighting',
                         'general service (LED)', 'retrofit'),
                        ('secondary', 'AIA_CZ2', 'single family home',
                         'electricity (grid)', 'lighting',
                         'general service (LED)', 'retrofit')]

    # Test the generation of a list of primary mseg key chains
    def test_primary(self):
        self.assertEqual(
            self.measure_instance.create_keychain("primary")[0],
            self.ok_out_primary)

    # Test the generation of a list of secondary mseg key chains
    def test_secondary(self):
        self.assertEqual(
            self.measure_instance.create_keychain("secondary")[0],
            self.ok_out_secondary)


class PartitionMicrosegmentTest(unittest.TestCase, CommonMethods):
    """ Test the operation of the partition_microsegment function to verify
    that it properly partitions an input microsegment to yield the required
    competed stock/energy/cost and energy efficient consumption information """

    # Create a measure instance to use in the testing
    measure_instance = run.Measure(**sample_measure)

    # Set sample stock and energy inputs for testing
    test_stock = [{"2009": 100, "2010": 200, "2011": 300},
                  {"2025": 400, "2026": 500, "2027": 600},
                  {"2020": 700, "2021": 800, "2022": 900}]
    test_energy = [{"2009": 10, "2010": 20, "2011": 30},
                   {"2025": 40, "2026": 50, "2027": 60},
                   {"2020": 70, "2021": 80, "2022": 90}]
    test_carb = [{"2009": 30, "2010": 60, "2011": 90},
                 {"2025": 120, "2026": 150, "2027": 180},
                 {"2020": 210, "2021": 240, "2022": 270}]

    # Set sample base and measure costs to use in the testing
    test_base_cost = [{"2009": 10, "2010": 10, "2011": 10},
                      {"2025": 20, "2026": 20, "2027": 20},
                      {"2020": 30, "2021": 30, "2022": 30}]
    test_cost_meas = [20, 30, 40]

    # Set sample energy costs for baseline and measure fuel
    cost_energy_base, cost_energy_meas = \
        (numpy.array((b'Test', 1, 2, 2, 2, 2, 2, 2, 2, 2),
                     dtype=[('Category', 'S11'), ('2009', '<f8'),
                            ('2010', '<f8'), ('2011', '<f8'),
                            ('2020', '<f8'), ('2021', '<f8'),
                            ('2022', '<f8'), ('2025', '<f8'),
                            ('2026', '<f8'), ('2027', '<f8')])
         for n in range(2))
    # Set sample carbon costs
    cost_carbon = numpy.array((b'Test', 1, 4, 1, 1, 1, 1, 1, 1, 3),
                              dtype=[('Category', 'S11'), ('2009', '<f8'),
                                     ('2010', '<f8'), ('2011', '<f8'),
                                     ('2020', '<f8'), ('2021', '<f8'),
                                     ('2022', '<f8'), ('2025', '<f8'),
                                     ('2026', '<f8'), ('2027', '<f8')])

    # Set sample site to source conversions for baseline and measure fuel
    site_source_conv_base, site_source_conv_meas = \
        (numpy.array((b'Test', 1, 1, 1, 1, 1, 1, 1, 1, 1),
                     dtype=[('Category', 'S11'), ('2009', '<f8'),
                            ('2010', '<f8'), ('2011', '<f8'),
                            ('2020', '<f8'), ('2021', '<f8'),
                            ('2022', '<f8'), ('2025', '<f8'),
                            ('2026', '<f8'), ('2027', '<f8')])
         for n in range(2))

    # Set sample carbon intensities for baseline and measure fuel
    intensity_carb_base, intensity_carb_meas = \
        (numpy.array((b'Test', 1, 1, 1, 1, 1, 1, 1, 1, 1),
                     dtype=[('Category', 'S11'), ('2009', '<f8'),
                            ('2010', '<f8'), ('2011', '<f8'),
                            ('2020', '<f8'), ('2021', '<f8'),
                            ('2022', '<f8'), ('2025', '<f8'),
                            ('2026', '<f8'), ('2027', '<f8')])
         for n in range(2))

    # Set both 'Technical potential' and 'Max adoption potential' test
    # scenarios
    test_schemes = ['Technical potential', 'Max adoption potential']

    # Establish the fraction of buildings that are newly constructed annually
    # and cumulatively since the beginning of the modeling time horizon
    new_bldg_frac = [{
        "added": {"2009": 0.1, "2010": 0.05, "2011": 0.1},
        "total": {"2009": 0.1, "2010": 0.15, "2011": 0.25}},
        {"added": {"2025": 0.1, "2026": 0.05, "2027": 0.1},
         "total": {"2025": 0.1, "2026": 0.15, "2027": 0.25}},
        {"added": {"2020": 0.1, "2021": 0.95, "2022": 0.1},
         "total": {"2020": 0.1, "2021": 1, "2022": 1}}]

    # Set a relative performance list that should yield a
    # full list of valid outputs
    ok_relperf = [{"2009": 0.30, "2010": 0.30, "2011": 0.30},
                  {"2025": 0.15, "2026": 0.15, "2027": 0.15},
                  {"2020": 0.75, "2021": 0.75, "2022": 0.75}]

    # Set placeholder for technology diffusion parameters (currently blank)
    diffuse_params = None

    # Set the lifetime of the sample measure to be tested and the
    # comparable baseline technology (for stock and flow calculations in the
    # 'Max adoption potential' scenario)
    life_meas = 10
    life_base = {"2009": 10, "2010": 10, "2011": 10,
                 "2020": 10, "2021": 10, "2022": 10,
                 "2025": 10, "2026": 10, "2027": 10}

    # Set dict key chains associated with the sample measure microsegment
    # being updated. This is needed to determine whether the microsegment
    # is primary or secondary (where the latter could reflect,
    # for example, the heating/cooling energy impacts of a lighting efficiency
    # measure); it also determines whether the microsegment applies to
    # new building structure types or retrofit building structure types
    mskeys = [('primary', 'AIA_CZ1', 'single family home',
               'electricity (grid)', 'heating', 'supply', 'boiler (electric)',
               'new'),
              ('primary', 'AIA_CZ1', 'single family home',
               'electricity (grid)', 'heating', 'supply', 'boiler (electric)',
               'retrofit')]

    # Correct output of the "ok" function test
    ok_out = [
        [[[
            {"2009": 100, "2010": 200, "2011": 300},
            {"2009": 3, "2010": 6, "2011": 9},
            {"2009": 9, "2010": 18, "2011": 27},
            {"2009": 100, "2010": 200, "2011": 300},
            {"2009": 10, "2010": 20, "2011": 30},
            {"2009": 30, "2010": 60, "2011": 90},
            {"2009": 100, "2010": 200, "2011": 300},
            {"2009": 3, "2010": 6, "2011": 9},
            {"2009": 9, "2010": 18, "2011": 27},
            {"2009": 1000, "2010": 2000, "2011": 3000},
            {"2009": 10, "2010": 40, "2011": 60},
            {"2009": 30, "2010": 240, "2011": 90},
            {"2009": 2000, "2010": 4000, "2011": 6000},
            {"2009": 3, "2010": 12, "2011": 18},
            {"2009": 9, "2010": 72, "2011": 27},
            {"2009": 1000, "2010": 2000, "2011": 3000},
            {"2009": 10, "2010": 40, "2011": 60},
            {"2009": 30, "2010": 240, "2011": 90},
            {"2009": 2000, "2010": 4000, "2011": 6000},
            {"2009": 3, "2010": 12, "2011": 18},
            {"2009": 9, "2010": 72, "2011": 27}],
            [
            {"2009": 100, "2010": 200, "2011": 300},
            {"2009": 3, "2010": 6, "2011": 9},
            {"2009": 9, "2010": 18, "2011": 27},
            {"2009": 100, "2010": 200, "2011": 300},
            {"2009": 10, "2010": 20, "2011": 30},
            {"2009": 30, "2010": 60, "2011": 90},
            {"2009": 100, "2010": 200, "2011": 300},
            {"2009": 3, "2010": 6, "2011": 9},
            {"2009": 9, "2010": 18, "2011": 27},
            {"2009": 1000, "2010": 2000, "2011": 3000},
            {"2009": 10, "2010": 40, "2011": 60},
            {"2009": 30, "2010": 240, "2011": 90},
            {"2009": 2000, "2010": 4000, "2011": 6000},
            {"2009": 3, "2010": 12, "2011": 18},
            {"2009": 9, "2010": 72, "2011": 27},
            {"2009": 1000, "2010": 2000, "2011": 3000},
            {"2009": 10, "2010": 40, "2011": 60},
            {"2009": 30, "2010": 240, "2011": 90},
            {"2009": 2000, "2010": 4000, "2011": 6000},
            {"2009": 3, "2010": 12, "2011": 18},
            {"2009": 9, "2010": 72, "2011": 27}]],
         [[
             {"2009": 100, "2010": 166.67, "2011": 286.67},
             {"2009": 3, "2010": 6, "2011": 9},
             {"2009": 9, "2010": 18, "2011": 27},
             {"2009": 100, "2010": 66.67, "2011": 120},
             {"2009": 10, "2010": 6.67, "2011": 12},
             {"2009": 30, "2010": 20, "2011": 36},
             {"2009": 100, "2010": 66.67, "2011": 120},
             {"2009": 3, "2010": 2, "2011": 3.6},
             {"2009": 9, "2010": 6, "2011": 10.8},
             {"2009": 1000, "2010": 2000, "2011": 3000},
             {"2009": 10, "2010": 40, "2011": 60},
             {"2009": 30, "2010": 240, "2011": 90},
             {"2009": 2000, "2010": 3666.67, "2011": 5866.67},
             {"2009": 3, "2010": 12, "2011": 18},
             {"2009": 9, "2010": 72, "2011": 27},
             {"2009": 1000, "2010": 666.67, "2011": 1200},
             {"2009": 10, "2010": 13.33, "2011": 24},
             {"2009": 30, "2010": 80, "2011": 36},
             {"2009": 2000, "2010": 1333.33, "2011": 2400},
             {"2009": 3, "2010": 4, "2011": 7.2},
             {"2009": 9, "2010": 24, "2011": 10.8}],
             [
             {"2009": 10, "2010": 30, "2011": 60},
             {"2009": 9.3, "2010": 17.34, "2011": 25.06},
             {"2009": 27.9, "2010": 52.02, "2011": 75.19},
             {"2009": 10, "2010": 20, "2011": 30},
             {"2009": 1, "2010": 2, "2011": 3},
             {"2009": 3, "2010": 6, "2011": 9},
             {"2009": 10, "2010": 20, "2011": 30},
             {"2009": 0.3, "2010": 0.6, "2011": 0.9},
             {"2009": 0.9, "2010": 1.8, "2011": 2.7},
             {"2009": 1000, "2010": 2000, "2011": 3000},
             {"2009": 10, "2010": 40, "2011": 60},
             {"2009": 30, "2010": 240, "2011": 90},
             {"2009": 1100, "2010": 2300, "2011": 3600},
             {"2009": 9.3, "2010": 34.68, "2011": 50.13},
             {"2009": 27.9, "2010": 208.08, "2011": 75.19},
             {"2009": 100, "2010": 200, "2011": 300},
             {"2009": 1, "2010": 4, "2011": 6},
             {"2009": 3, "2010": 24, "2011": 9},
             {"2009": 200, "2010": 400, "2011": 600},
             {"2009": 0.3, "2010": 1.2, "2011": 1.8},
             {"2009": 0.9, "2010": 7.2, "2011": 2.7}]]],
        [[[
            {"2025": 400, "2026": 500, "2027": 600},
            {"2025": 6, "2026": 7.5, "2027": 9},
            {"2025": 18, "2026": 22.5, "2027": 27},
            {"2025": 400, "2026": 500, "2027": 600},
            {"2025": 40, "2026": 50, "2027": 60},
            {"2025": 120, "2026": 150, "2027": 180},
            {"2025": 400, "2026": 500, "2027": 600},
            {"2025": 6, "2026": 7.5, "2027": 9},
            {"2025": 18, "2026": 22.5, "2027": 27},
            {"2025": 8000, "2026": 10000, "2027": 12000},
            {"2025": 80, "2026": 100, "2027": 120},
            {"2025": 120, "2026": 150, "2027": 540},
            {"2025": 12000, "2026": 15000, "2027": 18000},
            {"2025": 12, "2026": 15, "2027": 18},
            {"2025": 18, "2026": 22.5, "2027": 81},
            {"2025": 8000, "2026": 10000, "2027": 12000},
            {"2025": 80, "2026": 100, "2027": 120},
            {"2025": 120, "2026": 150, "2027": 540},
            {"2025": 12000, "2026": 15000, "2027": 18000},
            {"2025": 12, "2026": 15, "2027": 18},
            {"2025": 18, "2026": 22.5, "2027": 81}],
            [
            {"2025": 400, "2026": 500, "2027": 600},
            {"2025": 6, "2026": 7.5, "2027": 9},
            {"2025": 18, "2026": 22.5, "2027": 27},
            {"2025": 400, "2026": 500, "2027": 600},
            {"2025": 40, "2026": 50, "2027": 60},
            {"2025": 120, "2026": 150, "2027": 180},
            {"2025": 400, "2026": 500, "2027": 600},
            {"2025": 6, "2026": 7.5, "2027": 9},
            {"2025": 18, "2026": 22.5, "2027": 27},
            {"2025": 8000, "2026": 10000, "2027": 12000},
            {"2025": 80, "2026": 100, "2027": 120},
            {"2025": 120, "2026": 150, "2027": 540},
            {"2025": 12000, "2026": 15000, "2027": 18000},
            {"2025": 12, "2026": 15, "2027": 18},
            {"2025": 18, "2026": 22.5, "2027": 81},
            {"2025": 8000, "2026": 10000, "2027": 12000},
            {"2025": 80, "2026": 100, "2027": 120},
            {"2025": 120, "2026": 150, "2027": 540},
            {"2025": 12000, "2026": 15000, "2027": 18000},
            {"2025": 12, "2026": 15, "2027": 18},
            {"2025": 18, "2026": 22.5, "2027": 81}]],
         [[
             {"2025": 400, "2026": 500, "2027": 600},
             {"2025": 6, "2026": 7.5, "2027": 9},
             {"2025": 18, "2026": 22.5, "2027": 27},
             {"2025": 400, "2026": 166.67, "2027": 240},
             {"2025": 40, "2026": 16.67, "2027": 24},
             {"2025": 120, "2026": 50, "2027": 72},
             {"2025": 400, "2026": 166.67, "2027": 240},
             {"2025": 6, "2026": 2.5, "2027": 3.6},
             {"2025": 18, "2026": 7.5, "2027": 10.8},
             {"2025": 8000, "2026": 10000, "2027": 12000},
             {"2025": 80, "2026": 100, "2027": 120},
             {"2025": 120, "2026": 150, "2027": 540},
             {"2025": 12000, "2026": 15000, "2027": 18000},
             {"2025": 12, "2026": 15, "2027": 18},
             {"2025": 18, "2026": 22.5, "2027": 81},
             {"2025": 8000, "2026": 3333.33, "2027": 4800},
             {"2025": 80, "2026": 33.33, "2027": 48},
             {"2025": 120, "2026": 50, "2027": 216},
             {"2025": 12000, "2026": 5000, "2027": 7200},
             {"2025": 12, "2026": 5, "2027": 7.2},
             {"2025": 18, "2026": 7.5, "2027": 32.4}],
             [
             {"2025": 40, "2026": 90, "2027": 150},
             {"2025": 36.6, "2026": 41.92, "2027": 46.64},
             {"2025": 109.8, "2026": 125.78, "2027": 139.91},
             {"2025": 40, "2026": 50, "2027": 60},
             {"2025": 4, "2026": 5, "2027": 6},
             {"2025": 12, "2026": 15, "2027": 18},
             {"2025": 40, "2026": 50, "2027": 60},
             {"2025": 0.60, "2026": 0.75, "2027": 0.90},
             {"2025": 1.8, "2026": 2.25, "2027": 2.7},
             {"2025": 8000, "2026": 10000, "2027": 12000},
             {"2025": 80, "2026": 100, "2027": 120},
             {"2025": 120, "2026": 150, "2027": 540},
             {"2025": 8400, "2026": 10900, "2027": 13500},
             {"2025": 73.2, "2026": 83.85, "2027": 93.28},
             {"2025": 109.8, "2026": 125.78, "2027": 419.74},
             {"2025": 800, "2026": 1000, "2027": 1200},
             {"2025": 8, "2026": 10, "2027": 12},
             {"2025": 12, "2026": 15, "2027": 54},
             {"2025": 1200, "2026": 1500, "2027": 1800},
             {"2025": 1.2, "2026": 1.5, "2027": 1.8},
             {"2025": 1.8, "2026": 2.25, "2027": 8.1}]]],
        [[[
            {"2020": 700, "2021": 800, "2022": 900},
            {"2020": 52.5, "2021": 60, "2022": 67.5},
            {"2020": 157.5, "2021": 180, "2022": 202.5},
            {"2020": 700, "2021": 800, "2022": 900},
            {"2020": 70, "2021": 80, "2022": 90},
            {"2020": 210, "2021": 240, "2022": 270},
            {"2020": 700, "2021": 800, "2022": 900},
            {"2020": 52.5, "2021": 60, "2022": 67.5},
            {"2020": 157.5, "2021": 180, "2022": 202.5},
            {"2020": 21000, "2021": 24000, "2022": 27000},
            {"2020": 140, "2021": 160, "2022": 180},
            {"2020": 210, "2021": 240, "2022": 270},
            {"2020": 28000, "2021": 32000, "2022": 36000},
            {"2020": 105, "2021": 120, "2022": 135},
            {"2020": 157.5, "2021": 180, "2022": 202.5},
            {"2020": 21000, "2021": 24000, "2022": 27000},
            {"2020": 140, "2021": 160, "2022": 180},
            {"2020": 210, "2021": 240, "2022": 270},
            {"2020": 28000, "2021": 32000, "2022": 36000},
            {"2020": 105, "2021": 120, "2022": 135},
            {"2020": 157.5, "2021": 180, "2022": 202.5}],
            [
            {"2020": 700, "2021": 800, "2022": 900},
            {"2020": 52.5, "2021": 60, "2022": 67.5},
            {"2020": 157.5, "2021": 180, "2022": 202.5},
            {"2020": 700, "2021": 800, "2022": 900},
            {"2020": 70, "2021": 80, "2022": 90},
            {"2020": 210, "2021": 240, "2022": 270},
            {"2020": 700, "2021": 800, "2022": 900},
            {"2020": 52.5, "2021": 60, "2022": 67.5},
            {"2020": 157.5, "2021": 180, "2022": 202.5},
            {"2020": 21000, "2021": 24000, "2022": 27000},
            {"2020": 140, "2021": 160, "2022": 180},
            {"2020": 210, "2021": 240, "2022": 270},
            {"2020": 28000, "2021": 32000, "2022": 36000},
            {"2020": 105, "2021": 120, "2022": 135},
            {"2020": 157.5, "2021": 180, "2022": 202.5},
            {"2020": 21000, "2021": 24000, "2022": 27000},
            {"2020": 140, "2021": 160, "2022": 180},
            {"2020": 210, "2021": 240, "2022": 270},
            {"2020": 28000, "2021": 32000, "2022": 36000},
            {"2020": 105, "2021": 120, "2022": 135},
            {"2020": 157.5, "2021": 180, "2022": 202.5}]],
         [[
             {"2020": 700, "2021": 800, "2022": 890},
             {"2020": 52.5, "2021": 60, "2022": 67.5},
             {"2020": 157.5, "2021": 180.0, "2022": 202.5},
             {"2020": 700, "2021": 760, "2022": 90},
             {"2020": 70, "2021": 76, "2022": 9},
             {"2020": 210, "2021": 228, "2022": 27},
             {"2020": 700, "2021": 760, "2022": 90},
             {"2020": 52.50, "2021": 57.00, "2022": 6.75},
             {"2020": 157.50, "2021": 171.0, "2022": 20.25},
             {"2020": 21000, "2021": 24000, "2022": 27000},
             {"2020": 140, "2021": 160, "2022": 180},
             {"2020": 210, "2021": 240, "2022": 270},
             {"2020": 28000, "2021": 32000, "2022": 35900},
             {"2020": 105, "2021": 120, "2022": 135},
             {"2020": 157.5, "2021": 180.0, "2022": 202.5},
             {"2020": 21000, "2021": 22800, "2022": 2700},
             {"2020": 140, "2021": 152, "2022": 18.0},
             {"2020": 210, "2021": 228, "2022": 27.0},
             {"2020": 28000, "2021": 30400, "2022": 3600},
             {"2020": 105.0, "2021": 114.0, "2022": 13.5},
             {"2020": 157.50, "2021": 171.00, "2022": 20.25}],
             [
             {"2020": 70, "2021": 150, "2022": 240},
             {"2020": 68.25, "2021": 76.2, "2022": 83.95},
             {"2020": 204.75, "2021": 228.6, "2022": 251.86},
             {"2020": 70, "2021": 80, "2022": 90},
             {"2020": 7, "2021": 8, "2022": 9},
             {"2020": 21, "2021": 24, "2022": 27},
             {"2020": 70, "2021": 80, "2022": 90},
             {"2020": 5.25, "2021": 6.00, "2022": 6.75},
             {"2020": 15.75, "2021": 18.00, "2022": 20.25},
             {"2020": 21000, "2021": 24000, "2022": 27000},
             {"2020": 140, "2021": 160, "2022": 180},
             {"2020": 210, "2021": 240, "2022": 270},
             {"2020": 21700, "2021": 25500, "2022": 29400},
             {"2020": 136.5, "2021": 152.4, "2022": 167.91},
             {"2020": 204.75, "2021": 228.6, "2022": 251.86},
             {"2020": 2100, "2021": 2400, "2022": 2700},
             {"2020": 14, "2021": 16, "2022": 18},
             {"2020": 21, "2021": 24, "2022": 27},
             {"2020": 2800, "2021": 3200, "2022": 3600},
             {"2020": 10.5, "2021": 12.0, "2022": 13.5},
             {"2020": 15.75, "2021": 18.00, "2022": 20.25}]]]]

    # Test the function output against 'ok_out' above
    def test_ok(self):
        # Loop through 'ok_out' elements
        for elem in range(0, len(self.ok_out)):
            # Loop through two test schemes (Technical potential and Max
            # adoption potential)
            for scn in range(0, len(self.test_schemes)):
                # Loop through two microsegment key chains (one applying
                # to new structure type, another to retrofit structure type)
                for k in range(0, len(self.mskeys)):
                    # List of output dicts generated by the function
                    lists1 = self.measure_instance.partition_microsegment(
                        self.test_stock[elem],
                        self.test_energy[elem],
                        self.test_carb[elem],
                        self.ok_relperf[elem],
                        self.test_base_cost[elem],
                        self.test_cost_meas[elem],
                        self.cost_energy_base,
                        self.cost_energy_meas,
                        self.cost_carbon,
                        self.site_source_conv_base,
                        self.site_source_conv_meas,
                        self.intensity_carb_base,
                        self.intensity_carb_meas,
                        self.new_bldg_frac[elem],
                        self.diffuse_params,
                        self.test_schemes[scn],
                        self.life_base,
                        self.life_meas,
                        self.mskeys[k])
                    # Correct list of output dicts
                    lists2 = self.ok_out[elem][scn][k]
                    # Compare the lists of output dicts
                    for elem2 in range(0, len(lists1)):
                        self.dict_check(lists1[elem2], lists2[elem2])


class FindPartitionMasterMicrosegmentTest(unittest.TestCase, CommonMethods):
    """ Test the operation of the mseg_find_partition function to
    verify measure microsegment-related attribute inputs yield expected master
    microsegment output """

    # Sample input dict of microsegment performance/cost info. to reference in
    # generating and partitioning master microsegments for a measure
    sample_basein = {
        "AIA_CZ1": {
            "assembly": {
                "electricity (grid)": {
                    "heating": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 10, "2010": 10},
                                    "range": {"2009": 1, "2010": 1},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "lights": {
                                "performance": {
                                    "typical": 0,
                                    "best": 0,
                                    "units": "NA",
                                    "source":
                                    "NA"},
                                "installed cost": {
                                    "typical": 0,
                                    "best": 0,
                                    "units": "NA",
                                    "source": "NA"},
                                "lifetime": {
                                    "average": 0,
                                    "range": 0,
                                    "units": "NA",
                                    "source": "NA"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "secondary heating": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 10, "2010": 10},
                                    "range": {"2009": 1, "2010": 1},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "lights": {
                                "performance": {
                                    "typical": 0,
                                    "best": 0,
                                    "units": "NA",
                                    "source":
                                    "NA"},
                                "installed cost": {
                                    "typical": 0,
                                    "best": 0,
                                    "units": "NA",
                                    "source": "NA"},
                                "lifetime": {
                                    "average": 0,
                                    "range": 0,
                                    "units": "NA",
                                    "source": "NA"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "cooling": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 10, "2010": 10},
                                    "range": {"2009": 1, "2010": 1},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "lights": {
                                "performance": {
                                    "typical": 0,
                                    "best": 0,
                                    "units": "NA",
                                    "source":
                                    "NA"},
                                "installed cost": {
                                    "typical": 0,
                                    "best": 0,
                                    "units": "NA",
                                    "source": "NA"},
                                "lifetime": {
                                    "average": 0,
                                    "range": 0,
                                    "units": "NA",
                                    "source": "NA"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "lighting": {
                        "commercial light type X": {
                            "performance": {
                                "typical": {"2009": 14, "2010": 14},
                                "best": {"2009": 14, "2010": 14},
                                "units": "lm/W",
                                "source":
                                "EIA AEO"},
                            "installed cost": {
                                "typical": {"2009": 14, "2010": 14},
                                "best": {"2009": 14, "2010": 14},
                                "units": "2014$/unit",
                                "source": "EIA AEO"},
                            "lifetime": {
                                "average": {"2009": 140, "2010": 140},
                                "range": {"2009": 14, "2010": 14},
                                "units": "years",
                                "source": "EIA AEO"},
                            "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}}},
            "single family home": {
                "electricity (grid)": {
                    "heating": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 10, "2010": 10},
                                    "range": {"2009": 1, "2010": 1},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "infiltration": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 3},
                                    "best": {"2009": 2, "2010": 3},
                                    "units": "ACH50",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}},
                        "supply": {
                            "boiler (electric)": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "ASHP": {
                                "performance": {
                                    "typical": {"2009": 3, "2010": 3},
                                    "best": {"2009": 3, "2010": 3},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 3, "2010": 3},
                                    "best": {"2009": 3, "2010": 3},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 30, "2010": 30},
                                    "range": {"2009": 3, "2010": 3},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "GSHP": {
                                "performance": {
                                    "typical": {"2009": 4, "2010": 4},
                                    "best": {"2009": 4, "2010": 4},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 4, "2010": 4},
                                    "best": {"2009": 4, "2010": 4},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 40, "2010": 40},
                                    "range": {"2009": 4, "2010": 4},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "secondary heating": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 5, "2010": 5},
                                    "best": {"2009": 5, "2010": 5},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 5, "2010": 5},
                                    "best": {"2009": 5, "2010": 5},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 50, "2010": 50},
                                    "range": {"2009": 5, "2010": 5},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 6, "2010": 6},
                                    "best": {"2009": 6, "2010": 6},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 6, "2010": 6},
                                    "best": {"2009": 6, "2010": 6},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 60, "2010": 60},
                                    "range": {"2009": 6, "2010": 6},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "infiltration": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 3},
                                    "best": {"2009": 2, "2010": 3},
                                    "units": "ACH50",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}},
                        "supply": {
                            "non-specific": {
                                "performance": {
                                    "typical": {"2009": 7, "2010": 7},
                                    "best": {"2009": 7, "2010": 7},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 7, "2010": 7},
                                    "best": {"2009": 7, "2010": 7},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 70, "2010": 70},
                                    "range": {"2009": 7, "2010": 7},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "cooling": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 8, "2010": 8},
                                    "best": {"2009": 8, "2010": 8},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 8, "2010": 8},
                                    "best": {"2009": 8, "2010": 8},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 80, "2010": 80},
                                    "range": {"2009": 8, "2010": 8},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 9, "2010": 9},
                                    "best": {"2009": 9, "2010": 9},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 9, "2010": 9},
                                    "best": {"2009": 9, "2010": 9},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 90, "2010": 90},
                                    "range": {"2009": 9, "2010": 9},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "infiltration": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 3},
                                    "best": {"2009": 2, "2010": 3},
                                    "units": "ACH50",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}},
                        "supply": {
                            "central AC": {
                                "performance": {
                                    "typical": {"2009": 10, "2010": 10},
                                    "best": {"2009": 10, "2010": 10},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 10, "2010": 10},
                                    "best": {"2009": 10, "2010": 10},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 100, "2010": 100},
                                    "range": {"2009": 10, "2010": 10},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "room AC": {
                                "performance": {
                                    "typical": {"2009": 11, "2010": 11},
                                    "best": {"2009": 11, "2010": 11},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 11, "2010": 11},
                                    "best": {"2009": 11, "2010": 11},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 110, "2010": 110},
                                    "range": {"2009": 11, "2010": 11},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "ASHP": {
                                "performance": {
                                    "typical": {"2009": 12, "2010": 12},
                                    "best": {"2009": 12, "2010": 12},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 12, "2010": 12},
                                    "best": {"2009": 12, "2010": 12},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 120, "2010": 120},
                                    "range": {"2009": 12, "2010": 12},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "GSHP": {
                                "performance": {
                                    "typical": {"2009": 13, "2010": 13},
                                    "best": {"2009": 13, "2010": 13},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 13, "2010": 13},
                                    "best": {"2009": 13, "2010": 13},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 130, "2010": 130},
                                    "range": {"2009": 13, "2010": 13},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "lighting": {
                        "linear fluorescent (LED)": {
                                "performance": {
                                    "typical": {"2009": 14, "2010": 14},
                                    "best": {"2009": 14, "2010": 14},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 14, "2010": 14},
                                    "best": {"2009": 14, "2010": 14},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 140, "2010": 140},
                                    "range": {"2009": 14, "2010": 14},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "general service (LED)": {
                                "performance": {
                                    "typical": {"2009": 15, "2010": 15},
                                    "best": {"2009": 15, "2010": 15},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 15, "2010": 15},
                                    "best": {"2009": 15, "2010": 15},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 150, "2010": 150},
                                    "range": {"2009": 15, "2010": 15},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "reflector (LED)": {
                                "performance": {
                                    "typical": {"2009": 16, "2010": 16},
                                    "best": {"2009": 16, "2010": 16},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 16, "2010": 16},
                                    "best": {"2009": 16, "2010": 16},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 160, "2010": 160},
                                    "range": {"2009": 16, "2010": 16},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "external (LED)": {
                                "performance": {
                                    "typical": {"2009": 17, "2010": 17},
                                    "best": {"2009": 17, "2010": 17},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 17, "2010": 17},
                                    "best": {"2009": 17, "2010": 17},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 170, "2010": 170},
                                    "range": {"2009": 17, "2010": 17},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                "natural gas": {
                    "water heating": {
                        "performance": {
                            "typical": {"2009": 18, "2010": 18},
                            "best": {"2009": 18, "2010": 18},
                            "units": "EF",
                            "source":
                            "EIA AEO"},
                        "installed cost": {
                            "typical": {"2009": 18, "2010": 18},
                            "best": {"2009": 18, "2010": 18},
                            "units": "2014$/unit",
                            "source": "EIA AEO"},
                        "lifetime": {
                            "average": {"2009": 180, "2010": 180},
                            "range": {"2009": 18, "2010": 18},
                            "units": "years",
                            "source": "EIA AEO"},
                        "consumer choice": {
                            "competed market share": {
                                "source": "EIA AEO",
                                "model type": "logistic regression",
                                "parameters": {
                                    "b1": {"2009": None, "2010": None},
                                    "b2": {"2009": None,
                                           "2010": None}}},
                            "competed market": {
                                "source": "COBAM",
                                "model type": "bass diffusion",
                                "parameters": {
                                    "p": "NA",
                                    "q": "NA"}}}},
                    "heating": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 10, "2010": 10},
                                    "range": {"2009": 1, "2010": 1},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "infiltration": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 3},
                                    "best": {"2009": 2, "2010": 3},
                                    "units": "ACH50",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "secondary heating": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 5, "2010": 5},
                                    "best": {"2009": 5, "2010": 5},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 5, "2010": 5},
                                    "best": {"2009": 5, "2010": 5},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 50, "2010": 50},
                                    "range": {"2009": 5, "2010": 5},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 6, "2010": 6},
                                    "best": {"2009": 6, "2010": 6},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 6, "2010": 6},
                                    "best": {"2009": 6, "2010": 6},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 60, "2010": 60},
                                    "range": {"2009": 6, "2010": 6},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "infiltration": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 3},
                                    "best": {"2009": 2, "2010": 3},
                                    "units": "ACH50",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "cooling": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 8, "2010": 8},
                                    "best": {"2009": 8, "2010": 8},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 8, "2010": 8},
                                    "best": {"2009": 8, "2010": 8},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 80, "2010": 80},
                                    "range": {"2009": 8, "2010": 8},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 9, "2010": 9},
                                    "best": {"2009": 9, "2010": 9},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 9, "2010": 9},
                                    "best": {"2009": 9, "2010": 9},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 90, "2010": 90},
                                    "range": {"2009": 9, "2010": 9},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "infiltration": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 3},
                                    "best": {"2009": 2, "2010": 3},
                                    "units": "ACH50",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}}}},
            "multi family home": {
                "electricity (grid)": {
                    "heating": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 19, "2010": 19},
                                    "best": {"2009": 19, "2010": 19},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 19, "2010": 19},
                                    "best": {"2009": 19, "2010": 19},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 190, "2010": 190},
                                    "range": {"2009": 19, "2010": 19},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 20, "2010": 20},
                                    "best": {"2009": 20, "2010": 20},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 20, "2010": 20},
                                    "best": {"2009": 20, "2010": 20},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 200, "2010": 200},
                                    "range": {"2009": 20, "2010": 20},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}},
                        "supply": {
                            "boiler (electric)": {
                                "performance": {
                                    "typical": {"2009": 21, "2010": 21},
                                    "best": {"2009": 21, "2010": 21},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 21, "2010": 21},
                                    "best": {"2009": 21, "2010": 21},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 210, "2010": 210},
                                    "range": {"2009": 21, "2010": 21},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "ASHP": {
                                "performance": {
                                    "typical": {"2009": 22, "2010": 22},
                                    "best": {"2009": 22, "2010": 22},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 22, "2010": 22},
                                    "best": {"2009": 22, "2010": 22},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 220, "2010": 220},
                                    "range": {"2009": 22, "2010": 22},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "GSHP": {
                                "performance": {
                                    "typical": {"2009": 23, "2010": 23},
                                    "best": {"2009": 23, "2010": 23},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 23, "2010": 23},
                                    "best": {"2009": 23, "2010": 23},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 230, "2010": 230},
                                    "range": {"2009": 23, "2010": 23},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "lighting": {
                        "linear fluorescent (LED)": {
                                "performance": {
                                    "typical": {"2009": 24, "2010": 24},
                                    "best": {"2009": 24, "2010": 24},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 24, "2010": 24},
                                    "best": {"2009": 24, "2010": 24},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 240, "2010": 240},
                                    "range": {"2009": 24, "2010": 24},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "general service (LED)": {
                                "performance": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 250, "2010": 250},
                                    "range": {"2009": 25, "2010": 25},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "reflector (LED)": {
                                "performance": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 250, "2010": 250},
                                    "range": {"2009": 25, "2010": 25},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "external (LED)": {
                                "performance": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 250, "2010": 250},
                                    "range": {"2009": 25, "2010": 25},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}}}},
        "AIA_CZ2": {
            "single family home": {
                "electricity (grid)": {
                    "heating": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 1, "2010": 1},
                                    "best": {"2009": 1, "2010": 1},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 10, "2010": 10},
                                    "range": {"2009": 1, "2010": 1},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "infiltration": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 3},
                                    "best": {"2009": 2, "2010": 3},
                                    "units": "ACH50",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}},
                        "supply": {
                            "boiler (electric)": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "ASHP": {
                                "performance": {
                                    "typical": {"2009": 3, "2010": 3},
                                    "best": {"2009": 3, "2010": 3},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 3, "2010": 3},
                                    "best": {"2009": 3, "2010": 3},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 30, "2010": 30},
                                    "range": {"2009": 3, "2010": 3},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "GSHP": {
                                "performance": {
                                    "typical": {"2009": 4, "2010": 4},
                                    "best": {"2009": 4, "2010": 4},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 4, "2010": 4},
                                    "best": {"2009": 4, "2010": 4},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 40, "2010": 40},
                                    "range": {"2009": 4, "2010": 4},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "secondary heating": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 5, "2010": 5},
                                    "best": {"2009": 5, "2010": 5},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 5, "2010": 5},
                                    "best": {"2009": 5, "2010": 5},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 50, "2010": 50},
                                    "range": {"2009": 5, "2010": 5},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 6, "2010": 6},
                                    "best": {"2009": 6, "2010": 6},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 6, "2010": 6},
                                    "best": {"2009": 6, "2010": 6},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 60, "2010": 60},
                                    "range": {"2009": 6, "2010": 6},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "infiltration": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 3},
                                    "best": {"2009": 2, "2010": 3},
                                    "units": "ACH50",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}},
                        "supply": {
                            "non-specific": {
                                "performance": {
                                    "typical": {"2009": 7, "2010": 7},
                                    "best": {"2009": 7, "2010": 7},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 7, "2010": 7},
                                    "best": {"2009": 7, "2010": 7},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 70, "2010": 70},
                                    "range": {"2009": 7, "2010": 7},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "cooling": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 8, "2010": 8},
                                    "best": {"2009": 8, "2010": 8},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 8, "2010": 8},
                                    "best": {"2009": 8, "2010": 8},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 80, "2010": 80},
                                    "range": {"2009": 8, "2010": 8},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 9, "2010": 9},
                                    "best": {"2009": 9, "2010": 9},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 9, "2010": 9},
                                    "best": {"2009": 9, "2010": 9},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 90, "2010": 90},
                                    "range": {"2009": 9, "2010": 9},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "infiltration": {
                                "performance": {
                                    "typical": {"2009": 2, "2010": 3},
                                    "best": {"2009": 2, "2010": 3},
                                    "units": "ACH50",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 2, "2010": 2},
                                    "best": {"2009": 2, "2010": 2},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 20, "2010": 20},
                                    "range": {"2009": 2, "2010": 2},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}},
                        "supply": {
                            "central AC": {
                                "performance": {
                                    "typical": {"2009": 10, "2010": 10},
                                    "best": {"2009": 10, "2010": 10},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 10, "2010": 10},
                                    "best": {"2009": 10, "2010": 10},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 100, "2010": 100},
                                    "range": {"2009": 10, "2010": 10},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "room AC": {
                                "performance": {
                                    "typical": {"2009": 11, "2010": 11},
                                    "best": {"2009": 11, "2010": 11},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 11, "2010": 11},
                                    "best": {"2009": 11, "2010": 11},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 110, "2010": 110},
                                    "range": {"2009": 11, "2010": 11},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "ASHP": {
                                "performance": {
                                    "typical": {"2009": 12, "2010": 12},
                                    "best": {"2009": 12, "2010": 12},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 12, "2010": 12},
                                    "best": {"2009": 12, "2010": 12},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 120, "2010": 120},
                                    "range": {"2009": 12, "2010": 12},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "GSHP": {
                                "performance": {
                                    "typical": {"2009": 13, "2010": 13},
                                    "best": {"2009": 13, "2010": 13},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 13, "2010": 13},
                                    "best": {"2009": 13, "2010": 13},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 130, "2010": 130},
                                    "range": {"2009": 13, "2010": 13},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "lighting": {
                        "linear fluorescent (LED)": {
                                "performance": {
                                    "typical": {"2009": 14, "2010": 14},
                                    "best": {"2009": 14, "2010": 14},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 14, "2010": 14},
                                    "best": {"2009": 14, "2010": 14},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 140, "2010": 140},
                                    "range": {"2009": 14, "2010": 14},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "general service (LED)": {
                                "performance": {
                                    "typical": {"2009": 15, "2010": 15},
                                    "best": {"2009": 15, "2010": 15},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 15, "2010": 15},
                                    "best": {"2009": 15, "2010": 15},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 150, "2010": 150},
                                    "range": {"2009": 15, "2010": 15},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "reflector (LED)": {
                                "performance": {
                                    "typical": {"2009": 16, "2010": 16},
                                    "best": {"2009": 16, "2010": 16},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 16, "2010": 16},
                                    "best": {"2009": 16, "2010": 16},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 160, "2010": 160},
                                    "range": {"2009": 16, "2010": 16},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "external (LED)": {
                                "performance": {
                                    "typical": {"2009": 17, "2010": 17},
                                    "best": {"2009": 17, "2010": 17},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 17, "2010": 17},
                                    "best": {"2009": 17, "2010": 17},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 170, "2010": 170},
                                    "range": {"2009": 17, "2010": 17},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                "natural gas": {
                    "water heating": {
                            "performance": {
                                "typical": {"2009": 18, "2010": 18},
                                "best": {"2009": 18, "2010": 18},
                                "units": "EF",
                                "source":
                                "EIA AEO"},
                            "installed cost": {
                                "typical": {"2009": 18, "2010": 18},
                                "best": {"2009": 18, "2010": 18},
                                "units": "2014$/unit",
                                "source": "EIA AEO"},
                            "lifetime": {
                                "average": {"2009": 180, "2010": 180},
                                "range": {"2009": 18, "2010": 18},
                                "units": "years",
                                "source": "EIA AEO"},
                            "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
            "multi family home": {
                "electricity (grid)": {
                    "heating": {
                        "demand": {
                            "windows conduction": {
                                "performance": {
                                    "typical": {"2009": 19, "2010": 19},
                                    "best": {"2009": 19, "2010": 19},
                                    "units": "R Value",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 19, "2010": 19},
                                    "best": {"2009": 19, "2010": 19},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 190, "2010": 190},
                                    "range": {"2009": 19, "2010": 19},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "windows solar": {
                                "performance": {
                                    "typical": {"2009": 20, "2010": 20},
                                    "best": {"2009": 20, "2010": 20},
                                    "units": "SHGC",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 20, "2010": 20},
                                    "best": {"2009": 20, "2010": 20},
                                    "units": "2014$/sf",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 200, "2010": 200},
                                    "range": {"2009": 20, "2010": 20},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}},
                        "supply": {
                            "boiler (electric)": {
                                "performance": {
                                    "typical": {"2009": 21, "2010": 21},
                                    "best": {"2009": 21, "2010": 21},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 21, "2010": 21},
                                    "best": {"2009": 21, "2010": 21},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 210, "2010": 210},
                                    "range": {"2009": 21, "2010": 21},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "ASHP": {
                                "performance": {
                                    "typical": {"2009": 22, "2010": 22},
                                    "best": {"2009": 22, "2010": 22},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 22, "2010": 22},
                                    "best": {"2009": 22, "2010": 22},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 220, "2010": 220},
                                    "range": {"2009": 22, "2010": 22},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                            "GSHP": {
                                "performance": {
                                    "typical": {"2009": 23, "2010": 23},
                                    "best": {"2009": 23, "2010": 23},
                                    "units": "COP",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 23, "2010": 23},
                                    "best": {"2009": 23, "2010": 23},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 230, "2010": 230},
                                    "range": {"2009": 23, "2010": 23},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}},
                    "lighting": {
                        "linear fluorescent (LED)": {
                                "performance": {
                                    "typical": {"2009": 24, "2010": 24},
                                    "best": {"2009": 24, "2010": 24},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 24, "2010": 24},
                                    "best": {"2009": 24, "2010": 24},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 240, "2010": 240},
                                    "range": {"2009": 24, "2010": 24},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "general service (LED)": {
                                "performance": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 250, "2010": 250},
                                    "range": {"2009": 25, "2010": 25},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "reflector (LED)": {
                                "performance": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 250, "2010": 250},
                                    "range": {"2009": 25, "2010": 25},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "external (LED)": {
                                "performance": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 250, "2010": 250},
                                    "range": {"2009": 25, "2010": 25},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}}}},
        "AIA_CZ4": {
            "multi family home": {
                "electricity (grid)": {
                    "lighting": {
                        "linear fluorescent (LED)": {
                                "performance": {
                                    "typical": {"2009": 24, "2010": 24},
                                    "best": {"2009": 24, "2010": 24},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 24, "2010": 24},
                                    "best": {"2009": 24, "2010": 24},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 240, "2010": 240},
                                    "range": {"2009": 24, "2010": 24},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "general service (LED)": {
                                "performance": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 25, "2010": 25},
                                    "best": {"2009": 25, "2010": 25},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 250, "2010": 250},
                                    "range": {"2009": 25, "2010": 25},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "reflector (LED)": {
                                "performance": {
                                    "typical": {"2009": 26, "2010": 26},
                                    "best": {"2009": 26, "2010": 26},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 26, "2010": 26},
                                    "best": {"2009": 26, "2010": 26},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 260, "2010": 260},
                                    "range": {"2009": 26, "2010": 26},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}},
                        "external (LED)": {
                                "performance": {
                                    "typical": {"2009": 27, "2010": 27},
                                    "best": {"2009": 27, "2010": 27},
                                    "units": "lm/W",
                                    "source":
                                    "EIA AEO"},
                                "installed cost": {
                                    "typical": {"2009": 27, "2010": 27},
                                    "best": {"2009": 27, "2010": 27},
                                    "units": "2014$/unit",
                                    "source": "EIA AEO"},
                                "lifetime": {
                                    "average": {"2009": 270, "2010": 270},
                                    "range": {"2009": 27, "2010": 27},
                                    "units": "years",
                                    "source": "EIA AEO"},
                                "consumer choice": {
                                    "competed market share": {
                                        "source": "EIA AEO",
                                        "model type": "logistic regression",
                                        "parameters": {
                                            "b1": {"2009": None, "2010": None},
                                            "b2": {"2009": None,
                                                   "2010": None}}},
                                    "competed market": {
                                        "source": "COBAM",
                                        "model type": "bass diffusion",
                                        "parameters": {
                                            "p": "NA",
                                            "q": "NA"}}}}}}}}}

    # Sample input dict of microsegment stock/energy info. to reference in
    # generating and partitioning master microsegments for a measure
    sample_msegin = {
        "AIA_CZ1": {
            "assembly": {
                "electricity (grid)": {
                    "heating": {"demand": {"windows conduction": {
                                           "stock": "NA",
                                           "energy": {"2009": 0, "2010": 0}},
                                           "windows solar": {
                                           "stock": "NA",
                                           "energy": {"2009": 1, "2010": 1}},
                                           "lights": {
                                           "stock": "NA",
                                           "energy": {"2009": 1, "2010": 1}}}},
                    "secondary heating": {"demand": {"windows conduction": {
                                                     "stock": "NA",
                                                     "energy": {"2009": 5,
                                                                "2010": 5}},
                                                     "windows solar": {
                                                     "stock": "NA",
                                                     "energy": {"2009": 6,
                                                                "2010": 6}},
                                                     "lights": {
                                                     "stock": "NA",
                                                     "energy": {"2009": 6,
                                                                "2010": 6}}}},
                    "cooling": {"demand": {"windows conduction": {
                                           "stock": "NA",
                                           "energy": {"2009": 5, "2010": 5}},
                                           "windows solar": {
                                           "stock": "NA",
                                           "energy": {"2009": 6, "2010": 6}},
                                           "lights": {
                                           "stock": "NA",
                                           "energy": {"2009": 6, "2010": 6}}}},
                    "lighting": {"commercial light type X": {
                                 "stock": {"2009": 11, "2010": 11},
                                 "energy": {"2009": 11, "2010": 11}}}}},
            "single family home": {
                "square footage": {"2009": 100, "2010": 200},
                "total homes": {"2009": 1000, "2010": 1000},
                "new homes": {"2009": 100, "2010": 50},
                "electricity (grid)": {
                    "heating": {"demand": {"windows conduction": {
                                           "stock": "NA",
                                           "energy": {"2009": 0, "2010": 0}},
                                           "windows solar": {
                                           "stock": "NA",
                                           "energy": {"2009": 1, "2010": 1}},
                                           "infiltration": {
                                           "stock": "NA",
                                           "energy": {
                                               "2009": 10, "2010": 10}}},
                                "supply": {"boiler (electric)": {
                                           "stock": {"2009": 2, "2010": 2},
                                           "energy": {"2009": 2, "2010": 2}},
                                           "ASHP": {
                                           "stock": {"2009": 3, "2010": 3},
                                           "energy": {"2009": 3, "2010": 3}},
                                           "GSHP": {
                                           "stock": {"2009": 4, "2010": 4},
                                           "energy": {"2009": 4, "2010": 4}}}},
                    "secondary heating": {"demand": {"windows conduction": {
                                                     "stock": "NA",
                                                     "energy": {"2009": 5,
                                                                "2010": 5}},
                                                     "windows solar": {
                                                     "stock": "NA",
                                                     "energy": {"2009": 6,
                                                                "2010": 6}},
                                                     "infiltration": {
                                                     "stock": "NA",
                                                     "energy": {
                                                         "2009": 10,
                                                         "2010": 10}}},
                                          "supply": {"non-specific": 7}},
                    "cooling": {"demand": {"windows conduction": {
                                           "stock": "NA",
                                           "energy": {"2009": 5, "2010": 5}},
                                           "windows solar": {
                                           "stock": "NA",
                                           "energy": {"2009": 6, "2010": 6}},
                                           "infiltration": {
                                               "stock": "NA",
                                               "energy": {
                                                   "2009": 10, "2010": 10}}},
                                "supply": {"central AC": {
                                           "stock": {"2009": 7, "2010": 7},
                                           "energy": {"2009": 7, "2010": 7}},
                                           "room AC": {
                                           "stock": {"2009": 8, "2010": 8},
                                           "energy": {"2009": 8, "2010": 8}},
                                           "ASHP": {
                                           "stock": {"2009": 9, "2010": 9},
                                           "energy": {"2009": 9, "2010": 9}},
                                           "GSHP": {
                                           "stock": {"2009": 10, "2010": 10},
                                           "energy": {"2009": 10,
                                                      "2010": 10}}}},
                    "lighting": {"linear fluorescent (LED)": {
                                 "stock": {"2009": 11, "2010": 11},
                                 "energy": {"2009": 11, "2010": 11}},
                                 "general service (LED)": {
                                 "stock": {"2009": 12, "2010": 12},
                                 "energy": {"2009": 12, "2010": 12}},
                                 "reflector (LED)": {
                                 "stock": {"2009": 13, "2010": 13},
                                 "energy": {"2009": 13, "2010": 13}},
                                 "external (LED)": {
                                 "stock": {"2009": 14, "2010": 14},
                                 "energy": {"2009": 14, "2010": 14}}}},
                "natural gas": {
                    "water heating": {
                        "stock": {"2009": 15, "2010": 15},
                        "energy": {"2009": 15, "2010": 15}},
                    "heating": {
                        "demand": {
                            "windows conduction": {
                                "stock": "NA",
                                "energy": {"2009": 0,
                                           "2010": 0}},
                            "windows solar": {
                                "stock": "NA",
                                "energy": {"2009": 1,
                                           "2010": 1}},
                            "infiltration": {
                                "stock": "NA",
                                "energy": {
                                    "2009": 10, "2010": 10}}}},
                    "secondary heating": {
                        "demand": {
                            "windows conduction": {
                                "stock": "NA",
                                "energy": {"2009": 5,
                                           "2010": 5}},
                            "windows solar": {
                                "stock": "NA",
                                "energy": {"2009": 6,
                                           "2010": 6}},
                            "infiltration": {
                                "stock": "NA",
                                "energy": {
                                    "2009": 10, "2010": 10}}}},
                    "cooling": {
                        "demand": {
                            "windows conduction": {
                                "stock": "NA",
                                "energy": {"2009": 5, "2010": 5}},
                            "windows solar": {
                                "stock": "NA",
                                "energy": {"2009": 6, "2010": 6}},
                            "infiltration": {
                                "stock": "NA",
                                "energy": {
                                    "2009": 10, "2010": 10}}}}}},
            "multi family home": {
                "square footage": {"2009": 300, "2010": 400},
                "total homes": {"2009": 1000, "2010": 1000},
                "new homes": {"2009": 100, "2010": 50},
                "electricity (grid)": {
                    "heating": {"demand": {"windows conduction": {
                                           "stock": "NA",
                                           "energy": {"2009": 0, "2010": 0}},
                                           "windows solar": {
                                           "stock": "NA",
                                           "energy": {"2009": 1, "2010": 1}}},
                                "supply": {"boiler (electric)": {
                                           "stock": {"2009": 2, "2010": 2},
                                           "energy": {"2009": 2, "2010": 2}},
                                           "ASHP": {
                                           "stock": {"2009": 3, "2010": 3},
                                           "energy": {"2009": 3, "2010": 3}},
                                           "GSHP": {
                                           "stock": {"2009": 4, "2010": 4}}}},
                    "lighting": {"linear fluorescent (LED)": {
                                 "stock": {"2009": 11, "2010": 11},
                                 "energy": {"2009": 11, "2010": 11}},
                                 "general service (LED)": {
                                 "stock": {"2009": 12, "2010": 12},
                                 "energy": {"2009": 12, "2010": 12}},
                                 "reflector (LED)": {
                                 "stock": {"2009": 13, "2010": 13},
                                 "energy": {"2009": 13, "2010": 13}},
                                 "external (LED)": {
                                 "stock": {"2009": 14, "2010": 14},
                                 "energy": {"2009": 14, "2010": 14}}}}}},
        "AIA_CZ2": {
            "single family home": {
                "square footage": {"2009": 500, "2010": 600},
                "total homes": {"2009": 1000, "2010": 1000},
                "new homes": {"2009": 100, "2010": 50},
                "electricity (grid)": {
                    "heating": {"demand": {"windows conduction": {
                                           "stock": "NA",
                                           "energy": {"2009": 0, "2010": 0}},
                                           "windows solar": {
                                           "stock": "NA",
                                           "energy": {"2009": 1, "2010": 1}},
                                           "infiltration": {
                                           "stock": "NA",
                                           "energy": {
                                               "2009": 10, "2010": 10}}},
                                "supply": {"boiler (electric)": {
                                           "stock": {"2009": 2, "2010": 2},
                                           "energy": {"2009": 2, "2010": 2}},
                                           "ASHP": {
                                           "stock": {"2009": 3, "2010": 3},
                                           "energy": {"2009": 3, "2010": 3}},
                                           "GSHP": {
                                           "stock": {"2009": 4, "2010": 4},
                                           "energy": {"2009": 4, "2010": 4}}}},
                    "secondary heating": {"demand": {"windows conduction": {
                                                     "stock": "NA",
                                                     "energy": {"2009": 5,
                                                                "2010": 5}},
                                                     "windows solar": {
                                                     "stock": "NA",
                                                     "energy": {"2009": 6,
                                                                "2010": 6}},
                                                     "infiltration": {
                                                     "stock": "NA",
                                                     "energy": {
                                                         "2009": 10,
                                                         "2010": 10}}},
                                          "supply": {"non-specific": 7}},
                    "cooling": {"demand": {"windows conduction": {
                                           "stock": "NA",
                                           "energy": {"2009": 5, "2010": 5}},
                                           "windows solar": {
                                           "stock": "NA",
                                           "energy": {"2009": 6, "2010": 6}},
                                           "infiltration": {
                                               "stock": "NA",
                                               "energy": {
                                                   "2009": 10,
                                                   "2010": 10}}},
                                "supply": {"central AC": {
                                           "stock": {"2009": 7, "2010": 7},
                                           "energy": {"2009": 7, "2010": 7}},
                                           "room AC": {
                                           "stock": {"2009": 8, "2010": 8},
                                           "energy": {"2009": 8, "2010": 8}},
                                           "ASHP": {
                                           "stock": {"2009": 9, "2010": 9},
                                           "energy": {"2009": 9, "2010": 9}},
                                           "GSHP": {
                                           "stock": {"2009": 10, "2010": 10},
                                           "energy": {"2009": 10,
                                                      "2010": 10}}}},
                    "lighting": {"linear fluorescent (LED)": {
                                 "stock": {"2009": 11, "2010": 11},
                                 "energy": {"2009": 11, "2010": 11}},
                                 "general service (LED)": {
                                 "stock": {"2009": 12, "2010": 12},
                                 "energy": {"2009": 12, "2010": 12}},
                                 "reflector (LED)": {
                                 "stock": {"2009": 13, "2010": 13},
                                 "energy": {"2009": 13, "2010": 13}},
                                 "external (LED)": {
                                 "stock": {"2009": 14, "2010": 14},
                                 "energy": {"2009": 14, "2010": 14}}}},
                "natural gas": {"water heating": {
                                "stock": {"2009": 15, "2010": 15},
                                "energy": {"2009": 15, "2010": 15}}}},
            "multi family home": {
                "square footage": {"2009": 700, "2010": 800},
                "total homes": {"2009": 1000, "2010": 1000},
                "new homes": {"2009": 100, "2010": 50},
                "electricity (grid)": {
                    "heating": {"demand": {"windows conduction": {
                                           "stock": "NA",
                                           "energy": {"2009": 0, "2010": 0}},
                                           "windows solar": {
                                           "stock": "NA",
                                           "energy": {"2009": 1, "2010": 1}}},
                                "supply": {"boiler (electric)": {
                                           "stock": {"2009": 2, "2010": 2},
                                           "energy": {"2009": 2, "2010": 2}},
                                           "ASHP": {
                                           "stock": {"2009": 3, "2010": 3},
                                           "energy": {"2009": 3, "2010": 3}},
                                           "GSHP": {
                                           "stock": {"2009": 4, "2010": 4}}}},
                    "lighting": {"linear fluorescent (LED)": {
                                 "stock": {"2009": 11, "2010": 11},
                                 "energy": {"2009": 11, "2010": 11}},
                                 "general service (LED)": {
                                 "stock": {"2009": 12, "2010": 12},
                                 "energy": {"2009": 12, "2010": 12}},
                                 "reflector (LED)": {
                                 "stock": {"2009": 13, "2010": 13},
                                 "energy": {"2009": 13, "2010": 13}},
                                 "external (LED)": {
                                 "stock": {"2009": 14, "2010": 14},
                                 "energy": {"2009": 14, "2010": 14}}}}}},
        "AIA_CZ4": {
            "multi family home": {
                "square footage": {"2009": 900, "2010": 1000},
                "total homes": {"2009": 1000, "2010": 1000},
                "new homes": {"2009": 100, "2010": 50},
                "electricity (grid)": {
                    "lighting": {"linear fluorescent (LED)": {
                                 "stock": {"2009": 11, "2010": 11},
                                 "energy": {"2009": 11, "2010": 11}},
                                 "general service (LED)": {
                                 "stock": {"2009": 12, "2010": 12},
                                 "energy": {"2009": 12, "2010": 12}},
                                 "reflector (LED)": {
                                 "stock": {"2009": 13, "2010": 13},
                                 "energy": {"2009": 13, "2010": 13}},
                                 "external (LED)": {
                                 "stock": {"2009": 14, "2010": 14},
                                 "energy": {"2009": 14, "2010": 14}}}}}}}

    # List of measures with attribute combinations that should all be found in
    # the key chains of the "sample_msegin" dict above
    ok_measures = [{"name": "sample measure 1",
                    "installed_cost": 25,
                    "cost_units": "2014$/unit",
                    "energy_efficiency": {"primary":
                                          {"AIA_CZ1": {"heating": 30,
                                                       "cooling": 25},
                                           "AIA_CZ2": {"heating": 30,
                                                       "cooling": 15}},
                                          "secondary": None},
                    "energy_efficiency_units": {"primary": "COP",
                                                "secondary": None},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["single family home"],
                    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                    "fuel_type": {"primary": ["electricity (grid)"],
                                  "secondary": None},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["heating", "cooling"],
                                "secondary": None},
                    "technology_type": {"primary": "supply",
                                        "secondary": None},
                    "technology": {"primary": ["boiler (electric)",
                                   "ASHP", "GSHP", "room AC"],
                                   "secondary": None}},
                   {"name": "sample measure 2",
                    "installed_cost": 25,
                    "cost_units": "2014$/unit",
                    "energy_efficiency": {
                        "primary": {"new": 25, "retrofit": 25},
                        "secondary": None},
                    "energy_efficiency_units": {"primary": "EF",
                                                "secondary": None},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["single family home"],
                    "climate_zone": ["AIA_CZ1"],
                    "fuel_type": {"primary": ["natural gas"],
                                  "secondary": None},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["water heating"],
                                "secondary": None},
                    "technology_type": {"primary": "supply",
                                        "secondary": None},
                    "technology": {"primary": None,
                                   "secondary": None}},
                   {"name": "sample measure 3",
                    "installed_cost": 25,
                    "cost_units": "2014$/unit",
                    "energy_efficiency": {"primary": 25,
                                          "secondary": {
                                              "heating": 0.4,
                                              "secondary heating": 0.4,
                                              "cooling": -0.4}},
                    "energy_efficiency_units": {"primary": "lm/W",
                                                "secondary":
                                                "relative savings (constant)"},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["single family home",
                                  "multi family home"],
                    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                    "fuel_type": {"primary": ["electricity (grid)"],
                                  "secondary": ["electricity (grid)",
                                                "natural gas"]},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["lighting"],
                                "secondary": ["heating", "secondary heating",
                                              "cooling"]},
                    "technology_type": {"primary": "supply",
                                        "secondary": "demand"},
                    "technology": {"primary":
                                   ["linear fluorescent (LED)",
                                    "general service (LED)",
                                    "external (LED)"],
                                   "secondary":
                                   ["windows conduction",
                                    "windows solar"]}},
                   {"name": "sample measure 4",
                    "installed_cost": 10,
                    "cost_units": "2014$/sf",
                    "energy_efficiency": {"primary":
                                          {"windows conduction": 20,
                                           "windows solar": 1},
                                          "secondary": None},
                    "energy_efficiency_units": {"primary":
                                                {"windows conduction":
                                                 "R Value",
                                                 "windows solar": "SHGC"},
                                                "secondary": None},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["single family home",
                                  "multi family home"],
                    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                    "fuel_type": {"primary": ["electricity (grid)"],
                                  "secondary": None},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["heating"],
                                "secondary": None},
                    "technology_type": {"primary": "demand",
                                        "secondary": None},
                    "technology": {"primary": ["windows conduction",
                                   "windows solar"],
                                   "secondary": None}},
                   {"name": "sample measure 5",
                    "installed_cost": 10,
                    "cost_units": "2014$/sf",
                    "energy_efficiency": {"primary": 1, "secondary": None},
                    "energy_efficiency_units": {"primary": "SHGC",
                                                "secondary": None},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["single family home"],
                    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                    "fuel_type": {"primary": ["electricity (grid)"],
                                  "secondary": None},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["heating"],
                                "secondary": None},
                    "technology_type": {"primary": "demand",
                                        "secondary": None},
                    "technology": {"primary": ["windows solar"],
                                   "secondary": None}},
                   {"name": "sample measure 6",
                    "installed_cost": 10,
                    "cost_units": "2014$/sf",
                    "energy_efficiency": {"primary": {"windows conduction": 10,
                                                      "windows solar": 1},
                                          "secondary": None},
                    "energy_efficiency_units": {"primary":
                                                {"windows conduction":
                                                 "R Value",
                                                 "windows solar": "SHGC"},
                                                "secondary": None},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["single family home"],
                    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                    "fuel_type": {"primary": ["electricity (grid)"],
                                  "secondary": None},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["heating", "secondary heating",
                                            "cooling"],
                                "secondary": None},
                    "technology_type": {"primary": "demand",
                                        "secondary": None},
                    "technology": {"primary": ["windows conduction",
                                               "windows solar"],
                                   "secondary": None}},
                   {"name": "sample measure 7",
                    "installed_cost": 10,
                    "cost_units": "2014$/sf",
                    "energy_efficiency": {"primary":
                                          {"windows conduction": 0.4,
                                           "windows solar": 1},
                                          "secondary": None},
                    "energy_efficiency_units": {"primary":
                                                {"windows conduction":
                                                 "relative savings (constant)",
                                                 "windows solar": "SHGC"},
                                                "secondary": None},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["single family home"],
                    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                    "fuel_type": {"primary": ["electricity (grid)"],
                                  "secondary": None},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["heating", "secondary heating",
                                            "cooling"],
                                "secondary": None},
                    "technology_type": {"primary": "demand",
                                        "secondary": None},
                    "technology": {"primary": ["windows conduction",
                                               "windows solar"],
                                   "secondary": None}},
                   {"name": "sample measure 8",  # Add heat/cool end uses later
                    "installed_cost": 25,
                    "cost_units": "2014$/unit",
                    "energy_efficiency": {"primary": 25,
                                          "secondary": None},
                    "energy_efficiency_units": {"primary": "lm/W",
                                                "secondary": None},
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["assembly"],
                    "climate_zone": ["AIA_CZ1"],
                    "fuel_type": {"primary": ["electricity (grid)"],
                                  "secondary": ["electricity (grid)",
                                                "natural gas"]},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["lighting"],
                                "secondary": None},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "technology_type": {"primary": "supply",
                                        "secondary": None},
                    "technology": {"primary":
                                   ["commercial light type X"],
                                   "secondary": None}},
                   {"name": "sample measure 9",
                    "installed_cost": 25,
                    "cost_units": "2014$/unit",
                    "energy_efficiency": {"primary": 25,
                                          "secondary": None},
                    "energy_efficiency_units": {"primary": "EF",
                                                "secondary": None},
                    "product_lifetime": 10,
                    "structure_type": ["new"],
                    "bldg_type": ["single family home"],
                    "climate_zone": ["AIA_CZ1"],
                    "fuel_type": {"primary": ["natural gas"],
                                  "secondary": None},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["water heating"],
                                "secondary": None},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "technology_type": {"primary": "supply",
                                        "secondary": None},
                    "technology": {"primary": None,
                                   "secondary": None}},
                   {"name": "sample measure 10",
                    "installed_cost": 25,
                    "cost_units": "2014$/unit",
                    "energy_efficiency": {"primary": 25,
                                          "secondary": None},
                    "energy_efficiency_units": {"primary": "EF",
                                                "secondary": None},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "product_lifetime": 10,
                    "structure_type": ["retrofit"],
                    "bldg_type": ["single family home"],
                    "climate_zone": ["AIA_CZ1"],
                    "fuel_type": {"primary": ["natural gas"],
                                  "secondary": None},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["water heating"],
                                "secondary": None},
                    "technology_type": {"primary": "supply",
                                        "secondary": None},
                    "technology": {"primary": None,
                                   "secondary": None}},
                   {"name": "sample measure 11",
                    "installed_cost": 25,
                    "cost_units": "2014$/unit",
                    "energy_efficiency": {"primary": 25,
                                          "secondary": {
                                              "heating": 0.4,
                                              "secondary heating": 0.4,
                                              "cooling": -0.4}},
                    "energy_efficiency_units": {"primary": "lm/W",
                                                "secondary":
                                                "relative savings (constant)"},
                    "market_entry_year": 2010,
                    "market_exit_year": None,
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["single family home",
                                  "multi family home"],
                    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                    "fuel_type": {"primary": ["electricity (grid)"],
                                  "secondary": ["electricity (grid)",
                                                "natural gas"]},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["lighting"],
                                "secondary": ["heating", "secondary heating",
                                              "cooling"]},
                    "technology_type": {"primary": "supply",
                                        "secondary": "demand"},
                    "technology": {"primary":
                                   ["linear fluorescent (LED)",
                                    "general service (LED)",
                                    "external (LED)"],
                                   "secondary":
                                   ["windows conduction",
                                    "windows solar"]}},
                   {"name": "sample measure 12",
                    "installed_cost": 25,
                    "cost_units": "2014$/unit",
                    "energy_efficiency": {"primary": 25,
                                          "secondary": {
                                              "heating": 0.4,
                                              "secondary heating": 0.4,
                                              "cooling": -0.4}},
                    "energy_efficiency_units": {"primary": "lm/W",
                                                "secondary":
                                                "relative savings (constant)"},
                    "market_entry_year": None,
                    "market_exit_year": 2010,
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["single family home",
                                  "multi family home"],
                    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                    "fuel_type": {"primary": ["electricity (grid)"],
                                  "secondary": ["electricity (grid)",
                                                "natural gas"]},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["lighting"],
                                "secondary": ["heating", "secondary heating",
                                              "cooling"]},
                    "technology_type": {"primary": "supply",
                                        "secondary": "demand"},
                    "technology": {"primary":
                                   ["linear fluorescent (LED)",
                                    "general service (LED)",
                                    "external (LED)"],
                                   "secondary":
                                   ["windows conduction",
                                    "windows solar"]}},
                   {"name": "sample measure 13",
                    "installed_cost": 25,
                    "cost_units": "2014$/unit",
                    "energy_efficiency": {"primary": 25,
                                          "secondary": {
                                              "heating": 0.4,
                                              "secondary heating": 0.4,
                                              "cooling": -0.4}},
                    "energy_efficiency_units": {"primary": "lm/W",
                                                "secondary":
                                                ["relative savings (dynamic)",
                                                 2009]},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["single family home",
                                  "multi family home"],
                    "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                    "fuel_type": {"primary": ["electricity (grid)"],
                                  "secondary": ["electricity (grid)",
                                                "natural gas"]},
                    "fuel_switch_to": None,
                    "end_use": {"primary": ["lighting"],
                                "secondary": ["heating", "secondary heating",
                                              "cooling"]},
                    "technology_type": {"primary": "supply",
                                        "secondary": "demand"},
                    "technology": {"primary":
                                   ["linear fluorescent (LED)",
                                    "general service (LED)",
                                    "external (LED)"],
                                   "secondary":
                                   ["windows conduction",
                                    "windows solar",
                                    "infiltration"]}},
                   {"name": "sample measure 14",
                    "installed_cost": 25,
                    "cost_units": "2014$/unit",
                    "energy_efficiency": {
                        "primary": {"new": 25, "retrofit": 25},
                        "secondary": None},
                    "energy_efficiency_units": {"primary": "EF",
                                                "secondary": None},
                    "market_entry_year": None,
                    "market_exit_year": None,
                    "product_lifetime": 10,
                    "structure_type": ["new", "retrofit"],
                    "bldg_type": ["single family home"],
                    "climate_zone": ["AIA_CZ1"],
                    "fuel_type": {"primary": ["natural gas"],
                                  "secondary": None},
                    "fuel_switch_to": "electricity (grid)",
                    "end_use": {"primary": ["water heating"],
                                "secondary": None},
                    "technology_type": {"primary": "supply",
                                        "secondary": None},
                    "technology": {"primary": None,
                                   "secondary": None}}]

    # List of selected "ok" measures above with certain inputs now specified
    # as probability distributions
    ok_measures_dist = [{"name": "distrib measure 1",
                         "installed_cost": ["normal", 25, 5],
                         "cost_units": "2014$/unit",
                         "energy_efficiency": {"primary":
                                               {"AIA_CZ1": {"heating":
                                                            ["normal", 30, 1],
                                                            "cooling":
                                                            ["normal", 25, 2]},
                                                "AIA_CZ2": {"heating": 30,
                                                            "cooling":
                                                            ["normal", 15,
                                                             4]}},
                                               "secondary": None},
                         "energy_efficiency_units": {"primary": "COP",
                                                     "secondary": None},
                         "market_entry_year": None,
                         "market_exit_year": None,
                         "product_lifetime": 10,
                         "structure_type": ["new", "retrofit"],
                         "bldg_type": ["single family home"],
                         "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                         "fuel_type": {"primary": ["electricity (grid)"],
                                       "secondary": None},
                         "fuel_switch_to": None,
                         "end_use": {"primary": ["heating", "cooling"],
                                     "secondary": None},
                         "technology_type": {"primary": "supply",
                                             "secondary": None},
                         "technology": {"primary": ["boiler (electric)",
                                        "ASHP", "GSHP", "room AC"],
                                        "secondary": None}},
                        {"name": "distrib measure 2",
                         "installed_cost": ["lognormal", 3.22, 0.06],
                         "cost_units": "2014$/unit",
                         "energy_efficiency": {"primary": ["normal", 25, 5],
                                               "secondary": None},
                         "energy_efficiency_units": {"primary": "EF",
                                                     "secondary": None},
                         "market_entry_year": None,
                         "market_exit_year": None,
                         "product_lifetime": ["normal", 10, 1],
                         "structure_type": ["new", "retrofit"],
                         "bldg_type": ["single family home"],
                         "climate_zone": ["AIA_CZ1"],
                         "fuel_type": {"primary": ["natural gas"],
                                       "secondary": None},
                         "fuel_switch_to": None,
                         "end_use": {"primary": ["water heating"],
                                     "secondary": None},
                         "technology_type": {"primary": "supply",
                                             "secondary": None},
                         "technology": {"primary": None,
                                        "secondary": None}},
                        {"name": "distrib measure 3",
                         "installed_cost": ["normal", 10, 5],
                         "cost_units": "2014$/sf",
                         "energy_efficiency": {"primary":
                                               {"windows conduction":
                                                ["lognormal", 2.29, 0.14],
                                                "windows solar":
                                                ["normal", 1, 0.1]},
                                               "secondary": None},
                         "energy_efficiency_units": {
                             "primary": {
                                 "windows conduction": "R Value",
                                 "windows solar": "SHGC"},
                             "secondary": None},
                         "market_entry_year": None,
                         "market_exit_year": None,
                         "product_lifetime": 10,
                         "structure_type": ["new", "retrofit"],
                         "bldg_type": ["single family home"],
                         "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                         "fuel_type": {"primary": ["electricity (grid)"],
                                       "secondary": None},
                         "fuel_switch_to": None,
                         "end_use": {"primary": ["heating",
                                                 "secondary heating",
                                                 "cooling"],
                                     "secondary": None},
                         "technology_type": {"primary": "demand",
                                             "secondary": None},
                         "technology": {"primary": ["windows conduction",
                                                    "windows solar"],
                                        "secondary": None}}]

    # List of measures with attribute combinations that should match some of
    # the key chains in the "sample_msegin" dict above (i.e., AIA_CZ1 ->
    # single family home -> electricity (grid) -> cooling -> GSHP is
    # a valid chain, AIA_CZ1 -> single family home -> electricity (grid) ->
    # cooling -> linear fluorescent is not)
    partial_measures = [{"name": "partial measure 1",
                         "installed_cost": 25,
                         "cost_units": "2014$/unit",
                         "energy_efficiency": {"primary": 25,
                                               "secondary": None},
                         "product_lifetime": 10,
                         "structure_type": ["new", "retrofit"],
                         "energy_efficiency_units": {"primary": "COP",
                                                     "secondary": None},
                         "market_entry_year": None,
                         "market_exit_year": None,
                         "bldg_type": ["single family home"],
                         "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                         "fuel_type": {"primary": ["electricity (grid)"],
                                       "secondary": None},
                         "fuel_switch_to": None,
                         "end_use": {"primary": ["cooling"],
                                     "secondary": None},
                         "technology_type": {"primary": "supply",
                                             "secondary": None},
                         "technology": {"primary": ["boiler (electric)",
                                                    "ASHP"],
                                        "secondary": None}},
                        {"name": "partial measure 2",
                         "installed_cost": 25,
                         "cost_units": "2014$/unit",
                         "energy_efficiency": {"primary": 25,
                                               "secondary": None},
                         "market_entry_year": None,
                         "market_exit_year": None,
                         "product_lifetime": 10,
                         "structure_type": ["new", "retrofit"],
                         "energy_efficiency_units": {"primary": "COP",
                                                     "secondary": None},
                         "bldg_type": ["single family home"],
                         "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                         "fuel_type": {"primary": ["electricity (grid)"],
                                       "secondary": None},
                         "fuel_switch_to": None,
                         "end_use": {"primary": ["heating", "cooling"],
                                     "secondary": None},
                         "technology_type": {"primary": "supply",
                                             "secondary": None},
                         "technology": {"primary":
                                        ["linear fluorescent (LED)",
                                         "general service (LED)",
                                         "external (LED)", "GSHP", "ASHP"],
                                        "secondary": None}}]

    # List of measures with attribute combinations that should not match any
    # of the key chains in the "sample_msegin" dict above
    blank_measures = [{"name": "blank measure 1",
                       "installed_cost": 10,
                       "cost_units": "2014$/unit",
                       "energy_efficiency": {"primary": 10,
                                             "secondary": None},
                       "energy_efficiency_units": {"primary": "COP",
                                                   "secondary": None},
                       "market_entry_year": None,
                       "market_exit_year": None,
                       "product_lifetime": 10,
                       "structure_type": ["new", "retrofit"],
                       "bldg_type": ["single family home"],
                       "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                       "fuel_type": {"primary": ["electricity (grid)"],
                                     "secondary": None},
                       "fuel_switch_to": None,
                       "end_use": {"primary": ["cooling"],
                                   "secondary": None},
                       "technology_type": {"primary": "supply",
                                           "secondary": None},
                       "technology": {"primary": ["boiler (electric)"],
                                      "secondary": None}},
                      {"name": "blank measure 2",
                       "installed_cost": 10,
                       "cost_units": "2014$/unit",
                       "energy_efficiency": {"primary":
                                             {"AIA_CZ1": {"heating": 30,
                                                          "cooling": 25},
                                              "AIA_CZ2": {"heating": 30,
                                                          "cooling": 15}},
                                             "secondary": None},
                       "energy_efficiency_units": {"primary": "COP",
                                                   "secondary": None},
                       "market_entry_year": None,
                       "market_exit_year": None,
                       "product_lifetime": 10,
                       "structure_type": ["new", "retrofit"],
                       "bldg_type": ["single family home"],
                       "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                       "fuel_type": {"primary": ["electricity (grid)"],
                                     "secondary": None},
                       "fuel_switch_to": None,
                       "end_use": {"primary": ["heating", "cooling"],
                                   "secondary": None},
                       "technology_type": {"primary": "supply",
                                           "secondary": None},
                       "technology": {"primary": ["linear fluorescent (LED)",
                                                  "general service (LED)",
                                                  "external (LED)"],
                                      "secondary": None}},
                      {"name": "blank measure 3",
                       "installed_cost": 25,
                       "cost_units": "2014$/unit",
                       "energy_efficiency": {"primary": 25, "secondary": None},
                       "product_lifetime": 10,
                       "structure_type": ["new", "retrofit"],
                       "energy_efficiency_units": {"primary": "lm/W",
                                                   "secondary": None},
                       "market_entry_year": None,
                       "market_exit_year": None,
                       "bldg_type": ["single family home"],
                       "climate_zone": ["AIA_CZ1", "AIA_CZ2"],
                       "fuel_type": {"primary": ["natural gas"],
                                     "secondary": None},
                       "fuel_switch_to": None,
                       "end_use": {"primary": ["lighting"],
                                   "secondary": ["heating",
                                                 "secondary heating",
                                                 "cooling"]},
                       "technology_type": {"primary": "supply",
                                           "secondary": "demand"},
                       "technology": {"primary":
                                      ["linear fluorescent (LED)",
                                       "general service (LED)",
                                       "external (LED)"],
                                      "secondary":
                                      ["windows conduction",
                                       "windows solar"]}},
                      {"name": "blank measure 4",
                       "installed_cost": 25,
                       "cost_units": "2014$/unit",
                       "energy_efficiency": {"primary": 25, "secondary": None},
                       "product_lifetime": 10,
                       "structure_type": ["new", "retrofit"],
                       "energy_efficiency_units": {"primary": "lm/W",
                                                   "secondary": None},
                       "market_entry_year": None,
                       "market_exit_year": None,
                       "bldg_type": ["single family home"],
                       "climate_zone": "AIA_CZ1",
                       "fuel_type": {"primary": ["solar"],
                                     "secondary": None},
                       "fuel_switch_to": None,
                       "end_use": {"primary": ["lighting"],
                                   "secondary": ["heating",
                                                 "secondary heating",
                                                 "cooling"]},
                       "technology_type": {"primary": "supply",
                                           "secondary": "demand"},
                       "technology": {"primary":
                                      ["linear fluorescent (LED)",
                                       "general service (LED)",
                                       "external (LED)"],
                                      "secondary":
                                      ["windows conduction",
                                       "windows solar"]}}]

    # Master stock, energy, and cost information that should be generated by
    # "ok_measures" above using the "sample_msegin" dict
    ok_out = [{
        "stock": {
            "total": {
                "all": {"2009": 72, "2010": 72},
                "measure": {"2009": 72, "2010": 72}},
            "competed": {
                "all": {"2009": 72, "2010": 72},
                "measure": {"2009": 72, "2010": 72}}},
        "energy": {
            "total": {
                "baseline": {"2009": 229.68, "2010": 230.4},
                "efficient": {"2009": 117.0943, "2010": 117.4613}},
            "competed": {
                "baseline": {"2009": 229.68, "2010": 230.4},
                "efficient": {"2009": 117.0943, "2010": 117.4613}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 13056.63, "2010": 12941.16},
                "efficient": {"2009": 6656.461, "2010": 6597.595}},
            "competed": {
                "baseline": {"2009": 13056.63, "2010": 12941.16},
                "efficient": {"2009": 6656.461, "2010": 6597.595}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 710, "2010": 710},
                    "efficient": {"2009": 1800, "2010": 1800}},
                "competed": {
                    "baseline": {"2009": 710, "2010": 710},
                    "efficient": {"2009": 1800, "2010": 1800}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 2328.955, "2010": 2227.968},
                    "efficient": {"2009": 1187.336, "2010": 1135.851}},
                "competed": {
                    "baseline": {"2009": 2328.955, "2010": 2227.968},
                    "efficient": {"2009": 1187.336, "2010": 1135.851}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 430868.63, "2010": 427058.3},
                    "efficient": {"2009": 219663.21, "2010": 217720.65}},
                "competed": {
                    "baseline": {"2009": 430868.63, "2010": 427058.3},
                    "efficient": {"2009": 219663.21, "2010": 217720.65}}}},
        "lifetime": {"baseline": {"2009": 75, "2010": 75},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 15, "2010": 15},
                "measure": {"2009": 15, "2010": 15}},
            "competed": {
                "all": {"2009": 15, "2010": 15},
                "measure": {"2009": 15, "2010": 15}}},
        "energy": {
            "total": {
                "baseline": {"2009": 15.15, "2010": 15.15},
                "efficient": {"2009": 10.908, "2010": 10.908}},
            "competed": {
                "baseline": {"2009": 15.15, "2010": 15.15},
                "efficient": {"2009": 10.908, "2010": 10.908}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 856.2139, "2010": 832.0021},
                "efficient": {"2009": 616.474, "2010": 599.0415}},
            "competed": {
                "baseline": {"2009": 856.2139, "2010": 832.0021},
                "efficient": {"2009": 616.474, "2010": 599.0415}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 270, "2010": 270},
                    "efficient": {"2009": 375, "2010": 375}},
                "competed": {
                    "baseline": {"2009": 270, "2010": 270},
                    "efficient": {"2009": 375, "2010": 375}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 170.892, "2010": 163.317},
                    "efficient": {"2009": 123.0422, "2010": 117.5882}},
                "competed": {
                    "baseline": {"2009": 170.892, "2010": 163.317},
                    "efficient": {"2009": 123.0422, "2010": 117.5882}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 28255.06, "2010": 27456.07},
                    "efficient": {"2009": 20343.64, "2010": 19768.37}},
                "competed": {
                    "baseline": {"2009": 28255.06, "2010": 27456.07},
                    "efficient": {"2009": 20343.64, "2010": 19768.37}}}},
        "lifetime": {"baseline": {"2009": 180, "2010": 180},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 148, "2010": 148},
                "measure": {"2009": 148, "2010": 148}},
            "competed": {
                "all": {"2009": 148, "2010": 148},
                "measure": {"2009": 148, "2010": 148}}},
        "energy": {
            "total": {
                "baseline": {"2009": 648.47, "2010": 650.43},
                "efficient": {"2009": 550.0692, "2010": 551.722}},
            "competed": {
                "baseline": {"2009": 648.47, "2010": 650.43},
                "efficient": {"2009": 550.0692, "2010": 551.722}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 36855.9, "2010": 36504.45},
                "efficient": {"2009": 31262.24, "2010": 30960.7}},
            "competed": {
                "baseline": {"2009": 36855.9, "2010": 36504.45},
                "efficient": {"2009": 31262.24, "2010": 30960.7}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 2972, "2010": 2972},
                    "efficient": {"2009": 3700, "2010": 3700}},
                "competed": {
                    "baseline": {"2009": 2972, "2010": 2972},
                    "efficient": {"2009": 3700, "2010": 3700}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 6601.968, "2010": 6315.443},
                    "efficient": {"2009": 5603.723, "2010": 5360.489}},
                "competed": {
                    "baseline": {"2009": 6601.968, "2010": 6315.443},
                    "efficient": {"2009": 5603.723, "2010": 5360.489}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 1216244.58, "2010": 1204646.90},
                    "efficient": {"2009": 1031653.83, "2010": 1021703.20}},
                "competed": {
                    "baseline": {"2009": 1216244.58, "2010": 1204646.90},
                    "efficient": {"2009": 1031653.83, "2010": 1021703.20}}}},
        "lifetime": {"baseline": {"2009": 200, "2010": 200},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 1600, "2010": 2000},
                "measure": {"2009": 1600, "2010": 2000}},
            "competed": {
                "all": {"2009": 1600, "2010": 2000},
                "measure": {"2009": 1600, "2010": 2000}}},
        "energy": {
            "total": {
                "baseline": {"2009": 12.76, "2010": 12.8},
                "efficient": {"2009": 3.509, "2010": 3.52}},
            "competed": {
                "baseline": {"2009": 12.76, "2010": 12.8},
                "efficient": {"2009": 3.509, "2010": 3.52}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 725.3681, "2010": 718.9534},
                "efficient": {"2009": 199.4762, "2010": 197.7122}},
            "competed": {
                "baseline": {"2009": 725.3681, "2010": 718.9534},
                "efficient": {"2009": 199.4762, "2010": 197.7122}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 20400, "2010": 24600},
                    "efficient": {"2009": 16000, "2010": 20000}},
                "competed": {
                    "baseline": {"2009": 20400, "2010": 24600},
                    "efficient": {"2009": 16000, "2010": 20000}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 129.3864, "2010": 123.776},
                    "efficient": {"2009": 35.58126, "2010": 34.0384}},
                "competed": {
                    "baseline": {"2009": 129.3864, "2010": 123.776},
                    "efficient": {"2009": 35.58126, "2010": 34.0384}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 23937.15, "2010": 23725.46},
                    "efficient": {"2009": 6582.715, "2010": 6524.502}},
                "competed": {
                    "baseline": {"2009": 23937.15, "2010": 23725.46},
                    "efficient": {"2009": 6582.715, "2010": 6524.502}}}},
        "lifetime": {"baseline": {"2009": 105, "2010": 105},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 600, "2010": 800},
                "measure": {"2009": 600, "2010": 800}},
            "competed": {
                "all": {"2009": 600, "2010": 800},
                "measure": {"2009": 600, "2010": 800}}},
        "energy": {
            "total": {
                "baseline": {"2009": 6.38, "2010": 6.4},
                "efficient": {"2009": 3.19, "2010": 3.2}},
            "competed": {
                "baseline": {"2009": 6.38, "2010": 6.4},
                "efficient": {"2009": 3.19, "2010": 3.2}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 362.684, "2010": 359.4767},
                "efficient": {"2009": 181.342, "2010": 179.7383}},
            "competed": {
                "baseline": {"2009": 362.684, "2010": 359.4767},
                "efficient": {"2009": 181.342, "2010": 179.7383}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 1200, "2010": 1600},
                    "efficient": {"2009": 6000, "2010": 8000}},
                "competed": {
                    "baseline": {"2009": 1200, "2010": 1600},
                    "efficient": {"2009": 6000, "2010": 8000}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 64.6932, "2010": 61.888},
                    "efficient": {"2009": 32.3466, "2010": 30.944}},
                "competed": {
                    "baseline": {"2009": 64.6932, "2010": 61.888},
                    "efficient": {"2009": 32.3466, "2010": 30.944}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 11968.57, "2010": 11862.73},
                    "efficient": {"2009": 5984.287, "2010": 5931.365}},
                "competed": {
                    "baseline": {"2009": 11968.57, "2010": 11862.73},
                    "efficient": {"2009": 5984.287, "2010": 5931.365}}}},
        "lifetime": {"baseline": {"2009": 20, "2010": 20},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 600, "2010": 800},
                "measure": {"2009": 600, "2010": 800}},
            "competed": {
                "all": {"2009": 600, "2010": 800},
                "measure": {"2009": 600, "2010": 800}}},
        "energy": {
            "total": {
                "baseline": {"2009": 146.74, "2010": 147.2},
                "efficient": {"2009": 55.29333, "2010": 55.46667}},
            "competed": {
                "baseline": {"2009": 146.74, "2010": 147.2},
                "efficient": {"2009": 55.29333, "2010": 55.46667}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 8341.733, "2010": 8267.964},
                "efficient": {"2009": 3143.262, "2010": 3115.465}},
            "competed": {
                "baseline": {"2009": 8341.733, "2010": 8267.964},
                "efficient": {"2009": 3143.262, "2010": 3115.465}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 3100, "2010": 4133.33},
                    "efficient": {"2009": 6000, "2010": 8000}},
                "competed": {
                    "baseline": {"2009": 3100, "2010": 4133.33},
                    "efficient": {"2009": 6000, "2010": 8000}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 1487.944, "2010": 1423.424},
                    "efficient": {"2009": 560.6744, "2010": 536.3627}},
                "competed": {
                    "baseline": {"2009": 1487.944, "2010": 1423.424},
                    "efficient": {"2009": 560.6744, "2010": 536.3627}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 275277.18, "2010": 272842.8},
                    "efficient": {"2009": 103727.63, "2010": 102810.33}},
                "competed": {
                    "baseline": {"2009": 275277.18, "2010": 272842.8},
                    "efficient": {"2009": 103727.63, "2010": 102810.33}}}},
        "lifetime": {"baseline": {"2009": 51.67, "2010": 51.67},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 600, "2010": 800},
                "measure": {"2009": 600, "2010": 800}},
            "competed": {
                "all": {"2009": 600, "2010": 800},
                "measure": {"2009": 600, "2010": 800}}},
        "energy": {
            "total": {
                "baseline": {"2009": 146.74, "2010": 147.2},
                "efficient": {"2009": 52.10333, "2010": 52.26667}},
            "competed": {
                "baseline": {"2009": 146.74, "2010": 147.2},
                "efficient": {"2009": 52.10333, "2010": 52.26667}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 8341.733, "2010": 8267.964},
                "efficient": {"2009": 2961.92, "2010": 2935.726}},
            "competed": {
                "baseline": {"2009": 8341.733, "2010": 8267.964},
                "efficient": {"2009": 2961.92, "2010": 2935.726}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 3100, "2010": 4133.33},
                    "efficient": {"2009": 6000, "2010": 8000}},
                "competed": {
                    "baseline": {"2009": 3100, "2010": 4133.33},
                    "efficient": {"2009": 6000, "2010": 8000}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 1487.944, "2010": 1423.424},
                    "efficient": {"2009": 528.3278, "2010": 505.4187}},
                "competed": {
                    "baseline": {"2009": 1487.944, "2010": 1423.424},
                    "efficient": {"2009": 528.3278, "2010": 505.4187}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 275277.18, "2010": 272842.8},
                    "efficient": {"2009": 97743.35, "2010": 96878.97}},
                "competed": {
                    "baseline": {"2009": 275277.18, "2010": 272842.8},
                    "efficient": {"2009": 97743.35, "2010": 96878.97}}}},
        "lifetime": {"baseline": {"2009": 51.67, "2010": 51.67},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 11, "2010": 11},
                "measure": {"2009": 11, "2010": 11}},
            "competed": {
                "all": {"2009": 11, "2010": 11},
                "measure": {"2009": 11, "2010": 11}}},
        "energy": {
            "total": {
                "baseline": {"2009": 76.56, "2010": 76.8},
                "efficient": {"2009": 62.524, "2010": 62.72}},
            "competed": {
                "baseline": {"2009": 76.56, "2010": 76.8},
                "efficient": {"2009": 62.524, "2010": 62.72}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 4352.208, "2010": 4313.72},
                "efficient": {"2009": 3554.304, "2010": 3522.872}},
            "competed": {
                "baseline": {"2009": 4352.208, "2010": 4313.72},
                "efficient": {"2009": 3554.304, "2010": 3522.872}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 154, "2010": 154},
                    "efficient": {"2009": 275, "2010": 275}},
                "competed": {
                    "baseline": {"2009": 154, "2010": 154},
                    "efficient": {"2009": 275, "2010": 275}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 695.1648, "2010": 656.64},
                    "efficient": {"2009": 567.7179, "2010": 536.256}},
                "competed": {
                    "baseline": {"2009": 695.1648, "2010": 656.64},
                    "efficient": {"2009": 567.7179, "2010": 536.256}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 143622.88, "2010": 142352.77},
                    "efficient": {"2009": 117292.02, "2010": 116254.76}},
                "competed": {
                    "baseline": {"2009": 143622.88, "2010": 142352.77},
                    "efficient": {"2009": 117292.02, "2010": 116254.76}}}},
        "lifetime": {"baseline": {"2009": 140, "2010": 140},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 1.5, "2010": 2.25},
                "measure": {"2009": 1.5, "2010": 2.25}},
            "competed": {
                "all": {"2009": 1.5, "2010": 2.25},
                "measure": {"2009": 1.5, "2010": 2.25}}},
        "energy": {
            "total": {
                "baseline": {"2009": 1.515, "2010": 2.2725},
                "efficient": {"2009": 1.0908, "2010": 1.6362}},
            "competed": {
                "baseline": {"2009": 1.515, "2010": 2.2725},
                "efficient": {"2009": 1.0908, "2010": 1.6362}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 85.62139, "2010": 124.8003},
                "efficient": {"2009": 61.6474, "2010": 89.85622}},
            "competed": {
                "baseline": {"2009": 85.62139, "2010": 124.8003},
                "efficient": {"2009": 61.6474, "2010": 89.85622}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 27, "2010": 40.5},
                    "efficient": {"2009": 37.5, "2010": 56.25}},
                "competed": {
                    "baseline": {"2009": 27, "2010": 40.5},
                    "efficient": {"2009": 37.5, "2010": 56.25}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 17.0892, "2010": 24.49755},
                    "efficient": {"2009": 12.30422, "2010": 17.63823}},
                "competed": {
                    "baseline": {"2009": 17.0892, "2010": 24.49755},
                    "efficient": {"2009": 12.30422, "2010": 17.63823}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 2825.506, "2010": 4118.409},
                    "efficient": {"2009": 2034.364, "2010": 2965.256}},
                "competed": {
                    "baseline": {"2009": 2825.506, "2010": 4118.409},
                    "efficient": {"2009": 2034.364, "2010": 2965.256}}}},
        "lifetime": {"baseline": {"2009": 180, "2010": 180},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 13.5, "2010": 12.75},
                "measure": {"2009": 13.5, "2010": 12.75}},
            "competed": {
                "all": {"2009": 13.5, "2010": 12.75},
                "measure": {"2009": 13.5, "2010": 12.75}}},
        "energy": {
            "total": {
                "baseline": {"2009": 13.635, "2010": 12.8775},
                "efficient": {"2009": 9.8172, "2010": 9.2718}},
            "competed": {
                "baseline": {"2009": 13.635, "2010": 12.8775},
                "efficient": {"2009": 9.8172, "2010": 9.2718}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 770.5925, "2010": 707.2018},
                "efficient": {"2009": 554.8266, "2010": 509.1853}},
            "competed": {
                "baseline": {"2009": 770.5925, "2010": 707.2018},
                "efficient": {"2009": 554.8266, "2010": 509.1853}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 243, "2010": 229.5},
                    "efficient": {"2009": 337.5, "2010": 318.75}},
                "competed": {
                    "baseline": {"2009": 243, "2010": 229.5},
                    "efficient": {"2009": 337.5, "2010": 318.75}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 153.8028, "2010": 138.8195},
                    "efficient": {"2009": 110.738, "2010": 99.94998}},
                "competed": {
                    "baseline": {"2009": 153.8028, "2010": 138.8195},
                    "efficient": {"2009": 110.738, "2010": 99.94998}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 25429.55, "2010": 23337.66},
                    "efficient": {"2009": 18309.28, "2010": 16803.11}},
                "competed": {
                    "baseline": {"2009": 25429.55, "2010": 23337.66},
                    "efficient": {"2009": 18309.28, "2010": 16803.11}}}},
        "lifetime": {"baseline": {"2009": 180, "2010": 180},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 148, "2010": 148},
                "measure": {"2009": 0, "2010": 148}},
            "competed": {
                "all": {"2009": 0, "2010": 148},
                "measure": {"2009": 0, "2010": 148}}},
        "energy": {
            "total": {
                "baseline": {"2009": 648.47, "2010": 650.43},
                "efficient": {"2009": 648.47, "2010": 551.722}},
            "competed": {
                "baseline": {"2009": 0, "2010": 650.43},
                "efficient": {"2009": 0, "2010": 551.722}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 36855.9, "2010": 36504.45},
                "efficient": {"2009": 36855.9, "2010": 30960.7}},
            "competed": {
                "baseline": {"2009": 0, "2010": 36504.45},
                "efficient": {"2009": 0, "2010": 30960.7}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 2972, "2010": 2972},
                    "efficient": {"2009": 2972, "2010": 3700}},
                "competed": {
                    "baseline": {"2009": 0, "2010": 2972},
                    "efficient": {"2009": 0, "2010": 3700}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 6601.968, "2010": 6315.443},
                    "efficient": {"2009": 6601.968, "2010": 5360.489}},
                "competed": {
                    "baseline": {"2009": 0, "2010": 6315.443},
                    "efficient": {"2009": 0, "2010": 5360.489}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 1216244.58, "2010": 1204646.90},
                    "efficient": {"2009": 1216244.58, "2010": 1021703.20}},
                "competed": {
                    "baseline": {"2009": 0, "2010": 1204646.90},
                    "efficient": {"2009": 0, "2010": 1021703.20}}}},
        "lifetime": {"baseline": {"2009": 200, "2010": 200},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 148, "2010": 148},
                "measure": {"2009": 148, "2010": 140.6}},
            "competed": {
                "all": {"2009": 148, "2010": 0},
                "measure": {"2009": 148, "2010": 0}}},
        "energy": {
            "total": {
                "baseline": {"2009": 648.47, "2010": 650.43},
                "efficient": {"2009": 550.0692, "2010": 551.722}},
            "competed": {
                "baseline": {"2009": 648.47, "2010": 0},
                "efficient": {"2009": 550.0692, "2010": 0}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 36855.9, "2010": 36504.45},
                "efficient": {"2009": 31262.24, "2010": 30960.7}},
            "competed": {
                "baseline": {"2009": 36855.9, "2010": 0},
                "efficient": {"2009": 31262.24, "2010": 0}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 2972, "2010": 2972},
                    "efficient": {"2009": 3700, "2010": 3663.6}},
                "competed": {
                    "baseline": {"2009": 2972, "2010": 0},
                    "efficient": {"2009": 3700, "2010": 0}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 6601.968, "2010": 6315.443},
                    "efficient": {"2009": 5603.723, "2010": 5360.489}},
                "competed": {
                    "baseline": {"2009": 6601.968, "2010": 0},
                    "efficient": {"2009": 5603.723, "2010": 0}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 1216244.58, "2010": 1204646.90},
                    "efficient": {"2009": 1031653.83, "2010": 1021703.198}},
                "competed": {
                    "baseline": {"2009": 1216244.58, "2010": 0},
                    "efficient": {"2009": 1031653.83, "2010": 0}}}},
        "lifetime": {"baseline": {"2009": 200, "2010": 200},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 148, "2010": 148},
                "measure": {"2009": 148, "2010": 148}},
            "competed": {
                "all": {"2009": 148, "2010": 148},
                "measure": {"2009": 148, "2010": 148}}},
        "energy": {
            "total": {
                "baseline": {"2009": 870.17, "2010": 872.73},
                "efficient": {"2009": 742.209, "2010": 729.562}},
            "competed": {
                "baseline": {"2009": 870.17, "2010": 872.73},
                "efficient": {"2009": 742.209, "2010": 729.562}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 49448.84, "2010": 48952.76},
                "efficient": {"2009": 42176.13, "2010": 40919.35}},
            "competed": {
                "baseline": {"2009": 49448.84, "2010": 48952.76},
                "efficient": {"2009": 42176.13, "2010": 40919.35}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 2972, "2010": 2972},
                    "efficient": {"2009": 3700, "2010": 3700}},
                "competed": {
                    "baseline": {"2009": 2972, "2010": 2972},
                    "efficient": {"2009": 3700, "2010": 3700}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 8884.55, "2010": 8498.72},
                    "efficient": {"2009": 7581.96, "2010": 7107.11}},
                "competed": {
                    "baseline": {"2009": 8884.55, "2010": 8498.72},
                    "efficient": {"2009": 7581.96, "2010": 7107.11}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 1631811.885, "2010": 1615440.956},
                    "efficient": {"2009": 1391812.161, "2010": 1350338.441}},
                "competed": {
                    "baseline": {"2009": 1631811.885, "2010": 1615440.956},
                    "efficient": {"2009": 1391812.161, "2010": 1350338.441}}}},
        "lifetime": {"baseline": {"2009": 200, "2010": 200},
                     "measure": 10}},
              {
        "stock": {
            "total": {
                "all": {"2009": 15, "2010": 15},
                "measure": {"2009": 15, "2010": 15}},
            "competed": {
                "all": {"2009": 15, "2010": 15},
                "measure": {"2009": 15, "2010": 15}}},
        "energy": {
            "total": {
                "baseline": {"2009": 15.15, "2010": 15.15},
                "efficient": {"2009": 34.452, "2010": 34.56}},
            "competed": {
                "baseline": {"2009": 15.15, "2010": 15.15},
                "efficient": {"2009": 34.452, "2010": 34.56}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 856.2139, "2010": 832.0021},
                "efficient": {"2009": 1958.494, "2010": 1941.174}},
            "competed": {
                "baseline": {"2009": 856.2139, "2010": 832.0021},
                "efficient": {"2009": 1958.494, "2010": 1941.174}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 270, "2010": 270},
                    "efficient": {"2009": 375, "2010": 375}},
                "competed": {
                    "baseline": {"2009": 270, "2010": 270},
                    "efficient": {"2009": 375, "2010": 375}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 170.892, "2010": 163.317},
                    "efficient": {"2009": 349.3433, "2010": 334.1952}},
                "competed": {
                    "baseline": {"2009": 170.892, "2010": 163.317},
                    "efficient": {"2009": 349.3433, "2010": 334.1952}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 28255.06, "2010": 27456.07},
                    "efficient": {"2009": 64630.29, "2010": 64058.75}},
                "competed": {
                    "baseline": {"2009": 28255.06, "2010": 27456.07},
                    "efficient": {"2009": 64630.29, "2010": 64058.75}}}},
        "lifetime": {"baseline": {"2009": 180, "2010": 180},
                     "measure": 10}}]

    # Set the consumer choice dicts that should be generated by the
    # first two "ok_measures" above using the "sample_msegin" dict.
    # Consumer choice information is needed to apportion all measures
    # competing for a baseline microsegment to appropriate market shares
    compete_choice_val = {
        "b1": {"2009": None, "2010": None},
        "b2": {"2009": None, "2010": None}}
    ok_out_compete_choice = [{
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'heating', 'supply',
        'boiler (electric)', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'heating', 'supply', 'ASHP', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'heating', 'supply', 'GSHP', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'ASHP', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'GSHP', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'room AC', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'heating', 'supply',
        'boiler (electric)', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'heating', 'supply', 'ASHP', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'heating', 'supply', 'GSHP', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'ASHP', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'GSHP', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'room AC', 'new')""": compete_choice_val,
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'heating', 'supply',
        'boiler (electric)', 'retrofit')""": compete_choice_val,
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'heating', 'supply', 'ASHP', 'retrofit')""": compete_choice_val,
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'heating', 'supply', 'GSHP', 'retrofit')""": compete_choice_val,
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'ASHP', 'retrofit')""": compete_choice_val,
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'GSHP', 'retrofit')""": compete_choice_val,
        """('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'room AC', 'retrofit')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'heating', 'supply', 
        'boiler (electric)', 'retrofit')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'heating', 'supply', 'ASHP', 'retrofit')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'heating', 'supply', 'GSHP', 'retrofit')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'ASHP', 'retrofit')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'GSHP', 'retrofit')""": compete_choice_val,
        """('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)',
        'cooling', 'supply', 'room AC', 'retrofit')""": compete_choice_val},
        {"""('primary', 'AIA_CZ1', 'single family home', 'natural gas',
        'water heating', 'supply', '','new')""": compete_choice_val}]

    # Master supply-demand adjustment dicts that should be generated by
    # the first two "ok_measures" above using the "sample_msegin" dict.
    # Supply-demand adjustment information is needed to account for overlaps
    # between measures that access supply-side and demand-side microsegments
    # for the heating and cooling end uses.
    ok_out_compete_demand = [{
        "savings": {
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'boiler (electric)', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'ASHP', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'GSHP', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'ASHP', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'GSHP', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'room AC', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'boiler (electric)', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'ASHP', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'GSHP', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'ASHP', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'GSHP', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'room AC', 'new')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'boiler (electric)', 'retrofit')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'ASHP', 'retrofit')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'GSHP', 'retrofit')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'ASHP', 'retrofit')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'GSHP', 'retrofit')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'room AC', 'retrofit')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'boiler (electric)', 'retrofit')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'ASHP', 'retrofit')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'GSHP', 'retrofit')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'ASHP', 'retrofit')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'GSHP', 'retrofit')": {"2009": 0, "2010": 0},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'room AC', 'retrofit')": {"2009": 0, "2010": 0}},
        "total": {
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'boiler (electric)', 'new')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'ASHP', 'new')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'GSHP', 'new')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'ASHP', 'new')": {"2009": 108.46, "2010": 108.8},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'GSHP', 'new')": {"2009": 108.46, "2010": 108.8},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'room AC', 'new')": {"2009": 108.46, "2010": 108.8},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'boiler (electric)', 'new')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'ASHP', 'new')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'GSHP', 'new')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'ASHP', 'new')": {"2009": 108.46, "2010": 108.8},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'GSHP', 'new')": {"2009": 108.46, "2010": 108.8},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'room AC', 'new')": {"2009": 108.46, "2010": 108.8},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'boiler (electric)', 'retrofit')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'ASHP', 'retrofit')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'heating', 'supply', 'GSHP', 'retrofit')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'ASHP', 'retrofit')": {"2009": 108.46, "2010": 108.8},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'GSHP', 'retrofit')": {"2009": 108.46, "2010": 108.8},
            "('primary', 'AIA_CZ1', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'room AC', 'retrofit')": {"2009": 108.46, "2010": 108.8},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'boiler (electric)', 'retrofit')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'ASHP', 'retrofit')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'heating', 'supply', 'GSHP', 'retrofit')": {"2009": 28.71, "2010": 28.80},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'ASHP', 'retrofit')": {"2009": 108.46, "2010": 108.8},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'GSHP', 'retrofit')": {"2009": 108.46, "2010": 108.8},
            "('primary', 'AIA_CZ2', 'single family home', 'electricity (grid)', 'cooling', 'supply', 'room AC', 'retrofit')": {"2009": 108.46, "2010": 108.8}}},
        {"savings": {},
         "total": {}}]

    # Means and sampling Ns for energy, cost, and lifetime that should be
    # generated by "ok_measures_dist" above using the "sample_msegin" dict
    ok_out_dist = [[121.74, 50, 1844.58, 50, 10, 1],
                   [11.61, 50, 379.91, 50, 10.03, 50],
                   [57.20, 50, 6017.91, 50, 10, 1]]

    # Master stock, energy, and cost information that should be generated by
    # "partial_measures" above using the "sample_msegin" dict
    partial_out = [{
        "stock": {
            "total": {
                "all": {"2009": 18, "2010": 18},
                "measure": {"2009": 18, "2010": 18}},
            "competed": {
                "all": {"2009": 18, "2010": 18},
                "measure": {"2009": 18, "2010": 18}}},
        "energy": {
            "total": {
                "baseline": {"2009": 57.42, "2010": 57.6},
                "efficient": {"2009": 27.5616, "2010": 27.648}},
            "competed": {
                "baseline": {"2009": 57.42, "2010": 57.6},
                "efficient": {"2009": 27.5616, "2010": 27.648}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 3264.156, "2010": 3235.29},
                "efficient": {"2009": 1566.795, "2010": 1552.939}},
            "competed": {
                "baseline": {"2009": 3264.156, "2010": 3235.29},
                "efficient": {"2009": 1566.795, "2010": 1552.939}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 216, "2010": 216},
                    "efficient": {"2009": 450, "2010": 450}},
                "competed": {
                    "baseline": {"2009": 216, "2010": 216},
                    "efficient": {"2009": 450, "2010": 450}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 582.2388, "2010": 556.992},
                    "efficient": {"2009": 279.4746, "2010": 267.3562}},
                "competed": {
                    "baseline": {"2009": 582.2388, "2010": 556.992},
                    "efficient": {"2009": 279.4746, "2010": 267.3562}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 107717.16, "2010": 106764.58},
                    "efficient": {"2009": 51704.24, "2010": 51247}},
                "competed": {
                    "baseline": {"2009": 107717.16, "2010": 106764.58},
                    "efficient": {"2009": 51704.24, "2010": 51247}}}},
        "lifetime": {"baseline": {"2009": 120, "2010": 120},
                     "measure": 10}},
        {
        "stock": {
            "total": {
                "all": {"2009": 52, "2010": 52},
                "measure": {"2009": 52, "2010": 52}},
            "competed": {
                "all": {"2009": 52, "2010": 52},
                "measure": {"2009": 52, "2010": 52}}},
        "energy": {
            "total": {
                "baseline": {"2009": 165.88, "2010": 166.4},
                "efficient": {"2009": 67.1176, "2010": 67.328}},
            "competed": {
                "baseline": {"2009": 165.88, "2010": 166.4},
                "efficient": {"2009": 67.1176, "2010": 67.328}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 9429.785, "2010": 9346.394},
                "efficient": {"2009": 3815.436, "2010": 3781.695}},
            "competed": {
                "baseline": {"2009": 9429.785, "2010": 9346.394},
                "efficient": {"2009": 3815.436, "2010": 3781.695}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 526, "2010": 526},
                    "efficient": {"2009": 1300, "2010": 1300}},
                "competed": {
                    "baseline": {"2009": 526, "2010": 526},
                    "efficient": {"2009": 1300, "2010": 1300}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 1682.023, "2010": 1609.088},
                    "efficient": {"2009": 680.5725, "2010": 651.0618}},
                "competed": {
                    "baseline": {"2009": 1682.023, "2010": 1609.088},
                    "efficient": {"2009": 680.5725, "2010": 651.0618}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 311182.9, "2010": 308431},
                    "efficient": {"2009": 125909.39, "2010": 124795.93}},
                "competed": {
                    "baseline": {"2009": 311182.9, "2010": 308431},
                    "efficient": {"2009": 125909.39, "2010": 124795.93}}}},
        "lifetime": {"baseline": {"2009": 80, "2010": 80},
                     "measure": 10}}]

    # Test for correct output from "ok_measures" input
    def test_mseg_ok(self):
        # Adjust maxDiff parameter to ensure that any dict key discrepancies
        # revealed by the test are fully reported
        self.maxDiff = None
        for idx, measure in enumerate(self.ok_measures):
            # Create an instance of the object based on ok measure info
            measure_instance = run.Measure(**measure)
            # Assert that the first output of mseg_find partition (master
            # microsegment information) is correct
            dict_base = measure_instance.mseg_find_partition(
                self.sample_msegin, self.sample_basein,
                "Technical potential")
            dict1 = dict_base[0]
            dict2 = self.ok_out[idx]
            self.dict_check(dict1, dict2)

            # Assert that the consumer choice paramaters and supply-demand
            # adjustment information in the second output of
            # mseg_find_partition is correct (limit this check to the first
            # two sample measures only to reduce computation time)
            if idx < 2:
                # Consumer choice parameters output check
                dict3 = dict_base[1]["competed choice parameters"]
                dict4 = self.ok_out_compete_choice[idx]
                self.dict_check(dict3, dict4)
                # Supply-demand adjustment output check
                dict5 = dict_base[1]["supply-demand adjustment"]
                dict6 = self.ok_out_compete_demand[idx]
                self.dict_check(dict5, dict6)

    # Test for correct output from "ok_measures_dist" input
    def test_mseg_ok_distrib(self):
        # Seed random number generator to yield repeatable results
        numpy.random.seed(1234)
        for idx, measure in enumerate(self.ok_measures_dist):
            # Create an instance of the object based on ok_dist measure info
            measure_instance = run.Measure(**measure)
            # Generate lists of energy and cost output values
            test_outputs = measure_instance.mseg_find_partition(
                self.sample_msegin, self.sample_basein,
                "Technical potential")[0]
            test_e = test_outputs["energy"]["total"]["efficient"]["2009"]
            test_c = test_outputs[
                "cost"]["stock"]["total"]["efficient"]["2009"]
            test_l = test_outputs["lifetime"]["measure"]
            if type(test_l) == float:
                test_l = [test_l]
            # Calculate mean values from output lists for testing
            param_e = round(sum(test_e) / len(test_e), 2)
            param_c = round(sum(test_c) / len(test_c), 2)
            param_l = round(sum(test_l) / len(test_l), 2)
            # Check mean values and length of output lists to ensure correct
            self.assertEqual([param_e, len(test_e), param_c, len(test_c),
                              param_l, len(test_l)],
                             self.ok_out_dist[idx])

    # Test for correct output from "partial_measures" input
    def test_mseg_partial(self):
        for idx, measure in enumerate(self.partial_measures):
            # Create an instance of the object based on partial measure info
            measure_instance = run.Measure(**measure)
            # Assert output dict is correct
            dict1 = measure_instance.mseg_find_partition(
                self.sample_msegin,
                self.sample_basein,
                "Technical potential")[0]
            dict2 = self.partial_out[idx]
            self.dict_check(dict1, dict2)

    # Test for correct output from "blank_measures" input
    def test_mseg_blank(self):
        for idx, measure in enumerate(self.blank_measures):
            # Create an instance of the object based on blank measure info
            measure_instance = run.Measure(**measure)
            # Assert output dict is correct
            with self.assertRaises(KeyError):
                measure_instance.mseg_find_partition(
                    self.sample_msegin,
                    self.sample_basein,
                    "Technical potential")


class PrioritizationMetricsTest(unittest.TestCase, CommonMethods):
    """ Test the operation of the calc_metric_update function to
    verify measure master microsegment inputs yield expected savings
    and prioritization metrics outputs """

    # Set compete measures to True to ensure the full range of measure
    # outputs are calculated
    adjust_savings = True

    # Discount rate used for testing
    ok_rate = 0.07

    # Create an "ok" master microsegment input dict with all point
    # values to use in calculating savings and prioritization metrics
    # outputs to be tested
    ok_master_mseg_point = {
        "stock": {
            "total": {
                "all": {"2009": 10, "2010": 20},
                "measure": {"2009": 15, "2010": 25}},
            "competed": {
                "all": {"2009": 5, "2010": 10},
                "measure": {"2009": 5, "2010": 10}}},
        "energy": {
            "total": {
                "baseline": {"2009": 20, "2010": 30},
                "efficient": {"2009": 5, "2010": 10}},
            "competed": {
                "baseline": {"2009": 10, "2010": 15},
                "efficient": {"2009": 0, "2010": 5}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 200, "2010": 300},
                "efficient": {"2009": 50, "2010": 100}},
            "competed": {
                "baseline": {"2009": 100, "2010": 150},
                "efficient": {"2009": 50, "2010": 100}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 10, "2010": 15},
                    "efficient": {"2009": 15, "2010": 25}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 15},
                    "efficient": {"2009": 15, "2010": 25}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 35},
                    "efficient": {"2009": 10, "2010": 20}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 35},
                    "efficient": {"2009": 10, "2010": 20}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 40},
                    "efficient": {"2009": 25, "2010": 25}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 40},
                    "efficient": {"2009": 25, "2010": 25}}}},
        "lifetime": {
            "baseline": {"2009": 1, "2010": 1},
            "measure": 2}}

    # Create an "ok" master microsegment input dict with arrays for
    # measure energy use/cost and carbon emitted/cost to use in calculating
    # savings and prioritization metrics outputs to be tested
    ok_master_mseg_dist1 = {
        "stock": {
            "total": {
                "all": {"2009": 10, "2010": 20},
                "measure": {"2009": 15, "2010": 25}},
            "competed": {
                "all": {"2009": 5, "2010": 10},
                "measure": {"2009": 5, "2010": 10}}},
        "energy": {
            "total": {
                "baseline": {"2009": 20, "2010": 30},
                "efficient": {
                    "2009": numpy.array([1.6, 2.7, 3.1, 6, 5.1]),
                    "2010": numpy.array([10.6, 9.5, 8.1, 11, 12.4])}},
            "competed": {
                "baseline": {"2009": 10, "2010": 15},
                "efficient": {
                    "2009": numpy.array([0.6, 0.7, 0.1, 1.6, 0.1]),
                    "2010": numpy.array([3.6, 4.5, 6.1, 5, 5.4])}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 200, "2010": 300},
                "efficient": {
                    "2009": numpy.array([50.6, 57.7, 58.1, 50, 51.1]),
                    "2010": numpy.array([100.6, 108.7, 105.1, 105, 106.1])}},
            "competed": {
                "baseline": {"2009": 100, "2010": 150},
                "efficient": {
                    "2009": numpy.array([50.6, 57.7, 58.1, 50, 51.1]),
                    "2010": numpy.array([100.6, 108.7, 105.1, 105, 106.1])}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 10, "2010": 15},
                    "efficient": {"2009": 15, "2010": 25}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 15},
                    "efficient": {"2009": 15, "2010": 25}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 35},
                    "efficient": {
                        "2009": numpy.array([9.1, 8.7, 7.7, 11.2, 12.5]),
                        "2010": numpy.array([20.1, 18.7, 21.7, 21.2, 22.5])}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 35},
                    "efficient": {
                        "2009": numpy.array([9.1, 8.7, 7.7, 11.2, 12.5]),
                        "2010": numpy.array([20.1, 18.7, 21.7, 21.2, 22.5])}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 40},
                    "efficient": {
                        "2009": numpy.array([25.1, 24.7, 23.7, 31.2, 18.5]),
                        "2010": numpy.array([
                            20.1, 18.7, 21.7, 21.2, 22.5])}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 40},
                    "efficient": {
                        "2009": numpy.array([25.1, 24.7, 23.7, 31.2, 18.5]),
                        "2010": numpy.array([
                            20.1, 18.7, 21.7, 21.2, 22.5])}}}},
        "lifetime": {
            "baseline": {"2009": 1, "2010": 1},
            "measure": 2}}

    # Create an "ok" master microsegment input dict with arrays for
    # measure capital cost to use in calculating savings and prioritization
    # metrics outputs to be tested
    ok_master_mseg_dist2 = {
        "stock": {
            "total": {
                "all": {"2009": 10, "2010": 20},
                "measure": {"2009": 15, "2010": 25}},
            "competed": {
                "all": {"2009": 5, "2010": 10},
                "measure": {"2009": 5, "2010": 10}}},
        "energy": {
            "total": {
                "baseline": {"2009": 20, "2010": 30},
                "efficient": {"2009": 5, "2010": 10}},
            "competed": {
                "baseline": {"2009": 10, "2010": 15},
                "efficient": {"2009": 0, "2010": 5}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 200, "2010": 300},
                "efficient": {"2009": 50, "2010": 100}},
            "competed": {
                "baseline": {"2009": 100, "2010": 150},
                "efficient": {"2009": 50, "2010": 100}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 10, "2010": 15},
                    "efficient": {
                        "2009": numpy.array([15.1, 12.7, 14.1, 14.2, 15.5]),
                        "2010": numpy.array([20.1, 18.7, 21.7, 19.2, 20.5])
                    }},
                "competed": {
                    "baseline": {"2009": 10, "2010": 15},
                    "efficient": {
                        "2009": numpy.array([15.1, 12.7, 14.1, 14.2, 15.5]),
                        "2010": numpy.array([20.1, 18.7, 21.7, 19.2, 20.5])
                    }}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 35},
                    "efficient": {"2009": 10, "2010": 20}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 35},
                    "efficient": {"2009": 10, "2010": 20}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 40},
                    "efficient": {"2009": 25, "2010": 25}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 40},
                    "efficient": {"2009": 25, "2010": 25}}}},
        "lifetime": {
            "baseline": {"2009": 1, "2010": 1},
            "measure": 2}}

    # Create an "ok" master microsegment input dict with arrays for
    # measure lifetime to use in calculating savings and prioritization
    # metrics outputs to be tested
    ok_master_mseg_dist3 = {
        "stock": {
            "total": {
                "all": {"2009": 10, "2010": 20},
                "measure": {"2009": 15, "2010": 25}},
            "competed": {
                "all": {"2009": 5, "2010": 10},
                "measure": {"2009": 5, "2010": 10}}},
        "energy": {
            "total": {
                "baseline": {"2009": 20, "2010": 30},
                "efficient": {"2009": 5, "2010": 10}},
            "competed": {
                "baseline": {"2009": 10, "2010": 15},
                "efficient": {"2009": 0, "2010": 5}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 200, "2010": 300},
                "efficient": {"2009": 50, "2010": 100}},
            "competed": {
                "baseline": {"2009": 100, "2010": 150},
                "efficient": {"2009": 50, "2010": 100}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 10, "2010": 15},
                    "efficient": {"2009": 15, "2010": 25}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 15},
                    "efficient": {"2009": 15, "2010": 25}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 35},
                    "efficient": {"2009": 10, "2010": 20}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 35},
                    "efficient": {"2009": 10, "2010": 20}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 40},
                    "efficient": {"2009": 25, "2010": 25}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 40},
                    "efficient": {"2009": 25, "2010": 25}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": numpy.array([0.5, 1.2, 2.1, 2.2, 5.6])}}

    # Create an "ok" master microsegment input dict with arrays for
    # measure capital cost and lifetime to use in calculating savings
    # and prioritization metrics outputs to be tested
    ok_master_mseg_dist4 = {
        "stock": {
            "total": {
                "all": {"2009": 10, "2010": 20},
                "measure": {"2009": 15, "2010": 25}},
            "competed": {
                "all": {"2009": 5, "2010": 10},
                "measure": {"2009": 5, "2010": 10}}},
        "energy": {
            "total": {
                "baseline": {"2009": 20, "2010": 30},
                "efficient": {"2009": 5, "2010": 10}},
            "competed": {
                "baseline": {"2009": 10, "2010": 15},
                "efficient": {"2009": 0, "2010": 5}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 200, "2010": 300},
                "efficient": {"2009": 50, "2010": 100}},
            "competed": {
                "baseline": {"2009": 100, "2010": 150},
                "efficient": {"2009": 50, "2010": 100}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 10, "2010": 15},
                    "efficient": {
                        "2009": numpy.array([15.1, 12.7, 14.1, 14.2, 15.5]),
                        "2010": numpy.array([20.1, 18.7, 21.7, 19.2, 20.5])
                    }},
                "competed": {
                    "baseline": {"2009": 10, "2010": 15},
                    "efficient": {
                        "2009": numpy.array([15.1, 12.7, 14.1, 14.2, 15.5]),
                        "2010": numpy.array([20.1, 18.7, 21.7, 19.2, 20.5])
                    }}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 35},
                    "efficient": {"2009": 10, "2010": 20}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 35},
                    "efficient": {"2009": 10, "2010": 20}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 40},
                    "efficient": {"2009": 25, "2010": 25}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 40},
                    "efficient": {"2009": 25, "2010": 25}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": numpy.array([0.5, 1.2, 2.1, 2.2, 5.6])}}

    # Savings/prioritization metrics dict keys and values that should be
    # yielded by above point value master microsegment dict input used with
    # a residential measure instance
    ok_out_point_res = {
        "stock": {
            "cost savings (total)": {"2009": -5, "2010": -10},
            "cost savings (added)": {"2009": -5, "2010": -10}},
        "energy": {
            "savings (total)": {"2009": 15, "2010": 20},
            "savings (added)": {"2009": 10, "2010": 10},
            "cost savings (total)": {"2009": 10, "2010": 15},
            "cost savings (added)": {"2009": 10, "2010": 15}},
        "carbon": {
            "savings (total)": {"2009": 150, "2010": 200},
            "savings (added)": {"2009": 50, "2010": 50},
            "cost savings (total)": {"2009": 5, "2010": 15},
            "cost savings (added)": {"2009": 5, "2010": 15}},
        "metrics": {
            "anpv": {
                "stock cost": {
                    "2009": {
                        "residential": numpy.pmt(0.07, 2, 0.8691589),
                        "commercial": None},
                    "2010": {
                        "residential": numpy.pmt(0.07, 2, 0.4018692),
                        "commercial": None}},
                "energy cost": {
                    "2009": {
                        "residential": numpy.pmt(0.07, 2, 3.616036),
                        "commercial": None},
                    "2010": {
                        "residential": numpy.pmt(0.07, 2, 2.712027),
                        "commercial": None}},
                "carbon cost": {
                    "2009": {
                        "residential": numpy.pmt(0.07, 2, 1.808018),
                        "commercial": None},
                    "2010": {
                        "residential": numpy.pmt(0.07, 2, 2.712027),
                        "commercial": None}}},
            "irr (w/ energy $)": {
                "2009": 3.45, "2010": 2.44},
            "irr (w/ energy and carbon $)": {
                "2009": 4.54, "2010": 4.09},
            "payback (w/ energy $)": {
                "2009": 0.25, "2010": 0.33},
            "payback (w/ energy and carbon $)": {
                "2009": 0.2, "2010": 0.22},
            "cce": {"2009": -0.24, "2010": -0.22},
            "cce (w/ carbon $ benefits)": {
                "2009": -0.74, "2010": -1.72},
            "ccc": {"2009": -0.05, "2010": -0.04},
            "ccc (w/ energy $ benefits)": {
                "2009": -0.25, "2010": -0.34}}}

    # Savings/prioritization metrics dict keys and values that should be
    # yielded by above point value master microsegment dict input used with
    # a commercial measure instance
    ok_out_point_com = {
        "stock": {
            "cost savings (total)": {"2009": -5, "2010": -10},
            "cost savings (added)": {"2009": -5, "2010": -10}},
        "energy": {
            "savings (total)": {"2009": 15, "2010": 20},
            "savings (added)": {"2009": 10, "2010": 10},
            "cost savings (total)": {"2009": 10, "2010": 15},
            "cost savings (added)": {"2009": 10, "2010": 15}},
        "carbon": {
            "savings (total)": {"2009": 150, "2010": 200},
            "savings (added)": {"2009": 50, "2010": 50},
            "cost savings (total)": {"2009": 5, "2010": 15},
            "cost savings (added)": {"2009": 5, "2010": 15}},
        "metrics": {
            "anpv": {
                "stock cost": {
                    "2009": {
                        "residential": None,
                        "commercial": {
                            "rate 1": numpy.pmt(10.0, 2, -0.8181818),
                            "rate 2": numpy.pmt(1.0, 2, 0),
                            "rate 3": numpy.pmt(0.45, 2, 0.3793103),
                            "rate 4": numpy.pmt(0.25, 2, 0.6),
                            "rate 5": numpy.pmt(0.15, 2, 0.7391304),
                            "rate 6": numpy.pmt(0.065, 2, 0.8779343),
                            "rate 7": -0.5}},
                    "2010": {
                        "residential": None,
                        "commercial": {
                            "rate 1": numpy.pmt(10.0, 2, -0.8636364),
                            "rate 2": numpy.pmt(1.0, 2, -0.25),
                            "rate 3": numpy.pmt(0.45, 2, 0.03448276),
                            "rate 4": numpy.pmt(0.25, 2, 0.2),
                            "rate 5": numpy.pmt(0.15, 2, 0.3043478),
                            "rate 6": numpy.pmt(0.065, 2, 0.4084507),
                            "rate 7": -0.25}}},
                "energy cost": {
                    "2009": {
                        "residential": None,
                        "commercial": {
                            "rate 1": numpy.pmt(10.0, 2, 0.1983471),
                            "rate 2": numpy.pmt(1.0, 2, 1.5),
                            "rate 3": numpy.pmt(0.45, 2, 2.330559),
                            "rate 4": numpy.pmt(0.25, 2, 2.88),
                            "rate 5": numpy.pmt(0.15, 2, 3.251418),
                            "rate 6": numpy.pmt(0.065, 2, 3.641253),
                            "rate 7": -2}},
                    "2010": {
                        "residential": None,
                        "commercial": {
                            "rate 1": numpy.pmt(10.0, 2, 0.1487603),
                            "rate 2": numpy.pmt(1.0, 2, 1.125),
                            "rate 3": numpy.pmt(0.45, 2, 1.747919),
                            "rate 4": numpy.pmt(0.25, 2, 2.16),
                            "rate 5": numpy.pmt(0.15, 2, 2.438563),
                            "rate 6": numpy.pmt(0.065, 2, 2.73094),
                            "rate 7": -1.5}}},
                "carbon cost": {
                    "2009": {
                        "residential": None,
                        "commercial": {
                            "rate 1": numpy.pmt(10.0, 2, 0.09917355),
                            "rate 2": numpy.pmt(1.0, 2, 0.75),
                            "rate 3": numpy.pmt(0.45, 2, 1.165279),
                            "rate 4": numpy.pmt(0.25, 2, 1.44),
                            "rate 5": numpy.pmt(0.15, 2, 1.625709),
                            "rate 6": numpy.pmt(0.065, 2, 1.820626),
                            "rate 7": -1}},
                    "2010": {
                        "residential": None,
                        "commercial": {
                            "rate 1": numpy.pmt(10.0, 2, 0.1487603),
                            "rate 2": numpy.pmt(1.0, 2, 1.125),
                            "rate 3": numpy.pmt(0.45, 2, 1.747919),
                            "rate 4": numpy.pmt(0.25, 2, 2.16),
                            "rate 5": numpy.pmt(0.15, 2, 2.438563),
                            "rate 6": numpy.pmt(0.065, 2, 2.73094),
                            "rate 7": -1.5}}}},
            "irr (w/ energy $)": {
                "2009": 3.45, "2010": 2.44},
            "irr (w/ energy and carbon $)": {
                "2009": 4.54, "2010": 4.09},
            "payback (w/ energy $)": {
                "2009": 0.25, "2010": 0.33},
            "payback (w/ energy and carbon $)": {
                "2009": 0.2, "2010": 0.22},
            "cce": {"2009": -0.24, "2010": -0.22},
            "cce (w/ carbon $ benefits)": {
                "2009": -0.74, "2010": -1.72},
            "ccc": {"2009": -0.05, "2010": -0.04},
            "ccc (w/ energy $ benefits)": {
                "2009": -0.25, "2010": -0.34}}}

    # Savings/prioritization metrics dict keys and values that should be
    # yielded by above dist1 master microsegment dict input
    ok_out_dist1 = {
        "stock": {
            "cost savings (total)": {"2009": -5, "2010": -10},
            "cost savings (added)": {"2009": -5, "2010": -10}},
        "energy": {
            "savings (total)": {
                "2009": [18.4, 17.3, 16.9, 14.0, 14.9],
                "2010": [19.4, 20.5, 21.9, 19.0, 17.6]},
            "savings (added)": {
                "2009": [9.4, 9.3, 9.9, 8.4, 9.9],
                "2010": [11.4, 10.5, 8.9, 10.0, 9.6]},
            "cost savings (total)": {
                "2009": [10.9, 11.3, 12.3, 8.8, 7.5],
                "2010": [14.9, 16.3, 13.3, 13.8, 12.5]},
            "cost savings (added)": {
                "2009": [10.9, 11.3, 12.3, 8.8, 7.5],
                "2010": [14.9, 16.3, 13.3, 13.8, 12.5]}},
        "carbon": {
            "savings (total)": {
                "2009": [149.4, 142.3, 141.9, 150.0, 148.9],
                "2010": [199.4, 191.3, 194.9, 195.0, 193.9]},
            "savings (added)": {
                "2009": [49.4, 42.3, 41.9, 50.0, 48.9],
                "2010": [49.4, 41.3, 44.9, 45.0, 43.9]},
            "cost savings (total)": {
                "2009": [4.9, 5.3, 6.3, -1.2, 11.5],
                "2010": [19.9, 21.3, 18.3, 18.8, 17.5]},
            "cost savings (added)": {
                "2009": [4.9, 5.3, 6.3, -1.2, 11.5],
                "2010": [19.9, 21.3, 18.3, 18.8, 17.5]}},
        "metrics": {
            "anpv": {
                "stock cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 2, 0.8691589),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.8691589),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.8691589),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.8691589),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.8691589),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 2, 0.4018692),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.4018692),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.4018692),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.4018692),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.4018692),
                          "commercial": None}]},
                "energy cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 2, 3.94148),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 4.086121),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 4.447725),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.182112),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 2, 2.693947),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.94707),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.404664),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.495065),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.260023),
                          "commercial": None}]},
                "carbon cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 2, 1.7718578),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.9164993),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.2781029),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, -0.4339244),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 4.1584418),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 2, 3.597956),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.851079),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.308673),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.399074),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.164032),
                          "commercial": None}]}},
            "irr (w/ energy $)": {
                "2009": [3.65, 3.74, 3.96, 3.18, 2.89],
                "2010": [2.42, 2.58, 2.24, 2.30, 2.15]},
            "irr (w/ energy and carbon $)": {
                "2009": [4.71, 4.88, 5.31, 2.91, 5.39],
                "2010": [4.60, 4.90, 4.26, 4.37, 4.09]},
            "payback (w/ energy $)": {
                "2009": [0.24, 0.23, 0.22, 0.27, 0.29],
                "2010": [0.33, 0.32, 0.35, 0.35, 0.36]},
            "payback (w/ energy and carbon $)": {
                "2009": [0.19, 0.19, 0.17, 0.28, 0.17],
                "2010": [0.20, 0.19, 0.21, 0.21, 0.22]},
            "cce": {
                "2009": [-0.26, -0.26, -0.24, -0.29, -0.24],
                "2010": [-0.19, -0.21, -0.25, -0.22, -0.23]},
            "cce (w/ carbon $ benefits)": {
                "2009": [-0.78, -0.83, -0.88, -0.14, -1.40],
                "2010": [-1.94, -2.24, -2.31, -2.10, -2.05]},
            "ccc": {
                "2009": [-0.05, -0.06, -0.06, -0.05, -0.05],
                "2010": [-0.04, -0.05, -0.05, -0.05, -0.05]},
            "ccc (w/ energy $ benefits)": {
                "2009": [-0.27, -0.32, -0.35, -0.22, -0.20],
                "2010": [-0.35, -0.45, -0.35, -0.36, -0.34]}}}

    # Savings/prioritization metrics dict keys and values that should be
    # yielded by above dist2 master microsegment dict input
    ok_out_dist2 = {
        "stock": {
            "cost savings (total)": {"2009": [-5.1, -2.7, -4.1, -4.2, -5.5],
                                     "2010": [-5.1, -3.7, -6.7, -4.2, -5.5]},
            "cost savings (added)": {"2009": [-5.1, -2.7, -4.1, -4.2, -5.5],
                                     "2010": [-5.1, -3.7, -6.7, -4.2, -5.5]}},
        "energy": {
            "savings (total)": {"2009": 15, "2010": 20},
            "savings (added)": {"2009": 10, "2010": 10},
            "cost savings (total)": {"2009": 10, "2010": 15},
            "cost savings (added)": {"2009": 10, "2010": 15}},
        "carbon": {
            "savings (total)": {"2009": 150, "2010": 200},
            "savings (added)": {"2009": 50, "2010": 50},
            "cost savings (total)": {"2009": 5, "2010": 15},
            "cost savings (added)": {"2009": 5, "2010": 15}},
        "metrics": {
            "anpv": {
                "stock cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 2, 0.8491589),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.329159),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.049159),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.029159),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.7691589),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 2, 0.8918692),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.031869),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.7318692),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.9818692),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.8518692),
                          "commercial": None}]},
                "energy cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 2, 3.616036),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.616036),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.616036),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.616036),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.616036),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None}]},
                "carbon cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 2, 1.808018),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.808018),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.808018),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.808018),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.808018),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None}]}},
            "irr (w/ energy $)":
                {"2009": [3.37, 6.88, 4.34, 4.22, 3.08],
                 "2010": [5.35, 7.58, 3.93, 6.61, 4.92]},
            "irr (w/ energy and carbon $)":
                {"2009": [4.44, 8.82, 5.65, 5.50, 4.08],
                 "2010": [8.45, 11.80, 6.33, 10.34, 7.80]},
            "payback (w/ energy $)":
                {"2009": [0.26, 0.14, 0.21, 0.21, 0.28],
                 "2010": [0.17, 0.12, 0.22, 0.14, 0.18]},
            "payback (w/ energy and carbon $)":
                {"2009": [0.20, 0.11, 0.16, 0.17, 0.22],
                 "2010": [0.11, 0.08, 0.15, 0.09, 0.12]},
            "cce":
                {"2009": [-0.23, -0.37, -0.29, -0.28, -0.21],
                 "2010": [-0.49, -0.57, -0.40, -0.54, -0.47]},
            "cce (w/ carbon $ benefits)":
                {"2009": [-0.73, -0.87, -0.79, -0.78, -0.71],
                 "2010": [-1.99, -2.07, -1.90, -2.04, -1.97]},
            "ccc":
                {"2009": [-0.05, -0.07, -0.06, -0.06, -0.04],
                 "2010": [-0.10, -0.11, -0.08, -0.11, -0.09]},
            "ccc (w/ energy $ benefits)":
                {"2009": [-0.25, -0.27, -0.26, -0.26, -0.24],
                 "2010": [-0.40, -0.41, -0.38, -0.41, -0.39]}}}

    # Savings/prioritization metrics dict keys and values that should be
    # yielded by above dist3 master microsegment dict input
    ok_out_dist3 = {
        "stock": {
            "cost savings (total)": {"2009": -5, "2010": -10},
            "cost savings (added)": {"2009": -5, "2010": -10}},
        "energy": {
            "savings (total)": {"2009": 15, "2010": 20},
            "savings (added)": {"2009": 10, "2010": 10},
            "cost savings (total)": {"2009": 10, "2010": 15},
            "cost savings (added)": {"2009": 10, "2010": 15}},
        "carbon": {
            "savings (total)": {"2009": 150, "2010": 200},
            "savings (added)": {"2009": 50, "2010": 50},
            "cost savings (total)": {"2009": 5, "2010": 15},
            "cost savings (added)": {"2009": 5, "2010": 15}},
        "metrics": {
            "anpv": {
                "stock cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 1, -1.0000000),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, -1.0000000),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.8691589),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.8691589),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 5.7744225),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 1, -1.0000000),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, -1.0000000),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.4018692),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.4018692),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 4.080817),
                          "commercial": None}]},
                "energy cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 1, 1.869159),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, 1.869159),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.616036),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.616036),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 8.200395),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 1, 1.401869),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, 1.401869),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 6.150296),
                          "commercial": None}]},
                "carbon cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 1, 0.9345794),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, 0.9345794),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.808018),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.808018),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 4.1001974),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 1, 1.401869),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, 1.401869),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 6.150296),
                          "commercial": None}]}},
            "irr (w/ energy $)":
                {"2009": [1.00, 1.00, 3.45, 3.45, 4.00],
                 "2010": [0.50, 0.50, 2.44, 2.44, 2.99]},
            "irr (w/ energy and carbon $)":
                {"2009": [2.00, 2.00, 4.54, 4.54, 5.00],
                 "2010": [2.00, 2.00, 4.09, 4.09, 4.50]},
            "payback (w/ energy $)":
                {"2009": [0.50, 0.50, 0.25, 0.25, 0.25],
                 "2010": [0.67, 0.67, 0.33, 0.33, 0.33]},
            "payback (w/ energy and carbon $)":
                {"2009": [0.33, 0.33, 0.20, 0.20, 0.20],
                 "2010": [0.33, 0.33, 0.22, 0.22, 0.22]},
            "cce":
                {"2009": [0.54, 0.54, -0.24, -0.24, -0.7],
                 "2010": [1.07, 1.07, -0.22, -0.22, -1.0]},
            "cce (w/ carbon $ benefits)":
                {"2009": [0.03, 0.03, -0.74, -0.74, -1.2],
                 "2010": [-0.43, -0.43, -1.72, -1.72, -2.5]},
            "ccc":
                {"2009": [0.11, 0.11, -0.05, -0.05, -0.14],
                 "2010": [0.21, 0.21, -0.04, -0.04, -0.20]},
            "ccc (w/ energy $ benefits)":
                {"2009": [-0.09, -0.09, -0.25, -0.25, -0.34],
                 "2010": [-0.09, -0.09, -0.34, -0.34, -0.50]}}}

    # Savings/prioritization metrics dict keys and values that should be
    # yielded by above dist4 master microsegment dict input
    ok_out_dist4 = {
        "stock": {
            "cost savings (total)": {"2009": [-5.1, -2.7, -4.1, -4.2, -5.5],
                                     "2010": [-5.1, -3.7, -6.7, -4.2, -5.5]},
            "cost savings (added)": {"2009": [-5.1, -2.7, -4.1, -4.2, -5.5],
                                     "2010": [-5.1, -3.7, -6.7, -4.2, -5.5]}},
        "energy": {
            "savings (total)": {"2009": 15, "2010": 20},
            "savings (added)": {"2009": 10, "2010": 10},
            "cost savings (total)": {"2009": 10, "2010": 15},
            "cost savings (added)": {"2009": 10, "2010": 15}},
        "carbon": {
            "savings (total)": {"2009": 150, "2010": 200},
            "savings (added)": {"2009": 50, "2010": 50},
            "cost savings (total)": {"2009": 5, "2010": 15},
            "cost savings (added)": {"2009": 5, "2010": 15}},
        "metrics": {
            "anpv": {
                "stock cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 1, -1.02),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, -0.54),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.049159),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.029159),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 5.674423),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 1, -0.51),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, -0.37),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.7318692),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 0.9818692),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 4.530817),
                          "commercial": None}]},
                "energy cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 1, 1.869159),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, 1.869159),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.616036),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 3.616036),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 8.200395),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 1, 1.401869),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, 1.401869),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 6.150296),
                          "commercial": None}]},
                "carbon cost": {
                    "2009":
                        [{"residential":
                            numpy.pmt(0.07, 1, 0.9345794),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, 0.9345794),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.808018),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 1.808018),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 4.1001974),
                          "commercial": None}],
                    "2010":
                        [{"residential":
                            numpy.pmt(0.07, 1, 1.401869),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 1, 1.401869),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 2, 2.712027),
                          "commercial": None},
                         {"residential":
                            numpy.pmt(0.07, 5, 6.150296),
                          "commercial": None}]}},
            "irr (w/ energy $)":
                {"2009": [0.96, 2.70, 4.34, 4.22, 3.63],
                 "2010": [1.94, 3.05, 3.93, 6.61, 5.45]},
            "irr (w/ energy and carbon $)":
                {"2009": [1.94, 4.56, 5.65, 5.50, 4.54],
                 "2010": [4.88, 7.11, 6.33, 10.34, 8.18]},
            "payback (w/ energy $)":
                {"2009": [0.51, 0.27, 0.21, 0.21, 0.28],
                 "2010": [0.34, 0.25, 0.22, 0.14, 0.18]},
            "payback (w/ energy and carbon $)":
                {"2009": [0.34, 0.18, 0.16, 0.17, 0.22],
                 "2010": [0.17, 0.12, 0.15, 0.09, 0.12]},
            "cce":
                {"2009": [0.55, 0.29, -0.29, -0.28, -0.69],
                 "2010": [0.55, 0.40, -0.40, -0.54, -1.11]},
            "cce (w/ carbon $ benefits)":
                {"2009": [0.05, -0.21, -0.79, -0.78, -1.19],
                 "2010": [-0.95, -1.10, -1.90, -2.04, -2.61]},
            "ccc":
                {"2009": [0.11, 0.06, -0.06, -0.06, -0.14],
                 "2010": [0.11, 0.08, -0.08, -0.11, -0.22]},
            "ccc (w/ energy $ benefits)":
                {"2009": [-0.09, -0.14, -0.26, -0.26, -0.34],
                 "2010": [-0.19, -0.22, -0.38, -0.41, -0.52]}}}

    # Test for correct output from "ok_master_mseg_point_res"
    def test_metrics_ok_point_res(self):
        # Create a measure instance to use in the test
        measure_instance = run.Measure(**sample_measure)  # Residential
        # Set the master microsegment for the measure instance
        # to the "ok_master_mseg_point" dict defined above
        measure_instance.master_mseg = self.ok_master_mseg_point
        # Assert that output dict is correct
        dict1 = measure_instance.calc_metric_update(
            self.ok_rate, self.adjust_savings, run.com_timeprefs)
        dict2 = self.ok_out_point_res
        # Check calc_metric_update output (master savings dict)
        self.dict_check(dict1, dict2)

    # Test for correct output from "ok_master_mseg_point_com"
    def test_metrics_ok_point_com(self):
        # Create a measure instance to use in the test
        measure_instance = run.Measure(**sample_measure3)  # Commercial
        # Set the master microsegment for the measure instance
        # to the "ok_master_mseg_point" dict defined above
        measure_instance.master_mseg = self.ok_master_mseg_point
        # Assert that output dict is correct
        dict1 = measure_instance.calc_metric_update(
            self.ok_rate, self.adjust_savings, run.com_timeprefs)
        dict2 = self.ok_out_point_com
        # Check calc_metric_update output (master savings dict)
        self.dict_check(dict1, dict2)

    # Test for correct output from "ok_master_mseg_dist1"
    def test_metrics_ok_distrib1(self):
        # Create a measure instance to use in the test
        measure_instance = run.Measure(**sample_measure)
        # Set the master microsegment for the measure instance
        # to the "ok_master_mseg_dist1" dict defined above
        measure_instance.master_mseg = self.ok_master_mseg_dist1
        # Assert that output dict is correct
        dict1 = measure_instance.calc_metric_update(
            self.ok_rate, self.adjust_savings, run.com_timeprefs)
        dict2 = self.ok_out_dist1
        # Check calc_metric_update output (master savings dict)
        self.dict_check_list(dict1, dict2)

    # Test for correct output from "ok_master_mseg_dist2"
    def test_metrics_ok_distrib2(self):
        # Create a measure instance to use in the test
        measure_instance = run.Measure(**sample_measure)
        # Set the master microsegment for the measure instance
        # to the "ok_master_mseg_dist2" dict defined above
        measure_instance.master_mseg = self.ok_master_mseg_dist2
        # Assert that output dict is correct
        dict1 = measure_instance.calc_metric_update(
            self.ok_rate, self.adjust_savings, run.com_timeprefs)
        dict2 = self.ok_out_dist2
        # Check calc_metric_update output (master savings dict)
        self.dict_check_list(dict1, dict2)

    # Test for correct output from "ok_master_mseg_dist3"
    def test_metrics_ok_distrib3(self):
        # Create a measure instance to use in the test
        measure_instance = run.Measure(**sample_measure)
        # Set the master microsegment for the measure instance
        # to the "ok_master_mseg_point" dict defined above
        measure_instance.master_mseg = self.ok_master_mseg_dist3
        # Assert that output dict is correct
        dict1 = measure_instance.calc_metric_update(
            self.ok_rate, self.adjust_savings, run.com_timeprefs)
        dict2 = self.ok_out_dist3
        # Check calc_metric_update output (master savings dict)
        self.dict_check_list(dict1, dict2)

    # Test for correct output from "ok_master_mseg_dist4"
    def test_metrics_ok_distrib4(self):
        # Create a measure instance to use in the test
        measure_instance = run.Measure(**sample_measure)
        # Set the master microsegment for the measure instance
        # to the "ok_master_mseg_dist2" dict defined above
        measure_instance.master_mseg = self.ok_master_mseg_dist4
        # Assert that output dict is correct
        dict1 = measure_instance.calc_metric_update(
            self.ok_rate, self.adjust_savings, run.com_timeprefs)
        dict2 = self.ok_out_dist4
        # Check calc_metric_update output (master savings dict)
        self.dict_check_list(dict1, dict2)


class MetricUpdateTest(unittest.TestCase, CommonMethods):
    """ Test the operation of the metrics_update function to
    verify cashflow inputs generate expected prioritization metric outputs """

    # Define ok test inputs

    # Test discount rate
    ok_rate = 0.07
    # Test number of units
    ok_num_units = 10
    # Test ok base stock cost
    ok_base_scost = 10
    # Test ok base stock life
    ok_base_life = 3
    # Test ok life of the measure
    ok_product_lifetime = 6.2
    # Test ok capital cost increment
    ok_scostsave = -10
    # Test ok energy savings
    ok_esave = 25
    # Test ok energy cost savings
    ok_ecostsave = 5
    # Test ok carbon savings
    ok_csave = 50
    # Test ok carbon cost savings
    ok_ccostsave = 10
    # Test ok life ratio
    ok_life_ratio = 2

    # Correct ANPV dict output values that should be yielded by using "ok"
    # inputs above (first three elements of 'metric_update' output list)
    ok_out_dicts = [
        {"residential": numpy.pmt(0.07, 6, -0.1837021), "commercial": None},
        {"residential": numpy.pmt(0.07, 6, 2.38327), "commercial": None},
        {"residential": numpy.pmt(0.07, 6, 4.76654), "commercial": None}]

    # Correct floating point output values that should be yielded by
    # using "ok" inputs above (final eight elements of 'metric_update' output
    # list)
    ok_out_array = [0.62, 1.59, 2, 0.67, 0.02, -0.38, 0.01, -0.09]

    # Test for correct outputs given "ok" inputs above
    def test_metric_updates(self):
        # Create a sample measure instance using sample_measure
        measure_instance = run.Measure(**sample_measure)
        # Record the output for the test run of the 'metric_update'
        # function; the output will be split up and tested with expeted
        # output sets below
        function_output = measure_instance.metric_update(
            self.ok_rate, self.ok_base_scost, self.ok_base_life,
            self.ok_scostsave, self.ok_esave, self.ok_ecostsave,
            self.ok_csave, self.ok_ccostsave, int(self.ok_life_ratio),
            int(self.ok_product_lifetime), self.ok_num_units,
            run.com_timeprefs)

        # Test that "ok" inputs yield correct ANPV dict outputs
        # (the first three elements of the 'metric_update' output)
        for i in range(0, len(self.ok_out_dicts)):
            self.dict_check(function_output[i], self.ok_out_dicts[i])
        # Test that "ok" inputs yield correct irr, payback, and
        # cost of conserved energy/carbon floating point outputs
        # (the final eight elements of the 'metric_update' output)
        numpy.testing.assert_array_almost_equal(
            function_output[3:], self.ok_out_array, decimal=2)


class PaybackTest(unittest.TestCase):
    """ Test the operation of the payback function to
    verify cashflow input generates expected payback output """

    # Define ok test cashflow inputs
    ok_cashflows = [[-10, 1, 1, 1, 1, 5, 7, 8],
                    [-10, 14, 2, 3, 4],
                    [-10, 0, 1, 2],
                    [10, 4, 7, 8, 10]]

    # Correct outputs that should be yielded by above "ok" cashflow inputs
    ok_out = [5.14, 0.71, 999, 0]

    # Test for correct outputs given "ok" input cashflows above
    def test_cashflow_paybacks(self):
        # Create a sample measure instance using sample_measure
        measure_instance = run.Measure(**sample_measure)
        # Test that "ok" input cashflows yield correct output payback values
        for idx, cf in enumerate(self.ok_cashflows):
            self.assertAlmostEqual(measure_instance.payback(cf),
                                   self.ok_out[idx], places=2)


class ResCompeteTest(unittest.TestCase, CommonMethods):
    """ Test the operation of the res_compete and overlap_adjustment functions
    to verify that the former correctly calculates market shares and updates
    master microsegments for a series of competing residential measures, and
    the latter properly accounts for any supply-side and demand-side savings
    overlaps for HVAC measures """

    # Define sample strings for the competed demand-side and supply-side
    # microsegment key chains being tested
    adjust_key1 = str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'demand', 'windows conduction'])
    adjust_key2 = str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'supply', 'ASHP'])

    # Define master microsegments, the microsegment(s) that contribute to the
    # master microsegment (one of which is being competed), and capital/
    # operating cost information for five sample cooling measures
    compete_meas1 = {
        "name": "sample compete measure r1",
        "master_mseg": {
            "stock": {
                "total": {
                    "all": {"2009": 10, "2010": 10},
                    "measure": {"2009": 10, "2010": 10}},
                "competed": {
                    "all": {"2009": 5, "2010": 5},
                    "measure": {"2009": 5, "2010": 5}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 15, "2010": 15}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 5, "2010": 5}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 20, "2010": 20}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {"2009": 5, "2010": 5}}},
            "cost": {
                "stock": {
                    "total": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 5, "2010": 5}},
                    "competed": {
                        "baseline": {"2009": 5, "2010": 5},
                        "efficient": {"2009": 0, "2010": 0}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 15, "2010": 15}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 5, "2010": 5}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 20, "2010": 20}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 5, "2010": 5}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}},
        "mseg_adjust": {
            "contributing mseg keys and values": {
                adjust_key1: {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}}},
            "competed choice parameters": {
                adjust_key1: {"b1": {"2009": -0.95, "2010": -0.95},
                              "b2": {"2009": -0.10, "2010": -0.10}}},
            "supply-demand adjustment": {
                "savings": {
                    adjust_key1: {
                        "2009": 0, "2010": 0}},
                "total": {
                    adjust_key1: {
                        "2009": 100, "2010": 100}}},
            "savings updated": False},
        "master_savings": {
            "metrics": {
                "anpv": {
                    "stock cost": {
                        "2009": {"residential": 95, "commercial": None},
                        "2010": {"residential": 95, "commercial": None}},
                    "energy cost": {
                        "2009": {"residential": -150, "commercial": None},
                        "2010": {"residential": -150, "commercial": None}},
                    "carbon cost": {
                        "2009": {"residential": -150, "commercial": None},
                        "2010": {"residential": -50, "commercial": None}}}}}}

    # Create an alternate version of sample measure 1 above that
    # includes lists of energy/carbon and associated cost input values
    # instead of point values
    compete_meas1_dist = {
        "name": "sample compete measure r1 dist",
        "master_mseg": {
            "stock": {
                "total": {
                    "all": {"2009": 10, "2010": 10},
                    "measure": {"2009": 10, "2010": 10}},
                "competed": {
                    "all": {"2009": 5, "2010": 5},
                    "measure": {"2009": 5, "2010": 5}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {
                        "2009": numpy.array([15, 16, 17]),
                        "2010": numpy.array([15, 16, 17])}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {
                        "2009": numpy.array([5, 6, 7]),
                        "2010": numpy.array([5, 6, 7])}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {
                        "2009": numpy.array([20, 21, 22]),
                        "2010": numpy.array([20, 21, 22])}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {
                        "2009": numpy.array([5, 6, 7]),
                        "2010": numpy.array([5, 6, 7])}}},
            "cost": {
                "stock": {
                    "total": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 5, "2010": 5}},
                    "competed": {
                        "baseline": {"2009": 5, "2010": 5},
                        "efficient": {"2009": 0, "2010": 0}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {
                            "2009": numpy.array([15, 16, 17]),
                            "2010": numpy.array([15, 16, 17])}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {
                            "2009": numpy.array([5, 6, 7]),
                            "2010": numpy.array([5, 6, 7])}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {
                            "2009": numpy.array([20, 21, 22]),
                            "2010": numpy.array([20, 21, 22])}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {
                            "2009": numpy.array([5, 6, 7]),
                            "2010": numpy.array([5, 6, 7])}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}},
        "mseg_adjust": {
            "contributing mseg keys and values": {
                adjust_key1: {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {
                                "2009": numpy.array([15, 16, 17]),
                                "2010": numpy.array([15, 16, 17])}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {
                                "2009": numpy.array([5, 6, 7]),
                                "2010": numpy.array([5, 6, 7])}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {
                                "2009": numpy.array([20, 21, 22]),
                                "2010": numpy.array([20, 21, 22])}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {
                                "2009": numpy.array([5, 6, 7]),
                                "2010": numpy.array([5, 6, 7])}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {
                                    "2009": numpy.array([15, 16, 17]),
                                    "2010": numpy.array([15, 16, 17])}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {
                                    "2009": numpy.array([5, 6, 7]),
                                    "2010": numpy.array([5, 6, 7])}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {
                                    "2009": numpy.array([20, 21, 22]),
                                    "2010": numpy.array([20, 21, 22])}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {
                                    "2009": numpy.array([5, 6, 7]),
                                    "2010": numpy.array([5, 6, 7])}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}}},
            "competed choice parameters": {
                adjust_key1: {"b1": {"2009": -0.95, "2010": -0.95},
                              "b2": {"2009": -0.10, "2010": -0.10}}},
            "supply-demand adjustment": {
                "savings": {
                    adjust_key1: {
                        "2009": 0, "2010": 0}},
                "total": {
                    adjust_key1: {
                        "2009": 100, "2010": 100}}},
            "savings updated": False},
        "master_savings": {
            "metrics": {
                "anpv": {
                    "stock cost": {
                        "2009": {"residential": 95, "commercial": None},
                        "2010": {"residential": 95, "commercial": None}},
                    "energy cost": {
                        "2009": numpy.array([
                            {"residential": -150,
                             "commercial": None},
                            {"residential": -200,
                             "commercial": None},
                            {"residential": -100,
                             "commercial": None}]),
                        "2010": numpy.array([
                            {"residential": -150,
                             "commercial": None},
                            {"residential": -200,
                             "commercial": None},
                            {"residential": -100,
                             "commercial": None}])},
                    "carbon cost": {
                        "2009": numpy.array([
                            {"residential": -150,
                             "commercial": None},
                            {"residential": -200,
                             "commercial": None},
                            {"residential": -100,
                             "commercial": None}]),
                        "2010": numpy.array([
                            {"residential": -50,
                             "commercial": None},
                            {"residential": -100,
                             "commercial": None},
                            {"residential": -10,
                             "commercial": None}])}}}}}

    compete_meas2 = {
        "name": "sample compete measure r2",
        "master_mseg": {
            "stock": {
                "total": {
                    "all": {"2009": 20, "2010": 20},
                    "measure": {"2009": 20, "2010": 20}},
                "competed": {
                    "all": {"2009": 10, "2010": 10},
                    "measure": {"2009": 10, "2010": 10}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 40, "2010": 40},
                    "efficient": {"2009": 30, "2010": 30}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 10, "2010": 10}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {"2009": 40, "2010": 40}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 10, "2010": 10}}},
            "cost": {
                "stock": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 10, "2010": 10}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 0, "2010": 0}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 40, "2010": 40},
                        "efficient": {"2009": 30, "2010": 30}},
                    "competed": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 10, "2010": 10}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 60, "2010": 60},
                        "efficient": {"2009": 40, "2010": 40}},
                    "competed": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 10, "2010": 10}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}},
        "mseg_adjust": {
            "contributing mseg keys and values": {
                adjust_key1: {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}},
                str(['AIA_CZ2', 'single family home', 'electricity (grid)',
                     'lighting', 'reflector (LED)']): {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}}},
            "competed choice parameters": {
                adjust_key1: {"b1": {"2009": -0.95, "2010": -0.95},
                              "b2": {"2009": -0.10, "2010": -0.10}}},
            "supply-demand adjustment": {
                "savings": {
                    adjust_key1: {
                        "2009": 0, "2010": 0}},
                "total": {
                    adjust_key1: {
                        "2009": 100, "2010": 100}}},
            "savings updated": False},
        "master_savings": {
            "metrics": {
                "anpv": {
                    "stock cost": {
                        "2009": {"residential": 120, "commercial": None},
                        "2010": {"residential": 120, "commercial": None}},
                    "energy cost": {
                        "2009": {"residential": -400, "commercial": None},
                        "2010": {"residential": -400, "commercial": None}},
                    "carbon cost": {
                        "2009": {"residential": -50, "commercial": None},
                        "2010": {"residential": -50, "commercial": None}}}}}}

    compete_meas3 = {
        "name": "sample compete measure r3",
        "master_mseg": {
            "stock": {
                "total": {
                    "all": {"2009": 10, "2010": 10},
                    "measure": {"2009": 10, "2010": 10}},
                "competed": {
                    "all": {"2009": 5, "2010": 5},
                    "measure": {"2009": 5, "2010": 5}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 15, "2010": 15}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 5, "2010": 5}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 20, "2010": 20}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {"2009": 5, "2010": 5}}},
            "cost": {
                "stock": {
                    "total": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 5, "2010": 5}},
                    "competed": {
                        "baseline": {"2009": 5, "2010": 5},
                        "efficient": {"2009": 0, "2010": 0}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 15, "2010": 15}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 5, "2010": 5}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 20, "2010": 20}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 5, "2010": 5}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}},
        "mseg_adjust": {
            "contributing mseg keys and values": {
                adjust_key2: {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}}},
            "competed choice parameters": {
                adjust_key2: {"b1": {"2009": -0.95, "2010": -0.95},
                              "b2": {"2009": -0.10, "2010": -0.10}}},
            "supply-demand adjustment": {
                "savings": {
                    adjust_key2: {
                        "2009": 0, "2010": 0}},
                "total": {
                    adjust_key2: {
                        "2009": 100, "2010": 100}}},
            "savings updated": False},
        "master_savings": {
            "metrics": {
                "anpv": {
                    "stock cost": {
                        "2009": {"residential": 95, "commercial": None},
                        "2010": {"residential": 95, "commercial": None}},
                    "energy cost": {
                        "2009": {"residential": -150, "commercial": None},
                        "2010": {"residential": -150, "commercial": None}},
                    "carbon cost": {
                        "2009": {"residential": -150, "commercial": None},
                        "2010": {"residential": -50, "commercial": None}}}}}}

    # Create an alternate version of sample measure 3 above that
    # includes a list of capital cost input values instead of point values
    compete_meas3_dist = {
        "name": "sample compete measure r3 dist",
        "master_mseg": {
            "stock": {
                "total": {
                    "all": {"2009": 10, "2010": 10},
                    "measure": {"2009": 10, "2010": 10}},
                "competed": {
                    "all": {"2009": 5, "2010": 5},
                    "measure": {"2009": 5, "2010": 5}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 15, "2010": 15}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 5, "2010": 5}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 20, "2010": 20}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {"2009": 5, "2010": 5}}},
            "cost": {
                "stock": {
                    "total": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": numpy.array([5, 6, 7]),
                                      "2010": numpy.array([5, 6, 7])}},
                    "competed": {
                        "baseline": {"2009": 5, "2010": 5},
                        "efficient": {"2009": numpy.array([0, 1, 2]),
                                      "2010": numpy.array([0, 1, 2])}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 15, "2010": 15}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 5, "2010": 5}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 20, "2010": 20}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 5, "2010": 5}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}},
        "mseg_adjust": {
            "contributing mseg keys and values": {
                adjust_key2: {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                        "cost": {
                            "stock": {
                                "total": {
                                    "baseline": {
                                        "2009": 10, "2010": 10},
                                    "efficient": {
                                        "2009": numpy.array([5, 6, 7]),
                                        "2010": numpy.array([5, 6, 7])}},
                                "competed": {
                                    "baseline": {
                                        "2009": 5, "2010": 5},
                                    "efficient": {
                                        "2009": numpy.array([0, 1, 2]),
                                        "2010": numpy.array([0, 1, 2])}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}}},
            "competed choice parameters": {
                adjust_key2: {"b1": {"2009": -0.95, "2010": -0.95},
                              "b2": {"2009": -0.10, "2010": -0.10}}},
            "supply-demand adjustment": {
                "savings": {
                    adjust_key2: {
                        "2009": 0, "2010": 0}},
                "total": {
                    adjust_key2: {
                        "2009": 100, "2010": 100}}},
            "savings updated": False},
        "master_savings": {
            "metrics": {
                "anpv": {
                    "stock cost": {
                        "2009": numpy.array([
                            {"residential": 95,
                             "commercial": None},
                            {"residential": 100,
                             "commercial": None},
                            {"residential": 90,
                             "commercial": None}]),
                        "2010": numpy.array([
                            {"residential": 95,
                             "commercial": None},
                            {"residential": 100,
                             "commercial": None},
                            {"residential": 90,
                             "commercial": None}])},
                    "energy cost": {
                        "2009": {"residential": -150, "commercial": None},
                        "2010": {"residential": -150, "commercial": None}},
                    "carbon cost": {
                        "2009": {"residential": -150, "commercial": None},
                        "2010": {"residential": -50, "commercial": None}}}}}}

    compete_meas4 = {
        "name": "sample compete measure r4",
        "master_mseg": {
            "stock": {
                "total": {
                    "all": {"2009": 20, "2010": 20},
                    "measure": {"2009": 20, "2010": 20}},
                "competed": {
                    "all": {"2009": 10, "2010": 10},
                    "measure": {"2009": 10, "2010": 10}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 40, "2010": 40},
                    "efficient": {"2009": 30, "2010": 30}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 10, "2010": 10}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {"2009": 40, "2010": 40}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 10, "2010": 10}}},
            "cost": {
                "stock": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 10, "2010": 10}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 0, "2010": 0}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 40, "2010": 40},
                        "efficient": {"2009": 30, "2010": 30}},
                    "competed": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 10, "2010": 10}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 60, "2010": 60},
                        "efficient": {"2009": 40, "2010": 40}},
                    "competed": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 10, "2010": 10}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}},
        "mseg_adjust": {
            "contributing mseg keys and values": {
                adjust_key2: {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}}},
                str(['AIA_CZ2', 'single family home', 'electricity (grid)',
                     'lighting', 'reflector (LED)']): {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}},
            "competed choice parameters": {
                adjust_key2: {"b1": {"2009": -0.95, "2010": -0.95},
                              "b2": {"2009": -0.10, "2010": -0.10}}},
            "supply-demand adjustment": {
                "savings": {
                    adjust_key2: {
                        "2009": 0, "2010": 0}},
                "total": {
                    adjust_key2: {
                        "2009": 100, "2010": 100}}},
            "savings updated": False},
        "master_savings": {
            "metrics": {
                "anpv": {
                    "stock cost": {
                        "2009": {"residential": 120, "commercial": None},
                        "2010": {"residential": 120, "commercial": None}},
                    "energy cost": {
                        "2009": {"residential": -400, "commercial": None},
                        "2010": {"residential": -400, "commercial": None}},
                    "carbon cost": {
                        "2009": {"residential": -50, "commercial": None},
                        "2010": {"residential": -50, "commercial": None}}}}}}

    compete_meas5 = {
        "name": "sample compete measure r5",
        "master_mseg": {
            "stock": {
                "total": {
                    "all": {"2009": 30, "2010": 30},
                    "measure": {"2009": 30, "2010": 30}},
                "competed": {
                    "all": {"2009": 15, "2010": 15},
                    "measure": {"2009": 15, "2010": 15}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {"2009": 45, "2010": 45}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 15, "2010": 15}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 90, "2010": 90},
                    "efficient": {"2009": 60, "2010": 60}},
                "competed": {
                    "baseline": {"2009": 45, "2010": 45},
                    "efficient": {"2009": 15, "2010": 15}}},
            "cost": {
                "stock": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 15, "2010": 15}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 0, "2010": 0}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 60, "2010": 60},
                        "efficient": {"2009": 45, "2010": 45}},
                    "competed": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 15, "2010": 15}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 90, "2010": 90},
                        "efficient": {"2009": 60, "2010": 60}},
                    "competed": {
                        "baseline": {"2009": 45, "2010": 45},
                        "efficient": {"2009": 15, "2010": 15}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}},
        "mseg_adjust": {
            "contributing mseg keys and values": {
                adjust_key2: {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}}},
                str(['AIA_CZ2', 'single family home', 'electricity (grid)',
                     'lighting', 'reflector (LED)']): {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}},
                str(['AIA_CZ2', 'multi family home', 'electricity (grid)',
                     'lighting', 'reflector (LED)']): {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}},
            "competed choice parameters": {
                adjust_key2: {"b1": {"2009": -0.95, "2010": -0.95},
                              "b2": {"2009": -0.10, "2010": -0.10}}},
            "supply-demand adjustment": {
                "savings": {
                    adjust_key2: {
                        "2009": 0, "2010": 0}},
                "total": {
                    adjust_key2: {
                        "2009": 100, "2010": 100}}},
            "savings updated": False},
        "master_savings": {
            "metrics": {
                "anpv": {
                    "stock cost": {
                        "2009": {"residential": 100, "commercial": None},
                        "2010": {"residential": 100, "commercial": None}},
                    "energy cost": {
                        "2009": {"residential": -200, "commercial": None},
                        "2010": {"residential": -200, "commercial": None}},
                    "carbon cost": {
                        "2009": {"residential": -100, "commercial": None},
                        "2010": {"residential": -100, "commercial": None}}}}}}

    # Instantiate all sample measure objects and an engine object that uses
    # these measures as its input. Use two versions of the first and third
    # sample measures : one with all point values for inputs, and one with
    # list inputs for energy/carbon and associated costs in the first measure
    # and for capital cost in the third measure

    # Version with point value inputs for all sample measures

    # Define list of all competing/interacting cooling measures
    measures_all = [run.Measure(**x) for x in [
        compete_meas1, compete_meas2, compete_meas3, compete_meas4,
        compete_meas5]]
    # Define the demand and supply-side subsets of the above measures
    measures_demand = measures_all[0:2]
    measures_supply = measures_all[2:5]
    # Define the list of supply-side measures and associated contributing
    # microsegment keys that overlap with the above demand-side measures
    measures_overlap1 = {
        "measures": measures_all[2:5],
        "keys": [[str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'supply', 'ASHP'])],
                 [str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'supply', 'ASHP'])],
                 [str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'supply', 'ASHP'])]]}
    # Define the list of demand-side measures and associated contributing
    # microsegment keys that overlap with the above supply-side measures
    measures_overlap2 = {
        "measures": measures_all[0:2],
        "keys": [[str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'demand', 'windows conduction'])],
                 [str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'demand', 'windows conduction'])]]}

    # Instantiate engine object based on above measures
    a_run = run.Engine(measures_all)

    # Version with list inputs for sample measures 1 and 3

    # Define list of all competing/interacting measures
    measures_all_dist = [run.Measure(**x) for x in [
        compete_meas1_dist, copy.deepcopy(compete_meas2),
        compete_meas3_dist, copy.deepcopy(compete_meas4),
        copy.deepcopy(compete_meas5)]]
    # Define the demand and supply-side subsets of the above measures
    measures_demand_dist = measures_all_dist[0:2]
    measures_supply_dist = measures_all_dist[2:5]
    # Define a list of measures that require supply-demand adjustments
    # (none for the first part of this test, which runs only the
    # demand-side measures)
    supply_demand_adjust1_dist = measures_all_dist[0:2]
    supply_demand_adjust2_dist = measures_all_dist[2:5]
    # Define the list of supply-side measures and associated contributing
    # microsegment keys that overlap with the above demand-side measures
    measures_overlap1_dist = {
        "measures": measures_all_dist[2:5],
        "keys": [[str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'supply', 'ASHP'])],
                 [str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'supply', 'ASHP'])],
                 [str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'supply', 'ASHP'])]]}
    # No secondary effects for supply-side measures
    measures_overlap2_dist = {
        "measures": measures_all_dist[0:2],
        "keys": [[str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'demand', 'windows conduction'])],
                 [str(['AIA_CZ1', 'single family home', 'electricity (grid)',
                       'cooling', 'demand', 'windows conduction'])]]}
    # Instantiate engine object based on above measures
    a_run_dist = run.Engine(measures_all_dist)

    # Define the correct master microsegment output for each sample measure
    # after running its competition with the other sample measures to
    # determine market shares
    measures_master_msegs = [{
        "stock": {
            "total": {
                "all": {"2009": 10, "2010": 10},
                "measure": {"2009": 2.23, "2010": 2.23}},
            "competed": {
                "all": {"2009": 5, "2010": 5},
                "measure": {"2009": 1.11, "2010": 1.11}}},
        "energy": {
            "total": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {"2009": 18.94, "2010": 18.94}},
            "competed": {
                "baseline": {"2009": 10, "2010": 10},
                "efficient": {"2009": 8.94, "2010": 8.94}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {"2009": 27.88, "2010": 27.88}},
            "competed": {
                "baseline": {"2009": 15, "2010": 15},
                "efficient": {"2009": 12.88, "2010": 12.88}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 8.89, "2010": 8.89}},
                "competed": {
                    "baseline": {"2009": 5, "2010": 5},
                    "efficient": {"2009": 3.89, "2010": 3.89}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 18.94, "2010": 18.94}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 8.94, "2010": 8.94}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 27.88, "2010": 27.88}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {"2009": 12.88, "2010": 12.88}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 20, "2010": 20},
                "measure": {"2009": 17.77, "2010": 17.77}},
            "competed": {
                "all": {"2009": 10, "2010": 10},
                "measure": {"2009": 8.89, "2010": 8.89}}},
        "energy": {
            "total": {
                "baseline": {"2009": 40, "2010": 40},
                "efficient": {"2009": 31.31, "2010": 31.31}},
            "competed": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {"2009": 11.31, "2010": 11.31}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 60, "2010": 60},
                "efficient": {"2009": 42.62, "2010": 42.62}},
            "competed": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {"2009": 12.62, "2010": 12.62}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 11.11, "2010": 11.11}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 1.11, "2010": 1.11}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 40, "2010": 40},
                    "efficient": {"2009": 31.31, "2010": 31.31}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 11.31, "2010": 11.31}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {"2009": 42.62, "2010": 42.62}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 12.62, "2010": 12.62}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 10, "2010": 10},
                "measure": {"2009": 1.73, "2010": 1.73}},
            "competed": {
                "all": {"2009": 5, "2010": 5},
                "measure": {"2009": 0.87, "2010": 0.87}}},
        "energy": {
            "total": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {"2009": 19.18, "2010": 19.18}},
            "competed": {
                "baseline": {"2009": 10, "2010": 10},
                "efficient": {"2009": 9.18, "2010": 9.18}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {"2009": 28.35, "2010": 28.35}},
            "competed": {
                "baseline": {"2009": 15, "2010": 15},
                "efficient": {"2009": 13.35, "2010": 13.35}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 9.13, "2010": 9.13}},
                "competed": {
                    "baseline": {"2009": 5, "2010": 5},
                    "efficient": {"2009": 4.13, "2010": 4.13}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 19.18, "2010": 19.18}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 9.18, "2010": 9.18}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 28.35, "2010": 28.35}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {"2009": 13.35, "2010": 13.35}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 20, "2010": 20},
                "measure": {"2009": 16.04, "2010": 16.04}},
            "competed": {
                "all": {"2009": 10, "2010": 10},
                "measure": {"2009": 8.02, "2010": 8.02}}},
        "energy": {
            "total": {
                "baseline": {"2009": 40, "2010": 40},
                "efficient": {"2009": 32.13, "2010": 32.13}},
            "competed": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {"2009": 12.13, "2010": 12.13}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 60, "2010": 60},
                "efficient": {"2009": 44.26, "2010": 44.26}},
            "competed": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {"2009": 14.26, "2010": 14.26}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 11.98, "2010": 11.98}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 1.98, "2010": 1.98}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 40, "2010": 40},
                    "efficient": {"2009": 32.13, "2010": 32.13}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 12.13, "2010": 12.13}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {"2009": 44.26, "2010": 44.26}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 14.26, "2010": 14.26}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 30, "2010": 30},
                "measure": {"2009": 22.22, "2010": 22.22}},
            "competed": {
                "all": {"2009": 15, "2010": 15},
                "measure": {"2009": 11.11, "2010": 11.11}}},
        "energy": {
            "total": {
                "baseline": {"2009": 60, "2010": 60},
                "efficient": {"2009": 48.94, "2010": 48.94}},
            "competed": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {"2009": 18.94, "2010": 18.94}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 90, "2010": 90},
                "efficient": {"2009": 67.89, "2010": 67.89}},
            "competed": {
                "baseline": {"2009": 45, "2010": 45},
                "efficient": {"2009": 22.89, "2010": 22.89}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 18.89, "2010": 18.89}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {"2009": 3.89, "2010": 3.89}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {"2009": 48.94, "2010": 48.94}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 18.94, "2010": 18.94}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 90, "2010": 90},
                    "efficient": {"2009": 67.89, "2010": 67.89}},
                "competed": {
                    "baseline": {"2009": 45, "2010": 45},
                    "efficient": {"2009": 22.89, "2010": 22.89}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}}]

    # Correct master microsegment output for runs with list inputs
    # for sample measures 1 and 3
    measures_master_msegs_dist = [{
        "stock": {
            "total": {
                "all": {"2009": 10, "2010": 10},
                "measure": {
                    "2009": numpy.array([2.23, 9.77, 0.02]),
                    "2010": numpy.array([2.23, 9.77, 0.02])}},
            "competed": {
                "all": {"2009": 5, "2010": 5},
                "measure": {
                    "2009": numpy.array([1.11, 4.89, 0.01]),
                    "2010": numpy.array([1.11, 4.89, 0.01])}}},
        "energy": {
            "total": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {
                    "2009": numpy.array([18.94, 16.29, 19.99]),
                    "2010": numpy.array([18.94, 16.29, 19.99])}},
            "competed": {
                "baseline": {"2009": 10, "2010": 10},
                "efficient": {
                    "2009": numpy.array([8.94, 6.29, 9.99]),
                    "2010": numpy.array([8.94, 6.29, 9.99])}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {
                    "2009": numpy.array([27.88, 21.65, 29.99]),
                    "2010": numpy.array([27.88, 21.65, 29.99])}},
            "competed": {
                "baseline": {"2009": 15, "2010": 15},
                "efficient": {
                    "2009": numpy.array([12.88, 6.65, 14.99]),
                    "2010": numpy.array([12.88, 6.65, 14.99])}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {
                        "2009": numpy.array([8.89, 5.11, 9.99]),
                        "2010": numpy.array([8.89, 5.11, 9.99])}},
                "competed": {
                    "baseline": {"2009": 5, "2010": 5},
                    "efficient": {
                        "2009": numpy.array([3.89, 0.11, 4.99]),
                        "2010": numpy.array([3.89, 0.11, 4.99])}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {
                        "2009": numpy.array([18.94, 16.29, 19.99]),
                        "2010": numpy.array([18.94, 16.29, 19.99])}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {
                        "2009": numpy.array([8.94, 6.29, 9.99]),
                        "2010": numpy.array([8.94, 6.29, 9.99])}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {
                        "2009": numpy.array([27.88, 21.65, 29.99]),
                        "2010": numpy.array([27.88, 21.65, 29.99])}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {
                        "2009": numpy.array([12.88, 6.65, 14.99]),
                        "2010": numpy.array([12.88, 6.65, 14.99])}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 20, "2010": 20},
                "measure": {
                    "2009": numpy.array([17.77, 10.23, 19.98]),
                    "2010": numpy.array([17.77, 10.23, 19.98])}},
            "competed": {
                "all": {"2009": 10, "2010": 10},
                "measure": {
                    "2009": numpy.array([8.89, 5.11, 9.99]),
                    "2010": numpy.array([8.89, 5.11, 9.99])}}},
        "energy": {
            "total": {
                "baseline": {"2009": 40, "2010": 40},
                "efficient": {
                    "2009": numpy.array([31.31, 34.89, 30.26]),
                    "2010": numpy.array([31.31, 34.89, 30.26])}},
            "competed": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {
                    "2009": numpy.array([11.31, 14.89, 10.26]),
                    "2010": numpy.array([11.31, 14.89, 10.26])}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 60, "2010": 60},
                "efficient": {
                    "2009": numpy.array([42.62, 49.78, 40.52]),
                    "2010": numpy.array([42.62, 49.78, 40.52])}},
            "competed": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {
                    "2009": numpy.array([12.62, 19.78, 10.52]),
                    "2010": numpy.array([12.62, 19.78, 10.52])}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {
                        "2009": numpy.array([11.11, 14.89, 10.01]),
                        "2010": numpy.array([11.11, 14.89, 10.01])}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {
                        "2009": numpy.array([1.11, 4.89, 0.01]),
                        "2010": numpy.array([1.11, 4.89, 0.01])}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 40, "2010": 40},
                    "efficient": {
                        "2009": numpy.array([31.31, 34.89, 30.26]),
                        "2010": numpy.array([31.31, 34.89, 30.26])}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {
                        "2009": numpy.array([11.31, 14.89, 10.26]),
                        "2010": numpy.array([11.31, 14.89, 10.26])}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {
                        "2009": numpy.array([42.62, 49.78, 40.52]),
                        "2010": numpy.array([42.62, 49.78, 40.52])}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {
                        "2009": numpy.array([12.62, 19.78, 10.52]),
                        "2010": numpy.array([12.62, 19.78, 10.52])}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 10, "2010": 10},
                "measure": {
                    "2009": numpy.array([1.73, 0.02, 9.60]),
                    "2010": numpy.array([1.73, 0.02, 9.60])}},
            "competed": {
                "all": {"2009": 5, "2010": 5},
                "measure": {
                    "2009": numpy.array([0.87, 0.01, 4.80]),
                    "2010": numpy.array([0.87, 0.01, 4.80])}}},
        "energy": {
            "total": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {
                    "2009": numpy.array([19.18, 19.99, 15.43]),
                    "2010": numpy.array([19.18, 19.99, 15.43])}},
            "competed": {
                "baseline": {"2009": 10, "2010": 10},
                "efficient": {
                    "2009": numpy.array([9.18, 9.99, 5.43]),
                    "2010": numpy.array([9.18, 9.99, 5.43])}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {
                    "2009": numpy.array([28.35, 29.98, 20.88]),
                    "2010": numpy.array([28.35, 29.98, 20.88])}},
            "competed": {
                "baseline": {"2009": 15, "2010": 15},
                "efficient": {
                    "2009": numpy.array([13.35, 14.98, 5.88]),
                    "2010": numpy.array([13.35, 14.98, 5.88])}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {
                        "2009": numpy.array([9.13, 9.99, 7.12]),
                        "2010": numpy.array([9.13, 9.99, 7.12])}},
                "competed": {
                    "baseline": {"2009": 5, "2010": 5},
                    "efficient": {
                        "2009": numpy.array([4.13, 4.99, 2.12]),
                        "2010": numpy.array([4.13, 4.99, 2.12])}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {
                        "2009": numpy.array([19.18, 19.99, 15.44]),
                        "2010": numpy.array([19.18, 19.99, 15.44])}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {
                        "2009": numpy.array([9.18, 9.99, 5.44]),
                        "2010": numpy.array([9.18, 9.99, 5.44])}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {
                        "2009": numpy.array([28.35, 29.98, 20.88]),
                        "2010": numpy.array([28.35, 29.98, 20.88])}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {
                        "2009": numpy.array([13.35, 14.98, 5.88]),
                        "2010": numpy.array([13.35, 14.98, 5.88])}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 20, "2010": 20},
                "measure": {
                    "2009": numpy.array([16.04, 17.30, 10.29]),
                    "2010": numpy.array([16.04, 17.30, 10.29])}},
            "competed": {
                "all": {"2009": 10, "2010": 10},
                "measure": {
                    "2009": numpy.array([8.02, 8.65, 5.14]),
                    "2010": numpy.array([8.02, 8.65, 5.14])}}},
        "energy": {
            "total": {
                "baseline": {"2009": 40, "2010": 40},
                "efficient": {
                    "2009": numpy.array([32.13, 31.50, 34.86]),
                    "2010": numpy.array([32.13, 31.50, 34.86])}},
            "competed": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {
                    "2009": numpy.array([12.13, 11.50, 14.86]),
                    "2010": numpy.array([12.13, 11.50, 14.86])}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 60, "2010": 60},
                "efficient": {
                    "2009": numpy.array([44.26, 43.00, 49.72]),
                    "2010": numpy.array([44.26, 43.00, 49.72])}},
            "competed": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {
                    "2009": numpy.array([14.26, 13.00, 19.72]),
                    "2010": numpy.array([14.26, 13.00, 19.72])}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {
                        "2009": numpy.array([11.98, 11.35, 14.86]),
                        "2010": numpy.array([11.98, 11.35, 14.86])}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {
                        "2009": numpy.array([1.98, 1.35, 4.86]),
                        "2010": numpy.array([1.98, 1.35, 4.86])}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 40, "2010": 40},
                    "efficient": {
                        "2009": numpy.array([32.13, 31.50, 34.86]),
                        "2010": numpy.array([32.13, 31.50, 34.86])}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {
                        "2009": numpy.array([12.13, 11.50, 14.86]),
                        "2010": numpy.array([12.13, 11.50, 14.86])}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {
                        "2009": numpy.array([44.26, 43.00, 49.72]),
                        "2010": numpy.array([44.26, 43.00, 49.72])}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {
                        "2009": numpy.array([14.26, 13.00, 19.72]),
                        "2010": numpy.array([14.26, 13.00, 19.72])}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 30, "2010": 30},
                "measure": {
                    "2009": numpy.array([22.22, 22.68, 20.11]),
                    "2010": numpy.array([22.22, 22.68, 20.11])}},
            "competed": {
                "all": {"2009": 15, "2010": 15},
                "measure": {
                    "2009": numpy.array([11.11, 11.34, 10.05]),
                    "2010": numpy.array([11.11, 11.34, 10.05])}}},
        "energy": {
            "total": {
                "baseline": {"2009": 60, "2010": 60},
                "efficient": {
                    "2009": numpy.array([48.94, 48.71, 49.95]),
                    "2010": numpy.array([48.94, 48.71, 49.95])}},
            "competed": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {
                    "2009": numpy.array([18.94, 18.71, 19.95]),
                    "2010": numpy.array([18.94, 18.71, 19.95])}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 90, "2010": 90},
                "efficient": {
                    "2009": numpy.array([67.89, 67.42, 69.90]),
                    "2010": numpy.array([67.89, 67.42, 69.90])}},
            "competed": {
                "baseline": {"2009": 45, "2010": 45},
                "efficient": {
                    "2009": numpy.array([22.89, 22.42, 24.90]),
                    "2010": numpy.array([22.89, 22.42, 24.90])}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {
                        "2009": numpy.array([18.89, 18.66, 19.95]),
                        "2010": numpy.array([18.89, 18.66, 19.95])}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {
                        "2009": numpy.array([3.89, 3.66, 4.95]),
                        "2010": numpy.array([3.89, 3.66, 4.95])}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {
                        "2009": numpy.array([48.94, 48.71, 49.95]),
                        "2010": numpy.array([48.94, 48.71, 49.95])}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {
                        "2009": numpy.array([18.94, 18.71, 19.95]),
                        "2010": numpy.array([18.94, 18.71, 19.95])}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 90, "2010": 90},
                    "efficient": {
                        "2009": numpy.array([67.89, 67.42, 69.90]),
                        "2010": numpy.array([67.89, 67.42, 69.90])}},
                "competed": {
                    "baseline": {"2009": 45, "2010": 45},
                    "efficient": {
                        "2009": numpy.array([22.89, 22.42, 24.90]),
                        "2010": numpy.array([22.89, 22.42, 24.90])}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}}]

    # Define the correct outputs for the competition state of each
    # sample measure after having been competed against the other
    # sample measures (this attribute is used in the 'adjust_measures'
    # function to determine whether a measure has been competed, in which
    # case its savings/cost metrics are updated using 'calc_metric_update')
    measures_adjust_state = [True, True, True, True, True]

    # Test the residential measure competition routine by competing the
    # above sample measures on the specified overlapping microsegment
    # key chain and verifying that the resultant updated measure master
    # microsegment and competition state is correct for each sample measure

    # Test outcomes given sample measures with all point value inputs
    def test_compete_res(self):
        # Run the measure competition routine on all sample demand-side
        # measures first, given their cumulative affect on supply-side measures
        self.a_run.res_compete(self.measures_demand, self.adjust_key1)
        self.a_run.overlap_recording(
            self.measures_demand, self.measures_overlap1, self.adjust_key1)
        # Run the measure competition routine on sample supply-side
        # measures second, taking into consideration any secondary effects
        # from the demand-side measure competition run above
        self.a_run.res_compete(self.measures_supply, self.adjust_key2)
        self.a_run.overlap_recording(
            self.measures_supply, self.measures_overlap2, self.adjust_key2)
        # Make any hvac_envelope adjustments
        measures_overlap_adj = [
            x for x in self.a_run.measures if len(x.mseg_adjust[
                "supply-demand adjustment"]["savings"].keys()) > 0]
        self.a_run.overlap_adjustment(measures_overlap_adj)

        # Check outputs for each sample measure after all have been competed
        for ind, d in enumerate(self.a_run.measures):
            # Check updated measure master microsegment
            self.dict_check(
                self.measures_master_msegs[ind],
                self.a_run.measures[ind].master_mseg)
            # Check updated measure competition state
            self.assertEqual(
                self.measures_adjust_state[ind],
                self.a_run.measures[ind].mseg_adjust["savings updated"])

    # Test outcomes given list inputs for sample measures 1 and 3
    def test_compete_res_dist(self):
        # Run the measure competition and supply-demand overlap recording
        # routines on all sample cooling demand-side measures
        self.a_run_dist.res_compete(
            self.measures_demand_dist, self.adjust_key1)
        self.a_run.overlap_recording(
            self.measures_demand_dist, self.measures_overlap1_dist,
            self.adjust_key1)
        # Run the measure competition and supply-demand overlap recording
        # routines on all sample cooling supply-side measures
        self.a_run_dist.res_compete(
            self.measures_supply_dist, self.adjust_key2)
        self.a_run.overlap_recording(
            self.measures_supply_dist, self.measures_overlap2_dist,
            self.adjust_key2)
        # Remove any overlapping supply-side and demand-side savings
        # that were recorded across all the cooling measures
        measures_overlap_adj = [
            x for x in self.a_run_dist.measures if len(x.mseg_adjust[
                "supply-demand adjustment"]["savings"].keys()) > 0]
        self.a_run_dist.overlap_adjustment(measures_overlap_adj)

        # Check outputs for each sample measure after all have been competed
        for ind, d in enumerate(self.a_run_dist.measures):
            # Check updated measure master microsegment
            self.dict_check_list(
                self.measures_master_msegs_dist[ind],
                self.a_run_dist.measures[ind].master_mseg)
            # Check updated measure competition state
            self.assertEqual(
                self.measures_adjust_state[ind],
                self.a_run_dist.measures[ind].mseg_adjust["savings updated"])


class ComCompeteTest(unittest.TestCase, CommonMethods):
    """ Test the operation of the com_compete function to verify that
    it correctly calculates market shares and updates master microsegments
    for a series of competing commercial measures"""

    # Define sample string for the competed microsegment key chain being tested
    overlap_key = str(['AIA_CZ1', 'assembly', 'electricity (grid)',
                       'lighting', 'reflector (LED)'])

    # Define master microsegments, the microsegment(s) that contribute to the
    # master microsegment (one of which is being competed), and capital/
    # operating cost information for three competing sample lighting measures
    compete_meas1 = {
        "name": "sample compete measure c1",
        "master_mseg": {
            "stock": {
                "total": {
                    "all": {"2009": 10, "2010": 10},
                    "measure": {"2009": 10, "2010": 10}},
                "competed": {
                    "all": {"2009": 5, "2010": 5},
                    "measure": {"2009": 5, "2010": 5}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 15, "2010": 15}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 5, "2010": 5}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 20, "2010": 20}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {"2009": 5, "2010": 5}}},
            "cost": {
                "stock": {
                    "total": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 5, "2010": 5}},
                    "competed": {
                        "baseline": {"2009": 5, "2010": 5},
                        "efficient": {"2009": 0, "2010": 0}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 15, "2010": 15}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 5, "2010": 5}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 20, "2010": 20}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 5, "2010": 5}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}},
        "mseg_adjust": {
            "contributing mseg keys and values": {
                overlap_key: {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}}},
            "competed choice parameters": {
                overlap_key: {
                    "rate distribution": {
                        "2009": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.4],
                        "2010": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.4]}}},
            "supply-demand adjustment": {
                "savings": {},
                "total": {}},
            "savings updated": False},
        "master_savings": {
            "metrics": {
                "anpv": {
                    "stock cost": {
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": 85, "rate 2": 90, "rate 3": 95,
                                "rate 4": 100, "rate 5": 105,
                                "rate 6": 110, "rate 7": 115}},
                        "2010": {
                            "residential": None,
                            "commercial": {
                                "rate 1": 85, "rate 2": 90, "rate 3": 95,
                                "rate 4": 100, "rate 5": 105,
                                "rate 6": 110, "rate 7": 115}}},
                    "energy cost": {
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -435, "rate 2": -440,
                                "rate 3": -145,
                                "rate 4": -150, "rate 5": -155,
                                "rate 6": -160,
                                "rate 7": -370}},
                        "2010": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -435, "rate 2": -440,
                                "rate 3": -145,
                                "rate 4": -150, "rate 5": -155,
                                "rate 6": -160,
                                "rate 7": -370}}},
                    "carbon cost": {
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -135, "rate 2": -140,
                                "rate 3": -145,
                                "rate 4": -150, "rate 5": -155,
                                "rate 6": -160,
                                "rate 7": -170}},
                        "2010": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -135, "rate 2": -140,
                                "rate 3": -145,
                                "rate 4": -150, "rate 5": -155,
                                "rate 6": -160,
                                "rate 7": -170}}}}}}}

    # Create an alternate version of sample measure 1 above that
    # includes a list of capital cost input values instead of
    # point values
    compete_meas1_dist = {
        "name": "sample compete measure c1 dist",
        "master_mseg": {
            "stock": {
                "total": {
                    "all": {"2009": 10, "2010": 10},
                    "measure": {"2009": 10, "2010": 10}},
                "competed": {
                    "all": {"2009": 5, "2010": 5},
                    "measure": {"2009": 5, "2010": 5}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 15, "2010": 15}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 5, "2010": 5}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 20, "2010": 20}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {"2009": 5, "2010": 5}}},
            "cost": {
                "stock": {
                    "total": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": numpy.array([5, 6, 7]),
                                      "2010": numpy.array([5, 6, 7])}},
                    "competed": {
                        "baseline": {"2009": 5, "2010": 5},
                        "efficient": {"2009": numpy.array([0, 1, 2]),
                                      "2010": numpy.array([0, 1, 2])}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 15, "2010": 15}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 5, "2010": 5}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 20, "2010": 20}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 5, "2010": 5}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}},
        "mseg_adjust": {
            "contributing mseg keys and values": {
                overlap_key: {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": numpy.array([5, 6, 7]),
                                              "2010": numpy.array([5, 6, 7])}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": numpy.array([0, 1, 2]),
                                              "2010": numpy.array([
                                                  0, 1, 2])}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}}},
            "competed choice parameters": {
                overlap_key: {
                    "rate distribution": {
                        "2009": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.4],
                        "2010": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.4]}}},
            "supply-demand adjustment": {
                "savings": {},
                "total": {}},
            "savings updated": False},
        "master_savings": {
            "metrics": {
                "anpv": {
                    "stock cost": {
                        "2009": numpy.array(
                            [{"residential": None,
                              "commercial": {
                                  "rate 1": 85, "rate 2": 90, "rate 3": 95,
                                  "rate 4": 100, "rate 5": 105,
                                  "rate 6": 110, "rate 7": 115}},
                             {"residential": None,
                              "commercial": {
                                  "rate 1": 205, "rate 2": 100, "rate 3": 105,
                                  "rate 4": 110, "rate 5": 115,
                                  "rate 6": 120, "rate 7": 125}},
                             {"residential": None,
                              "commercial": {
                                  "rate 1": 105, "rate 2": 110, "rate 3": 115,
                                  "rate 4": 120, "rate 5": 125,
                                  "rate 6": 10, "rate 7": 135}}]),
                        "2010": numpy.array(
                            [{"residential": None,
                              "commercial": {
                                  "rate 1": 85, "rate 2": 90, "rate 3": 95,
                                  "rate 4": 100, "rate 5": 105,
                                  "rate 6": 110, "rate 7": 115}},
                             {"residential": None,
                              "commercial": {
                                  "rate 1": 205, "rate 2": 100, "rate 3": 105,
                                  "rate 4": 110, "rate 5": 115,
                                  "rate 6": 120, "rate 7": 125}},
                             {"residential": None,
                              "commercial": {
                                  "rate 1": 105, "rate 2": 110, "rate 3": 115,
                                  "rate 4": 120, "rate 5": 125,
                                  "rate 6": 10, "rate 7": 135}}])},
                    "energy cost": {
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -435, "rate 2": -440,
                                "rate 3": -145,
                                "rate 4": -150, "rate 5": -155,
                                "rate 6": -160,
                                "rate 7": -370}},
                        "2010": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -435, "rate 2": -440,
                                "rate 3": -145,
                                "rate 4": -150, "rate 5": -155,
                                "rate 6": -160,
                                "rate 7": -370}}},
                    "carbon cost": {
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -135, "rate 2": -140,
                                "rate 3": -145,
                                "rate 4": -150, "rate 5": -155,
                                "rate 6": -160,
                                "rate 7": -170}},
                        "2010": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -135, "rate 2": -140,
                                "rate 3": -145,
                                "rate 4": -150, "rate 5": -155,
                                "rate 6": -160,
                                "rate 7": -170}}}}}}}

    compete_meas2 = {
        "name": "sample compete measure c2",
        "master_mseg": {
            "stock": {
                "total": {
                    "all": {"2009": 20, "2010": 20},
                    "measure": {"2009": 20, "2010": 20}},
                "competed": {
                    "all": {"2009": 10, "2010": 10},
                    "measure": {"2009": 10, "2010": 10}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 40, "2010": 40},
                    "efficient": {"2009": 30, "2010": 30}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 10, "2010": 10}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {"2009": 40, "2010": 40}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 10, "2010": 10}}},
            "cost": {
                "stock": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 10, "2010": 10}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 0, "2010": 0}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 40, "2010": 40},
                        "efficient": {"2009": 30, "2010": 30}},
                    "competed": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 10, "2010": 10}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 60, "2010": 60},
                        "efficient": {"2009": 40, "2010": 40}},
                    "competed": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 10, "2010": 10}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}},
        "mseg_adjust": {
            "contributing mseg keys and values": {
                overlap_key: {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}}},
                str(['AIA_CZ2', 'single family home', 'electricity (grid)',
                     'lighting', 'reflector (LED)']): {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}},
            "competed choice parameters": {
                overlap_key: {
                    "rate distribution": {
                        "2009": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.4],
                        "2010": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.4]}}},
            "supply-demand adjustment": {
                "savings": {},
                "total": {}},
            "savings updated": False},
        "master_savings": {
            "metrics": {
                "anpv": {
                    "stock cost": {
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": 100, "rate 2": 110,
                                "rate 3": 120, "rate 4": 130,
                                "rate 5": 140, "rate 6": 150,
                                "rate 7": 160}},
                        "2010": {
                            "residential": None,
                            "commercial": {
                                "rate 1": 100, "rate 2": 110,
                                "rate 3": 120, "rate 4": 130,
                                "rate 5": 140, "rate 6": 150,
                                "rate 7": 160}}},
                    "energy cost": {
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -350, "rate 2": -60,
                                "rate 3": -70, "rate 4": -380,
                                "rate 5": -390, "rate 6": -150,
                                "rate 7": -400}},
                        "2010": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -350, "rate 2": -60,
                                "rate 3": -70, "rate 4": -380,
                                "rate 5": -390, "rate 6": -150,
                                "rate 7": -400}}},
                    "carbon cost": {
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -40, "rate 2": -50,
                                "rate 3": -55, "rate 4": -60,
                                "rate 5": -65, "rate 6": -70,
                                "rate 7": -75}},
                        "2010": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -40, "rate 2": -50,
                                "rate 3": -55, "rate 4": -60,
                                "rate 5": -65, "rate 6": -70,
                                "rate 7": -75}}}}}}}

    compete_meas3 = {
        "name": "sample compete measure c3",
        "master_mseg": {
            "stock": {
                "total": {
                    "all": {"2009": 30, "2010": 30},
                    "measure": {"2009": 30, "2010": 30}},
                "competed": {
                    "all": {"2009": 15, "2010": 15},
                    "measure": {"2009": 15, "2010": 15}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {"2009": 45, "2010": 45}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 15, "2010": 15}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 90, "2010": 90},
                    "efficient": {"2009": 60, "2010": 60}},
                "competed": {
                    "baseline": {"2009": 45, "2010": 45},
                    "efficient": {"2009": 15, "2010": 15}}},
            "cost": {
                "stock": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 15, "2010": 15}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 0, "2010": 0}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 60, "2010": 60},
                        "efficient": {"2009": 45, "2010": 45}},
                    "competed": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 15, "2010": 15}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 90, "2010": 90},
                        "efficient": {"2009": 60, "2010": 60}},
                    "competed": {
                        "baseline": {"2009": 45, "2010": 45},
                        "efficient": {"2009": 15, "2010": 15}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}},
        "mseg_adjust": {
            "contributing mseg keys and values": {
                overlap_key: {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}}},
                str(['AIA_CZ2', 'single family home', 'electricity (grid)',
                     'lighting', 'reflector (LED)']): {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}},
                str(['AIA_CZ2', 'multi family home', 'electricity (grid)',
                     'lighting', 'reflector (LED)']): {
                    "stock": {
                        "total": {
                            "all": {"2009": 10, "2010": 10},
                            "measure": {"2009": 10, "2010": 10}},
                        "competed": {
                            "all": {"2009": 5, "2010": 5},
                            "measure": {"2009": 5, "2010": 5}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 15, "2010": 15}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 20, "2010": 20}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 5, "2010": 5}}},
                    "cost": {
                        "stock": {
                            "total": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}},
                            "competed": {
                                "baseline": {"2009": 5, "2010": 5},
                                "efficient": {"2009": 0, "2010": 0}}},
                        "energy": {
                            "total": {
                                "baseline": {"2009": 20, "2010": 20},
                                "efficient": {"2009": 15, "2010": 15}},
                            "competed": {
                                "baseline": {"2009": 10, "2010": 10},
                                "efficient": {"2009": 5, "2010": 5}}},
                        "carbon": {
                            "total": {
                                "baseline": {"2009": 30, "2010": 30},
                                "efficient": {"2009": 20, "2010": 20}},
                            "competed": {
                                "baseline": {"2009": 15, "2010": 15},
                                "efficient": {"2009": 5, "2010": 5}}}},
                    "lifetime": {"baseline": {"2009": 1, "2010": 1},
                                 "measure": {"2009": 1, "2010": 1}}},
            "competed choice parameters": {
                overlap_key: {
                    "rate distribution": {
                        "2009": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.4],
                        "2010": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.4]}}},
            "supply-demand adjustment": {
                "savings": {},
                "total": {}},
            "savings updated": False},
        "master_savings": {
            "metrics": {
                "anpv": {
                    "stock cost": {
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": 50, "rate 2": 60, "rate 3": 70,
                                "rate 4": 80, "rate 5": 90, "rate 6": 100,
                                "rate 7": 110}},
                        "2010": {
                            "residential": None,
                            "commercial": {
                                "rate 1": 50, "rate 2": 60, "rate 3": 70,
                                "rate 4": 80, "rate 5": 90, "rate 6": 100,
                                "rate 7": 110}}},
                    "energy cost": {
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -190, "rate 2": -195,
                                "rate 3": -190,
                                "rate 4": -205, "rate 5": -180,
                                "rate 6": -230,
                                "rate 7": -200}},
                        "2010": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -190, "rate 2": -195,
                                "rate 3": -190,
                                "rate 4": -205, "rate 5": -180,
                                "rate 6": -230,
                                "rate 7": -200}}},
                    "carbon cost": {
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -90, "rate 2": -95,
                                "rate 3": -100,
                                "rate 4": -105, "rate 5": -110,
                                "rate 6": -115,
                                "rate 7": -120}},
                        "2009": {
                            "residential": None,
                            "commercial": {
                                "rate 1": -90, "rate 2": -95,
                                "rate 3": -100,
                                "rate 4": -105, "rate 5": -110,
                                "rate 6": -115,
                                "rate 7": -120}}}}}}}

    # Instantiate the three competing sample supply-side measure objects
    # and an engine object that uses these measures as its input. Use
    # two versions of the first sample measure: one with all point
    # values for inputs, and one with a list input for capital cost

    # Version with point value inputs for all sample measures

    # Define list of all competing measures
    measures_compete = [run.Measure(**x) for x in [
        compete_meas1, compete_meas2, compete_meas3]]
    # Instantiate engine object based on above measures
    a_run = run.Engine(measures_compete)

    # Version with a list input for sample measure 1

    # Define list of all competing measures
    measures_compete_dist = [run.Measure(**x) for x in [
        compete_meas1_dist, copy.deepcopy(compete_meas2),
        copy.deepcopy(compete_meas3)]]
    # Instantiate engine object based on above measures
    a_run_dist = run.Engine(measures_compete_dist)

    # No supply-demand overlaps for lighting measures (only heating/cooling)
    measures_overlap = {"measures": [], "keys": []}

    # Define the correct master microsegment output for each sample measure
    # after running its competition with the other sample measures to
    # determine market shares

    # Correct master microsegment output for runs with point value inputs
    # for all sample measures
    measures_master_msegs = [{
        "stock": {
            "total": {
                "all": {"2009": 10, "2010": 10},
                "measure": {"2009": 6, "2010": 6}},
            "competed": {
                "all": {"2009": 5, "2010": 5},
                "measure": {"2009": 3, "2010": 3}}},
        "energy": {
            "total": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {"2009": 17, "2010": 17}},
            "competed": {
                "baseline": {"2009": 10, "2010": 10},
                "efficient": {"2009": 7, "2010": 7}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {"2009": 24, "2010": 24}},
            "competed": {
                "baseline": {"2009": 15, "2010": 15},
                "efficient": {"2009": 9, "2010": 9}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 7, "2010": 7}},
                "competed": {
                    "baseline": {"2009": 5, "2010": 5},
                    "efficient": {"2009": 2, "2010": 2}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 17, "2010": 17}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 7, "2010": 7}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 24, "2010": 24}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {"2009": 9, "2010": 9}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 20, "2010": 20},
                "measure": {"2009": 12, "2010": 12}},
            "competed": {
                "all": {"2009": 10, "2010": 10},
                "measure": {"2009": 6, "2010": 6}}},
        "energy": {
            "total": {
                "baseline": {"2009": 40, "2010": 40},
                "efficient": {"2009": 34, "2010": 34}},
            "competed": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {"2009": 14, "2010": 14}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 60, "2010": 60},
                "efficient": {"2009": 48, "2010": 48}},
            "competed": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {"2009": 18, "2010": 18}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 14, "2010": 14}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {"2009": 4, "2010": 4}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 40, "2010": 40},
                    "efficient": {"2009": 34, "2010": 34}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {"2009": 14, "2010": 14}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {"2009": 48, "2010": 48}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 18, "2010": 18}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 30, "2010": 30},
                "measure": {"2009": 22, "2010": 22}},
            "competed": {
                "all": {"2009": 15, "2010": 15},
                "measure": {"2009": 11, "2010": 11}}},
        "energy": {
            "total": {
                "baseline": {"2009": 60, "2010": 60},
                "efficient": {"2009": 49, "2010": 49}},
            "competed": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {"2009": 19, "2010": 19}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 90, "2010": 90},
                "efficient": {"2009": 68, "2010": 68}},
            "competed": {
                "baseline": {"2009": 45, "2010": 45},
                "efficient": {"2009": 23, "2010": 23}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 19, "2010": 19}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {"2009": 4, "2010": 4}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {"2009": 49, "2010": 49}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {"2009": 19, "2010": 19}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 90, "2010": 90},
                    "efficient": {"2009": 68, "2010": 68}},
                "competed": {
                    "baseline": {"2009": 45, "2010": 45},
                    "efficient": {"2009": 23, "2010": 23}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}}]

    # Correct master microsegment output for runs with a list
    # input for sample measure 1 capital cost
    measures_master_msegs_dist = [{
        "stock": {
            "total": {
                "all": {"2009": 10, "2010": 10},
                "measure": {
                    "2009": numpy.array([6, 5, 3]),
                    "2010": numpy.array([6, 5, 3])}},
            "competed": {
                "all": {"2009": 5, "2010": 5},
                "measure": {
                    "2009": numpy.array([3.0, 2.5, 1.5]),
                    "2010": numpy.array([3.0, 2.5, 1.5])}}},
        "energy": {
            "total": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {
                    "2009": numpy.array([17.0, 17.5, 18.5]),
                    "2010": numpy.array([17.0, 17.5, 18.5])}},
            "competed": {
                "baseline": {"2009": 10, "2010": 10},
                "efficient": {
                    "2009": numpy.array([7.0, 7.5, 8.5]),
                    "2010": numpy.array([7.0, 7.5, 8.5])}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {
                    "2009": numpy.array([24, 25, 27]),
                    "2010": numpy.array([24, 25, 27])}},
            "competed": {
                "baseline": {"2009": 15, "2010": 15},
                "efficient": {
                    "2009": numpy.array([9, 10, 12]),
                    "2010": numpy.array([9, 10, 12])}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {
                        "2009": numpy.array([7, 8, 9.1]),
                        "2010": numpy.array([7, 8, 9.1])}},
                "competed": {
                    "baseline": {"2009": 5, "2010": 5},
                    "efficient": {
                        "2009": numpy.array([2, 3, 4.1]),
                        "2010": numpy.array([2, 3, 4.1])}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {
                        "2009": numpy.array([17, 17.5, 18.5]),
                        "2010": numpy.array([17, 17.5, 18.5])}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {
                        "2009": numpy.array([7, 7.5, 8.5]),
                        "2010": numpy.array([7, 7.5, 8.5])}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {
                        "2009": numpy.array([24, 25, 27]),
                        "2010": numpy.array([24, 25, 27])}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {
                        "2009": numpy.array([9, 10, 12]),
                        "2010": numpy.array([9, 10, 12])}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 20, "2010": 20},
                "measure": {
                    "2009": numpy.array([12, 13, 16]),
                    "2010": numpy.array([12, 13, 16])}},
            "competed": {
                "all": {"2009": 10, "2010": 10},
                "measure": {
                    "2009": numpy.array([6, 6.5, 8]),
                    "2010": numpy.array([6, 6.5, 8])}}},
        "energy": {
            "total": {
                "baseline": {"2009": 40, "2010": 40},
                "efficient": {
                    "2009": numpy.array([34, 33.5, 32]),
                    "2010": numpy.array([34, 33.5, 32])}},
            "competed": {
                "baseline": {"2009": 20, "2010": 20},
                "efficient": {
                    "2009": numpy.array([14, 13.5, 12]),
                    "2010": numpy.array([14, 13.5, 12])}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 60, "2010": 60},
                "efficient": {
                    "2009": numpy.array([48, 47, 44]),
                    "2010": numpy.array([48, 47, 44])}},
            "competed": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {
                    "2009": numpy.array([18, 17, 14]),
                    "2010": numpy.array([18, 17, 14])}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {
                        "2009": numpy.array([14, 13.5, 12]),
                        "2010": numpy.array([14, 13.5, 12])}},
                "competed": {
                    "baseline": {"2009": 10, "2010": 10},
                    "efficient": {
                        "2009": numpy.array([4, 3.5, 2]),
                        "2010": numpy.array([4, 3.5, 2])}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 40, "2010": 40},
                    "efficient": {
                        "2009": numpy.array([34, 33.5, 32]),
                        "2010": numpy.array([34, 33.5, 32])}},
                "competed": {
                    "baseline": {"2009": 20, "2010": 20},
                    "efficient": {
                        "2009": numpy.array([14, 13.5, 12]),
                        "2010": numpy.array([14, 13.5, 12])}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {
                        "2009": numpy.array([48, 47, 44]),
                        "2010": numpy.array([48, 47, 44])}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {
                        "2009": numpy.array([18, 17, 14]),
                        "2010": numpy.array([18, 17, 14])}}}},
        "lifetime": {"baseline": {"2009": 1, "2010": 1},
                     "measure": {"2009": 1, "2010": 1}}},
        {
        "stock": {
            "total": {
                "all": {"2009": 30, "2010": 30},
                "measure": {
                    "2009": numpy.array([22, 22, 21]),
                    "2010": numpy.array([22, 22, 21])}},
            "competed": {
                "all": {"2009": 15, "2010": 15},
                "measure": {
                    "2009": numpy.array([11, 11, 10.5]),
                    "2010": numpy.array([11, 11, 10.5])}}},
        "energy": {
            "total": {
                "baseline": {"2009": 60, "2010": 60},
                "efficient": {
                    "2009": numpy.array([49, 49, 49.5]),
                    "2010": numpy.array([49, 49, 49.5])}},
            "competed": {
                "baseline": {"2009": 30, "2010": 30},
                "efficient": {
                    "2009": numpy.array([19, 19, 19.5]),
                    "2010": numpy.array([19, 19, 19.5])}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 90, "2010": 90},
                "efficient": {
                    "2009": numpy.array([68, 68, 69]),
                    "2010": numpy.array([68, 68, 69])}},
            "competed": {
                "baseline": {"2009": 45, "2010": 45},
                "efficient": {
                    "2009": numpy.array([23, 23, 24]),
                    "2010": numpy.array([23, 23, 24])}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {
                        "2009": numpy.array([19, 19, 19.5]),
                        "2010": numpy.array([19, 19, 19.5])}},
                "competed": {
                    "baseline": {"2009": 15, "2010": 15},
                    "efficient": {
                        "2009": numpy.array([4, 4, 4.5]),
                        "2010": numpy.array([4, 4, 4.5])}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 60, "2010": 60},
                    "efficient": {
                        "2009": numpy.array([49, 49, 49.5]),
                        "2010": numpy.array([49, 49, 49.5])}},
                "competed": {
                    "baseline": {"2009": 30, "2010": 30},
                    "efficient": {
                        "2009": numpy.array([19, 19, 19.5]),
                        "2010": numpy.array([19, 19, 19.5])}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 90, "2010": 90},
                    "efficient": {
                        "2009": numpy.array([68, 68, 69]),
                        "2010": numpy.array([68, 68, 69])}},
                "competed": {
                    "baseline": {"2009": 45, "2010": 45},
                    "efficient": {
                        "2009": numpy.array([23, 23, 24]),
                        "2010": numpy.array([23, 23, 24])}}}},
            "lifetime": {"baseline": {"2009": 1, "2010": 1},
                         "measure": {"2009": 1, "2010": 1}}}]

    # Define the correct outputs for the competition state of each
    # sample measure after having been competed against the other
    # sample measures (this attribute is used in the 'adjust_measures'
    # function to determine whether a measure has been competed, in which
    # case its savings/cost metrics are updated using 'calc_metric_update')
    measures_adjust_state = [True, True, True]

    # Test the commercial measure competition routine by competing the
    # above sample measures on the specified overlapping microsegment
    # key chain and verifying that the resultant updated measure master
    # microsegment and competition state is correct for each sample measure

    # Test outcomes given sample measures with all point value inputs
    def test_compete_com(self):
        # Run the measure competition routine on sample measures
        self.a_run.com_compete(self.measures_compete, self.overlap_key)
        # Check outputs for each sample measure after competition
        for ind, d in enumerate(self.a_run.measures):
            # Check updated measure master microsegment
            self.dict_check(
                self.measures_master_msegs[ind],
                self.a_run.measures[ind].master_mseg)
            # Check updated measure competition state
            self.assertEqual(
                self.measures_adjust_state[ind],
                self.a_run.measures[ind].mseg_adjust["savings updated"])

    # Test outcomes given a list input for sample measure 1 capital cost
    def test_compete_com_dist(self):
        # Run the measure competition routine on sample measures
        self.a_run_dist.com_compete(
            self.measures_compete_dist, self.overlap_key)
        # Check outputs for each sample measure after competition
        for ind, d in enumerate(self.a_run_dist.measures):
            # Check updated measure master microsegment
            self.dict_check_list(
                self.measures_master_msegs_dist[ind],
                self.a_run_dist.measures[ind].master_mseg)
            # Check updated measure competition state
            self.assertEqual(
                self.measures_adjust_state[ind],
                self.a_run_dist.measures[ind].mseg_adjust["savings updated"])


class PackageMergeTest(unittest.TestCase, CommonMethods):
    """ Test the operation of the package_merge function to verify that
    it correctly calculates building energy use shares and updates master
    microsegments for a series of individual measures to be packaged """

    # Initialize package input measures list
    sample_measure_list_package = [run.Measure(**x) for x in [
        sample_measure6, sample_measure7]]
    # Set package measure name
    p = "HVAC"
    # Instantiate package measure object
    packaged_measure = run.Measure_Package(
        sample_measure_list_package, p)
    # Set the measures that contribute to the package measure
    # object that have overlapping baseline microsegments (in this sample
    # case, the two contributing measures overlap)
    overlap_measures = packaged_measure.measures_to_package
    # Set the key name for the overlapping baseline microsegment
    overlap_key = ("('AIA_CZ5', 'single family home', 'electricity (grid)',"
                   "'cooling', 'supply', 'ASHP', 'new')")

    # Set the sample contributing microsegment information that should be
    # generated for each measure to be packaged after accounting for
    # measure overlaps. The contributing microsegment information is
    # needed in 'run.py' to determine measure competition outcomes
    ok_mseg_adjust = [{
        "contributing mseg keys and values": {
            ("('AIA_CZ5', 'single family home', 'electricity (grid)',"
             "'cooling', 'supply', 'ASHP', 'new')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 1000, "2010": 1000},
                        "measure": {"2009": 300, "2010": 300}},
                    "competed": {
                        "all": {"2009": 500, "2010": 500},
                        "measure": {"2009": 50, "2010": 50}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 2000, "2010": 2000},
                        "efficient": {"2009": 1600, "2010": 1600}},
                    "competed": {
                        "baseline": {"2009": 1000, "2010": 1000},
                        "efficient": {"2009": 600, "2010": 600}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 3000, "2010": 3000},
                        "efficient": {"2009": 2400, "2010": 2400}},
                    "competed": {
                        "baseline": {"2009": 1500, "2010": 1500},
                        "efficient": {"2009": 900, "2010": 900}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 140, "2010": 140}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 140, "2010": 140}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 200, "2010": 200},
                            "efficient": {"2009": 160, "2010": 160}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 60, "2010": 60}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 300, "2010": 300},
                            "efficient": {"2009": 240, "2010": 240}},
                        "competed": {
                            "baseline": {"2009": 150, "2010": 150},
                            "efficient": {"2009": 90, "2010": 90}}}},
                "lifetime": {
                    "baseline": {"2009": 18, "2010": 18},
                    "measure": 18}}},
        "competed choice parameters": {
            ("('AIA_CZ5', 'single family home', 'electricity (grid)',"
             "'cooling', 'supply', 'ASHP', 'new')"): {
                "b1": {"2009": 0.75, "2010": 0.75},
                "b2": {"2009": 0.75, "2010": 0.75}}},
        "supply-demand adjustment": {
            "savings": {},
            "total": {}},
        "savings updated": True},
        {
        "contributing mseg keys and values": {
            ("('AIA_CZ5', 'single family home', 'electricity (grid)',"
             "'cooling', 'supply', 'ASHP', 'new')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 1000, "2010": 1000},
                        "measure": {"2009": 300, "2010": 300}},
                    "competed": {
                        "all": {"2009": 500, "2010": 500},
                        "measure": {"2009": 50, "2010": 50}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 2000, "2010": 2000},
                        "efficient": {"2009": 1600, "2010": 1600}},
                    "competed": {
                        "baseline": {"2009": 1000, "2010": 1000},
                        "efficient": {"2009": 600, "2010": 600}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 3000, "2010": 3000},
                        "efficient": {"2009": 2400, "2010": 2400}},
                    "competed": {
                        "baseline": {"2009": 1500, "2010": 1500},
                        "efficient": {"2009": 900, "2010": 900}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 140, "2010": 140}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 140, "2010": 140}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 200, "2010": 200},
                            "efficient": {"2009": 160, "2010": 160}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 60, "2010": 60}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 300, "2010": 300},
                            "efficient": {"2009": 240, "2010": 240}},
                        "competed": {
                            "baseline": {"2009": 150, "2010": 150},
                            "efficient": {"2009": 90, "2010": 90}}}},
                "lifetime": {
                    "baseline": {"2009": 18, "2010": 18},
                    "measure": 18}}},
        "competed choice parameters": {
            ("('AIA_CZ5', 'single family home', 'electricity (grid)',"
             "'cooling', 'supply', 'ASHP', 'new')"): {
                "b1": {"2009": 0.75, "2010": 0.75},
                "b2": {"2009": 0.75, "2010": 0.75}}},
        "supply-demand adjustment": {
            "savings": {},
            "total": {}},
        "savings updated": True}]

    # Set the sample master microsegments that should be generated for
    # each measure to be packaged after accounting for measure overlaps
    ok_master_mseg = [{
        "stock": {
            "total": {
                "all": {"2009": 1000, "2010": 1000},
                "measure": {"2009": 300, "2010": 300}},
            "competed": {
                "all": {"2009": 500, "2010": 500},
                "measure": {"2009": 50, "2010": 50}}},
        "energy": {
            "total": {
                "baseline": {"2009": 2000, "2010": 2000},
                "efficient": {"2009": 1600, "2010": 1600}},
            "competed": {
                "baseline": {"2009": 1000, "2010": 1000},
                "efficient": {"2009": 600, "2010": 600}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 3000, "2010": 3000},
                "efficient": {"2009": 2400, "2010": 2400}},
            "competed": {
                "baseline": {"2009": 1500, "2010": 1500},
                "efficient": {"2009": 900, "2010": 900}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 140, "2010": 140}},
                "competed": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 140, "2010": 140}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 200, "2010": 200},
                    "efficient": {"2009": 160, "2010": 160}},
                "competed": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 60, "2010": 60}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 300, "2010": 300},
                    "efficient": {"2009": 240, "2010": 240}},
                "competed": {
                    "baseline": {"2009": 150, "2010": 150},
                    "efficient": {"2009": 90, "2010": 90}}}},
        "lifetime": {
            "baseline": {"2009": 18, "2010": 18},
            "measure": 18}},
        {
        "stock": {
            "total": {
                "all": {"2009": 1000, "2010": 1000},
                "measure": {"2009": 300, "2010": 300}},
            "competed": {
                "all": {"2009": 500, "2010": 500},
                "measure": {"2009": 50, "2010": 50}}},
        "energy": {
            "total": {
                "baseline": {"2009": 2000, "2010": 2000},
                "efficient": {"2009": 1600, "2010": 1600}},
            "competed": {
                "baseline": {"2009": 1000, "2010": 1000},
                "efficient": {"2009": 600, "2010": 600}}},
        "carbon": {
            "total": {
                "baseline": {"2009": 3000, "2010": 3000},
                "efficient": {"2009": 2400, "2010": 2400}},
            "competed": {
                "baseline": {"2009": 1500, "2010": 1500},
                "efficient": {"2009": 900, "2010": 900}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 140, "2010": 140}},
                "competed": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 140, "2010": 140}}},
            "energy": {
                "total": {
                    "baseline": {"2009": 200, "2010": 200},
                    "efficient": {"2009": 160, "2010": 160}},
                "competed": {
                    "baseline": {"2009": 100, "2010": 100},
                    "efficient": {"2009": 60, "2010": 60}}},
            "carbon": {
                "total": {
                    "baseline": {"2009": 300, "2010": 300},
                    "efficient": {"2009": 240, "2010": 240}},
                "competed": {
                    "baseline": {"2009": 150, "2010": 150},
                    "efficient": {"2009": 90, "2010": 90}}}},
        "lifetime": {
            "baseline": {"2009": 18, "2010": 18},
            "measure": 18}}]

    # Test outcomes of the package_merge function, given sample measure
    # inputs and overlapping microsegment information defined above
    def test_package_merge(self):
        # Run the package_merge routine to remove overlapping market
        # microsegments across the sample measures to be packaged
        self.packaged_measure.package_merge(
            self.overlap_measures, self.overlap_key)
        # Check for correctly updated mseg_adjust and master_mseg
        # attributes for the sample measures to be packaged, following
        # the package_merge run
        for m in range(0, len(self.overlap_measures)):
            # Contributing microsegment dictionary output
            self.dict_check(self.packaged_measure.measures_to_package[
                m].mseg_adjust, self.ok_mseg_adjust[m])
            # Master microsegment dictionary output
            self.dict_check(self.packaged_measure.measures_to_package[
                m].master_mseg, self.ok_master_mseg[m])


class MergeMeasuresTest(unittest.TestCase, CommonMethods):
    """ Test the operation of the merge_measures function to verify that
    it correctly assembles a series of input measures into a package measure"""

    # Initialize package input measures list
    sample_measure_list_package = [run.Measure(**x) for x in [
        sample_measure4, sample_measure5, sample_measure6]]
    # Set package measure name
    p = "CAC + CFLs + NGWH"
    # Instantiate package measure object
    packaged_measure = run.Measure_Package(
        sample_measure_list_package, p)

    # Set the name, climate zone, building type, structure type,
    # fuel type, and end use attributes that should be generated
    # for the packaged measure
    ok_general_attributes = [
        'Package: CAC + CFLs + NGWH',
        ['AIA_CZ1', 'AIA_CZ2', 'AIA_CZ5'],
        ['single family home', 'multi family home'],
        ['new', 'retrofit'],
        ['electricity (grid)', 'natural gas'],
        ['water heating', 'lighting', 'cooling']]

    # Set the sample contributing microsegment information that should be
    # generated for the packaged measure. Contributing microsegment info.
    # is needed in 'run.py' to determine measure competition outcomes
    ok_mseg_adjust = {
        "contributing mseg keys and values": {
            ("('AIA_CZ1', 'single family home', 'natural gas',"
             "'water heating', None, 'new')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 10, "2010": 10},
                        "measure": {"2009": 6, "2010": 6}},
                    "competed": {
                        "all": {"2009": 5, "2010": 5},
                        "measure": {"2009": 1, "2010": 1}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 12, "2010": 12}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 2, "2010": 2}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 18, "2010": 18}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 3, "2010": 3}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 12, "2010": 12}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 2, "2010": 2}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 3, "2010": 3}}}},
                "lifetime": {
                    "baseline": {"2009": 5, "2010": 5},
                    "measure": 10}},
            ("('AIA_CZ1', 'single family home', 'natural gas',"
             "'water heating', None, 'retrofit')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 10, "2010": 10},
                        "measure": {"2009": 6, "2010": 6}},
                    "competed": {
                        "all": {"2009": 5, "2010": 5},
                        "measure": {"2009": 1, "2010": 1}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 12, "2010": 12}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 2, "2010": 2}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 18, "2010": 18}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 3, "2010": 3}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 12, "2010": 12}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 2, "2010": 2}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 3, "2010": 3}}}},
                "lifetime": {
                    "baseline": {"2009": 5, "2010": 5},
                    "measure": 10}},
            ("('AIA_CZ2', 'single family home', 'natural gas',"
             "'water heating', None, 'new')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 10, "2010": 10},
                        "measure": {"2009": 6, "2010": 6}},
                    "competed": {
                        "all": {"2009": 5, "2010": 5},
                        "measure": {"2009": 1, "2010": 1}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 12, "2010": 12}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 2, "2010": 2}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 18, "2010": 18}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 3, "2010": 3}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 12, "2010": 12}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 2, "2010": 2}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 3, "2010": 3}}}},
                "lifetime": {
                    "baseline": {"2009": 5, "2010": 5},
                    "measure": 10}},
            ("('AIA_CZ2', 'single family home', 'natural gas',"
             "'water heating', None, 'retrofit')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 10, "2010": 10},
                        "measure": {"2009": 6, "2010": 6}},
                    "competed": {
                        "all": {"2009": 5, "2010": 5},
                        "measure": {"2009": 1, "2010": 1}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 20, "2010": 20},
                        "efficient": {"2009": 12, "2010": 12}},
                    "competed": {
                        "baseline": {"2009": 10, "2010": 10},
                        "efficient": {"2009": 2, "2010": 2}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 30, "2010": 30},
                        "efficient": {"2009": 18, "2010": 18}},
                    "competed": {
                        "baseline": {"2009": 15, "2010": 15},
                        "efficient": {"2009": 3, "2010": 3}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 18, "2010": 18}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 20, "2010": 20},
                            "efficient": {"2009": 12, "2010": 12}},
                        "competed": {
                            "baseline": {"2009": 10, "2010": 10},
                            "efficient": {"2009": 2, "2010": 2}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 30, "2010": 30},
                            "efficient": {"2009": 18, "2010": 18}},
                        "competed": {
                            "baseline": {"2009": 15, "2010": 15},
                            "efficient": {"2009": 3, "2010": 3}}}},
                "lifetime": {
                    "baseline": {"2009": 5, "2010": 5},
                    "measure": 10}},

            ("('AIA_CZ1', 'single family home', 'electricity (grid)',"
             "'lighting', 'reflector (incandescent)', 'retrofit')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 100, "2010": 100},
                        "measure": {"2009": 60, "2010": 60}},
                    "competed": {
                        "all": {"2009": 50, "2010": 50},
                        "measure": {"2009": 10, "2010": 10}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 200, "2010": 200},
                        "efficient": {"2009": 120, "2010": 120}},
                    "competed": {
                        "baseline": {"2009": 100, "2010": 100},
                        "efficient": {"2009": 20, "2010": 20}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 300, "2010": 300},
                        "efficient": {"2009": 180, "2010": 180}},
                    "competed": {
                        "baseline": {"2009": 150, "2010": 150},
                        "efficient": {"2009": 30, "2010": 30}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 200, "2010": 200},
                            "efficient": {"2009": 120, "2010": 120}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 20, "2010": 20}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 300, "2010": 300},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 150, "2010": 150},
                            "efficient": {"2009": 30, "2010": 30}}}},
                "lifetime": {
                    "baseline": {"2009": 1, "2010": 1},
                    "measure": 20}},
            ("('AIA_CZ1', 'single family home', 'electricity (grid)',"
             "'lighting', 'reflector (halogen)', 'retrofit')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 100, "2010": 100},
                        "measure": {"2009": 60, "2010": 60}},
                    "competed": {
                        "all": {"2009": 50, "2010": 50},
                        "measure": {"2009": 10, "2010": 10}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 200, "2010": 200},
                        "efficient": {"2009": 120, "2010": 120}},
                    "competed": {
                        "baseline": {"2009": 100, "2010": 100},
                        "efficient": {"2009": 20, "2010": 20}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 300, "2010": 300},
                        "efficient": {"2009": 180, "2010": 180}},
                    "competed": {
                        "baseline": {"2009": 150, "2010": 150},
                        "efficient": {"2009": 30, "2010": 30}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 200, "2010": 200},
                            "efficient": {"2009": 120, "2010": 120}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 20, "2010": 20}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 300, "2010": 300},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 150, "2010": 150},
                            "efficient": {"2009": 30, "2010": 30}}}},
                "lifetime": {
                    "baseline": {"2009": 2, "2010": 2},
                    "measure": 15}},

            ("('AIA_CZ5', 'single family home', 'electricity (grid)',"
             "'cooling', 'supply', 'ASHP', 'new')"): {
                "stock": {
                    "total": {
                        "all": {"2009": 1000, "2010": 1000},
                        "measure": {"2009": 600, "2010": 600}},
                    "competed": {
                        "all": {"2009": 500, "2010": 500},
                        "measure": {"2009": 100, "2010": 100}}},
                "energy": {
                    "total": {
                        "baseline": {"2009": 2000, "2010": 2000},
                        "efficient": {"2009": 1200, "2010": 1200}},
                    "competed": {
                        "baseline": {"2009": 1000, "2010": 1000},
                        "efficient": {"2009": 200, "2010": 200}}},
                "carbon": {
                    "total": {
                        "baseline": {"2009": 3000, "2010": 3000},
                        "efficient": {"2009": 1800, "2010": 1800}},
                    "competed": {
                        "baseline": {"2009": 1500, "2010": 1500},
                        "efficient": {"2009": 300, "2010": 300}}},
                "cost": {
                    "stock": {
                        "total": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 180, "2010": 180}}},
                    "energy": {
                        "total": {
                            "baseline": {"2009": 200, "2010": 200},
                            "efficient": {"2009": 120, "2010": 120}},
                        "competed": {
                            "baseline": {"2009": 100, "2010": 100},
                            "efficient": {"2009": 20, "2010": 20}}},
                    "carbon": {
                        "total": {
                            "baseline": {"2009": 300, "2010": 300},
                            "efficient": {"2009": 180, "2010": 180}},
                        "competed": {
                            "baseline": {"2009": 150, "2010": 150},
                            "efficient": {"2009": 30, "2010": 30}}}},
                "lifetime": {
                    "baseline": {"2009": 18, "2010": 18},
                    "measure": 18}}},
        "competed choice parameters": {
            ("('AIA_CZ1', 'single family home', 'natural gas',"
             "'water heating', None, 'new')"): {
                "b1": {"2009": 0.5, "2010": 0.5},
                "b2": {"2009": 0.5, "2010": 0.5}},
            ("('AIA_CZ1', 'single family home', 'natural gas',"
             "'water heating', None, 'retrofit')"): {
                "b1": {"2009": 0.5, "2010": 0.5},
                "b2": {"2009": 0.5, "2010": 0.5}},
            ("('AIA_CZ2', 'single family home', 'natural gas',"
             "'water heating', None, 'new')"): {
                "b1": {"2009": 0.5, "2010": 0.5},
                "b2": {"2009": 0.5, "2010": 0.5}},
            ("('AIA_CZ2', 'single family home', 'natural gas',"
             "'water heating', None, 'retrofit')"): {
                "b1": {"2009": 0.5, "2010": 0.5},
                "b2": {"2009": 0.5, "2010": 0.5}},
            ("('AIA_CZ1', 'single family home', 'electricity (grid)',"
             "'lighting', 'reflector (incandescent)', 'retrofit')"): {
                "b1": {"2009": 0.25, "2010": 0.25},
                "b2": {"2009": 0.25, "2010": 0.25}},
            ("('AIA_CZ1', 'single family home', 'electricity (grid)',"
             "'lighting', 'reflector (halogen)', 'retrofit')"): {
                "b1": {"2009": 0.25, "2010": 0.25},
                "b2": {"2009": 0.25, "2010": 0.25}},
            ("('AIA_CZ5', 'single family home', 'electricity (grid)',"
             "'cooling', 'supply', 'ASHP', 'new')"): {
                "b1": {"2009": 0.75, "2010": 0.75},
                "b2": {"2009": 0.75, "2010": 0.75}}},
        "supply-demand adjustment": {
            "savings": {},
            "total": {}},
        "savings updated": False}

    # Set the sample master microsegment that should be generated for
    # the packaged measure
    ok_master_mseg = {
        "stock": {
            "total": {
                "all": {'2010': 1240, '2009': 1240},
                "measure": {'2010': 744, '2009': 744}},
            "competed": {
                "all": {'2010': 620, '2009': 620},
                "measure": {'2010': 124, '2009': 124}}},
        "energy": {
            "total": {
                "baseline": {'2010': 2480, '2009': 2480},
                "efficient": {'2010': 1488, '2009': 1488}},
            "competed": {
                "baseline": {'2010': 1240, '2009': 1240},
                "efficient": {'2010': 248, '2009': 248}}},
        "carbon": {
            "total": {
                "baseline": {'2010': 3720, '2009': 3720},
                "efficient": {'2010': 2232, '2009': 2232}},
            "competed": {
                "baseline": {'2010': 1860, '2009': 1860},
                "efficient": {'2010': 372, '2009': 372}}},
        "cost": {
            "stock": {
                "total": {
                    "baseline": {'2010': 340, '2009': 340},
                    "efficient": {'2010': 612, '2009': 612}},
                "competed": {
                    "baseline": {'2010': 340, '2009': 340},
                    "efficient": {'2010': 612, '2009': 612}}},
            "energy": {
                "total": {
                    "baseline": {'2010': 680, '2009': 680},
                    "efficient": {'2010': 408, '2009': 408}},
                "competed": {
                    "baseline": {'2010': 340, '2009': 340},
                    "efficient": {'2010': 68, '2009': 68}}},
            "carbon": {
                "total": {
                    "baseline": {'2010': 1020, '2009': 1020},
                    "efficient": {'2010': 612, '2009': 612}},
                "competed": {
                    "baseline": {'2010': 510, '2009': 510},
                    "efficient": {'2010': 102, '2009': 102}}}},
        "lifetime": {
            "baseline": {'2010': 5.86, '2009': 5.86},
            "measure": 13.29}}

    # Test outcomes of the merge_measures function, given sample packaged
    # measure object defined above
    def test_package_measure(self):
        # Run the merge measures routine
        self.packaged_measure.merge_measures()
        # Check for correct package measure name, climate zone, building
        # type, structure type, fuel type, and end use outputs
        output_lists = [
            self.packaged_measure.name, self.packaged_measure.climate_zone,
            self.packaged_measure.bldg_type,
            self.packaged_measure.structure_type,
            self.packaged_measure.fuel_type["primary"],
            self.packaged_measure.end_use["primary"]]
        for ind in range(0, len(output_lists)):
            self.assertEqual(
                sorted(self.ok_general_attributes[ind]),
                sorted(output_lists[ind]))
        # Check for correct package measure mseg_adjust and master_mseg outputs
        self.dict_check(self.packaged_measure.mseg_adjust, self.ok_mseg_adjust)
        self.dict_check(self.packaged_measure.master_mseg, self.ok_master_mseg)


# Offer external code execution (include all lines below this point in all
# test files)
def main():
    # Triggers default behavior of running all test fixtures in the file
    unittest.main()

if __name__ == "__main__":
    main()
