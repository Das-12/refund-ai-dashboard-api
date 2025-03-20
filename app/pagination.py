from typing import Any, Dict, List, Union, Optional
from fastapi import Request

def paginate(
    data: Union[List[Any], Dict[Any, Any], Any], 
    skip: int = 1, 
    limit: int = 10,
    request: Optional[Request] = None,
    pagination: bool = True
) -> Dict[str, Any]:
    """
    Paginate a list, dictionary, or queryset-like object.

    :param data: The data to paginate (list, dict, or iterable).
    :param skip: The current skip number (1-based index).
    :param limit: The number of items per skip.
    :return: A dictionary containing paginated results.
    """     
    if isinstance(data, dict):
        data = list(data.items())  # Convert dictionary to list of tuples
        
    if not isinstance(data, list):
        raise ValueError("Data must be a list or convertible to a list")
    
    total_items = len(data)

    if not pagination:  # If pagination is disabled, return full data
        return {
            "pagination": False,
            "total_items": total_items,
            "results": data
        }

    if hasattr(data, "offset") and hasattr(data, "limit"):  # Handle ORM querysets
        paginated_data = data.offset((skip - 1) * limit).limit(limit).all()
        total_items = data.count() if hasattr(data, "count") else len(data)
    else:
        total_items = len(data)
        start = (skip - 1) * limit
        end = start + limit
        paginated_data = data[start:end]
    
    total_skips = (total_items + limit - 1) // limit
    
    # Generate next and previous skip URLs if request object is provided
    base_url = str(request.url).split("?")[0] if request else ""
    next_page = f"{base_url}?skip={skip + 1}&limit={limit}" if request and skip < total_skips else None
    prev_page = f"{base_url}?skip={skip - 1}&limit={limit}" if request and skip > 1 else None


    return {
        "skip": skip,
        "limit": limit,
        "total_items": total_items,
        "total_pages": (total_items + limit - 1) // limit,
        "next_page": next_page,
        "prev_page": prev_page,
        "results": paginated_data
    }
