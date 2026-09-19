from typing import Literal
from pydantic import BaseModel

class JobCategory(BaseModel):
    
    JobCategory = Literal[
            "IT-SWare/DB/QA/Web/Graphics/GIS",
            "IT-HWare/Networks/Systems",
            "Accounting/Auditing/Finance",
            "Banking & Finance/Insurance",
            "Sales/Marketing/Merchandising",
            "HR/Training",
            "Corporate Management/Analysts",
            "Office Admin/Secretary/Receptionist",
            "Civil Eng/Interior Design/Architecture",
            "IT-Telecoms",
            "Customer Relations/Public Relations",
            "Logistics/Warehouse/Transport",
            "Eng-Mech/Auto/Elec",
            "Manufacturing/Operations",
            "Media/Advert/Communication",
            "Hotel/Restaurant/Hospitality",
            "Travel/Tourism",
            "Sports/Fitness/Recreation",
            "Medical/Nursing/Healthcare",
            "Legal/Law",
            "Supervision/Quality Control",
            "Apparel/Clothing",
            "Ticketing/Airline/Marine",
            "Education",
            "R&D/Science/Research",
            "Agriculture/Dairy/Environment",
            "Security",
            "Fashion/Design/Beauty",
            "International Development",
            "KPO/BPO",
            "Imports/Exports",
            "All Vacancies",
]