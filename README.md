1. Create a virtualenv and activate it

```
virtualenv -p python3.7 ./metrics-venv
source metrics-venv/bin/activate
```

2. Install requirements

```bash
pip install -r requirements.txt
```

3. Download models (e.g., COMET models)

```python
import COMET
comet = COMET(modelname="wmt21-small-da-152012")
```

4. Start the app

For example, with COMET:

```bash
 python app.py comet
```

You can pass arguments to COMET, such as `cuda` support and `modelname`:

```bash
 python app.py comet:cuda=true:modelname=wmt21-small-da-152012
```


5. Make requests

Via command line:

```bash
curl -X POST -d '{"hyps": ["A", "hello world!"], "refs": ["A", "Hello, World!"], "srcs": ["a", "Ola, mundo!"]}' -H "Content-Type: application/json" -v localhost:4000/score
```

Or programmatically (e.g., in python):

```python
import requests

jobs = {'hyps': ['A', 'B'], 'refs': ['A', 'B'], 'srcs': ['a', 'b']}
results = requests.post("http://localhost:4000/score", json=jobs, headers={'Content-Type': 'application/json'}).json()

print(results)
```
