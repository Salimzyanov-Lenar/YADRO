from pydantic import BaseModel
from typing import List, Optional, Union


# Scheme for list user for our service

class UserCreateModel(BaseModel):
    gender: str
    first_name: str
    second_name: str
    phone_number: str
    email: str
    residing_place: str
    photo_url: str


class UserResponseModel(UserCreateModel):
    id: int

    class Config:
        from_attributes = True


# Scheme for response from randomuser.me

class Name(BaseModel):
    title: str
    first: str
    last: str


class Street(BaseModel):
    number: int
    name: str


class Coordinates(BaseModel):
    latitude: str
    longitude: str


class Timezone(BaseModel):
    offset: str
    description: str


class Location(BaseModel):
    street: Street
    city: str
    state: str
    country: str
    postcode: Union[str, int]
    coordinates: Coordinates
    timezone: Timezone


class Login(BaseModel):
    uuid: str
    username: str
    password: str
    salt: str
    md5: str
    sha1: str
    sha256: str


class DOB(BaseModel):
    date: str
    age: int


class Registered(BaseModel):
    date: str
    age: int


class ID(BaseModel):
    name: str
    value: Optional[str]


class Picture(BaseModel):
    large: str
    medium: str
    thumbnail: str


class ExternalUser(BaseModel):
    gender: str
    name: Name
    location: Location
    email: str
    login: Login
    dob: DOB
    registered: Registered
    phone: str
    cell: str
    id: ID
    picture: Picture
    nat: str


class ExternalResponse(BaseModel):
    results: List[ExternalUser]
    info: dict


class PaginatedUsersResponse(BaseModel):
    users: List[UserResponseModel]
    total_amount: int
    has_next: bool