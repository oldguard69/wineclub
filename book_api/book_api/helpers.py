def get_validated_data(serializer, request, raise_exception=True):
    '''Return (validated_data, serializer_instance)'''
    s = serializer(data=request.data)
    s.is_valid(raise_exception=raise_exception)
    return (s.validated_data, s)


def get_user_id(request):
    '''Ensure IsAuthenticated permission is provide'''
    return request.auth.payload.get('user_id')