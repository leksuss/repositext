from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View
from repositext.settings import MAX_RECENT_DOCS
from apps.repo.models import Document, Folder
from .forms import AddFolderForm, AddDocumentForm, AddDocumentVersionForm


def get_user_home_folder(request, home_folder):
    user_folder = Folder()
    user_folder.name = request.user.username
    user_folder.description = f'Home folder for {request.user.username}'
    user_folder.owner = request.user
    user_folder.parent = home_folder
    user_folder.save()
    return user_folder


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
        add_folder_form = AddFolderForm(owner=request.user, parent=top_folder, auto_id="folder_id_%s")
        add_document_form = AddDocumentForm(owner=request.user, parent=top_folder, auto_id="document_id_%s")
        add_document_version_form = AddDocumentVersionForm()
        return render(
            request,
            'docweb/repository.html',
            {
                'top_folder': top_folder,
                'child_folders': child_folders,
                'child_documents': child_documents,
                'add_folder_form': add_folder_form,
                'add_document_form': add_document_form,
                'add_document_version_form': add_document_version_form,
            }
        )

    def post(self, request, folder_id):
        parent_folder = Folder.objects.get(pk=folder_id)
        add_folder_form = AddFolderForm(
            request.POST, parent=parent_folder, owner=request.user
        )

        if add_folder_form.is_valid():
            new_folder = add_folder_form.save(commit=False)
            new_folder.owner = request.user
            new_folder.parent = parent_folder
            new_folder.save()
            return HttpResponseRedirect(reverse('repo-view', args=[folder_id]))
        else:
            child_folders = Folder.objects.filter(parent=parent_folder)
            child_documents = Document.objects.filter(parent=parent_folder)
            return render(
                request,
                'docweb/repository.html',
                {
                    'top_folder': parent_folder,
                    'child_folders': child_folders,
                    'child_documents': child_documents,
                    'add_folder_form': add_folder_form,
                    'display_add_form_dialog': True,
                }
            )



class UserHomeView(View):
    def get(self, request, username):
        root_folder = Folder.objects.get(name='-ROOT-')
        home_folder = Folder.objects.get(name='Home', parent=root_folder)

        try:
            top_folder = Folder.objects.get(
                name=request.user.username,
                parent=home_folder
            )
        except Folder.DoesNotExist:
            top_folder = get_user_home_folder(request, home_folder)
        
        return HttpResponseRedirect(reverse('repo-view', args=[top_folder.id]))


class AddDocumentView(View):
    def post(self, request, folder_id):
        parent_folder = Folder.objects.get(pk=folder_id)
        add_document_form = AddDocumentForm(request.POST, owner=request.user, parent=parent_folder)
        add_document_version_form = AddDocumentVersionForm(request.POST, request.FILES)

        if add_document_form.is_valid() and add_document_version_form.is_valid():
            doc = add_document_form.save(commit=False)
            doc.parent = parent_folder
            doc.owner = request.user
            doc.save()

            dv = add_document_version_form.save(commit=False)
            dv.parent = doc
            dv.save()

            doc.versions.add(dv)
            doc.save()
            return HttpResponseRedirect(reverse('repo-view', args=[parent_folder.id]))
        else:
            child_folders = Folder.objects.filter(parent=parent_folder)
            child_documents = Document.objects.filter(parent=parent_folder)
            return render(
                request,
                'docweb/repository.html',
                {
                    'top_folder': parent_folder,
                    'child_folders': child_folders,
                    'child_documents': child_documents,
                    'add_document_form': add_document_form,
                    'add_document_version_form': add_document_version_form,
                    'display_add_document_dialog': True,
                }
            )