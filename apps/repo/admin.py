from django.contrib import admin
from .models import Document, Folder, DocumentVersion, Organization


admin.site.register(Document)
admin.site.register(Folder)
admin.site.register(DocumentVersion)
admin.site.register(Organization)
