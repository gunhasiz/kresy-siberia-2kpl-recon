# constants.py
# This file contains constants used across the recon project.

# H4 section titles on the record page
from typing import NoReturn

from recon.models.person import Person as PersonModel
from recon.models.personal_situation_outbreak import PersonalSituationOutbreak as PersonalSituationOutbreakModel
from recon.models.deportation_and_repression import DeportationAndRepression as DeportationAndRepressionModel, Place
from recon.models.repatriation import Repatriation as RepatriationModel
from recon.models.occupation_period import OccupationPeriod as OccupationPeriodModel
from recon.models.military_experience import MilitaryExperience as MilitaryExperienceModel
from recon.models.other_military_experience import OtherMilitaryExperience as OtherMilitaryExperienceModel
from recon.models.sources import Source
from recon.models.related_galleries import RelatedGallery


PERSONAL_DETAILS: str = r"Personal Details"
PERSONAL_SITUATION_OUTBREAK: str = r"Personal Situation at the outbreak of WWll"
DEPORTATIONS_AND_REPRESSIONS: str = r"Deportations and Repressions"
REPATRIATION: str = r"For those who were repatriated to Poland from the Kresy or the USSR, please provide the following information"
OCCUPATION_PERIOD: str = r"For those who stayed in the Kresy area during WWII, please provide the following information"
MILITARY_EXPERIENCE: str = r"Military Experience"
OTHER_MILITARY_EXPERIENCE: str = r"Other Wartime Circumstances"
SOURCES: str = r"Sources"
RELATED_GALLERIES: str = r"Related Museum Galleries"

class Person:
    NAME = "Name"
    MAIDEN_NAME = "Maiden Name"
    NICKNAME = "Nickname/Pseudonym"
    GENDER = "Gender"
    BIRTH_DATE = "Date of birth"
    BIRTH_PLACE = "Place of birth"
    DIED_IN_WW2 = "Did this person die during World War ll?"
    DEATH_DATE= "Date of death"
    DEATH_PLACE = "Place of death"
    DEATH_CAUSE = "Cause of Death"
    FATHER_NAME = "Fathers given name"
    MOTHER_NAME = "Mothers given name"
    MOTHER_MAIDEN_NAME = "Mothers maiden name"
    SPOUSE_NAME = "Given name of spouse"
    SPOUSE_MAIDEN_NAME = "Maiden name of spouse"
    CHILDERN_NAMES = "Given name(s) of children"
    DESCRIPTION = "Description"

class PersonalSituationOutbreak:
    RESIDENCE = "Residence at the outbreak of WWll"
    KRESY_INHABITANT_STATUS = "Kresy Inhabitant Status"
    ETHNICITY = "Ethnicity"
    RELIGION = "Religion"
    EDUCATION_LEVEL = "Education Level"
    OCCUPATION = "Occupation at the outbreak of WWll"
    MILITARY_STATUS = "Military status at the outbreak of WWll"
    MILITARY_RANK = "Military Rank at the outbreak of WWll"

    def __setattr__(self, key, value) -> NoReturn:
        raise AttributeError("Constants are read-only")

class DeportationAndRepression:
    OTHER_INFORMATION = "Other Information"
    
    def __setattr__(self, key, value) -> NoReturn:
        raise AttributeError("Constants are read-only")

class Place:
    FROM_YYYY = "FROM: yyyy"
    MM = "mm"
    DD = "dd"
    TO_YYYY = "to: yyyy"
    DEPORTING_AUTHORITY = "To"
    OBLAST = "Oblast"
    CITY = "Locality"
    
    def __setattr__(self, key, value) -> NoReturn:
        raise AttributeError("Constants are read-only")

class Repatriation:
    RETURN_DATE = "Date of return to Poland"
    PROVINCE = "Province"
    COUNTY = "County"
    LOCALITY = "Locality"
    NEAREST_LARGE_CITY = "Nearest large city"

    def __setattr__(self, key, value) -> NoReturn:
        raise AttributeError("Constants are read-only")

class OccupationPeriod:
    PROVINCE = "Province - as at 1939"
    COUNTY = "County"
    CITY_PLACE = "City / Place"
    NEAREST_LARGE_CITY = "Nearest Large City"

    def __setattr__(self, key, value) -> NoReturn:
        raise AttributeError("Constants are read-only")

class MilitaryService:
    SERVED_IN = "Served in"
    UNIT_NAME = "Unit"
    FROM_YYYY = "From: yyyy"
    MM = "mm"
    DD = "dd"
    TO_YYYY = "To: yyyy"

    def __setattr__(self, key, value) -> NoReturn:
        raise AttributeError("Constants are read-only")

class MilitaryExperience:
    OTHER_MILITARY_SERVICE = "Other Military Service"
    PARTICIPATION_IN_WWII_BATTLES = "Participation in WWII battles"
    MEDALS_RECEIVED = "Medals received"
    OTHER_BATTLES = "Other Battles"

    def __setattr__(self, key, value) -> NoReturn:
        raise AttributeError("Constants are read-only")

