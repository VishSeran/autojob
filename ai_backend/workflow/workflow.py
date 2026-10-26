import asyncio
import uuid

from langchain_core.documents import Document
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from sqlalchemy.orm import Session

from ai_backend.agents.cover_letter_agent import CoverLetterAgent
from ai_backend.agents.image_data_extractor_agent import ImageDataExtractorAgent
from ai_backend.agents.job_relevance_agent import JobRelevanceAgent
from ai_backend.agents.profile_extractor_agent import ProfileExtractorAgent
from ai_backend.agents.query_extractor_agent import QueryHandlerAgent
from ai_backend.client_server_sources.topjob_client_server import (
    TopJobClientServerSource,
)
from ai_backend.documents_handler.resume_handler import ResumeDocumentHandler
from ai_backend.mcp_client.client import MCPClient
from ai_backend.workflow.workflow_state import WorkflowState
from configs.configurations import (
    BUCKET_NAME,
    JOB_RELEVANCY_THRESHOLD,
    TOPJOB_SERVER_URL,
)
from configs.logger import get_logger
from schema.job_image_schema import JobDetails
from schema.job_schema import Job
from schema.query_schema import QuerySchema
from schema.resume_schema import ResumeSchema
from services.gmail_service import GmailService
from services.user_service import UserService

logger = get_logger("agent-workflow")



