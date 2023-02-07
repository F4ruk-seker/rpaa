from django import forms


class ManyQueryForm(forms.Form):
    query_list=forms.JSONField()
