from django import (
    forms,
)

from posts.models import (
    Group,
)


class PostForm(forms.Form):

    text = forms.CharField(
        widget=forms.Textarea()
    )
    group = forms.ChoiceField(
        choices=[(None, 'Не задано')],
        required=False
    )

    def __init__(self, groups: list[Group], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['group'].choices += [
            (group.id, group.title)
            for group in groups
        ]

    def clean_group(self):
        value = self.cleaned_data['group']
        if value:
            return int(value)


class CommentForm(forms.Form):

    text = forms.CharField(
        widget=forms.Textarea()
    )
