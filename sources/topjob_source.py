import re
import json
from bs4 import BeautifulSoup
from httpx import AsyncClient
from configs.helper_functions import normalize_text
from configs.logger import get_logger

from schema.job_category import JobCategory
from schema.job_summary import JobSummary
from sources.jobsource import JobSource

logger = get_logger("top-job-source")

class TopJobSource(JobSource):
    
    async def search_job(self, keyword:str, category:JobCategory, location = None, limit:int | None = 10):
        
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
                    
                case "All_Vacancies":
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
            
            # table = soup.find("table",id="table")
            
            # if not table:
            #     logger.warning("Jobs table not found")
            #     return []
            
            # rows = table.select("tbody > tr")
            # logger.info("Found %d job rows", len(rows))
            
            for row in soup.select("tr[onclick^='createAlert']"):
                
                columns = row.find_all("td")
                onclick = row.get("onclick")
                
                if not onclick:
                    continue
                
                if len(columns) < 7:
                    continue
                
                title_element = columns[2].find("h2")
                company_element = columns[2].find("h1")
                
                if not title_element or not company_element:
                    continue
                
                title = title_element.get_text(
                    " ",
                    strip=True
                )
                
                company_name = company_element.get_text(
                    " ",
                    strip=True
                )
                
                starting_date = columns[4].get_text(
                    " ",
                    strip=True
                )
                
                closing_date = columns[5].get_text(
                    " ",
                    strip=True
                )
                
                job_location = columns[6].get_text(
                    " ",
                    strip=True
                )
                
                image_id = columns[2].find_all("span")[0].get_text(
                    " ",
                    strip=True
                )
                
                normalized_keyword = normalize_text(keyword)
                normalized_title = normalize_text(title)
                
                if normalized_keyword not in normalized_title:
                    continue
                
                if location and (job_location.lower() not in location.lower()):
                    continue
                
                onclick_match = re.search(r"createAlert\((.*?)\)", onclick)
                onclick_params = onclick_match.group(1).split(",")
                
                onclick_params = [param.strip("'") for param in onclick_params]
                
                print(onclick_params)
                
                rid, ac, jc, ec, token = onclick_params

                job = JobSummary(
                    job_title=title,
                    company_name=company_name,
                    image_number=image_id,
                    starting_date=starting_date if starting_date else "Not Mentioned",
                    closing_date=closing_date if closing_date else "Not Mentioned",
                    location=job_location if job_location else "Not Mentioned",
                    rid = int(rid),
                    ac=ac,
                    jc=jc,
                    ec=ec,
                    token=token
                    
                )
                
                jobs.append(job)
                logger.info("Job has appended to the Jobs list successfully")
                
                
                if limit and (len(jobs) >= limit):
                    break
                
            text = "\n\n"    
            for job in jobs:
                
                job = job.model_dump()
                
                job_title: str = job.get("job_title", "") 
                company_name: str = job.get("company_name", "")
                image_number: int = job.get("image_number", "")
                
                starting_date: str = job.get("starting_date", "")
                closing_date: str = job.get("closing_date", "")
                location: str = job.get("location", "")
                rid = job.get("rid", "")
                ac= job.get("ac", "")
                jc= job.get("jc", "")
                ec= job.get("ec", "")
                token= job.get("token", "")
                
                
                job_text = f"""
                    job_title: {job_title}
                    company_name: {company_name}
                    image_number: {image_number}
                    starting_date: {starting_date}
                    closing_date: {closing_date}
                    location: {location}
                    rid: {rid}
                    ac: {ac}
                    jc: {jc}
                    ec: {ec}
                    token: {token}
                """
                
                text += job_text
                
            with open("job_details.txt", "w") as file:
                file.write(text)
            
            return jobs

        except Exception:
            logger.exception('Error in serach job in top job')
            raise
            
            
    async def get_job_details(self, job_img_no):
        
        try:
            
            #job_url = 
            pass
            
        except Exception:
            logger.exception("Error in get job details")
            raise