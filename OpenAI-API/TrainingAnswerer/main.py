import os
import time
from pathlib import Path
from dotenv import load_dotenv
from screen_reader import ScreenReader
from openai_answerer import OpenAIAnswerer


def main():
    """
    Main application for capturing screenshots and answering questions
    using OpenAI with transcript context
    """
    print("="*60)
    print("Training Question Answerer")
    print("="*60)
    
    # Load environment variables
    path = Path("../Environment-Variables/.env")
    load_dotenv(dotenv_path=path)
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: API key not found in environment variables!")
        return
    
    # Initialize components
    screen_reader = ScreenReader()
    answerer = OpenAIAnswerer(api_key=api_key)
    
    # Get screen dimensions
    width, height = screen_reader.get_screen_size()
    print(f"\nScreen size detected: {width}x{height}")
    
    # Load transcript
    print("\n" + "-"*60)
    use_transcript = input("\nDo you want to load a transcript file for context? (y/n): ").strip().lower()
    
    if use_transcript == 'y':
        transcript_path = input("Enter the path to the transcript file: ").strip()
        if answerer.load_transcript(transcript_path):
            print("✓ Transcript loaded and will be used as context")
        else:
            print("✗ Failed to load transcript. Continuing without context...")
    else:
        print("Proceeding without transcript context")
    
    # Main loop
    while True:
        print("\n" + "="*60)
        print("Options:")
        print("1. Capture full screen and answer question")
        print("2. Capture custom region (enter coordinates)")
        print("3. Capture custom region (click and drag with mouse)")
        print("4. Answer a manually typed question")
        print("5. Load a new transcript")
        print("6. Exit")
        print("="*60)
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            # Full screen capture
            print("\nPreparing to capture screen in 3 seconds...")
            print("Switch to the window with the question now!")
            time.sleep(3)
            
            screenshot = screen_reader.capture_screenshot()
            
            if screenshot:
                print("Screenshot captured!")
                
                # Optionally save screenshot
                save = input("Do you want to save the screenshot? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Enter filename (e.g., screenshot.png): ").strip()
                    screen_reader.save_screenshot(filename)
                
                # Convert to base64 and process
                image_base64 = screen_reader.image_to_base64(screenshot)
                if image_base64:
                    question, answer = answerer.answer_from_screenshot(image_base64)
                    
                    if question and answer:
                        print("\n" + "="*60)
                        print("RESULT")
                        print("="*60)
                        print(f"\n📝 Question:\n{question}")
                        print(f"\n💡 Answer:\n{answer}")
                        print("\n" + "="*60)
                    elif question and not answer:
                        print("\n⚠️  Screenshot saved as 'debug_screenshot.png' for review.")
                        screen_reader.save_screenshot("debug_screenshot.png")
                    else:
                        print("\n❌ Failed to extract question from screenshot.")
        
        elif choice == '2':
            # Custom region capture
            print(f"\nScreen size: {width}x{height}")
            print("Enter the region to capture (x, y, width, height)")
            
            try:
                x = int(input("X coordinate: "))
                y = int(input("Y coordinate: "))
                w = int(input("Width: "))
                h = int(input("Height: "))
                
                print("\nPreparing to capture region in 3 seconds...")
                time.sleep(3)
                
                screenshot = screen_reader.capture_screenshot(region=(x, y, w, h))
                
                if screenshot:
                    print("Screenshot captured!")
                    
                    # Optionally save screenshot
                    save = input("Do you want to save the screenshot? (y/n): ").strip().lower()
                    if save == 'y':
                        filename = input("Enter filename (e.g., screenshot.png): ").strip()
                        screen_reader.save_screenshot(filename)
                    
                    # Convert to base64 and process
                    image_base64 = screen_reader.image_to_base64(screenshot)
                    if image_base64:
                        question, answer = answerer.answer_from_screenshot(image_base64)
                        
                        if question and answer:
                            print("\n" + "="*60)
                            print("RESULT")
                            print("="*60)
                            print(f"\n📝 Question:\n{question}")
                            print(f"\n💡 Answer:\n{answer}")
                            print("\n" + "="*60)
                        elif question and not answer:
                            print("\n⚠️  Screenshot saved as 'debug_screenshot.png' for review.")
                            screen_reader.save_screenshot("debug_screenshot.png")
                        else:
                            print("\n❌ Failed to extract question from screenshot.")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
        
        elif choice == '3':
            # Mouse-based region selection
            print("\nA semi-transparent overlay will appear.")
            print("Click and drag to select the region to capture.")
            print("Press ESC to cancel.\n")
            input("Press Enter when ready...")
            
            screenshot = screen_reader.capture_region_with_mouse()
            
            if screenshot:
                print("Screenshot captured!")
                
                # Optionally save screenshot
                save = input("Do you want to save the screenshot? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Enter filename (e.g., screenshot.png): ").strip()
                    screen_reader.save_screenshot(filename)
                
                # Convert to base64 and process
                image_base64 = screen_reader.image_to_base64(screenshot)
                if image_base64:
                    question, answer = answerer.answer_from_screenshot(image_base64)
                    
                    if question and answer:
                        print("\n" + "="*60)
                        print("RESULT")
                        print("="*60)
                        print(f"\n📝 Question:\n{question}")
                        print(f"\n💡 Answer:\n{answer}")
                        print("\n" + "="*60)
                    elif question and not answer:
                        print("\n⚠️  Screenshot saved as 'debug_screenshot.png' for review.")
                        screen_reader.save_screenshot("debug_screenshot.png")
                    else:
                        print("\n❌ Failed to extract question from screenshot.")
        
        elif choice == '4':
            # Manual question input
            question = input("\nEnter your question: ").strip()
            
            if question:
                print("\nGenerating answer...")
                answer = answerer.answer_question(question, use_transcript=True)
                
                if answer:
                    print("\n" + "="*60)
                    print("RESULT")
                    print("="*60)
                    print(f"\n📝 Question:\n{question}")
                    print(f"\n💡 Answer:\n{answer}")
                    print("\n" + "="*60)
        
        elif choice == '5':
            # Load new transcript
            transcript_path = input("\nEnter the path to the transcript file: ").strip()
            if answerer.load_transcript(transcript_path):
                print("✓ Transcript loaded successfully")
            else:
                print("✗ Failed to load transcript")
        
        elif choice == '6':
            # Exit
            print("\nExiting application. Goodbye!")
            break
        
        else:
            print("\nInvalid option. Please select 1-6.")
        
        # Pause before next iteration
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
