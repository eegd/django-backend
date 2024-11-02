from rest_framework.throttling import UserRateThrottle


class DailyRateThrottle(UserRateThrottle):
    scope = "user_day"


class MinuteRateThrottle(UserRateThrottle):
    scope = "user_minute"
