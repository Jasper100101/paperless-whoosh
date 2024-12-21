from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from .search_manager import SearchManager
        search_manager = SearchManager()
        search_manager.add_document(self.id, self.title, self.content)

