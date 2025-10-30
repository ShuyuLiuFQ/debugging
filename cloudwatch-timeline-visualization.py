
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from config import CLOUDWATCH_TIMELINE_DURATION_SECONDS, CLOUDWATCH_TIMELINE_START_TIME, MESSAGE_FILTERS

# Load the JSON file
with open('/home/shuyu/Documents/scripts/AWS/assets/auth-service/dev-20251030-01.json') as f:
    data = json.load(f)

# Extract all timestamps and convert to datetime
timestamps = [event['timestamp'] for event in data.get('events', [])]
datetimes = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]

# Create a DataFrame for all events
df = pd.DataFrame({'datetime': datetimes})
df['count'] = 1


# Filter events for each message in MESSAGE_FILTERS
filtered_events = []
for msg_filter in MESSAGE_FILTERS:
    message = msg_filter['message']
    color = msg_filter['color']
    label = msg_filter.get('label', message)
    events = [event for event in data.get('events', []) if message in event.get('message', '')]
    timestamps = [event['timestamp'] for event in events]
    datetimes = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]
    filtered_events.append({
        'datetimes': datetimes,
        'color': color,
        'label': label
    })


# Focus on the first N hours of events (configurable)
if not df.empty:
    if CLOUDWATCH_TIMELINE_START_TIME:
        CLOUDWATCH_TIMELINE_START_TIME = pd.to_datetime(CLOUDWATCH_TIMELINE_START_TIME)
    else:
        CLOUDWATCH_TIMELINE_START_TIME = df['datetime'].min()
    end_time = CLOUDWATCH_TIMELINE_START_TIME + pd.Timedelta(seconds=CLOUDWATCH_TIMELINE_DURATION_SECONDS)
else:
    CLOUDWATCH_TIMELINE_START_TIME = None
    end_time = None

# Filter datetimes for each message to be within the time window
for fe in filtered_events:
    if CLOUDWATCH_TIMELINE_START_TIME and end_time:
        fe['datetimes'] = [dt for dt in fe['datetimes'] if CLOUDWATCH_TIMELINE_START_TIME <= dt <= end_time]

# Plot
plt.figure(figsize=(180, 6))
# Draw each message as a different color dot
for fe in filtered_events:
    count = len(fe['datetimes'])
    if count:
        label_with_count = f"{fe['label']} ({count})"
        plt.scatter(fe['datetimes'], [1]*count, color=fe['color'], label=label_with_count, zorder=5, s=8, marker='o')
plt.title('Error Events Timeline (First {} Seconds)'.format(CLOUDWATCH_TIMELINE_DURATION_SECONDS))
plt.xlabel('Time')
plt.yticks([])
plt.legend()
plt.tight_layout()
plt.title('Error Events Timeline ({} for {} Seconds)'.format(CLOUDWATCH_TIMELINE_START_TIME.strftime('%Y-%m-%d_%H-%M-%S') if CLOUDWATCH_TIMELINE_START_TIME else 'NA', CLOUDWATCH_TIMELINE_DURATION_SECONDS))
filename = './output/cloudwatch_timeline_{}_{}s.png'.format(CLOUDWATCH_TIMELINE_START_TIME.strftime('%Y-%m-%d_%H-%M-%S') if CLOUDWATCH_TIMELINE_START_TIME else 'NA', CLOUDWATCH_TIMELINE_DURATION_SECONDS)
plt.savefig(filename)