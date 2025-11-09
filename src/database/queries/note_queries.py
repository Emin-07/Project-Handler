from . import *


async def get_notes(
    get_employees_commons: PaginationDep_get,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[NoteSchema]:
    e = aliased(Note)
    res = await session.scalars(
        select(e)
        .where(e.id >= get_employees_commons.skip)
        .limit(get_employees_commons.limit)
        .order_by(e.id)
    )
    notes = res.all()
    validated_notes = [NoteSchema.model_validate(note) for note in notes]
    for note in validated_notes:
        print(note)
    return validated_notes


async def get_note(
    note_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> NoteRelSchema:
    note = await session.get(
        Note,
        note_id,
        options=(
            joinedload(Note.note_task),
            joinedload(Note.written_by),
        ),
    )
    if note is None:
        raise HTTPException(
            status_code=404,
            detail=f"There's no note with id {note_id}",
        )
    res = NoteRelSchema.model_validate(note)
    print(res)
    return res


async def delete_notes(
    notes_id: List[int] | int, session: Annotated[AsyncSession, Depends(get_session)]
) -> List[NoteSchema]:
    if isinstance(notes_id, int):
        notes_id = [notes_id]
    deleted_notes: List[NoteSchema] = []
    for note_id in notes_id:
        note = await session.get(Note, note_id)
        if note is not None:
            deleted_note = NoteSchema.model_validate(note)
            await session.delete(note)
            await session.commit()
            deleted_notes.append(deleted_note)
        else:
            raise HTTPException(
                status_code=404, detail=f"Note with id:{note_id} not found!"
            )
    return deleted_notes


async def create_notes(
    notes: List[NoteBase], session: Annotated[AsyncSession, Depends(get_session)]
) -> List[NoteSchema]:
    mapped_notes: List[Note] = [
        Note(
            note_info=note.note_info.strip(),
            employee_id=note.employee_id,
            task_id=note.task_id,
        )
        for note in notes
    ]
    session.add_all(mapped_notes)

    await session.commit()

    for new_note in mapped_notes:
        await session.refresh(new_note)

    notes_validated = [NoteSchema.model_validate(note) for note in mapped_notes]

    return notes_validated


async def update_note(
    update_id: int,
    update_data: UpdateNoteSchema,
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> NoteSchema:
    prev_note = await session.get(Note, update_id)
    if prev_note is None:
        raise HTTPException(
            status_code=404, detail=f"Note with id:{update_id} not found"
        )
    if request.method == "PATCH":
        update_dict = update_data.model_dump(exclude_unset=True)
    else:
        update_dict = update_data.model_dump()

    for key, val in update_dict.items():
        setattr(prev_note, key, val)

    await session.commit()
    await session.refresh(prev_note)

    note_validated = NoteSchema.model_validate(prev_note)
    print(note_validated)
    return note_validated


# # async def main():
# #     # await create_tables()
# #     # await insert_data()
# #     await get_note(200)


# # asyncio.run(main())
