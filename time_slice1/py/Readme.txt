Content of the *py files:

Modified/developed by Zixuan:
zz01.py - Copy from /time clustering/All_time_steps
           Modified by adding the input data path and basic settings like 'midnight',
			  'region' for algorithm picking 48 time slices.
zz02.py - Copy from /time clustering/All_time_steps
           Integrated version for dealing with any chosen number of time slices.
           E.g., to sort 48 time slices (with 2 representative daily time step in a week)
           it calls the 'algorithm' function defined in zz03.
zz03.py - Copy from /time clustering/Time_steps_clustering_48.py
           It defines the function for picking up 48 time slices.
zz04.py - Copy from zz02.py
           Use for read data and call the 'algorithm' in zz05 for select 48 time slices.
zz05.py - Copy and modified from zz03.
           Delete hydro.


Modified/developed by Marek:
mm01.py - based on zzx01.py, adapted to iMac, and to only CN data (from china.xlsx)
mm02.py - based on zzx02.py, same adaptation as mm01
mm03.py - based on zzx03.py, same adaptation as mm01 (only for algorithm() definition,
	imported by mm02)