class AgentWorkflow:
    def __init__(self, db:Session, user_id:uuid.UUID, thread_id:str, checkpointer):  

        try:
            self.workflow = None
            self.topjob_mcp_client = MCPClient(TOPJOB_SERVER_URL)
            self.topjob_client_server_Source = None
            self.query_handler_agent = QueryHandlerAgent()
            self.image_handler_agent = ImageDataExtractorAgent()
            self.profile_extractor_agent = ProfileExtractorAgent()
            self.resume_handler = ResumeDocumentHandler(db)
            self.job_relevancy_agent = JobRelevanceAgent()
            self.cover_letter_agent = CoverLetterAgent()
            self.gmail_service = GmailService(db)
            self.user_service = UserService(db)
            self.user_id = user_id
            self.thread_id = str(thread_id)
            self.checkpointer = checkpointer
            
            logger.info("workflow - Agents are initialized")


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
            graph.add_node("profile_extractor_node", self.profile_extractor_node)
            graph.add_node("query_handler_node", self.query_handler_node)
            graph.add_node("topjob_search_node", self.topjob_search_node)
            graph.add_node("image_data_handler_node", self.image_data_handler_node)
            graph.add_node("get_full_job_summary_node", self.get_full_job_summary_node)
            graph.add_node("relevancy_node", self.relevancy_node)
            graph.add_node("job_selection_node", self.job_selection_node)
            graph.add_node("next_job_node", self.next_job_node)
            graph.add_node("cover_letter_node", self.cover_letter_node)
            graph.add_node("email_review_node", self.final_review_node)
            graph.add_node("cancel_application_node", self.cancel_application_node)
            graph.add_node("send_mail_node", self.send_mail_node)
            
            graph.add_edge(START, "profile_extractor_node")
            #graph.add_edge(START,"query_handler_node")
            graph.add_edge("profile_extractor_node", "query_handler_node")
            
            graph.add_edge("query_handler_node", "topjob_search_node")
            
            graph.add_edge("topjob_search_node", "image_data_handler_node")
            
            graph.add_edge("image_data_handler_node", "get_full_job_summary_node")
            
            graph.add_edge("get_full_job_summary_node", "relevancy_node")
            
            graph.add_edge("relevancy_node", "job_selection_node")
            
            graph.add_conditional_edges("job_selection_node",
                                        self.job_selection_route,{
                                            "cover_letter": "cover_letter_node",
                                            "next_job": "next_job_node",
                                            "end": END
                                        })
            
            graph.add_edge("next_job_node", "job_selection_node")
            graph.add_edge("cover_letter_node", "email_review_node")
            
            graph.add_conditional_edges(
                "email_review_node",
                self.final_review_route,
                {
                    "cancel": "cancel_application_node",
                    "send_email": "send_mail_node"
                }
            )
            
            graph.add_edge("cancel_application_node", "next_job_node")
            
            graph.add_conditional_edges(
                "send_mail_node",
                self.send_mail_route,
                {
                    "end": END,
                    "job_selection": "job_selection_node" 
                }
            )

            self.workflow = graph.compile(
                checkpointer=self.checkpointer
            )
            
            logger.info(
                "Workflow graph compiled successfully"
            )
            logger.info("Workflow build is completed")
            
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
            logger.info(f"response= \nkeyword: {response.keyword}\nlocation:{response.location}\ncategory:{response.category}\nno of jobs: {response.number_of_jobs}")

            return {
                "keyword": response.keyword,
                "location": response.location,
                "job_field": response.category,
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
                
            logger.info("Job list if fetched")

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

    def get_full_job_summary_node(self, state: WorkflowState):

        try:
            source = state.get("source", "")
            complete_job_details = []

            if source == "topjob":
                job_list = state.get("topjob_summary") or []
                topjob_image_details = state.get("topjob_images_details", {})
                topjob_image_urls = state.get("topjob_images_urls", {})

                for job in job_list:
                    job = job.model_dump()
                    job_title = job.get("job_title")

                    image_data:dict = topjob_image_details.get(job_title)

                    if not image_data:
                        logger.warning(f"No image details found for job: {job_title}")
                        continue

                    job_summary = Job(
                        source= source,
                        job_url= topjob_image_urls[job_title],
                        title =  image_data["job_titile"] or job_title,
                        company_name= job.get("company_name",""),
                        company_email= image_data.get("company_email"),
                        company_contact= image_data.get("company_contact"),
                        description= image_data.get("description"),
                        responsibilities= image_data.get("responsibilities"),
                        requirments= image_data.get("requirments"),
                        location= job.get("location", ""),
                        salary= image_data.get("salary"),
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
            
            resume_data = state.get("current_resume")
            user_id = state.get("user_id")

            if not resume_data:
                
                user = state.get("user")
                resume_path = state.get("current_resume_id")

                if not user:
                    
                    raise ValueError(
                        "User is missing from workflow state"
                    )
                
                if not resume_path:
                                    
                    raise ValueError(
                        "Resume path is missing from workflow state"
                    )

                user_data = self.user_service.get_user_by_id(self.user_id)
                resume_data = self.resume_handler.load_from_storage(
                    user_data.id,
                    resume_path
                )

            if not resume_data:
                raise ValueError("Resume data could not be loaded")

            logger.info(
                "Resume data type: %s",
                type(resume_data).__name__
            )

            logger.info(
                "First item type: %s",
                type(resume_data[0]).__name__
            )

            logger.info("Number of pages: %s", len(resume_data))
            
            resume_text = "\n".join(
                doc.page_content for doc in resume_data
            )
            logger.info(f"resume data: {resume_text}")

            response = await self.profile_extractor_agent.get_response(
                resume_text
            )
            
            logger.info(f"response: {response}")

            return {
                "current_resume": resume_data,
                "profile_data": response
            }

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
        

    def job_selection_node(self, state: WorkflowState):

        try:
            
            relevant_jobs_list = state.get("relevant_jobs_list", [])
            current_job_index = state.get("current_job_index", 0)
            
            if current_job_index >= len(relevant_jobs_list):
                logger.info(
                    "No more relevant jobs available"
                )

                return {
                    "current_job": None
                }
                
            current_job = relevant_jobs_list[current_job_index]
            
            decision = interrupt({
                
                "type": "job_review",
                "job": current_job,
                "message": "review the job for approve or reject"
                
            })
            
            return {
                
                "current_job": current_job,
                "user_decision": decision
            }

        except Exception:
            logger.exception("Unexpected error in ats analyze node")
            raise

        
    def job_selection_route(self, state: WorkflowState):
        
        try:
            
            user_decision = state.get("user_decision", {})
            relevant_jobs = state['relevant_jobs_list']
            current_job_index = state['current_job_index']
            
            
            if current_job_index >= len(relevant_jobs):
                logger.info("No further jobs to proceed")
                return "end" 
            
            if not user_decision:
                raise ValueError("User decision is missing")
            
            decision = user_decision.get('decision')
            
            if decision == "approve":
                return "cover_letter"
            
            if decision == "reject":
                return "next_job"
            
            raise ValueError(f"Unsupported decision: {decision}")
        
        except Exception:
            logger.exception("Unexpected error in user decision")
            raise
        
        
    def next_job_node(self, state:WorkflowState):
        
        try:
            
            current_job_index = state.get("current_job_index", 0)
            current_job = state.get("current_job")
            
            if current_job is None:
                raise ValueError("No current job available to reject")

            
            rejected_jobs = state.get("rejected_jobs", [])
            rejected_job = current_job['job']             

            if rejected_job is not None:

                rejected_jobs = [
                    *rejected_jobs,
                    rejected_job
                ]
            
            return {
                
                "rejected_jobs": rejected_jobs,
                "current_job_index": current_job_index + 1,
                "user_decision": None,
                "current_job":None,
                "email_details":None,
                "email_review_response":None,
                "final_response": None
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
            
            if not job_details:
                raise ValueError("Job details are missing from current job")
            
            company_email = job_details.get("company_email")
            
            if not company_email:
                raise ValueError("Company email is missing from job details")
            
            response = await self.cover_letter_agent.get_llm_response(
                candidate_profile=candidate_details,
                job_details=job_details
            )
            
            results = response.model_dump()
            logger.info("workflow - cover letter generated successfully")
 
            email_details = {
                
                "company_email": company_email,
                "subject": results['subject'],
                "cover_letter": results['cover_letter']
            }
            
            return {
                "email_details": email_details
            }
        
        except ValueError:
            logger.exception("Invalid data in cover letter node")
            raise
        
        except Exception:
            logger.exception("Unexpected error in cover letter node")
            raise
        
        
    def final_review_node(self, state: WorkflowState):
        
        try:
            
            email_data = state.get("email_details",{})
            
            
            if not email_data:
                raise ValueError("Application email is missing")
            
            decision = interrupt({
                
                "type":"email_review",
                "email": email_data,
                "message": "Review, edit, and approve this email."
            })
            
            #{
            #     "decision": "send",
            #     "company_email": "abccompany@gmail.com"
            #     "subject": "Application for AI Engineer",
            #     "cover_letter": "Edited cover letter..."
            #}
            
            return {

                "email_review_response": decision,
                
            }
            
        except Exception:
            logger.exception("Unexpected error in final review decision node")
            raise
        
        
    def final_review_route(self, state:WorkflowState):
        
        try: 
            
            email_review_response = state.get("email_review_response",{} )
            
            decision = email_review_response.get("decision")
            
            if not decision:
                raise ValueError("email review response is missing")
            
            if decision == "cancel":
                return "cancel"
            
            if decision == "send":
                return "send_email" 
            
            raise ValueError(f"Unsupported decision: {decision}")
        
        except ValueError:
            logger.exception("Unexpected value error in final review node")
            raise  
         
        except Exception:
            logger.exception("Unexpected error in final review node")
            raise   
        
        
    async def send_mail_node(self, state: WorkflowState):

        try:
            email_data = state.get("email_details")
            current_job_index = state['current_job_index']
            
            if not email_data:
                raise ValueError("Email data is missing")

            send_mail = await self.gmail_service.send_email(
                self.user_id,
                email_data.get("company_email"),
                email_data.get("subject"),
                email_data.get("cover_letter")
            )

            logger.info(f"Email sent successfully: {send_mail.id}")

            return {
                
                "email_sent": True,
                "final_response": f"Email sent successfully: {send_mail.id}",
                "current_job_index": current_job_index + 1,
                "current_job":
                    None,

                "email_details":
                    None,

                "email_review_response":
                    None,

                "user_decision":
                    None,
            }

        
        except Exception:
            logger.exception("Unexpected error in send mail node")

            return {
                "final_response": "Email sending failed. Please try again."
            }
        
        
    def cancel_application_node(
        self,
        state: WorkflowState
    ):

        try:

            logger.info(
                "User cancelled current application"
            )

            return {
                "final_response":
                    "Application cancelled by user.",

                "current_job_index":
                    state.get(
                        "current_job_index",
                        0
                    ) + 1,

                "current_job":
                    None,

                "email_details":
                    None,

                "email_review_response":
                    None,

                "email_sent":
                    False,
            }

        except Exception:
            logger.exception(
                "Unexpected error in cancel application node"
            )
            raise
        
        
    def send_mail_route(self, state:WorkflowState):
        
        try:
            email_sent = state.get("email_sent", False)
            
            if not email_sent:
                logger.warning(
                    "Email was not sent. "
                    "Returning to current job selection."
                )
                
                return "job_selection"
            
            relevant_jobs_list = state.get(
                "relevant_jobs_list",
                []
            )

            current_job_index = state.get(
                "current_job_index",
                0
            )

            if current_job_index >= len(
                relevant_jobs_list
            ):

                logger.info(
                    "All relevant jobs have been processed"
                )

                return "end"
            
            return "job_selection"

        except Exception:
            logger.exception(
                "Unexpected error in send mail route"
            )
            raise
    
    @property
    def config(self):
        
        return {
            "configurable": {
                "thread_id": str(self.thread_id)
            }
        }
    
    async def get_response(self, initial_state):
        
        try:
            
            if self.workflow is None:
                raise RuntimeError(
                    "Workflow is not initialized"
                )
            
            if self.topjob_client_server_Source is None:
                raise RuntimeError(
                    "Workflow dependencies are not initialized"
                )
            
            response = await self.workflow.ainvoke(
                input=initial_state,
                config=self.config,
                durability="sync"
            )
            logger.info(
            "Workflow execution completed or interrupted"
            )
            return response
        
        except Exception:
            logger.exception(
                "Unexpected error in  executing workflow"
            )
            raise
        
    async def get_response_from_existing_workflow(self):
            
            try:
                
                if self.workflow is None:
                    raise RuntimeError(
                        "Workflow is not initialized"
                    )
                
                if self.topjob_client_server_Source is None:
                    raise RuntimeError(
                        "Workflow dependencies are not initialized"
                    )
                    
                saved_state = await self.get_latest_save_state()
                logger.info(f"Saved state data: {saved_state}")
                
                response = await self.workflow.ainvoke(
                    input=None,
                    config=self.config
                )
                
                logger.info(
                "Workflow execution completed or interrupted"
                )
            
                return response
            
            except Exception:
                logger.exception(
                    "Unexpected error in  executing workflow"
                )
                raise
            
            
    async def get_latest_save_state(self):

        try:
            config = self.config

            checkpoint = await self.checkpointer.aget_tuple(config)

            if checkpoint is None:
                logger.warning(
                    "No PostgreSQL checkpoint found for thread: %s",
                    self.thread_id
                )

                return None

            snapshot = await self.workflow.aget_state(config)

            logger.info(
                "Checkpoint found: %s",
                checkpoint.config
            )

            logger.info("Saved state: %s", snapshot.values)
            logger.info("Next nodes: %s", snapshot.next)
            logger.info("Tasks: %s", snapshot.tasks)

            return snapshot

        except Exception:
            logger.exception("Failed to retrieve workflow checkpoint")
            raise
            
        
    async def resume(
        self,
        resume_data:dict
    ):
        
        
        try:
            
            if self.workflow is None:
                raise RuntimeError(
                    "Workflow is not initialized"
                )
                
            response = await self.workflow.ainvoke(
                Command(
                    resume=resume_data
                ),
                config=self.config
            )
            
            logger.info(
                "Workflow resumed successfully"
            )

            return response
 
        except Exception:
            logger.exception(
            "Unexpected error while resuming workflow"
            )

            raise