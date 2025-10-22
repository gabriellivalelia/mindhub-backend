from datetime import date, datetime
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, File, Form, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse

from application.common.page import Page
from application.dtos.appointment_dto import AppointmentDTO
from application.dtos.psychologist_dto import PsychologistDTO
from application.services.iauth_service import JWTData
from application.use_cases.psychologist.add_availabilities import (
    AddAvailabilitiesDTO,
    AddAvailabilitiesUseCase,
)
from application.use_cases.psychologist.complete_appointment import (
    CompleteAppointmentDTO,
    CompleteAppointmentUseCase,
)
from application.use_cases.psychologist.confirm_payment import (
    ConfirmPaymentDTO,
    ConfirmPaymentUseCase,
)
from application.use_cases.psychologist.create_psychologist import (
    CreatePsychologistDTO,
    CreatePsychologistUseCase,
)
from application.use_cases.psychologist.get_psychologist_by_id import (
    GetPsychologistByIdDTO,
    GetPsychologistByIdUseCase,
)
from application.use_cases.psychologist.get_psychologists import (
    GetPsychologistsDTO,
    GetPsychologistsUseCase,
)
from application.use_cases.psychologist.remove_availabilities import (
    RemoveAvailabilitiesDTO,
    RemoveAvailabilitiesUseCase,
)
from application.use_cases.psychologist.update_psychologist import (
    UpdatePsychologistDTO,
    UpdatePsychologistUseCase,
)
from infra.routers.utils import ConvertEmptyStrToNoneBeforeValidator

router = APIRouter(route_class=DishkaRoute)
route = "/psychologists"


@router.post(
    route,
    status_code=status.HTTP_201_CREATED,
    response_model=PsychologistDTO,
    tags=["psychologists"],
)
async def create_psychologist(
    name: Annotated[str, Form(examples=["Cleber"])],
    email: Annotated[str, Form(examples=["cleber@psy.com"])],
    password: Annotated[str, Form(examples=["AcC123456*"])],
    cpf: Annotated[str, Form(examples=["86231101533"])],
    phone_number: Annotated[str, Form(examples=["71999258225"])],
    birth_date: Annotated[
        date, Form(examples=["1999-07-28"]), ConvertEmptyStrToNoneBeforeValidator
    ],
    gender: Annotated[str, Form(examples=["male"])],
    city_id: Annotated[
        UUID,
        Form(examples=["c51e05bc-c48b-4229-980e-3841e62ae413"]),
        ConvertEmptyStrToNoneBeforeValidator,
    ],
    crp: Annotated[str, Form(examples=["05/5555"])],
    specialty_ids: Annotated[
        list[UUID],
        Form(examples=[["b5a736f6-834f-46ad-94f0-4cab9a7a90f5"]]),
        ConvertEmptyStrToNoneBeforeValidator,
    ],
    approach_ids: Annotated[
        list[UUID],
        Form(examples=[["b5a736f6-834f-46ad-94f0-4cab9a7a90f5"]]),
        ConvertEmptyStrToNoneBeforeValidator,
    ],
    audiences: Annotated[
        list[str], Form(examples=[["children"]]), ConvertEmptyStrToNoneBeforeValidator
    ],
    use_case: FromDishka[CreatePsychologistUseCase],
    value_per_appointment: Annotated[
        float, Form(examples=[150.00]), ConvertEmptyStrToNoneBeforeValidator
    ] = 150,
    description: Annotated[str | None, Form(example=[None])] = None,
    profile_picture: Annotated[
        UploadFile | None, File(), ConvertEmptyStrToNoneBeforeValidator
    ] = None,
) -> PsychologistDTO | JSONResponse:
    dto = CreatePsychologistDTO(
        name=name,
        email=email,
        password=password,
        cpf=cpf,
        phone_number=phone_number,
        birth_date=birth_date,
        gender=gender,
        city_id=city_id,
        crp=crp,
        description=description,
        specialty_ids=specialty_ids,
        approach_ids=approach_ids,
        audiences=audiences,
        profile_picture=profile_picture,
        value_per_appointment=value_per_appointment,
    )
    return await use_case.execute(dto)


@router.get(
    f"{route}/{{psychologist_id}}",
    status_code=status.HTTP_200_OK,
    response_model=PsychologistDTO,
    tags=["psychologists"],
)
async def get_psychologist_by_id(
    psychologist_id: Annotated[UUID, Path()],
    use_case: FromDishka[GetPsychologistByIdUseCase],
) -> PsychologistDTO:
    dto = GetPsychologistByIdDTO(psychologist_id=psychologist_id)
    return await use_case.execute(dto)


@router.get(
    route,
    status_code=status.HTTP_200_OK,
    response_model=Page[PsychologistDTO],
    tags=["psychologists"],
)
async def get_psychologists(
    dto: Annotated[GetPsychologistsDTO, Query()],
    use_case: FromDishka[GetPsychologistsUseCase],
) -> Page[PsychologistDTO]:
    return await use_case.execute(dto)


