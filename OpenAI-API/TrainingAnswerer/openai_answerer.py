from openai import OpenAI


class OpenAIAnswerer:
    """
    Class to interact with OpenAI API for answering questions based on 
    transcript context and screen content
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the OpenAI Answerer.
        
        Args:
            api_key: OpenAI API key for authentication
        """
        # Set up OpenAI client
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"
        self.transcript_context = None
    
    def load_transcript(self, filepath):
        """
        Load transcript from a text file to use as context
        
        Args:
            filepath: Path to the transcript text file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.transcript_context = f.read()
            print(f"Transcript loaded successfully from {filepath}")
            print(f"Transcript length: {len(self.transcript_context)} characters")
            return True
        except Exception as e:
            print(f"Error loading transcript: {e}")
            return False
    
    def extract_question_from_image(self, image_base64):
        """
        Use OpenAI Vision API to extract the question from a screenshot
        
        Args:
            image_base64: Base64 encoded image string
            
        Returns:
            str: Extracted question text
        """
        try:
            print("Sending image to OpenAI Vision API...")
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Using the latest model with vision capabilities
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please read and transcribe any text, questions, or prompts visible in this image. Extract all readable text content."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_base64,
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            question = response.choices[0].message.content
            
            # Check if the response is a refusal
            if "sorry" in question.lower() and "can't" in question.lower():
                print("\n⚠️  WARNING: OpenAI refused to process the image.")
                print("This could be due to:")
                print("  - Content policy violation")
                print("  - Personal/sensitive information in the screenshot")
                print("  - Poor image quality or unreadable text")
                print("\nTry:")
                print("  - Capturing a cleaner/smaller region")
                print("  - Removing any sensitive information from view")
                print("  - Using Option 4 to type the question manually\n")
            
            return question
        except Exception as e:
            print(f"\n❌ Error extracting question from image: {e}")
            print(f"Error type: {type(e).__name__}")
            return None
    
    def answer_question(self, question, use_transcript=True, return_option_only=False):
        """
        Answer a question using OpenAI, optionally with transcript context
        
        Args:
            question: The question to answer
            use_transcript: Whether to use loaded transcript as context
            return_option_only: If True, returns ONLY the correct option text (for auto-click)
            
        Returns:
            str: Answer to the question (or just the option text if return_option_only=True)
        """
        try:
            messages = []
            
            # Add system message with transcript context if available
            if use_transcript and self.transcript_context:
                if return_option_only:
                    messages.append({
                        "role": "system",
                        "content": f"You are a helpful assistant answering multiple choice questions based on this transcript:\n\n{self.transcript_context}\n\nCRITICAL: Return ONLY the core text of the correct answer option - just the essential keywords that identify it. Remove any prefixes like 'a)', 'A.', numbers, or extra punctuation. Return 1-5 words maximum that uniquely identify the correct answer.\n\nExample: If the option is 'A) Machine Learning algorithms', return 'Machine Learning'"
                    })
                else:
                    messages.append({
                        "role": "system",
                        "content": f"You are a helpful assistant answering questions based on the following transcript/context:\n\n{self.transcript_context}\n\nPlease answer questions based primarily on this context. If the context doesn't contain the answer, you may use your general knowledge but indicate that the information is not in the provided transcript."
                    })
            else:
                if return_option_only:
                    messages.append({
                        "role": "system",
                        "content": "You are answering multiple choice questions. Return ONLY the core text of the correct answer option - just the essential keywords. Remove any prefixes like 'a)', 'A.', numbers, or extra punctuation. Return 1-5 words maximum.\n\nExample: If the option is 'A) Machine Learning algorithms', return 'Machine Learning'"
                    })
            
            # Add the question with specific instructions for option-only mode
            if return_option_only:
                messages.append({
                    "role": "user",
                    "content": f"{question}\n\nReturn ONLY the core keywords from the correct option (1-5 words max). Remove prefixes, numbers, and punctuation. Just the essential identifying text that appears on screen."
                })
            else:
                messages.append({
                    "role": "user",
                    "content": question
                })
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=50 if return_option_only else 1000,  # Shorter for option-only
                temperature=0.3 if return_option_only else 0.7  # More deterministic for options
            )
            
            answer = response.choices[0].message.content
            return answer
        except Exception as e:
            print(f"Error answering question: {e}")
            return None
    
    def answer_from_screenshot(self, image_base64, use_transcript=True):
        """
        Complete workflow: extract question from image and answer it
        
        Args:
            image_base64: Base64 encoded screenshot
            use_transcript: Whether to use loaded transcript as context
            
        Returns:
            tuple: (question, answer)
        """
        print("\n" + "="*50)
        print("Extracting question from screenshot...")
        question = self.extract_question_from_image(image_base64)
        
        if not question:
            return None, None
        
        # Check if OpenAI refused to process
        if "sorry" in question.lower() and "can't" in question.lower():
            print("\n" + "="*50)
            print("⚠️  OpenAI could not process this image")
            print("="*50)
            return question, None
        
        print(f"\nExtracted Text:\n{question}")
        print("\n" + "="*50)
        print("Generating answer...")
        
        answer = self.answer_question(question, use_transcript)
        
        return question, answer