class OtherMilitaryExperience:
    INFORMATION = "Other Information"
    ORPHANAGES = "Orphanages"
    CIVILIAN_CAMP_MIDDLE_EAST = "Civilian Camp in the Middle East"
    CIVILIAN_CAMP_INDIA = "Civilian Camp in India"
    CIVILIAN_CAMP_AFRICA = "Civilian Camp in Africa"
    OTHER_INFORMATION = "Please provide information if none of the preceding apply"

    def __setattr__(self, key, value) -> NoReturn:
        raise AttributeError("Constants are read-only")

MODEL_FIELD_MAP: dict[type, dict] = {
    PersonModel: {
        Person.NAME: "full_name",
        Person.MAIDEN_NAME: "maiden_name",
        Person.NICKNAME: "nickname",
        Person.GENDER: "gender",
        Person.BIRTH_DATE: "birth_date",
        Person.BIRTH_PLACE: "birth_place",
        Person.DIED_IN_WW2: "died_in_ww2",
        Person.DEATH_DATE: "death_date",
        Person.DEATH_PLACE: "death_place",
        Person.DEATH_CAUSE: "death_cause",
        Person.FATHER_NAME: "father_name",
        Person.MOTHER_NAME: "mother_name",
        Person.MOTHER_MAIDEN_NAME: "mother_maiden_name",
        Person.SPOUSE_NAME: "spouse_name",
        Person.SPOUSE_MAIDEN_NAME: "spouse_maiden_name",
        Person.CHILDERN_NAMES: "children_names",
        Person.DESCRIPTION: "description"
    },
    PersonalSituationOutbreakModel: {
        PersonalSituationOutbreak.RESIDENCE: "residence",
        PersonalSituationOutbreak.KRESY_INHABITANT_STATUS: "kresy_inhabitant_status",
        PersonalSituationOutbreak.ETHNICITY: "ethnicity",
        PersonalSituationOutbreak.RELIGION: "religion",
        PersonalSituationOutbreak.EDUCATION_LEVEL: "education_level",
        PersonalSituationOutbreak.OCCUPATION: "occupation",
        PersonalSituationOutbreak.MILITARY_STATUS: "military_status",
        PersonalSituationOutbreak.MILITARY_RANK: "military_rank",
    },
    DeportationAndRepressionModel: {
    DeportationAndRepression.OTHER_INFORMATION: "other_information",
        "_nested": {
            "place": {
                "model": Place,
                "map_sequence": [
                    (Place.FROM_YYYY, "from_yyyy"),
                    (Place.MM,        "mm_first"),
                    (Place.DD,        "dd_first"),
                    (Place.TO_YYYY,   "to_yyyy"),
                    (Place.MM,        "mm_last"),
                    (Place.DD,        "dd_last"),
                    (Place.DEPORTING_AUTHORITY, "deporting_authority"),
                    (Place.OBLAST,    "oblast"),
                    (Place.CITY,      "city"),
                ]
            }
        }
    },
    RepatriationModel: {
        Repatriation.RETURN_DATE: "return_date",
        Repatriation.PROVINCE: "province",
        Repatriation.COUNTY: "county",
        Repatriation.LOCALITY: "locality",
        Repatriation.NEAREST_LARGE_CITY: "nearest_large_city",
    },
    OccupationPeriodModel: {
        OccupationPeriod.PROVINCE: "province",
        OccupationPeriod.COUNTY: "county",
        OccupationPeriod.CITY_PLACE: "city_place",
        OccupationPeriod.NEAREST_LARGE_CITY: "nearest_large_city",
    },
    MilitaryExperienceModel: {
        MilitaryExperience.OTHER_MILITARY_SERVICE: "other_military_service",
        MilitaryExperience.PARTICIPATION_IN_WWII_BATTLES: "participation_in_wwii_battles",
        MilitaryExperience.MEDALS_RECEIVED: "medals_received",
        MilitaryExperience.OTHER_BATTLES: "other_battles",
        "_list": {
            "military_services": {
                "model": MilitaryService,
                "map_sequence": [
                    (MilitaryService.SERVED_IN,  "served_in"),
                    (MilitaryService.UNIT_NAME,  "unit_name"),
                    (MilitaryService.FROM_YYYY,  "from_yyyy"),
                    (MilitaryService.MM,         "mm_first"),
                    (MilitaryService.DD,         "dd_first"),
                    (MilitaryService.TO_YYYY,    "to_yyyy"),
                    (MilitaryService.MM,         "mm_last"),
                    (MilitaryService.DD,         "dd_last"),
                ]
            }
        }
    },
    OtherMilitaryExperienceModel: {
        OtherMilitaryExperience.INFORMATION: "information",
        OtherMilitaryExperience.ORPHANAGES: "orphanages",
        OtherMilitaryExperience.CIVILIAN_CAMP_MIDDLE_EAST: "civilian_camp_middle_east",
        OtherMilitaryExperience.CIVILIAN_CAMP_INDIA: "civilian_camp_india",
        OtherMilitaryExperience.CIVILIAN_CAMP_AFRICA: "civilian_camp_africa",
        OtherMilitaryExperience.OTHER_INFORMATION: "other_information",
    }
}