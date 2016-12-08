# BASE SERVER URL
BASE_URL = "http://etiennedesticourt.pythonanywhere.com"

# REGISTER & LOGIN
REGISTER_URL = BASE_URL + "/register"
LOGIN_URL = BASE_URL + "/login"
USER_KEY = "username"
PASS_KEY = "password"
ROBOT_KEY = "is_robot"

#BATTERY
BATTERY_URL = BASE_URL + "/update_battery_info"

# COMMAND POLLING
COMMAND_URL = BASE_URL + "/get_last_command"
COMMAND_ID_KEY = "id"
COMMAND_TYPE_KEY = "command"
COMMAND_CONTENT_KEY = "content"
POLL_DELAY = 3

# COMMAND REPLIES
REPLY_URL = BASE_URL + "reply"
REPLY_DATA_KEY = "reply"

# STATUS
STATUS_KEY = "result"
SUCCESS = "SUCCESS"
FAILURE = "FAILURE"
ERROR_KEY = "error_message"

# STREAMING
STREAM_URL = BASE_URL + "stream"