@router.post(
    f"{route}/availabilities",
    status_code=status.HTTP_200_OK,
    response_model=PsychologistDTO,
    tags=["psychologists"],
)
async def add_availabilities(
    jwt_data: FromDishka[JWTData],
    request_dto: Annotated[
        list[datetime],
        Body(
            examples=[
                [
                    "2025-10-05T18:50:29.022Z",
                    "2025-10-15T18:50:29.022Z",
                    "2025-10-25T18:50:29.022Z",
                ]
            ]
        ),
    ],
    use_case: FromDishka[AddAvailabilitiesUseCase],
) -> PsychologistDTO | JSONResponse:
    dto = AddAvailabilitiesDTO(
        availability_datetimes=request_dto,
        psychologist_id=jwt_data.id,
    )

    return await use_case.execute(dto)


@router.delete(
    f"{route}/availabilities",
    status_code=status.HTTP_200_OK,
    response_model=PsychologistDTO,
    tags=["psychologists"],
)
async def remove_availabilities(
    jwt_data: FromDishka[JWTData],
    request_dto: Annotated[
        list[datetime],
        Body(
            examples=[
                [
                    "2025-10-05T18:50:29.022Z",
                    "2025-10-15T18:50:29.022Z",
                    "2025-10-25T18:50:29.022Z",
                ]
            ]
        ),
    ],
    use_case: FromDishka[RemoveAvailabilitiesUseCase],
) -> PsychologistDTO | JSONResponse:
    dto = RemoveAvailabilitiesDTO(
        availability_datetimes=request_dto,
        psychologist_id=jwt_data.id,
    )

    return await use_case.execute(dto)


@router.put(
    f"{route}",
    status_code=status.HTTP_200_OK,
    response_model=PsychologistDTO,
    tags=["psychologists"],
)
async def update_psychologist(
    jwt_data: FromDishka[JWTData],
    use_case: FromDishka[UpdatePsychologistUseCase],
    name: Annotated[str | None, Form(examples=[""])] = None,
    email: Annotated[str | None, Form(examples=[""])] = None,
    cpf: Annotated[str | None, Form(examples=[""])] = None,
    phone_number: Annotated[str | None, Form(examples=[""])] = None,
    birth_date: Annotated[
        date | None, Form(examples=[""]), ConvertEmptyStrToNoneBeforeValidator
    ] = None,
    gender: Annotated[str | None, Form(examples=[""])] = None,
    city_id: Annotated[
        UUID | None, Form(examples=[""]), ConvertEmptyStrToNoneBeforeValidator
    ] = None,
    crp: Annotated[str | None, Form(examples=[""])] = None,
    description: Annotated[str | None, Form(examples=[""])] = None,
    specialty_ids: Annotated[
        list[UUID] | None, Form(examples=[[""]]), ConvertEmptyStrToNoneBeforeValidator
    ] = None,
    approach_ids: Annotated[
        list[UUID] | None, Form(examples=[[""]]), ConvertEmptyStrToNoneBeforeValidator
    ] = None,
    audiences: Annotated[
        list[str] | None, Form(examples=[[""]]), ConvertEmptyStrToNoneBeforeValidator
    ] = None,
    value_per_appointment: Annotated[
        float | None, Form(examples=[None]), ConvertEmptyStrToNoneBeforeValidator
    ] = None,
    profile_picture: Annotated[
        UploadFile | None, File(examples=[None]), ConvertEmptyStrToNoneBeforeValidator
    ] = None,
    delete_profile_picture: Annotated[bool, Form(examples=[False])] = False,
) -> PsychologistDTO | JSONResponse:
    dto = UpdatePsychologistDTO(
        psychologist_id=jwt_data.id,
        name=name,
        email=email,
        cpf=cpf,
        phone_number=phone_number,
        birth_date=birth_date,
        gender=gender,
        city_id=city_id,
        crp=crp,
        description=description,
        specialty_ids=specialty_ids,
        approach_ids=approach_ids,
        audiences=audiences,
        value_per_appointment=value_per_appointment,
        profile_picture=profile_picture,
        delete_profile_picture=delete_profile_picture,
    )
    return await use_case.execute(dto)


@router.post(
    f"{route}/appointments/{{appointment_id}}/confirm-payment",
    status_code=status.HTTP_200_OK,
    response_model=AppointmentDTO,
    tags=["psychologists"],
)
async def confirm_payment(
    jwt_data: FromDishka[JWTData],
    appointment_id: Annotated[UUID, Path()],
    use_case: FromDishka[ConfirmPaymentUseCase],
) -> AppointmentDTO | JSONResponse:
    dto = ConfirmPaymentDTO(appointment_id=appointment_id, psychologist_id=jwt_data.id)
    return await use_case.execute(dto)


@router.post(
    f"{route}/appointments/{{appointment_id}}/complete",
    status_code=status.HTTP_200_OK,
    response_model=AppointmentDTO,
    tags=["psychologists"],
)
async def complete_appointment(
    jwt_data: FromDishka[JWTData],
    appointment_id: Annotated[UUID, Path()],
    use_case: FromDishka[CompleteAppointmentUseCase],
) -> AppointmentDTO | JSONResponse:
    dto = CompleteAppointmentDTO(
        appointment_id=appointment_id, psychologist_id=jwt_data.id
    )
    return await use_case.execute(dto)
