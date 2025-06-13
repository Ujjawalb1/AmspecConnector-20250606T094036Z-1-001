from logger import logger

MALAYSIA_STATE_CODE_MAP = {
    "johor": "01",
    "kedah": "02",
    "kelantan": "03",
    "melaka": "04",
    "negeri sembilan": "05",
    "pahang": "06",
    "pulau pinang": "07",
    "perak": "08",
    "perlis": "09",
    "selangor": "10",
    "terengganu": "11",
    "sabah": "12",
    "sarawak": "13",
    "wilayah persekutuan kuala lumpur": "14",
    "wilayah persekutuan labuan": "15",
    "wilayah persekutuan putrajaya": "16",
    "not applicable": "17"
}

def get_state_codes(state):
    normalized = state.strip().lower()
    return MALAYSIA_STATE_CODE_MAP.get(normalized, "17")