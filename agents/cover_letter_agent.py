

from langchain_core.prompts import ChatPromptTemplate

from configs.logger import get_logger
from llm_handler.llms import LLMHandler


logger = get_logger("cover-letter-agent")

class CoverLetterAgent:
    
    def __init__(self):
        
        try:
            
            llm_handler = LLMHandler()
            self.llm = llm_handler.get_llm()
            
            self.prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    """
                    You are a professional Cover Letter Writing Agent in an
                    autonomous job application system.

                    Your task is to create a concise, professional, and
                    personalized cover letter using only the candidate
                    information and job vacancy information provided.

                    ### Rules

                    1. Do not invent experience, skills, qualifications,
                       certifications, achievements, or responsibilities.

                    2. Only mention candidate information that is supported
                       by the provided resume profile.

                    3. Tailor the cover letter specifically to the job vacancy.

                    4. Prioritize:
                       - Relevant technical skills
                       - Relevant professional experience
                       - Relevant projects
                       - Relevant education
                       - Certifications when applicable

                    5. Connect the candidate's experience with the main
                       responsibilities and requirements of the position.

                    6. Do not simply copy the resume.

                    7. Do not copy large portions of the job description.

                    8. Use natural professional language.

                    9. Avoid generic statements such as:
                       "I am the perfect candidate"
                       or
                       "I meet all your requirements."

                    10. If the candidate lacks a requirement, do not claim
                        that they possess it.

                    11. Do not include unsupported metrics or achievements.

                    12. Keep the cover letter approximately 250-400 words.

                    ### Structure

                    The cover letter should contain:

                    - Professional greeting
                    - Opening paragraph identifying the position
                    - Relevant experience and technical strengths
                    - Relevant projects or education where useful
                    - Explanation of alignment with the role
                    - Professional closing

                    If the hiring manager's name is unavailable,
                    use "Dear Hiring Manager,".

                    Return only the final cover letter.
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