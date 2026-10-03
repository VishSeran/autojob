import asyncio

from langchain_core.documents import Document
from langgraph.graph import StateGraph

from agents.cover_letter_agent import CoverLetterAgent
from agents.image_data_extractor_agent import ImageDataExtractorAgent
from agents.job_relevance_agent import JobRelevanceAgent
from agents.profile_extractor_agent import ProfileExtractorAgent
from agents.query_extractor_agent import QueryHandlerAgent
from client_server_sources.topjob_client_server import TopJobClientServerSource
from configs.configurations import JOB_RELEVANCY_THRESHOLD, TOPJOB_SERVER_URL
from configs.logger import get_logger
from mcp_client.client import MCPClient
from schema.job_image_schema import JobDetails
from schema.job_schema import Job
from schema.query_schema import QuerySchema
from schema.resume_schema import ResumeSchema
from workflow.workflow_state import WorkflowState

logger = get_logger("agent-workflow")



class AgentWorkflow:
    def __init__(self):

        try:
            self.workflow = None
            self.topjob_mcp_client = MCPClient(TOPJOB_SERVER_URL)
            self.topjob_client_server_Source = None
            self.query_handler_agent = QueryHandlerAgent()
            self.image_handler_agent = ImageDataExtractorAgent()
            self.profile_extractor_agent = ProfileExtractorAgent()
            self.job_relevancy_agent = JobRelevanceAgent()
            self.cover_letter_agent = CoverLetterAgent()

            logger.info("workflow - Agents are initialized")
            self.build_workflow()
            logger.info("Workflow build is completed")

        except Exception:
            logger.exception("Unexpected error in agent workflow")
            raise

    async def initialize(self):

        try:
            await self.topjob_mcp_client.init_connection()
            logger.info("workflow - Topjob mcp client is connected")

            self.topjob_client_server_Source = TopJobClientServerSource(
                self.topjob_mcp_client
            )

        except Exception:
            logger.exception("Unexpected error in worlflow initialize")
            raise

    def build_workflow(self):

        try:
            if self.workflow is not None:
                raise RuntimeError("Workflow is already running")

            graph = StateGraph(WorkflowState)
            graph.add_node("query_handler_node", self.query_handler_node)
            graph.add_node("topjob_search_node", self.topjob_search_node)
            graph.add_node("image_data_handler_node", self.image_data_handler_node)
            graph.add_node("get_full_job_summary_node", self.get_full_job_summary_node)
            graph.add_node("profile_extractor_node", self.profile_extractor_node)
            graph.add_node("relevancy_node", self.relevancy_node)
            graph.add_node("decision_making_node", self.decision_making_node)
            graph.add_node("next_job_node", self.next_job_node)

        except Exception:
            logger.exception("Unexpected error in build workflow")
            raise

    async def query_handler_node(self, state: WorkflowState):

        try:
            query = state.get("query", "")

            if not query:
                final_answer = "It seems like you have no questions my friend."

                return {"final_response": final_answer}

            response: QuerySchema = await self.query_handler_agent.get_response(query)
            logger.info("workflow - query response is fetched")

            return {
                "keyword": response.keyword,
                "location": response.location,
                "job_field": response.field,
                "no_of_jobs": response.number_of_jobs,
            }

        except ValueError:
            logger.exception("Unexpected value error in query handler node")
            raise

        except Exception:
            logger.exception("Unexpected error in query handler node")
            raise

    async def topjob_search_node(self, state: WorkflowState):

        try:
            keyword = state.get("keyword", "")
            location = state.get("location", "")
            field = state.get("job_field", "")
            limit = state.get("no_of_jobs")

            job_list = await self.topjob_client_server_Source.search_jobs(
                keyword, location, field, limit
            )

            if not job_list:
                logger.info("No relevant jobs found")

                return {
                    "source": "topjob",
                    "topjob_summary": [],
                    "topjob_images_urls": {},
                }

            relavant_job_images = (
                await self.topjob_client_server_Source.get_jobs_details(job_list)
            )

            logger.info("workflow - Relavant jobs extracted")

            return {
                "source": "topjob",
                "topjob_summary": job_list,
                "topjob_images_urls": relavant_job_images,
            }

        except Exception:
            logger.exception("Unexpected error in job search node")
            raise

    async def image_data_handler_node(self, state: WorkflowState):

        try:
            source = state.get("source", "")
            results = {}

            if source == "topjob":
                
                job_images_urls = state.get("topjob_images_urls", {})
                
                # Maximum number of vision requests running simultaneously
                semaphore = asyncio.Semaphore(3)

                async def process_job(job_title, image_urls):
    
                    try:
                        logger.info(f"Extracting {job_title}...")
                        
                        if not image_urls:
                            return job_title, JobDetails().model_dump()

                        images = [
                            {"type": "image_url", "image_url": {"url": img_url}}
                            for img_url in image_urls
                        ]
                        
                        async with semaphore:
                            response = await self.image_handler_agent.get_vision_response(
                                images
                            )
                            
                        logger.info("Image data response is fetched")

                        return job_title, response.model_dump()

                    except Exception:
                        logger.exception(
                            "Failed to extract image data for job: %s", job_title
                        )
                        return job_title, JobDetails().model_dump()

                # Create concurrent tasks
                tasks = [
                    asyncio.create_task(
                        process_job(job_title, image_urls)
                    )
                    for job_title, image_urls in job_images_urls.items()
                ]
                
                # Wait for all jobs
                job_results = await asyncio.gather(*tasks)
                
                results = dict(job_results)

                logger.info("workflow - TopJob job images final details are fetched")

            return {"topjob_images_details": results}

        except Exception:
            logger.exception("Unexpected error in image data handler node")
            raise

    async def get_full_job_summary_node(self, state: WorkflowState):

        try:
            source = state.get("source", "")
            complete_job_details = []

            if source == "topjob":
                job_list = state.get("topjob_summary")
                topjob_image_details = state.get("topjob_images_details", {})
                topjob_image_urls = state.get("topjob_images_urls", {})

                for job in job_list:
                    job = job.model_dump()
                    job_title = job.get("job_title")

                    image_data = topjob_image_details.get(job_title)

                    if not image_data:
                        logger.warning(f"No image details found for job: {job_title}")
                        continue

                    job_summary = Job(
                        source= source,
                        job_url= topjob_image_urls[job_title],
                        company_name= job.get("company_name", ""),
                        company_email= image_data["company_email", ""],
                        company_contact= image_data["company_contact", ""],
                        description= image_data["description"],
                        responsibilities= image_data["responsibilities"],
                        requirments= image_data["requirements"],
                        location= job.get("location", ""),
                        salary= image_data["salary"],
                        starting_date= job.get("starting_date", ""),
                        closing_date= job.get("closing_date", ""),
                    )

                    complete_job_details.append(job_summary)
                    logger.info(f"Topjob job is listed: {job_title}")

                logger.info("workflow - Topjob- job listing is finished")

            return {"complete_job_details": complete_job_details}

        except Exception:
            logger.exception("Unexpected error in get full job summary")
            raise

    async def profile_extractor_node(self, state: WorkflowState):

        try:
            current_resume: list[Document] = state.get("current_resume", [])

            resume_text = "\n".join(doc.page_content for doc in current_resume)

            response = await self.profile_extractor_agent.get_response(resume_text)
            logger.info("workflow - Response is fetched")

            return {"profile_data": response}

        except Exception:
            logger.exception("Unexpected error in profile extractor")
            raise

    async def relevancy_node(self, state: WorkflowState):

        try:
            profile = state.get("profile_data", ResumeSchema())
            jobs = state.get("complete_job_details", [])

            job_relevancy = []
            is_relevant = False

            profile_data = profile.model_dump()
            profile_detail = f"""
                personal_details: {profile_data.get("personal_details", [])}
                education: {profile_data.get("education", [])}
                skills: {profile_data.get("skills", [])}
                experiences: {profile_data.get("experiences", [])} 
                projects: {profile_data.get("projects", [])}
                certifications: {profile_data.get("certifications", [])}
                extra_curricular_activities: {profile_data.get("extra_curricular_activities", [])}
            """

            for job in jobs:
                
                job_object = job
                job = job.model_dump()
                job_detail = f"""
                
                Job title: {job.get("title", "")}
                company_name: {job.get("company_name", "")}
                description: {job.get("description", "")}
                responsibilities: {job.get("responsibilities", "")}
                requirments: {job.get("requirments", "")}
                location: {job.get("location", "")}
                salary: {job.get("salary", "")}
                starting_date : {job.get("starting_date", "")}
                closing_date: {job.get("closing_date", "")}
                """

                relevancy_response = await self.job_relevancy_agent.get_response(
                    candidate_profile=profile_detail, job_details=job_detail
                )

                logger.info("workflow - Relevancy response is fetched")

                relevance_score = relevancy_response.relevancy_score

                is_relevant = relevance_score >= JOB_RELEVANCY_THRESHOLD
                
                if not is_relevant:
                    continue

                per_job_relevancy_summary = {
                    "job_title": job.get("title", ""),
                    "company_name": job.get("company_name", ""),
                    "relevance_score": relevance_score,
                    "is_relevant": is_relevant,
                    "relevancy_details": relevancy_response,
                    "job": job_object
                }

                job_relevancy.append(per_job_relevancy_summary)
                logger.info(
                    f"workflow - relevancy results of {job.get('title', '')} is added"
                )

            logger.info("workflow - Final job relevancy results have fetched")

            return {"relevant_jobs_list": job_relevancy}

        except Exception:
            logger.exception("Unexpected error in relevancy node")
            raise
        

    async def decision_making_node(self, state: WorkflowState):

        try:
            
            relevant_jobs_list = state.get("relevant_jobs_list", [])
            current_job_index = state.get("current_job_index", 0)
            
            if current_job_index > len(relevant_jobs_list):
                
                return {
                    "current_job": None
                }
                
            current_job = relevant_jobs_list[current_job_index]
            
            return {
                "current_job": current_job,
                "user_decision": None
            }

        except Exception:
            logger.exception("Unexpected error in ats analyze node")
            raise

        
    async def user_decision(self, state: WorkflowState):
        
        try:
            
            user_decision = state.get("user_decision", "")
            
            if user_decision == "approve":
                return "cover_letter"
            
            elif user_decision == "reject":
                return "next_job"
            
            else:
                return "wait"
            
        except Exception:
            logger.exception("Unexpected error in user decision")
            raise
        
        
    async def next_job_node(self, state:WorkflowState):
        
        try:
            
            current_job_index = state.get("current_job_index", 0)
            current_job = state.get("current_job")
            
            if current_job is None:
                raise ValueError("No current job available to reject")

            
            rejected_jobs = state.get("rejected_jobs", [])
            rejected_job = current_job['job']             
        
            
            return {
                
                "rejected_jobs": [*rejected_jobs, rejected_job],
                "current_job_index": current_job_index + 1,
                "user_decision": None
            }
            
        except ValueError:
            logger.exception("Unexpected value error in next job node")
            raise
        
        except Exception:
            logger.exception("Unexpected error in next job node")
            raise
        
        
    async def cover_letter_node(self, state:WorkflowState):
        
        try:
            
            candidate_profile = state.get("profile_data", ResumeSchema())
            current_job = state.get("current_job",{})
            
            if not current_job:
                raise ValueError("Current job is missing")
            
            job_details = current_job['job'].model_dump()
            
            
            candidate_details = candidate_profile.model_dump()
            
            response = await self.cover_letter_agent.get_llm_response(
                candidate_profile=candidate_details,
                job_details=job_details
            )
            
        except Exception:
            logger.exception("Unexpected error in cover letter node")
            raise
    
