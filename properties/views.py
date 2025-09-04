import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from .models import Property
from .utils import get_all_properties, get_redis_cache_metrics

logger = logging.getLogger(__name__)

@cache_page(60 * 15)  # Cache for 15 minutes
@require_http_methods(["GET"])
def property_list(request):
    """
    Return all properties with page-level caching.
    """
    properties = get_all_properties()
    
    properties_data = []
    for prop in properties:
        properties_data.append({
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),
            'location': prop.location,
            'created_at': prop.created_at.isoformat()
        })
    
    return JsonResponse({
        'properties': properties_data,
        'count': len(properties_data)
    })

@require_http_methods(["GET"])
def cache_metrics(request):
    """
    Return Redis cache metrics.
    """
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)
