from typing import List
from pydantic import BaseModel

class StoryIdea(BaseModel):
    concept: str
    theme: str
    genre: str
    target_audience: str
    world_building: str
    plot_possibilities: List[str]

class Character(BaseModel):
    name: str
    psychological_profile: str
    backstory: str
    complete_profile: str

class DialogueStyle(BaseModel):
    overall_style: str
    character_voices: dict
    refined_dialogue: str

class ImagePrompt(BaseModel):
    scene_description: str
    style_guide: str
    prompt: str
    visual_notes: str

class StorySection(BaseModel):
    content: str
    image_prompt: ImagePrompt
    dialogue: str

class Story(BaseModel):
    title: str
    sections: List[StorySection]
    characters: List[Character]
    style_guide: str
    final_edit: str

class StoryState(BaseModel):
    title: str = "Untitled Story"
    story: Story = None
    raw_ideas: StoryIdea = None
    characters: List[Character] = []
    dialogue_style: DialogueStyle = None
    image_prompts: List[ImagePrompt] = []
    edited_content: str = ""
    user_prompt: str = ""
    target_length: int = 10  # Number of sections/paragraphs