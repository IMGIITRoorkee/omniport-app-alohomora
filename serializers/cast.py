import random
import string

from rest_framework import serializers

from base_auth.managers.get_user import get_user
from base_auth.models import User


class CastAlohomoraSerializer(serializers.Serializer):
    """
    Stores the user whose Alohomora access is being hijacked by a maintainer
    """

    user = None
    username = serializers.CharField()
    new_password = serializers.CharField(default='')

    def validate_username(self, username):
        """
        Validate the supplied username by checking if a user with the supplied
        username even exists
        :param username: the supplied username
        :return: the username if it is valid
        :raise serializers.ValidationError: if the username does not exist
        """

        try:
            self.user = get_user(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid username')

        return username

    def validate_new_password(self, new_password):
        """
        Generate a random password in case one is not provided
        :param new_password: the data to check for validity
        :return: the new password after validation
        """

        if not new_password:
            # Get a list of all characters
            allowed_chars = list(string.ascii_uppercase + string.digits)

            # Remove confusing characters
            allowed_chars.remove('0')
            allowed_chars.remove('O')
            allowed_chars.remove('1')
            allowed_chars.remove('I')
            allowed_chars.remove('5')
            allowed_chars.remove('S')

            # Generate new password
            password_length = 8
            new_password = ''.join(
                random.SystemRandom().choice(allowed_chars)
                for _ in range(password_length)
            )

        return new_password
