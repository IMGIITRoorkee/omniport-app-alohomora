from rest_framework import generics, response, status, permissions

from alohomora.serializers.cast import CastAlohomoraSerializer
from kernel.permissions.alohomora import HasAlohomoraRights


class CastAlohomoraView(generics.GenericAPIView):
    """
    Set the ``allows_alohomora`` field on the user model to ``true``
    """

    permission_classes = [
        permissions.IsAuthenticated,
        HasAlohomoraRights,
    ]
    serializer_class = CastAlohomoraSerializer

    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            new_password = serializer.data.get('new_password')
            user.set_password(new_password)
            user.save()
            response_data = {
                'status': 'Successfully cast Alohomora spell.',
                'new_password': new_password,
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_200_OK
            )
        else:
            response_data = {
                'errors': serializer.errors,
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
