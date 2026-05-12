from pydantic import BaseModel


class MembershipRead(BaseModel):
    workspace_id: str
    role: str


class OrganizationMembershipRead(BaseModel):
    organization_id: str
    role: str


class UserRead(BaseModel):
    id: str
    email: str
    name: str | None = None
    picture: str | None = None
    memberships: list[MembershipRead]
    organizations: list[OrganizationMembershipRead] = []


class TokenClaims(BaseModel):
    sub: str
    email: str
    iss: str
    aud: str
    exp: int
    iat: int
