import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Union
import openai

import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")



class LLMAnalyzer:
    """
    A utility class for analyzing raw text (like transcripts) using OpenAI's LLM
    to extract structured insights that can be used as sample data for embeddings.
    """
    
    def __init__(self, 
                 openai_api_key: Optional[str] = openai_api_key,
                 model: str = "gpt-4o-mini",
                 max_tokens: int = 1000,
                 temperature: float = 0.3):
        """
        Initialize the LLMAnalyzer class.
        
        Args:
            openai_api_key: OpenAI API key (defaults to environment variable)
            model: OpenAI model to use for analysis
            max_tokens: Maximum tokens for response
            temperature: Temperature for response generation (0.0-1.0)
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # Initialize OpenAI client
        if self.openai_api_key:
            self.client = openai.OpenAI(api_key=self.openai_api_key)
        else:
            logger.warning("OpenAI API key not found. LLM analysis functionality will be limited.")
            self.client = None
    
    def extract_insights(self, text: str, 
                        insight_types: List[str] = None,
                        max_insights: int = 10) -> List[Dict[str, Any]]:
        """
        Extract structured insights from raw text using LLM analysis.
        
        Args:
            text: Raw text to analyze (e.g., transcript)
            insight_types: Types of insights to extract (defaults to common types)
            max_insights: Maximum number of insights to generate
            
        Returns:
            List of insight dictionaries with id, text, category, and metadata
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized. Please provide a valid API key.")
        
        if insight_types is None:
            insight_types = [
                "key_concepts", "main_points", "action_items", 
                "quotes", "questions_raised", "conclusions"
            ]
        
        prompt = self._create_analysis_prompt(text, insight_types, max_insights)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert text analyst. Extract structured insights from the given text and return them as a JSON array."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            insights_text = response.choices[0].message.content
            insights = self._parse_insights(insights_text)
            
            logger.info(f"Extracted {len(insights)} insights from text")
            return insights
            
        except Exception as e:
            logger.error(f"Failed to extract insights: {e}")
            raise
    
    def _create_analysis_prompt(self, text: str, insight_types: List[str], max_insights: int) -> str:
        """Create a structured prompt for LLM analysis."""
        return f"""
                    Analyze the following text and extract {max_insights} key insights. Focus on these types: {', '.join(insight_types)}.

                    Text to analyze:
                    {text[:4000]}  # Limit text length to avoid token limits

                    Return the insights as a JSON array with this structure:
                    [
                        {{
                            "id": "insight_1",
                            "text": "The actual insight text",
                            "category": "one of the insight types",
                            "relevance_score": 0.8,
                            "metadata": {{
                                "context": "brief context",
                                "timestamp": "if applicable"
                            }}
                        }}
                    ]

                    Ensure each insight is:
                    - Self-contained and meaningful
                    - 1-2 sentences long
                    - Relevant to the original text
                    - Categorized appropriately
                    - Has a relevance score (0.0-1.0)
                    """
    
    def _parse_insights(self, insights_text: str) -> List[Dict[str, Any]]:
        """Parse the LLM response into structured insights."""
        import json
        import re
        
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\[.*\]', insights_text, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group())
                return insights
        except json.JSONDecodeError:
            pass
        
        # Fallback: parse as text if JSON parsing fails
        logger.warning("Failed to parse JSON response, using text parsing fallback")
        return self._parse_text_insights(insights_text)
    
    def _parse_text_insights(self, insights_text: str) -> List[Dict[str, Any]]:
        """Fallback method to parse insights from text format."""
        insights = []
        lines = insights_text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 10:
                insights.append({
                    "id": f"insight_{i+1}",
                    "text": line,
                    "category": "general",
                    "relevance_score": 0.7,
                    "metadata": {"source": "text_parsing"}
                })
        
        return insights
    
    def create_sample_data(self, text: str, 
                          namespace: str = "transcript_insights",
                          insight_types: List[str] = None) -> List[Dict[str, Any]]:
        """
        Create sample data for embeddings from text analysis.
        
        Args:
            text: Raw text to analyze
            namespace: Namespace for the insights
            insight_types: Types of insights to extract
            
        Returns:
            List of dictionaries ready for embedding processing
        """
        insights = self.extract_insights(text, insight_types)
        
        sample_data = []
        for i, insight in enumerate(insights):
            sample_data.append({
                "id": f"{namespace}_{i+1}",
                "text": insight["text"],
                "category": insight["category"],
                "relevance_score": insight["relevance_score"],
                "source": "llm_analysis",
                "namespace": namespace,
                "metadata": insight.get("metadata", {})
            })
        
        return sample_data
    
    def analyze_transcript(self, transcript: str, 
                          video_id: str = None,
                          speaker: str = None) -> Dict[str, Any]:
        """
        Comprehensive analysis of a transcript with multiple insight types.
        
        Args:
            transcript: The transcript text
            video_id: Optional video identifier
            speaker: Optional speaker name
            
        Returns:
            Dictionary containing various types of analysis
        """
        analysis = {
            "video_id": video_id,
            "speaker": speaker,
            "insights": self.extract_insights(transcript),
            "summary": self._generate_summary(transcript),
            "key_topics": self._extract_topics(transcript),
            "sample_data": self.create_sample_data(transcript)
        }
        
        return analysis
    
    def _generate_summary(self, text: str) -> str:
        """Generate a summary of the text."""
        if not self.client:
            return "Summary not available - OpenAI client not initialized"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Create a concise 2-3 sentence summary of the following text."},
                    {"role": "user", "content": f"Summarize: {text[:2000]}"}
                ],
                max_tokens=200,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            return "Summary generation failed"
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract main topics from the text."""
        if not self.client:
            return []
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Extract 5-7 main topics from the text. Return as a comma-separated list."},
                    {"role": "user", "content": f"Extract topics from: {text[:2000]}"}
                ],
                max_tokens=150,
                temperature=0.2
            )
            topics_text = response.choices[0].message.content
            return [topic.strip() for topic in topics_text.split(',')]
        except Exception as e:
            logger.error(f"Failed to extract topics: {e}")
            return []


    def chat_assist(self, 
                   user_message: str,
                   entity_type: str,
                   field_name: str = None,
                   form_data: Dict[str, Any] = None,
                   conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Chat-based assistance for filling entity form fields.
        
        Args:
            user_message: The user's message/question
            entity_type: Type of entity (Component, Theme, Technique, etc.)
            field_name: The specific field being filled (optional)
            form_data: Current form data for context (optional)
            conversation_history: Previous messages in the conversation (optional)
            
        Returns:
            Dictionary with AI response and metadata
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized. Please provide a valid API key.")
        
        if conversation_history is None:
            conversation_history = []
        
        # Build context-aware system prompt
        system_prompt = self._create_chat_system_prompt(entity_type, field_name, form_data)
        
        # Build message history
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            ai_response = response.choices[0].message.content
            
            logger.info(f"Chat assist response generated for {entity_type}.{field_name}")
            
            return {
                "response": ai_response,
                "field_name": field_name,
                "entity_type": entity_type,
                "can_apply_to_field": field_name is not None,
                "token_usage": {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to generate chat response: {e}")
            raise
    
    def _create_chat_system_prompt(self, entity_type: str, field_name: str = None, form_data: Dict[str, Any] = None) -> str:
        """Create a context-aware system prompt for chat assistance."""
        
        # Entity-specific context
        entity_contexts = {
            "Component": "video editing components (effects, transitions, presets)",
            "Concept": "core concepts in video editing and production",
            "Reference": "reference materials and resources",
            "Technique": "video editing techniques and workflows",
            "Theme": "thematic elements in video production",
            "Tool": "software tools and applications for video editing",
            "Composition": "complete video compositions and projects"
        }
        
        entity_context = entity_contexts.get(entity_type, "entity")
        
        # Field-specific guidance
        field_guidance = ""
        if field_name:
            field_guidance = f"\n\nThe user is currently working on the '{field_name}' field. "
            if field_name == "description":
                field_guidance += "Provide a clear, detailed description that explains what this is and its purpose."
            elif field_name == "instructions":
                field_guidance += "Provide step-by-step instructions that are clear and actionable."
            elif field_name == "outcome":
                field_guidance += "Describe the expected result or outcome of using this technique."
            elif field_name == "name":
                field_guidance += "Suggest a concise, descriptive name."
        
        # Form data context
        form_context = ""
        if form_data and len(form_data) > 0:
            filled_fields = {k: v for k, v in form_data.items() if v and v != "" and v != 0 and v != []}
            if filled_fields:
                form_context = f"\n\nCurrent form data:\n"
                for key, value in filled_fields.items():
                    if isinstance(value, list):
                        form_context += f"- {key}: {', '.join(map(str, value))}\n"
                    else:
                        form_context += f"- {key}: {value}\n"
        
        prompt = f"""
                    You are an AI assistant helping users create {entity_context} in a video editing knowledge management system.
                    Your role is to:
                    1. Help users articulate and refine their ideas through conversation
                    2. Generate clear, professional content for form fields
                    3. Provide suggestions based on the entity type and context
                    4. Be concise but informative
                    5. Use video editing terminology appropriately

                    When the user likes your response, they can send it directly to the form field.{field_guidance}{form_context}

                    Provide helpful, context-aware responses that are ready to use in the form.
                """
                
        return prompt


def llm_analysis_example():
    """Example of how to use the LLMAnalyzer class."""
    
    # Initialize the analyzer
    analyzer = LLMAnalyzer()
    
    # Example transcript
    sample_transcript = """
    Welcome to today's discussion about artificial intelligence and machine learning. 
    We'll be covering the basics of neural networks, how they work, and their applications 
    in real-world scenarios. The key thing to understand is that AI is not just about 
    replacing human jobs, but augmenting human capabilities. We should focus on ethical 
    considerations and responsible development of these technologies.
    """
    
    # Extract insights
    insights = analyzer.extract_insights(sample_transcript)
    print("Extracted insights:")
    for insight in insights:
        print(f"- {insight['text']} (Category: {insight['category']})")
    
    # Create sample data for embeddings
    sample_data = analyzer.create_sample_data(sample_transcript, namespace="ai_discussion")
    print(f"\nCreated {len(sample_data)} sample data entries for embeddings")
    
    # Comprehensive analysis
    analysis = analyzer.analyze_transcript(sample_transcript, video_id="ai_101", speaker="Expert")
    print(f"\nAnalysis complete:")
    print(f"Summary: {analysis['summary']}")
    print(f"Topics: {', '.join(analysis['key_topics'])}")