from typing import Any, Dict, List, Union, Optional
from fastapi import Request

def paginate(
    data: Union[List[Any], Dict[Any, Any], Any], 
    page: int = 1, 
    page_size: int = 10,
    request: Optional[Request] = None,
    pagination: bool = True
) -> Dict[str, Any]:
    """
    Paginate a list, dictionary, or queryset-like object.

    :param data: The data to paginate (list, dict, or iterable).
    :param page: The current page number (1-based index).
    :param page_size: The number of items per page.
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
        paginated_data = data.offset((page - 1) * page_size).limit(page_size).all()
        total_items = data.count() if hasattr(data, "count") else len(data)
    else:
        total_items = len(data)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_data = data[start:end]
    
    total_pages = (total_items + page_size - 1) // page_size
    
    # Generate next and previous page URLs if request object is provided
    base_url = str(request.url).split("?")[0] if request else ""
    next_page = f"{base_url}?page={page + 1}&page_size={page_size}" if request and page < total_pages else None
    prev_page = f"{base_url}?page={page - 1}&page_size={page_size}" if request and page > 1 else None


    return {
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": (total_items + page_size - 1) // page_size,
        "next_page": next_page,
        "prev_page": prev_page,
        "results": paginated_data
    }
