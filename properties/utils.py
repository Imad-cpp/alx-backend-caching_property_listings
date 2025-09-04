import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieve all properties with caching.
    Cache for 1 hour (3600 seconds).
    """
    cache_key = 'all_properties'
    properties = cache.get(cache_key)
    
    if properties is None:
        logger.info("Cache miss: Fetching properties from database")
        properties = list(Property.objects.all())
        cache.set(cache_key, properties, 3600)  # Cache for 1 hour
        logger.info(f"Cached {len(properties)} properties")
    else:
        logger.info(f"Cache hit: Retrieved {len(properties)} properties from cache")
    
    return properties

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()
        
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests) * 100 if total_requests > 0 else 0
        
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 2)
        }
        
        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0,
            'error': str(e)
        }