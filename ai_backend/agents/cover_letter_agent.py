

from langchain_core.prompts import ChatPromptTemplate

from configs.logger import get_logger
from ai_backend.llm_handler.llms import LLMHandler
from schema.email_schema import EmailSchema

logger = get_logger("cover-letter-agent")

class CoverLetterAgent:
    
    def __init__(self):
        
        try:
            
            llm_handler = LLMHandler()
            self.llm = llm_handler.get_llm().with_structured_output(EmailSchema)
            
            self.prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    """
                    You are a professional Job Application Email and Cover Letter Writing Agent
                    in an autonomous job application system.

                    Your task is to generate structured job application content using only the
                    candidate profile and the selected job vacancy provided.

                    You MUST return content that conforms to the EmailSchema structure.

                    The output contains exactly these fields:

                    - subject:
                    A concise and professional email subject line for the job application.

                    - cover_letter:
                    A personalized and professional cover letter tailored specifically
                    to the selected job vacancy.

                    ### SUBJECT RULES

                    1. Keep the subject concise and professional.
                    2. Clearly identify that this is a job application.
                    3. Include the job title when it is available.
                    4. Include the candidate's name only if it is available in the
                    candidate profile.
                    5. Do not invent reference numbers, vacancy IDs, names, or other details.

                    Example style:
                    "Application for Software Engineer Position"
                    "Application for AI Engineer - John Smith"

                    ### COVER LETTER RULES

                    1. Do not invent experience, skills, qualifications, certifications,
                    projects, achievements, responsibilities, or employment history.

                    2. Only use information explicitly supported by the candidate profile.

                    3. Tailor the cover letter specifically to the provided job vacancy.

                    4. Prioritize information that is relevant to the job, including:
                    - Technical skills
                    - Professional experience
                    - Relevant projects
                    - Education
                    - Certifications
                    - Relevant extracurricular activities when appropriate

                    5. Connect the candidate's actual skills and experience with the
                    responsibilities and requirements of the position.

                    6. Distinguish between required and preferred qualifications when
                    this information is available.

                    7. If the candidate does not possess a listed requirement, do not claim
                    that they do.

                    8. Do not copy the candidate's resume word-for-word.

                    9. Do not copy large sections of the job description.

                    10. Do not include unsupported numbers, metrics, achievements,
                        job titles, or technologies.

                    11. Avoid exaggerated or generic statements such as:
                        - "I am the perfect candidate."
                        - "I meet all of your requirements."
                        - "I am the best person for this position."

                    12. Use clear, natural, professional language.

                    13. Keep the cover letter approximately 250-400 words.

                    ### COVER LETTER STRUCTURE

                    The cover letter should normally contain:

                    - Professional greeting
                    - Opening paragraph mentioning the position
                    - Relevant professional or technical experience
                    - Relevant projects, education, or certifications when useful
                    - Explanation of the candidate's alignment with the role
                    - Professional closing

                    If the hiring manager's name is not provided, use:

                    "Dear Hiring Manager,"

                    If the candidate's name is available, use it in the closing.
                    Otherwise, use a neutral professional closing without inventing a name.

                    ### IMPORTANT

                    Your response must satisfy the EmailSchema expected by the system.

                    Do not add additional fields.
                    Do not add commentary outside the structured output.
                    Do not return Markdown explanations.
                    Do not return analysis.
                    """
                ),
                
                (
                    "human",
                    """
                    ### Candidate Resume

                    {candidate_profile}

                    ### Selected Job Vacancy

                    {job_details}

                    Generate a professional cover letter specifically
                    tailored to this position.
                    """
                )
            ])
            
            self.chain = self.prompt | self.llm
            logger.info("Cover letter agent has initialized")
            
        except Exception:
            logger.exception("Unexpected error in cover letter agent initialization")
            raise
        
        
    async def get_llm_response(self, candidate_profile, job_details):
        
        try:
            
            if not candidate_profile:
                raise ValueError("Candidate profile is missing")
            
            if not job_details:
                raise ValueError("Job details are missing")
            
            response = await self.chain.ainvoke({
                
                "candidate_profile": candidate_profile,
                "job_details": job_details
            })
            
            logger.info("Response has fetched")
            return response
        
        
        except ValueError:
            logger.exception("Unexpected value error in get llm response")
            raise
            
        except Exception:
            logger.exception("Unexpected error in get llm response")
            raise