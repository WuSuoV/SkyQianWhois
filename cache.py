from flask_caching import Cache

cache_config = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DEFAULT_TIMEOUT': 3600,
    'CACHE_IGNORE_ERRORS': True,
    'CACHE_DIR': './cache/flask',
    'CACHE_THRESHOLD': 10 ** 2,
}

cache = Cache(config=cache_config)
