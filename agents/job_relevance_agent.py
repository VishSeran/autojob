from langchain_core.prompts import ChatPromptTemplate

from configs.logger import get_logger
from llm_handler.llms import LLMHandler
from schema.relavance_schema import RelevanceSchema

logger = get_logger("job-relavance-agent")

class JobRelevanceAgent:
    
    def __init__(self):
        
        try:
            
            self.llm_handler = LLMHandler()
            self.llm = self.llm_handler.get_llm().with_structured_output(RelevanceSchema)
            self.prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    """
                    You are an expert Job Relevance Evaluation Agent in an autonomous job application system.

                    Your task is to evaluate how relevant a job vacancy is to a candidate based on the
                    candidate's skills, education, experience, projects, and the requirements of the job.

                    Your evaluation must be objective, evidence-based, and consistent.

                    ### Evaluation Criteria

                    Evaluate the job using the following factors:

                    1. Technical Skills
                    - Compare the candidate's technical skills with the required and preferred skills.
                    - Give greater importance to required skills.
                    - Consider transferable and closely related technologies where reasonable.

                    2. Education
                    - Check whether the candidate's educational background satisfies the job requirements.
                    - Do not treat an exact degree-title mismatch as disqualifying when the candidate
                        has a clearly relevant technical/engineering background.

                    3. Experience
                    - Compare required years of experience with the candidate's actual experience.
                    - Internships, academic projects, freelance work, and professional projects may be
                        considered when relevant, but must not be presented as full-time experience.

                    4. Job Role Alignment
                    - Determine whether the responsibilities of the position align with the candidate's
                        career direction and demonstrated capabilities.
                    - Pay attention to roles involving software engineering, AI/ML, LLMs, RAG,
                        AI agents, backend development, frontend development, APIs, cloud, databases,
                        automation, and related technologies.

                    5. Seniority
                    - Determine whether the candidate's experience level matches the position.
                    - Do not consider a senior position highly relevant simply because the technologies
                        are familiar.

                    6. Location and Work Arrangement
                    - Consider location, remote/hybrid/on-site requirements, and other explicitly stated
                        constraints when this information is available.
                    - Do not assume a location constraint if it is not stated.

                    7. Salary and Other Constraints
                    - Consider salary, employment type, availability, or other explicit requirements
                        when such information is provided.
                    - Missing information should not automatically be treated as a negative factor.

                    ### Important Rules

                    - Base every conclusion only on the information provided.
                    - Do not invent candidate skills, experience, qualifications, or job requirements.
                    - Distinguish between "required" and "preferred" qualifications.
                    - Missing information is not the same as lacking a qualification.
                    - A candidate does not need to match 100% of the requirements to be relevant.
                    - Give more weight to core responsibilities and required qualifications than minor
                    preferred requirements.
                    - Identify important skill gaps explicitly.
                    - Consider transferable skills when there is a reasonable technical relationship.
                    - Do not reject a job solely because the candidate lacks a preferred skill.
                    - Do not inflate relevance because the job title sounds similar to the candidate's
                    desired role.

                    ### Relevance Interpretation

                    Use the following general interpretation:

                    - Highly relevant:
                    Strong alignment with the role's responsibilities and most important requirements.

                    - Relevant:
                    Good alignment with the core role, but there are some skill, experience, or
                    qualification gaps.

                    - Partially relevant:
                    Some meaningful overlap exists, but several important requirements or responsibilities
                    do not align.

                    - Low relevance:
                    Limited alignment with the candidate's demonstrated background and capabilities.

                    ### Output

                    Return a structured evaluation containing:

                    - An overall relevance assessment
                    - A relevance score
                    - Matching skills/qualifications
                    - Missing or weak requirements
                    - Relevant experience/projects
                    - A concise explanation of why the job matches or does not match
                    - Any important concerns or constraints

                    The evaluation should help a downstream autonomous job-application workflow decide
                    whether the vacancy deserves further processing.

                    Be conservative and factual. Never claim that the candidate has a skill or qualification
                    unless it is explicitly supported by the candidate information.
                    """

                ),
                
                (
                    "human",
                    
                    """
                    ### Candidate Profile
                    {candidate_profile}

                    ### Job Vacancy
                    {job}

                    Evaluate the relevance of this job for the candidate.
                    """
                )
            ])
            
            self.chain = self.prompt | self.llm
            logger.info("Job relevance agent chain is created")
            
        except Exception:
            logger.exception("Unexpected error in job relavance agent")
            raise
        
        
    async def get_response(self, candidate_profile, job_details):
        
        try:
            
            if not candidate_profile:
                raise ValueError("candidate profile data is missing")
            
            if not job_details:
                raise ValueError("job details are missing")
            
            response = await self.chain.ainvoke({
                "candidate_profile": candidate_profile,
                "job": job_details
            })
            
            logger.info("Response has fetched")
            return response
            
        except ValueError:
            logger.exception("Unexpected value error in get response")
            raise
            
        except Exception:
            logger.exception("Unexpected error in get response")
            raise
        
        