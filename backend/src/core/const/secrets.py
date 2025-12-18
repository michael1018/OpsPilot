"""
System Error Code Definitions
"""

__author__ = 'Michael'


class CODES:
    # ======================
    # General
    # ======================

    SUCCESS = 0                     # Success
    UNKNOWN_ERROR = 1               # Unknown error
    SERVICE_UNAVAILABLE = 2         # Service temporarily unavailable
    INVALID_METHOD = 3              # Invalid method
    UNREGISTERED_METHOD = 4         # Unregistered method
    API_REQUEST_LIMIT_REACHED = 5   # API request limit reached
    UNAUTHORIZED_IP_CLIENT = 6      # Unauthorized client IP
    NO_PERMISSION_USER_DATA = 7     # No permission to access user data
    NO_PERMISSION_REFER = 8         # No permission for this referer
    API_ERROR = 9                   # Default API error (message only)
    LOCK_ERROR = 10                 # Lock error

    # ======================
    # File / Directory
    # ======================

    FILE_NOT_FOUND = 40.1           # File not found
    FILE_EXISTS = 40.2              # File already exists
    DIR_NOT_FOUND = 40.3            # Directory not found
    DIR_EXISTS = 40.4               # Directory already exists
    FILE_CONTENT_EMPTY = 40.5       # File content is empty
    SHELL_ERROR = 50                # Shell execution error

    # ======================
    # Parameter Errors
    # ======================

    PARAMETER_INVALID = 100         # Invalid parameter
    PARAMETER_TOO_MANY = 101        # Too many parameters
    PARAMETER_MISSING = 102         # Missing parameter
    PARAMETER_KEYWORD_CONFLICT = 103  # Parameter contains forbidden keyword
    PARAMETER_INVALID_JSON = 104    # Invalid JSON format
    PARAMETER_INVALID_TYPE = 105    # Invalid parameter type

    # ======================
    # Authentication / Authorization
    # ======================

    ACCESS_TOKEN_INVALID = 110          # Invalid access token
    ACCESS_TOKEN_EXPIRED = 111          # Access token expired
    ACCESS_TOKEN_SIGNATURE_INVALID = 112  # Invalid token signature
    ACCESS_TOKEN_CHANGE = 113           # Access token replaced

    USERNAME_INVALID = 114              # Invalid username
    PASSWORD_INVALID = 115              # Invalid password

    GAC_NOT_CONF = 116.1                # Google Authenticator not configured
    GAC_INVALID = 116.2                 # Invalid Google Authenticator code

    USER_NAME_EXITS = 117.1             # Username already exists
    USER_TYPE_NOT_MATCH = 117.2         # User type mismatch
    USER_DISABLED = 117.3               # User disabled
    USER_INVALID = 117.4                # Invalid user
    USER_LOCK_LOGIN = 118               # User login locked

    API_SECRET_KEY_INVALID = 120        # Invalid API secret key
    API_SIGNATURE_INVALID = 121         # Invalid API signature

    # ======================
    # Database
    # ======================

    DATABASE_UNIQUE_VIOLATION_ERROR = 200  # Unique constraint violation

    # ======================
    # System / Permission
    # ======================

    NOT_IMPLEMENTED = 301             # Not implemented
    ALREADY_CHECK_NAME_SERVER = 400   # Name server already checked
    UNAUTHORIZED = 401                # Unauthorized
    PERMISSION_DENIED = 402           # Permission denied
    NOT_ALLOW = 405                   # Operation not allowed
    RECORD_NOT_EXITS = 410             # Record does not exist
    SETTING_NOT_EXITS = 411            # Setting does not exist
    TIMEOUT = 510                     # Timeout

    # ======================
    # DNS Errors
    # ======================

    DNS_DOMAIN_NOT_EXISTS = 601            # DNS domain does not exist
    DNS_DOMAIN_ALREADY_EXISTS = 602        # DNS domain already exists
    DNS_RECORD_ALREADY_EXISTS = 603        # DNS record already exists
    DNS_INVALID_ZONE_IDENTIFIER = 604      # Invalid DNS zone identifier
    DNS_INVALID_DNS_RECORD_IDENTIFIER = 605  # Invalid DNS record value
    DNS_A_AND_CNAME_CONFLICT = 606         # A record conflicts with CNAME
    DNS_AUTH_KEY_ERROR = 607               # DNS authorization failed
    DNS_RECORD_DOES_NOT_EXIST = 608        # DNS record does not exist
    DNS_ZONE_CREATE_ERROR = 609            # DNS zone creation error
    AUTHENTICATION_ERROR = 610             # Authentication error
    DNS_VALIDATION_ERROR = 611             # DNS validation error
    NEED_VALID_A_RECORD = 612              # Valid A record required
    DNS_DOMAIN_DO_NOT_DELETE = 613          # Domain cannot be deleted
    DNS_UNREGISTERED_DOMAIN_NAME = 614      # Unregistered domain name
    DNS_INVALID_DOMAIN_FORMAT = 615         # Invalid domain format
    DOMAIN_NAME_ADDED_BY_ANOTHER = 616      # Domain added by another user
    DNS_RECORD_MX_CONFLICT_CNAME = 617      # MX conflicts with CNAME

    # ======================
    # Server
    # ======================

    SERVER_CHANGE_IP_FAIL = 700             # Server IP change failed
    SERVER_CHANGE_IP_ERROR = 701            # Server IP change error
