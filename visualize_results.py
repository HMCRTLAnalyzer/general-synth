#run as interactive to show plots / access them!
import pandas
result_folder = "fft_gen_delay_sweep_2to40ns_2023-11-05-20-36"
csv_name = "results_2023-11-06 08:09:06.535201.csv"
csv_path = f"../general-synth/results_dir/{result_folder}/{csv_name}"
df = pandas.read_csv(csv_path) 

df.plot.scatter(x = "period", y = "crit_path")
df.plot.scatter(x = "period", y = "logic_levels")
df.plot.scatter(x = "period", y = "combo_area")
df.plot.scatter(x = "period", y = "noncombo_area")
df.plot.scatter(x = "period", y = "synth_runtime")