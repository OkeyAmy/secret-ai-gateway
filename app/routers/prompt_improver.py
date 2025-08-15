from fastapi import APIRouter, HTTPException, Body, Query
from app.config import settings
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.models import AvailableModels, PromptTargets

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
        "- Structure instructions with numbered steps or bullet points where appropriate.\n"
        "- Use clear headings only if the user already used headings.\n"
        "- Include examples or templates only if they add clarity and the user expects them.\n\n"
        "Comprehensiveness:\n"
        "- Address edge cases (e.g., 'include fallback options for low-bandwidth users').\n"
        "- Cover all deliverables (e.g., 'final files in .PNG and .SVG formats').\n"
        "- Anticipate user questions (e.g., 'explain how to adjust for different screen sizes').\n\n"
        "Preservation of Intent & Format:\n"
        "- Cross-reference the enhanced prompt against the original to ensure alignment.\n"
        "- Preserve the user’s existing structure and formatting. Do NOT introduce new titles, subtitles, or sections unless the user already used them.\n"
        "- If the user used headings/sections, keep that pattern; otherwise, keep a single inline prompt.\n\n"
        "Target-specific guidance:\n"
        "- TEXT target: Focus on clarity, actionable instructions, constraints, and expected outputs without adding new headings.\n"
        "- IMAGE target: Optimize visual clarity (subject, composition) and fold attributes inline (style, medium, lighting, color palette, camera/lens/angle, aspect ratio, negatives) without adding headings.\n\n"
        "Output Rules:\n"
        "- Return ONLY the improved prompt, with no meta commentary or explanations.\n"
        "- Preserve the user's structural style (headings, bullets, paragraphs) and do not add titles/subtitles unless the user did so."
    )
}

class PromptRequest(BaseModel):
    prompt: str
    target: Optional[str] = "text"  # "text" or "image"


def _improve(prompt: str, target: str) -> str:
    from app.main import get_gemini_client
    gemini_client = get_gemini_client()

    target = (target or "text").strip().lower()
    if target not in ("text", "image"):
        target = "text"

    target_section = (
        "Target: IMAGE prompt. Optimize for image models (describe visuals with concrete nouns/adjectives; fold style, lighting, camera, aspect ratio inline; avoid new headings).\n"
        if target == "image"
        else "Target: TEXT prompt. Optimize for clarity, structure, and implementable instructions without adding new headings.\n"
    )

    improvement_prompt = f"""{target_section}
Improve the following prompt according to the instructions.

USER PROMPT:
{prompt}

Return ONLY the improved prompt, nothing else.
"""

    contents = f"{PROMPT_IMPROVER_SYSTEM_PROMPT['content']}\n\nUser: {improvement_prompt}"
    response = gemini_client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=contents
    )
    return getattr(response, 'text', str(response))

@router.get("/improve-prompt", tags=["Prompt Improvement"])
async def improve_prompt_get(
    prompt: str = Query(..., description="The prompt text to improve"),
    target: PromptTargets = Query(PromptTargets.TEXT, description="Optional: tailor improvement for text or image prompts")
) -> dict:
    try:
        content = _improve(prompt=prompt, target=target.value)
        return {"response": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error improving prompt: {str(e)}")

@router.post("/improve-prompt", tags=["Prompt Improvement"])
async def improve_prompt(
    request: PromptRequest
) -> dict:
    try:
        content = _improve(prompt=request.prompt, target=request.target or "text")
        return {"response": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error improving prompt: {str(e)}")