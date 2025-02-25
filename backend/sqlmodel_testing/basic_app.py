from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

# Define the models

class CountryMissionLink(SQLModel, table=True):
    country_id: Optional[int] = Field(
        default=None, foreign_key="country.id", primary_key=True
    )
    mission_id: Optional[int] = Field(
        default=None, foreign_key="mission.id", primary_key=True
    )


class Affiliation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    countries: list["Country"] = Relationship(back_populates="affiliation")


class Country(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    capital: str
    age: Optional[int] = None
    affiliation_id: Optional[int] = Field(default=None, foreign_key="affiliation.id")

    affiliation: Optional[Affiliation] = Relationship(back_populates="countries")
    missions: list["Mission"] = Relationship(
        back_populates="countries", link_model=CountryMissionLink
    )


class Mission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str

    countries: list[Country] = Relationship(
        back_populates="missions", link_model=CountryMissionLink
    )


# Setup FastAPI app
app = FastAPI()

# Create the SQLite database engine
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)
SQLModel.metadata.create_all(engine)


# Dependency: Database session
def get_session():
    with Session(engine) as session:
        yield session


# Create Affiliation
@app.post("/affiliation/", response_model=Affiliation)
def create_affiliation(team: Affiliation, session: Session = Depends(get_session)):
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


# Create Country
@app.post("/countries/", response_model=Country)
def create_country(country: Country, session: Session = Depends(get_session)):
    session.add(country)
    session.commit()
    session.refresh(country)
    return country


# Assign Country to Affiliation
@app.put("/countries/{country_id}/affiliation/{affiliation_id}", response_model=Country)
def assign_hero_to_team(
    country_id: int, affiliation_id: int, session: Session = Depends(get_session)
):
    country = session.get(Country, country_id)
    affiliation = session.get(Affiliation, affiliation_id)
    if not country or not affiliation:
        raise HTTPException(status_code=404, detail="Country or Affiliation not found")
    country.affiliation_id = affiliation_id
    session.commit()
    session.refresh(country)
    return country


# Create Mission
@app.post("/mission/", response_model=Mission)
def create_mission(mission: Mission, session: Session = Depends(get_session)):
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission


# Assign Country to Mission (Many-to-Many)
@app.put("/missions/{mission_id}/countries/{country_id}", response_model=Mission)
def assign_country_to_mission(
    mission_id: int, country_id: int, session: Session = Depends(get_session)
):
    country = session.get(Country, country_id)
    mission = session.get(Mission, mission_id)
    if not country or not mission:
        raise HTTPException(status_code=404, detail="Country or Mission not found")
    country_mission_link = CountryMissionLink(country_id=country_id, mission_id=mission_id)
    session.add(country_mission_link)
    session.commit()
    return mission


# Read Country with relationships
@app.get("/countries/{country_id}", response_model=Country)
def read_hero(country_id: int, session: Session = Depends(get_session)):
    country = session.get(Country, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


# Read Affiliation with Countries
@app.get("/affiliation/{affiliation_id}", response_model=Affiliation)
def read_team(affiliation_id: int, session: Session = Depends(get_session)):
    affiliation = session.get(Affiliation, affiliation_id)
    if not affiliation:
        raise HTTPException(status_code=404, detail="Affiliation not found")
    return affiliation


# Read Mission with Countries
@app.get("/missions/{mission_id}", response_model=Mission)
def read_mission(mission_id: int, session: Session = Depends(get_session)):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


# Delete a Country from archives
@app.delete("/countries/{country_id}", response_model=Country)
def delete_country(country_id: int, session: Session = Depends(get_session)):
    country = session.get(Country, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    session.delete(country)
    session.commit()
    return country


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)