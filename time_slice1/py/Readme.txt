Content of the *py files:

Modified/developed by Zixuan:
zzx01.py - Copy from /time clustering/All_time_steps
           Modified with adding the input data path and basic settings like 'midnight', 'region'
           for algorithm picking 48 time slices.

zzx02.py - Copy from /time clustering/All_time_steps
           It is an integrated version for dealing with whatever the number of time slices we choose.
           When we choose to sort 48 time slices (with 2 representative daily time step in a week),
           it calls the function 'algorithm' defined in zzx03.

zzx03.py - Copy from /time clustering/Time_steps_clustering_48.py
           It is a function definition file, define the algorithm used for picking up 48 time slices.

Modified/developed by Marek:
mm01.py - based on zzx01.py, adapted to iMac, and to only CN data (from china.xlsx)
mm02.py - based on zzx02.py, same adaptation as mm01
mm03.py - based on zzx03.py, same adaptation as mm01 (only for algorithm() definition,
	imported by mm02)
