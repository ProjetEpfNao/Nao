# BASE SERVER URL
BASE_URL = "http://etiennedesticourt.pythonanywhere.com"

# CREDENTIALS REQUEST
CREDENTIALS_URL = BASE_URL + "credentials"
CRED_USER_KEY = "username"
CRED_PASS_KEY = "password"

# AUTHENTICATION REQUEST

# COMMAND POLLING
COMMAND_URL = BASE_URL + "/get_last_command"
COMMAND_ID_KEY = "id"
COMMAND_TYPE_KEY = "command"
POLL_DELAY = 3

# COMMAND REPLIES
REPLY_URL = BASE_URL + "reply"
REPLY_DATA_KEY = "reply"

# STATUS
STATUS_KEY = "result"
SUCCESS = "SUCCESS"
FAILURE = "FAILURE"
ERROR_KEY = "error_message"
