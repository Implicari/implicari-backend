from django.core.exceptions import PermissionDenied

from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphene_django.forms.mutation import DjangoModelFormMutation

from graphql_jwt.decorators import login_required

import graphene

from .forms import ClassroomForm
from .models import Classroom


class ClassroomType(DjangoObjectType):
    class Meta:
        model = Classroom


class Query(graphene.ObjectType):
    classroom = graphene.Field(ClassroomType, id=graphene.ID(required=True))
    classrooms_as_teacher = graphene.List(ClassroomType)
    classrooms_as_student = graphene.List(ClassroomType)
    classrooms_as_parent = graphene.List(ClassroomType)

    @login_required
    def resolve_classroom(self, info, **kwargs):
        id = kwargs.get('id')

        classroom = Classroom.objects.get(id=id)

        if not info.context.user.is_authenticated or not (
            classroom.creator == info.context.user or
            classroom.students.filter(id=info.context.user.id).exists() or
            classroom.students.filter(parents=info.context.user).exists()
        ):
            raise PermissionDenied(f'Permission denied for {info.context.user}')

        return classroom

    @login_required
    def resolve_classrooms_as_teacher(self, info):
        return Classroom.objects.filter(creator=info.context.user)

    @login_required
    def resolve_classrooms_as_student(self, info):
        return Classroom.objects.filter(students=info.context.user)

    @login_required
    def resolve_classrooms_as_parent(self, info):
        return Classroom.objects.filter(students__parents=info.context.user).distinct()


class ClassroomMutation(DjangoModelFormMutation):
    classroom = graphene.Field(ClassroomType)
    debug = graphene.Field(DjangoDebug, name="_debug")

    class Meta:
        form_class = ClassroomForm

    @classmethod
    @login_required
    def get_form_kwargs(cls, root, info, **input):
        kwargs = {"data": input}
        pk = input.pop("id", None)

        if pk:
            instance = cls.get_object(pk, info)
            kwargs["instance"] = instance

        return kwargs

    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        if (form.instance.id is None):
            form.instance.creator = info.context.user

        return super().perform_mutate(form, info)

    @classmethod
    @login_required
    def get_object(cls, pk, info):
        obj = cls._meta.model._default_manager.get(pk=pk)

        if obj.creator_id != info.context.user.id:
            raise PermissionDenied('Permission denied')

        return obj


class Mutation(graphene.ObjectType):
    classroom = ClassroomMutation.Field()
