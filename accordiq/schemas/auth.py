from pydantic import BaseModel


class MembershipRead(BaseModel):
    workspace_id: str
    role: str


class UserRead(BaseModel):
    id: str
    email: str
    name: str | None = None
    picture: str | None = None
    memberships: list[MembershipRead]


class TokenClaims(BaseModel):
    sub: str
    email: str
    iss: str
    aud: str
    exp: int
    iat: int
