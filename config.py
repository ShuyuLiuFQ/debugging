# config.py
# Configuration for cloudwatch-timeline-visualization


# Duration in seconds to display on the timeline
CLOUDWATCH_TIMELINE_DURATION_SECONDS = 60 * 60 * 3
# Optional: Set the start time for the timeline (format: 'YYYY-MM-DD HH:MM:SS'), or set to None to use the earliest event
CLOUDWATCH_TIMELINE_START_TIME = '2025-10-30 05:30:00'

# Message filters and their colors (add up to 10)
MESSAGE_FILTERS = [
	{
		'message': '[CORS] CORS origin check failed in auth service. undefined is not in allowlist.',
		'color': 'red',
		'label': 'CORS Failed (undefined)'
	},
    {
        'message': 'Returning HTTP 404. Route not found',
        'color': 'blue',
        'label': 'Route not found'
    }
	# Example additional filters:
	# {'message': 'Some other error message', 'color': 'green', 'label': 'Other Error'},
	# ... add up to 10 ...
]
