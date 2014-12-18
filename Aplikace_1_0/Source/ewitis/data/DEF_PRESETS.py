'''
Created on 17.12.2014

@author: z002ys1y
'''
import sys

DEF_PRESETS = {
               
# 1. BLIZAK                
"blizak": {
        "remote": {
            "GET_SET": {
                "value": 0
            },
            "permanent": True,
            "name": "Remote Race"
        },
        "race_name": {
            "GET_SET": {
                "changed": False,
                "value": "Blizak"
            },
            "permanent": True,
            "name": "race_name"
        },
        "rfid": {
            "GET_SET": {
                "value": 2
            },
            "permanent": True,
            "name": "rfid"
        },
        "tag_filter": {
            "GET_SET": {
                "value": 0
            },
            "permanent": True
        },
        "export": {
            "GET_SET": {
                "changed": False,
                "value": {
                    "best_laptime": 0,
                    "points_categories": 2,
                    "club": 2,
                    "lapsformat": 0,
                    "laps": 0,
                    "year": 2,
                    "option_1": 0,
                    "sex": 0,
                    "option_4_name": "o4",
                    "laptime": 2,
                    "option_4": 0,
                    "option_2_name": "o2",
                    "option_2": 0,
                    "option_3": 0,
                    "gap": 0,
                    "option_3_name": "o3",
                    "points_groups": 2,
                    "option_1_name": "o1",
                    "points_race": 2
                }
            },
            "permanent": True,
            "name": "export"
        },
        "evaluation": {
            "GET_SET": {
                "value": {
                    "points_formula1": {
                        "formula": "laptime-laptime1",
                        "minimum": 0,
                        "maximum": 9999
                    },
                    "points_formula3": {
                        "formula": "2",
                        "minimum": 0,
                        "maximum": 500
                    },
                    "points_formula2": {
                        "formula": "3",
                        "minimum": 0,
                        "maximum": 500
                    },
                    "laptime": 0,
                    "starttime": 0,
                    "order": 0,
                    "points": 1
                }
            },
            "permanent": True
        },
        "additional_info": {
            "GET_SET": {
                "value": {
                    "best_laptime": 2,
                    "order_cat": 2,
                    "points1": 2,
                    "points2": 2,
                    "points3": 2,
                    "enabled": 2,
                    "laptime": 2,
                    "lap":     2,
                    "order":   2
                }
            },
            "permanent": True,
            "name": "additinal info"
        }
    },
               
               
# 2. MTB                 
"mtb": {
        "remote": {
            "GET_SET": {
                "value": 0
            },
            "permanent": True,
            "name": "Remote Race"
        },
        "race_name": {
            "GET_SET": {
                "changed": False,
                "value": "Formula Student 2013"
            },
            "permanent": True,
            "name": "race_name"
        },
        "rfid": {
            "GET_SET": {
                "value": 2
            },
            "permanent": True,
            "name": "rfid"
        },
        "tag_filter": {
            "GET_SET": {
                "value": 0
            },
            "permanent": True
        },
        "export": {
            "GET_SET": {
                "changed": False,
                "value": {
                    "best_laptime": 0,
                    "points_categories": 2,
                    "club": 2,
                    "lapsformat": 0,
                    "laps": 0,
                    "year": 2,
                    "option_1": 0,
                    "sex": 0,
                    "option_4_name": "o4",
                    "laptime": 2,
                    "option_4": 0,
                    "option_2_name": "o2",
                    "option_2": 0,
                    "option_3": 0,
                    "gap": 0,
                    "option_3_name": "o3",
                    "points_groups": 2,
                    "option_1_name": "o1",
                    "points_race": 2
                }
            },
            "permanent": True,
            "name": "export"
        },
        "evaluation": {
            "GET_SET": {
                "value": {
                    "points_formula1": {
                        "formula": "laptime-laptime1",
                        "minimum": 0,
                        "maximum": 9999
                    },
                    "points_formula3": {
                        "formula": "2",
                        "minimum": 0,
                        "maximum": 500
                    },
                    "points_formula2": {
                        "formula": "3",
                        "minimum": 0,
                        "maximum": 500
                    },
                    "laptime": 0,
                    "starttime": 0,
                    "order": 0,
                    "points": 1
                }
            },
            "permanent": True
        },
        "additional_info": {
            "GET_SET": {
                "value": {
                    "best_laptime": 2,
                    "order_cat": 2,
                    "points1": 2,
                    "points2": 2,
                    "points3": 2,
                    "enabled": 2,
                    "laptime": 2,
                    "lap":     2,
                    "order":   2
                }
            },
            "permanent": True,
            "name": "additinal info"
        }
    }
}