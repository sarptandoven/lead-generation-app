from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List
import time

class RateLimiter:
    def __init__(self, max_requests_per_minute: int, max_requests_per_hour: int):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_requests_per_hour = max_requests_per_hour
        self.minute_requests: Dict[str, List[datetime]] = defaultdict(list)
        self.hour_requests: Dict[str, List[datetime]] = defaultdict(list)
        self._cleanup_interval = 3600  # 1 hour
        self._last_cleanup = time.time()

    def _cleanup_old_requests(self):
        """Remove requests older than 1 hour."""
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return

        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        
        for user in list(self.minute_requests.keys()):
            self.minute_requests[user] = [
                req_time for req_time in self.minute_requests[user]
                if req_time > cutoff_time
            ]
            if not self.minute_requests[user]:
                del self.minute_requests[user]

        for user in list(self.hour_requests.keys()):
            self.hour_requests[user] = [
                req_time for req_time in self.hour_requests[user]
                if req_time > cutoff_time
            ]
            if not self.hour_requests[user]:
                del self.hour_requests[user]

        self._last_cleanup = current_time

    def check_rate_limit(self, user: str) -> bool:
        """
        Check if the user has exceeded rate limits.
        Returns True if the request is allowed, False otherwise.
        """
        self._cleanup_old_requests()
        
        current_time = datetime.utcnow()
        minute_ago = current_time - timedelta(minutes=1)
        hour_ago = current_time - timedelta(hours=1)

        # Check minute limit
        minute_requests = [
            req_time for req_time in self.minute_requests[user]
            if req_time > minute_ago
        ]
        if len(minute_requests) >= self.max_requests_per_minute:
            return False

        # Check hour limit
        hour_requests = [
            req_time for req_time in self.hour_requests[user]
            if req_time > hour_ago
        ]
        if len(hour_requests) >= self.max_requests_per_hour:
            return False

        # Update request counts
        self.minute_requests[user].append(current_time)
        self.hour_requests[user].append(current_time)
        
        return True

    def get_remaining_requests(self, user: str) -> Dict[str, int]:
        """
        Get the number of remaining requests for the user.
        Returns a dictionary with remaining requests for both minute and hour limits.
        """
        self._cleanup_old_requests()
        
        current_time = datetime.utcnow()
        minute_ago = current_time - timedelta(minutes=1)
        hour_ago = current_time - timedelta(hours=1)

        minute_requests = len([
            req_time for req_time in self.minute_requests[user]
            if req_time > minute_ago
        ])
        hour_requests = len([
            req_time for req_time in self.hour_requests[user]
            if req_time > hour_ago
        ])

        return {
            "minute": max(0, self.max_requests_per_minute - minute_requests),
            "hour": max(0, self.max_requests_per_hour - hour_requests)
        } 