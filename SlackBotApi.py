from slacker import Slacker

slack_api_token = 'xoxb-73308703585-Q8MmzbZYJ4k7IMkHoZo35BkQ'
slack_hook_url ='https://hooks.slack.com/services/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'

from slacker import Slacker

token = slack_api_token
slack = Slacker(token)
slack.chat.post_message('#general', 'message')