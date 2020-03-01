from django.shortcuts import render
from django.views import View
from repositext.settings import MAX_RECENT_DOCS
from apps.repo.models import Document, Folder
from django.contrib.auth import logout

class IndexView(View):
    def get(self, request):
        root_folder = Folder.objects.get(name='-ROOT-')
        child_folders = Folder.objects.filter(parent=root_folder)
        recent_docs = Document.objects.filter().order_by(
            '-created'
        )[:MAX_RECENT_DOCS]

        return render(
            request,
            'docweb/index.html',
            {
                'root_folder': root_folder,
                'child_folders': child_folders,
                'recent_docs': recent_docs,
            }
        )


class RepositoryView(View):
    def get(self, request, folder_id=None):
        if folder_id:
            top_folder = Folder.objects.get(pk=folder_id)
        else:
            top_folder = Folder.objects.get(name='-ROOT-')
        child_folders = Folder.objects.filter(parent=top_folder)
        child_documents = Document.objects.filter(parent=top_folder)
        return render(
            request,
            'docweb/repository.html',
            {
                'top_folder': top_folder,
                'child_folders': child_folders,
                'child_documents': child_documents,
            }
        )


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')