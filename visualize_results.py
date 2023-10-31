#run as interactive to show plots / access them!
import pandas

csv_path = "/home/nlimpert/clinic/general-synth/results_dir/qdiv_area_0_40k_2023-10-30-07-46/results_2023-10-30 07:49:54.182985.csv"
df = pandas.read_csv(csv_path) 

df.plot.scatter(x = "period", y = "crit_path")
df.plot.scatter(x = "period", y = "logic_levels")
df.plot.scatter(x = "period", y = "combo_area")
df.plot.scatter(x = "period", y = "noncombo_area")
df.plot.scatter(x = "period", y = "synth_runtime")