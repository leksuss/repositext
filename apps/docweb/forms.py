from django.forms import ModelForm, ValidationError
from apps.repo.models import Folder


class AddFolderForm(ModelForm):

    def __init__(self,*args,**kwargs): 
        self.owner=kwargs.pop('owner')
        self.parent=kwargs.pop('parent') 
        super(AddFolderForm, self).__init__(*args,**kwargs)

    class Meta:
        model = Folder
        fields = ['name', 'description',]

    def clean_name(self):
        name = self.cleaned_data['name']
        children = Folder.objects.filter(parent=self.parent)
        for child in children:
            if child.name == name:
                raise ValidationError('Subfolder names must be unique in parent folder.')
        return name