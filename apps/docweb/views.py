from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View
from repositext.settings import MAX_RECENT_DOCS
from apps.repo.models import Document, Folder

class IndexView(View):
    def get(self, request):
        if request.user.username == 'admin':
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
        else:
            return HttpResponseRedirect(reverse('user-home-view', args = [request.user.username]))



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


class UserHomeView(View):
    def get(self, request, username):
        root_folder = Folder.objects.get(name='-ROOT-')
        home_folder = Folder.objects.get(name='Home', parent=root_folder)

        try:
            top_folder = Folder.objects.get(
                name=request.user.username,
                parent=Folder.objects.get(name='Home', parent=home_folder)
            )
        except Folder.DoesNotExist:
            user_folder = Folder()
            user_folder.name = request.user.username
            user_folder.description = f'Home folder for {username}'
            user_folder.owner = request.user
            user_folder.parent = home_folder
            user_folder.save()
            top_folder = user_folder
        
        child_folders = Folder.objects.filter(parent=top_folder)
        print(child_folders)
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

