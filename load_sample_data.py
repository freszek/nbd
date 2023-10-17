
from sqlalchemy.orm import Session
from combined_kino_db_model import Klient, Film, Sala, Siedzenie, Jedzenie, Bilet, BiletNormalny, BiletUlgowy, engine
from sample_data import sample_data  # importowanie pliku z danymi

# sesja alchemiczna sql
session = Session(engine)


# ladowanie danych do tabeli
for table, data in sample_data.items():
    if table == 'Klient':
        for record in data:
            session.add(Klient(**record))
    elif table == 'Film':
        for record in data:
            session.add(Film(**record))
    elif table == 'Sala':
        for record in data:
            session.add(Sala(**record))
    elif table == 'Siedzenie':
        for record in data:
            session.add(Siedzenie(**record))
    elif table == 'Jedzenie':
        for record in data:
            session.add(Jedzenie(**record))
    elif table == 'Bilet':
        for i, record in enumerate(data):
            if i % 2 == 0:
                session.add(BiletNormalny(**record, cena_dodatkowa=2.0))
            else:
                session.add(BiletUlgowy(**record, procent_ulg=10.0))
    session.commit()

for table, data in sample_data.items():
    model = globals()[table]  # model klasy bazujący na nazwie
    for row_data in data:
        row = model(**row_data)  # tworzenie modelu z danych
        session.add(row)  # dodanie obiektu do sesji

# wyslanie 
session.commit()
