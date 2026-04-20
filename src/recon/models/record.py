from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

from recon.models.person import Person
from recon.models.personal_situation_outbreak import PersonalSituationOutbreak
from recon.models.deportation_and_repression import DeportationAndRepression
from recon.models.repatriation import Repatriation
from recon.models.occupation_period import OccupationPeriod
from recon.models.military_experience import MilitaryExperience
from recon.models.other_military_experience import OtherMilitaryExperience
from recon.models.sources import Source
from recon.models.related_galleries import RelatedGallery

class Record(BaseModel):
    person: Person = Person(external_entry_id="0")
    personal_situation_outbreak: PersonalSituationOutbreak = PersonalSituationOutbreak()
    deportation_and_repression: DeportationAndRepression = DeportationAndRepression()
    repatration: Repatriation = Repatriation()
    occupation_period: OccupationPeriod = OccupationPeriod()
    military_experience: MilitaryExperience = MilitaryExperience()
    other_military_experience: OtherMilitaryExperience = OtherMilitaryExperience()
    sources: List[Source] = []
    related_galleries: List[RelatedGallery] = []

    model_config: ConfigDict = ConfigDict(from_attributes=True)