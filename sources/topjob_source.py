from bs4 import BeautifulSoup
from httpx import AsyncClient
from configs.logger import get_logger
from schema.job_category import JobCategory
from schema.job_summary import JobSummary
from sources.jobsource import JobSource

logger = get_logger("top-job-source")

class TopJobSource(JobSource):
    
    async def search_job(self, keyword, location, category:JobCategory, limit = 10):
        
        try:
            params = {
                "FA": None,
                "jst": "OPEN"
            }
            
            topjob_url = "https://www.topjobs.lk/applicant/vacancybyfunctionalarea.jsp"
            
            match category:
                
                case "IT-SWare/DB/QA/Web/Graphics/GIS":
                    params['FA'] = "SDQ"
                    
                case "IT-HWare/Networks/Systems":
                    params['FA'] = "HNS"
                    
                case "Accounting/Auditing/Finance":
                    params['FA'] = "ACA"
                    
                case "Banking & Finance/Insurance":
                    params['FA'] = "BAF"
                    
                case "Sales/Marketing/Merchandising":
                    params['FA'] = "SMM"
                    
                case "HR/Training":
                    params['FA'] = "HAT"
                    
                case "Corporate Management/Analysts":
                    params['FA'] = "COM"
                
                case "Office Admin/Secretary/Receptionist":
                    params['FA'] = "OAS"
                
                case "Civil Eng/Interior Design/Architecture":
                    params['FA'] = "CCE"
                    
                case  "IT-Telecoms":
                    params['FA'] = "ITT"
                
                case "Customer Relations/Public Relations":
                    params['FA'] = "CUR"
                    
                case  "Logistics/Warehouse/Transport":
                    params['FA'] = "LWT"
                    
                case "Eng-Mech/Auto/Elec":
                    params['FA'] = "MAE"
                    
                case "Manufacturing/Operations":
                    params['FA'] = "POS"
                    
                case "Media/Advert/Communication":
                    params['FA'] = "MAC"
                    
                case "Hotel/Restaurant/Hospitality":
                    params['FA'] = "HRF"
                    
                case "Travel/Tourism":
                    params["FA"] = "HOT"
                    
                case "Sports/Fitness/Recreation":
                    params['FA'] = "SRF"
                    
                case "Medical/Nursing/Healthcare":
                    params['FA'] = "MHN"
                
                case "Legal/Law":
                    params['FA'] = "LEL"
                    
                case "Supervision/Quality Control":
                    params['FA'] = "SQC"
                    
                case "Apparel/Clothing":
                    params['FA'] = "APC"
                
                case "Ticketing/Airline/Marine":
                    params['FA'] = "AIM"
                    
                case "Education":
                    params['FA'] = "TAL"

                case "R&D/Science/Research":
                    params['FA'] = "RLT"
                    
                case "Agriculture/Dairy/Environment":
                    params['FA'] = "AGD"
                    
                case "Security":
                    params['FA'] = "SEC"
                    
                case "Fashion/Design/Beauty":
                    params['FA'] = "BEC"
                
                case  "International Development":
                    params['FA'] = "IDV"
                    
                case "KPO/BPO":
                    params['FA'] = "KPO"
                    
                case "Imports/Exports":
                    params['FA'] = "IME"
                    
                case "All Vacancies":
                    params['FA'] = None
            
            
            async with AsyncClient(
                follow_redirects=True,
                timeout=20,
            ) as client:
                
                response = await client.get(topjob_url, params=params)
                response.raise_for_status()
                
                logger.info(
                    "Fetching TopJobs URL: %s",
                    response.request.url
                )
                
                soup = BeautifulSoup(
                    response.text,
                    "html.parser"
                )
                
            jobs:list[JobSummary] = []
            
            for row in soup.select("tr[onclick^='createAlert']"):
                
                columns = row.find_all("td")
                
                if len(columns) < 7:
                    continue
                
                title_element = columns[2].find("h1")
                company_elemt = columns[2].find("h1")
                
                if not title_element or not company_elemt:
                    continue
                
                
                
                
                

        except Exception:
            logger.exception('Error in serach job in top job')
            raise
            
            
    async def get_job_details(self, job_url):
        pass