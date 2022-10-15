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
scenario.add_spatial_sets("commodity", ["electricity", "hydrogen", "water"])
scenario.add_set("level", ["secondary", "storage", "tertiary", "final"])
scenario.add_set("technology", ["wind_ppl", "electrolyser", "hydro_turbine", "battery", "fuel_cell", "grid"])
scenario.add_set("mode", "standard")

# supply and demand (balancing commodities)
demand_per_year = 8000  # just assume, need modified
electricity_demand = pd.DataFrame({"node": country, "level": "useful", "year": model_horizon, "time": "year",
                                   "value": (demand_per_year * gdp_profile).round(), "unit": "GWa",})
