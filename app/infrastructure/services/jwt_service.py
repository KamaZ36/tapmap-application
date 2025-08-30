import jwt
from typing import Any

from uuid import UUID
from datetime import datetime, timezone, timedelta

from app.domain.entities.user import UserRole
from app.infrastructure.exceptions.base import InvalidAccessToken
from app.settings import settings


class JWTService:
    def __init__(
            self,
            access_secret: str,
            refresh_secret: str,
            algorithm: str,
            access_exp: int,
            refresh_exp: int,
    ):
        self.algorithm = algorithm
        self.access_secret = access_secret
        self.refresh_secret = refresh_secret
        self.access_exp = access_exp
        self.refresh_exp = refresh_exp

    def _generate_token(self, payload: dict, secret: str, expiration: timedelta) -> str:
        payload['exp'] = datetime.now(timezone.utc) + expiration
        return jwt.encode(payload, secret, algorithm=self.algorithm)

    def create_access_token(self, user_id: UUID, roles: list[UserRole]) -> str:
        access_payload = {'user_id': str(user_id), 'roles': roles, 'type': 'access_token'}
        return self._generate_token(access_payload, self.access_secret, timedelta(hours=self.access_exp))

    def create_refresh_token(self, user_id: UUID) -> str:
        refresh_payload = {'user_id': str(user_id), 'type': 'refresh_token'}
        return self._generate_token(refresh_payload, self.refresh_secret, timedelta(days=self.refresh_exp))

    def create_tokens(self, user_id: UUID, roles: list[UserRole]) -> dict[str, str]:
        access_token = self.create_access_token(user_id=user_id, roles=roles)
        refresh_token = self.create_refresh_token(user_id=user_id)
        return {'user_id': str(user_id), 'access_token': access_token, 'refresh_token': refresh_token}

    def decode_access_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self.access_secret, algorithms=[self.algorithm])
            if payload['type'] != 'access_token':
                raise InvalidAccessToken
            return payload
        except jwt.DecodeError:
            raise InvalidAccessToken
        except jwt.ExpiredSignatureError:
            raise InvalidAccessToken()

    def decode_refresh_token(self, token: str) -> dict[str, str]:
        try:
            payload = jwt.decode(token, self.refresh_secret, algorithms=[self.algorithm])
            if payload['type'] != 'refresh_token':
                raise InvalidAccessToken()
            return payload
        except jwt.DecodeError:
            raise InvalidAccessToken()
        except jwt.ExpiredSignatureError:
            raise InvalidAccessToken()


jwt_service = JWTService(
    access_secret=settings.access_jwt_secret_key,
    refresh_secret=settings.refresh_jwt_secret_key,
    algorithm=settings.algorithm,
    access_exp=settings.accesss_token_expire_hours,
    refresh_exp=settings.refresh_token_expire_days,
)
