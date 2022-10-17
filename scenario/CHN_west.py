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
scenario.add_set("level", ["secondary", "storage", "tertiary", "final", "useful"])
scenario.add_set("technology", ["wind_ppl", "electrolyser", "hydro_turbine", "battery", "fuel_cell", "grid", "bulb"])
scenario.add_set("mode", "standard")

# supply and demand (balancing commodities)
gdp_profile = pd.Series([1.0, 1.5, 1.9], index=pd.Index(model_horizon, name="Time"))
gdp_profile.plot(title="GDP profile")

demand_per_year = 8000  # just assume, need modified
light_demand = pd.DataFrame({"node": country, "commodity": "light", "level": "useful",
                             "year": model_horizon, "time": "year",
                             "value": (demand_per_year * gdp_profile).round(), "unit": "GWa",
                             })
light_demand
scenario.add_par("demand", light_demand)

# define input and output commodities of each technology
# define some common keys
# Input quantities require _origin keys that specify where the inputs are received from.
# Output quantities require _dest keys that specify where the outputs are transferred to.

year_df = scenario.vintage_and_active_years()
vintage_years = year_df["year_vtg"]
act_years = year_df["year_act"]

# Some common values to be used for both the "input" and "output" parameters
base = dict(
    node_loc=country,
    year_vtg=vintage_years,
    year_act=act_years,
    mode="standard",
    time="year",
    unit="-",
)

# Use the message_ix utility function make_df() to create a base data frame for
# different "input" parameter values
base_input = make_df("input", **base, node_origin=country, time_origin="year")

# Create a base data frame for different "output" parameter values
base_output = make_df("output", **base, node_dest=country, time_dest="year")

# Extend `base_output` by filling in some of the other columns, using the
# pandas.DataFrame.assign() method
bulb_out = base_output.assign(
    technology="bulb", commodity="light", level="useful", value=1.0
)
scenario.add_par("output", bulb_out)

bulb_in = base_input.assign(
    technology="bulb", commodity="electricity", level="final", value=1.0
)
scenario.add_par("input", bulb_in)

# parameterize the electrical "grid", receives electricity at the "Tertiary" energy level.
# also outputs electricity, but at the "final" energy level (to be used by the light bulb).
grid_efficiency = 0.9
grid_out = base_output.assign(
    technology="grid",
    commodity="electricity",
    level="final",
    value=grid_efficiency,
)
scenario.add_par("output", grid_out)

grid_in = base_input.assign(
    technology="grid", commodity="electricity", level="secondary", value=1.0
)
scenario.add_par("input", grid_in)

# power plants
wind_out = base_output.assign(
    technology="wind_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)

# Operational Constraints and Parameters
# capacity constraint

capacity_factor = {"wind_ppl": 0.36, "bulb": 1}
for tec, val in capacity_factor.items():
    df = make_df(
        "capacity_factor",
        node_loc=country,
        year_vtg=vintage_years,
        year_act=act_years,
        time="year",
        unit="-",
        technology=tec,
        value=val,
    )
    scenario.add_par("capacity_factor", df)

lifetime = {
    "wind_ppl": 20,
    "bulb": 1,
}

for tec, val in lifetime.items():
    df = make_df(
        "technical_lifetime",
        node_loc=country,
        year_vtg=model_horizon,
        unit="y",
        technology=tec,
        value=val,
    )
    scenario.add_par("technical_lifetime", df)

# Technological Diffusion and Contraction
growth_technologies = [
    "wind_ppl",
]
for tec in growth_technologies:
    df = make_df(
        "growth_activity_up",
        node_loc=country,
        year_act=model_horizon,
        time="year",
        unit="-",
        technology=tec,
        value=0.1,
    )
    scenario.add_par("growth_activity_up", df)

# Defining an Energy Mix (Model Calibration)
historic_demand = 0.5 * demand_per_year
historic_generation = historic_demand / grid_efficiency
old_activity = {
    "wind_ppl": historic_generation,
}
for tec, val in old_activity.items():
    df = make_df(
        "historical_activity",
        node_loc=country,
        year_act=history,
        mode="standard",
        time="year",
        unit="GWa",
        technology=tec,
        value=val,
    )
    scenario.add_par("historical_activity", df)
# And the new capacity in the historic period.
for tec in old_activity:
    value = old_activity[tec] / (1 * 10 * capacity_factor[tec])
    df = make_df(
        "historical_new_capacity",
        node_loc=country,
        year_vtg=history,
        unit="GWa",
        technology=tec,
        value=value,
    )
    scenario.add_par("historical_new_capacity", df)

# Objective Function
# add the interest rate parameter.
scenario.add_par("interestrate", model_horizon, value=0.05, unit="-")
# investment cost
# Add a new unit for ixmp to recognize as valid
mp.add_unit("USD/kW")

# in $ / kW (specific investment cost)
costs = {
    "wind_ppl": 1500,
    "bulb": 5,
}

for tec, val in costs.items():
    df = make_df(
        "inv_cost",
        node_loc=country,
        year_vtg=model_horizon,
        unit="USD/kW",
        technology=tec,
        value=val,
    )
    scenario.add_par("inv_cost", df)
# Fixed O&M Costs
costs = {
    "wind_ppl": 10,
}

for tec, val in costs.items():
    df = make_df(
        "fix_cost",
        node_loc=country,
        year_vtg=vintage_years,
        year_act=act_years,
        unit="USD/kWa",
        technology=tec,
        value=val,
    )
    scenario.add_par("fix_cost", df)
# Variable O&M Costs
costs = {
    "grid": 50,
}

for tec, val in costs.items():
    df = make_df(
        "var_cost",
        node_loc=country,
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="USD/kWa",
        technology=tec,
        value=val,
    )
    scenario.add_par("var_cost", df)

# Time to Solve the Model
from message_ix import log
log.info(f"version number before commit(): {scenario.version}")
scenario.commit(comment="basic model of Westeros electrification")
log.info(f"version number after commit(): {scenario.version}")

scenario.set_as_default()
scenario.solve()
scenario.var("OBJ")["lvl"]