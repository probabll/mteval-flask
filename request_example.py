import requests

jobs = {'hyps': ['A', 'B'], 'refs': ['A', 'B'], 'srcs': ['a', 'b']}

results = requests.post("http://localhost:4000/score", json=jobs, headers={'Content-Type': 'application/json'}).json()

for name, values in results.items():
    print(name, values)
