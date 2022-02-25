import os
import pandas as pd

src_folder = "xlsCrossValidate"
out_folder = "raw_crossvalidate_data"

count_states = {
    "active": 5,
    "meditate": 5,
    "neutral": 5
}

for state in count_states:
    for i in range (1, count_states[state] + 1):
        read_file = pd.read_excel(os.path.join(src_folder, state + str(i) + ".xlsx"))
        read_file.to_csv(os.path.join(out_folder, state + str(i) + ".csv"), index=False)

