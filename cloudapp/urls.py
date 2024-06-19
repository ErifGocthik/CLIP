from django.urls import path

from cloudapp.views import MainListView, UploadingFilesView, InfinityListView, ArchivesListView, GetImageId, \
    AddInArchive, CheckImageInArchive, ArchiveDetailView, InfinityArchiveListView, RemoveFromArchive, download_image, \
    info_view, get_link

app_name = 'cloudapp'

urlpatterns = [
    path('', MainListView.as_view(), name='main'),
    path('uploading/', UploadingFilesView.as_view(), name='upload'),
    path('inf/', InfinityListView.as_view(), name='inf'),
    path('infArc/', InfinityArchiveListView.as_view(), name='infArc'),
    path('archives/', ArchivesListView.as_view(), name='archives'),
    path('archive/<int:pk>/', ArchiveDetailView.as_view(), name='archive'),
    path('getimage/', GetImageId.as_view(), name='getimage'),
    path('addInArchive/', AddInArchive.as_view(), name='addInArchive'),
    path('removeInArchive/', RemoveFromArchive.as_view(), name='removeInArchive'),
    path('checkIIA/', CheckImageInArchive.as_view(), name='checkIIA'),
    path('image/<int:pk>/download/', download_image, name='download'),
    path('info/', info_view, name='info'),
    path('link/<int:pk>/', get_link, name='link'),
    # path('render_images/', get_neuro_images, name='ner')
]