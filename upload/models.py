from django.db import models
from django import forms
from django.contrib.auth.models import User
from settings import UPLOAD_DIR
from utils.splitter import run_process_file

# Create your models here.

class UploadFileForm(forms.Form):
    file  = forms.FileField()

class Page(models.Model):
    num = models.IntegerField()
    filename = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()

class Document(models.Model):
    name = models.TextField()
    owner = models.ForeignKey(User)
    refer = models.ForeignKey('courses.Course', related_name="back_course")
    size = models.IntegerField(null=True)
    ready = models.BooleanField(default=False)
    pages = models.ManyToManyField(Page)

    @classmethod
    def new(cls, owner, course, file):
        doc = cls(name=file.name, owner=owner, refer=course)
        doc.save()
        run_process_file(doc, file)
        return doc
    
    def get_content(self):
        f = open(UPLOAD_DIR + '/' + str(self.pk) + '.pdf', 'r')
        content = f.read()
        f.close()
        return content

    def set_npages(self, num):
        self.size = num
        self.save()

    def add_page(self, num, fname, w, h):
        p = Page(num=num, filename=fname, width=w, height=h)
        p.save()
        self.pages.add(p)
