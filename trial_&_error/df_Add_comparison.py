
import pandas as pd
import numpy as np
import time

# Initial DataFrame
df = pd.DataFrame({'A': np.random.rand(10000), 'B': np.random.rand(10000)})

# New row data
new_row = {'A': 0.5, 'B': 0.5}

# Method 1: Using loc
start_time = time.time()
df1 = df.copy()
df1.loc[len(df1)] = new_row
loc_time = time.time() - start_time

# Method 2: Using append
start_time = time.time()
df2 = df.copy()
df2._append(new_row, ignore_index=True)
append_time = time.time() - start_time

# Method 3: Using concat
start_time = time.time()
df3 = df.copy()
df3 = pd.concat([df3, pd.DataFrame([new_row])], ignore_index=True)
concat_time = time.time() - start_time

# Method 4: Using assign with T
start_time = time.time()
df4 = df.copy()
df4 = df4.T.assign(new_row=len(df4)).T
assign_time = time.time() - start_time

print(loc_time, append_time, concat_time, assign_time)
# 0.0010848045349121094 0.00043320655822753906 0.0002949237823486328 0.003961086273193359
