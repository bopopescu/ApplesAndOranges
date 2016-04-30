class MultiSerializerViewSetMixin(object):

    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        Thanks gonz: http://stackoverflow.com/a/22922156/11440

        """

        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class CustomErrorMessagesMixin(object):
    """
    Replaces built-in validator messages with messages, defined in Meta class.
    This mixin should be inherited before the actual Serializer class in order to call __init__ method.

    Example of Meta class:

    >>> class Meta:
    >>>     model = User
    >>>     fields = ('url', 'username', 'email', 'groups')
    >>>     custom_error_messages_for_validators = {
    >>>         'username': {
    >>>             UniqueValidator: _('This username is already taken. Please, try again'),
    >>>             RegexValidator: _('Invalid username')
    >>>         }
    >>>     }
    """

    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super().__init__(*args, **kwargs)
        self.replace_validators_messages()

    def replace_validators_messages(self):
        for field_name, validators_lookup in self.custom_error_messages_for_validators.items():
            # noinspection PyUnresolvedReferences
            for validator in self.fields[field_name].validators:
                if type(validator) in validators_lookup:
                    validator.message = validators_lookup[type(validator)]

    @property
    def custom_error_messages_for_validators(self):
        meta = getattr(self, 'Meta', None)
        return getattr(meta, 'custom_error_messages_for_validators', {})
