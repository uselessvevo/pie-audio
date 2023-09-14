import os

from piekit.config import Max, Min, Lock

TEST_PLUGIN_ENABLE: Lock = bool(int(os.getenv("PIE_TEST_PLUGIN_ENABLE", False)))
REGISTER_ON_MAIN_LAYOUT: Lock = bool(int(os.getenv("PIE_TEST_PLUGIN_REGISTER_ON_MW_LAYOUT", False)))

FIELD_MIN: Min[3] = [1, 2]
FIELD_MAX: Max[3] = [1, 2, 3, 4]
IMMUTABLE_FIELD: Lock = "Immutable string"

TEST_STR_ATTRIBUTE: str = "Test Value"
TEST_LIST_ATTRIBUTE: list[int] = [1, 2, 3]
