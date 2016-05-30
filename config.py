import os
root_path = os.path.dirname(os.path.abspath(__file__))
# print("root_path:", root_path)
pickle_path = os.path.join(root_path, 'data/')
source_path = os.path.join(root_path, 'source/')
data_path = os.path.join(root_path, 'data/')

demo_data = {'users' : 'users.pkl' }
