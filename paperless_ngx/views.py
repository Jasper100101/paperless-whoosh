from django.http import JsonResponse
from .search_manager import SearchManager

def search_documents(request):
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse({"error": "Query string is empty"}, status=400)

    search_manager = SearchManager()
    results = search_manager.search(query)
    return JsonResponse({"results": results})