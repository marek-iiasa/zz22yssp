import pandas as pd
import ixmp
import message_ix

from message_ix.util import make_df
# %matplotlib inline

# connection to a database for storing model input data and scenario results
mp = ixmp.Platform()

scenario = message_ix.Scenario(mp, model="West China storage", scenario="baseline", version="new")

# Model Structure
# assume model horizon span 3 decades (2020-2050)
history = [2020]
model_horizon = [2030, 2040, 2050]
scenario.add_horizon(year=history + model_horizon, firstmodelyear=model_horizon[0])

# single "node"
country = "China"
scenario.add_spatial_sets({"country": country})

# modes of operation of technologies, define how certain technologies operate
scenario.add_spatial_sets("commodity", ["electricity", "hydrogen"])
scenario.add_set("level", ["secondary", "", ""])
