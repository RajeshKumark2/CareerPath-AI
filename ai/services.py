import openai
from django.conf import settings
from django.core.cache import cache
import json

openai.api_key = settings.OPENAI_API_KEY

class CareerAIAssistant:
    """
    AI-powered career assistant using OpenAI
    """
    
    @staticmethod
    def get_job_insights(job_name):
        """
        Get AI-generated insights about a job role
        """
        cache_key = f"job_insights_{job_name}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a career guidance expert. Provide detailed, accurate information about job roles."
                    },
                    {
                        "role": "user",
                        "content": f"Provide a comprehensive overview of the {job_name} role including responsibilities, required skills, and career prospects."
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response['choices'][0]['message']['content']
            cache.set(cache_key, content, 86400)  # Cache for 24 hours
            return content
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    def analyze_skill_gap(user_skills, required_skills):
        """
        Analyze skill gap and suggest learning path
        """
        try:
            prompt = f"""Analyze the skill gap for someone with these skills: {', '.join(user_skills)}
            They need to develop: {', '.join(required_skills)}
            Provide a prioritized learning plan."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a career development advisor."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    def generate_interview_tips(job_name, question=None):
        """
        Generate interview preparation tips
        """
        try:
            if question:
                prompt = f"Provide tips to answer this interview question for {job_name}: {question}"
            else:
                prompt = f"Provide general interview preparation tips for {job_name} role"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an interview coach."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    def review_resume(resume_text):
        """
        AI-powered resume review
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an ATS expert and resume coach. Review resumes for ATS compatibility and content quality."
                    },
                    {
                        "role": "user",
                        "content": f"Review this resume and provide specific improvements:\n\n{resume_text}"
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"


