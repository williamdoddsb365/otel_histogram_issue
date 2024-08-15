# Pre-requisites:
- Python3.11
- PIP

# Setup:
- Create python3.11 venv
```
python3.11 -m venv venv
```
- Activate python3.11 venv
```
source venv/bin/activate
```
- Install requirements in venv
```
pip install -r requirements.txt
```

# Usage:
- Run `example.py` and observe the otel metrics which are exported to the console.
- Note that `start_time_unix_nano` value does not change, despite the start_time changing by 10seconds every iteration.
- Note that if you were to send **static** attribute values, e.g. by changing `example.py` Line 28
  - From:
    - `attributes={"dynamic_attribute": random.randint(1, 999)})`
  - To:
    - `attributes={"dynamic_attribute": 1})`

Then `start_time_unix_nano` should begin to increment as expected.

# Example output

Example output when sending **static** value as an attribute, e.g. `"attributes": {"dynamic_attribute": 1 }`
- `start_time_unix_nano": 1723729821322137664`
- `start_time_unix_nano": 1723729831273079179`
- `start_time_unix_nano": 1723729841259350604`
- `start_time_unix_nano": 1723729851258692341`
- `start_time_unix_nano": 1723729861230025552`

Example output when sending **dynamic** value as an attribute, e.g. `"attributes": {"dynamic_attribute": < RANDOM NUMBER > }`
- `start_time_unix_nano": 1723730041127767707`
- `start_time_unix_nano": 1723730041127767707`
- `start_time_unix_nano": 1723730041127767707`
- `start_time_unix_nano": 1723730041127767707`
- `start_time_unix_nano": 1723730041127767707`
