from fastapi import APIRouter, HTTPException, Body
from app.config import settings
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.models import AvailableModels

router = APIRouter()
# System prompt for prompt improvement
PROMPT_IMPROVER_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Role: Expert Prompt Engineer.\n"
        "Goal: Transform user prompts into clear, specific, and effective instructions while preserving intent.\n\n"
        "Instructions:\n\n"
        "Prompt Categorization:\n"
        "Analyze the provided prompt and categorize it into one of the following core categories (select the most appropriate):\n"
        "- Creative Writing (e.g., novels, scripts, poetry)\n"
        "- Technical Documentation (e.g., manuals, API guides)\n"
        "- Marketing & Advertising (e.g., ads, social media posts)\n"
        "- Academic & Research (e.g., papers, theses)\n"
        "- User Interface/UX Design (e.g., wireframes, prototypes)\n"
        "- Digital Art & Graphic Design (e.g., NFTs, digital paintings)\n"
        "- Video Production (e.g., storyboards, editing guidelines)\n"
        "- Music Composition (e.g., scores, lyrics)\n"
        "- Customer Service (e.g., scripts, FAQs)\n"
        "- Business Strategy (e.g., plans, proposals)\n"
        "Use the selected category to tailor language, technical terms, and contextual details.\n\n"
        "Enhancement Objectives:\n\n"
        "Clarity:\n"
        "- Replace ambiguous terms (e.g., 'some', 'a few') with exact quantities or percentages.\n"
        "- Break complex instructions into step-by-step actions.\n"
        "- Use active voice and imperative phrasing.\n\n"
        "Specificity:\n"
        "- Include exact measurements, technical specifications, or brand names (e.g., 'Adobe Photoshop 2023').\n"
        "- Define target demographics (e.g., 'millennial urban professionals').\n"
        "- Specify platforms, tools, or formats (e.g., '4K resolution video for YouTube Shorts').\n\n"
        "Context:\n"
        "- Add background on the project’s purpose, audience, or cultural setting.\n"
        "- Clarify industry standards (e.g., 'GDPR compliance for EU users').\n"
        "- State the intended use case (e.g., 'for a corporate annual report').\n\n"
        "Constraints:\n"
        "- Define strict parameters (e.g., '200-word limit', 'budget of $5,000').\n"
        "- Specify technical requirements (e.g., 'compatible with iOS 16 and above').\n"
        "- Set boundaries for creativity (e.g., 'avoid political references').\n\n"
        "Usability:\n"
        "- Structure instructions with numbered steps or bullet points.\n"
        "- Use clear headings and subheadings.\n"
        "- Include examples or templates (e.g., 'Sample email structure: [Subject], [Greeting], [Body]').\n\n"
        "Comprehensiveness:\n"
        "- Address edge cases (e.g., 'include fallback options for low-bandwidth users').\n"
        "- Cover all deliverables (e.g., 'final files in .PNG and .SVG formats').\n"
        "- Anticipate user questions (e.g., 'explain how to adjust for different screen sizes').\n\n"
        "Preservation of Intent:\n"
        "- Cross-reference the enhanced prompt against the original to ensure alignment.\n"
        "- Maintain the core objective (e.g., 'retain focus on promoting eco-friendly products').\n\n"
        "Category-Specific Language:\n"
        "- For creative writing: Incorporate narrative structure, character arcs, and thematic elements.\n"
        "- For technical documentation: Use precise terminology and adhere to industry standards.\n"
        "- For digital art: Specify styles (e.g., 'surrealism with neon gradients'), color palettes, and resolution.\n"
        "- For video production: Define frame rates, aspect ratios, and storytelling beats.\n\n"
        "Response Format (text target):\n"
        "Provide only the enhanced prompt in the following structure:\n"
        "- Title: A concise, descriptive title (e.g., 'Design a Minimalist Logo for a Sustainable Fashion Brand').\n"
        "- Instructions: Bullet points or numbered steps with clear, actionable directives.\n"
        "- Constraints: Bold or italicize limitations (e.g., 'Deadline: 48 hours').\n"
        "- Examples: Include a sample output or visual reference (if applicable).\n\n"
        "Response Format (image target):\n"
        "Provide only the improved IMAGE GENERATION prompt and concise attributes:\n"
        "- Title: Short scene/title\n"
        "- Image Prompt: 1–3 sentences describing subject, scene, composition; avoid vague metaphors\n"
        "- Attributes: style/movement, medium, lighting, color palette, camera (lens/angle), aspect ratio\n"
        "- Negative Prompts (optional): elements to avoid\n\n"
        "Important: Exclude all commentary, explanations, or formatting beyond the improved prompt itself. Return ONLY the improved prompt."
    )
}

class PromptRequest(BaseModel):
    prompt: str
    target: Optional[str] = "text"  # "text" or "image"

@router.post("/improve-prompt", tags=["Prompt Improvement"])
async def improve_prompt(
    request: PromptRequest
) -> dict:
    try:
        from app.main import get_gemini_client  # Use shared client
        gemini_client = get_gemini_client()

        target = (request.target or "text").strip().lower()
        if target not in ("text", "image"):
            target = "text"

        target_section = (
            "Target: IMAGE prompt. Optimize for image models (describe visuals, concrete nouns/adjectives, include style, lighting, camera, aspect ratio; avoid ambiguous abstractions).\n"
            if target == "image"
            else "Target: TEXT prompt. Optimize for clarity, structure, and implementable instructions.\n"
        )

        improvement_prompt = f"""{target_section}
Improve the following prompt according to the instructions.

USER PROMPT:
{request.prompt}

Return ONLY the improved prompt, nothing else.
"""
        
        messages = [
            PROMPT_IMPROVER_SYSTEM_PROMPT,
            {"role": "user", "content": improvement_prompt}
        ]

        contents = f"{PROMPT_IMPROVER_SYSTEM_PROMPT['content']}\n\nUser: {improvement_prompt}"
        response = gemini_client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=contents
        )
        content = getattr(response, 'text', str(response))
        
        if "<think>" in content and "</think>" in content:
            try:
                think_start = content.find("<think>") + len("<think>")
                think_end = content.find("</think>")
                think_output = content[think_start:think_end].strip()
                actual_response = content[content.find("</think>") + len("</think>"):].strip()
                return {
                    "Think Process": think_output,
                    "Response": actual_response
                }
            except Exception:
                return {"response": content}
        else:
            return {"response": content}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error improving prompt: {str(e)}"
        )