import graphene


class BaseMutation(graphene.Mutation):
    class Meta:
        abstract = True

    ok = graphene.Boolean()
    error_message = graphene.String()

    @classmethod
    def mutate(cls, info, **kwargs):
        raise NotImplementedError("Subclasses should implement this method.")

    @classmethod
    def success(cls, **kwargs):
        return cls(ok=True, error_message=None, **kwargs)

    @classmethod
    def failure(cls, error_message):
        return cls(ok=False, error_message=error_message)
