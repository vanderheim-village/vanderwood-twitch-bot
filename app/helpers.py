from datetime import datetime

async def date_validate(date_text: str) -> bool:
    try:
        if date_text != datetime.strptime(date_text, "%d/%m/%Y").strftime('%d/%m/%Y'):
            raise ValueError
        return True
    except ValueError:
        return False