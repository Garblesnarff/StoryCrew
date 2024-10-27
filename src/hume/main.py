#!/usr/bin/env python
import asyncio
from typing import List
from crewai.flow.flow import Flow, listen, start
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

from crews.idea_crew.idea_crew import IdeaCrewCrew
from crews.character_crew.character_crew import CharacterCrewCrew
from crews.writing_crew.writing_crew import WritingCrewCrew
from crews.dialog_crew.dialog_crew import DialogCrewCrew
from crews.editing_crew.editing_crew import EditingCrewCrew
from crews.image_crew.image_crew import ImageCrewCrew

class StoryFlow(Flow[StoryState]):
    initial_state = StoryState

    @start()
    def generate_story_concept(self):
        """Generate initial story concept and ideas"""
        print("Starting Idea Generation Crew")
        output = IdeaCrewCrew().crew().kickoff(
            inputs={"prompt": self.state.user_prompt}
        )
        self.state.raw_ideas = output
        return output

    @listen(generate_story_concept)
    async def create_characters(self):
        """Create and develop characters"""
        print("Starting Character Development Crew")
        output = await CharacterCrewCrew().crew().kickoff_async(
            inputs={
                "story_concept": self.state.raw_ideas.model_dump(),
                "target_length": self.state.target_length
            }
        )
        self.state.characters = output["characters"]
        return self.state.characters

    @listen(create_characters)
    async def write_initial_draft(self):
        """Write the initial story draft"""
        print("Starting Writing Crew")
        output = await WritingCrewCrew().crew().kickoff_async(
            inputs={
                "story_concept": self.state.raw_ideas.model_dump(),
                "characters": [char.model_dump() for char in self.state.characters],
                "target_length": self.state.target_length
            }
        )
        self.state.story = output
        return output

    @listen(write_initial_draft)
    async def refine_dialogue(self):
        """Refine and polish dialogue"""
        print("Starting Dialogue Crew")
        output = await DialogCrewCrew().crew().kickoff_async(
            inputs={
                "story": self.state.story.model_dump(),
                "characters": [char.model_dump() for char in self.state.characters]
            }
        )
        self.state.dialogue_style = output
        self.state.story.sections = output["refined_sections"]
        return output

    @listen(refine_dialogue)
    async def generate_image_prompts(self):
        """Generate image prompts for each section"""
        print("Starting Image Prompt Generation Crew")
        output = await ImageCrewCrew().crew().kickoff_async(
            inputs={
                "story": self.state.story.model_dump(),
                "style_guide": self.state.story.style_guide
            }
        )
        self.state.image_prompts = output["prompts"]
        return output

    @listen(generate_image_prompts)
    async def edit_final_story(self):
        """Edit and polish the final story"""
        print("Starting Editing Crew")
        output = await EditingCrewCrew().crew().kickoff_async(
            inputs={
                "story": self.state.story.model_dump(),
                "dialogue_style": self.state.dialogue_style.model_dump(),
                "image_prompts": [prompt.model_dump() for prompt in self.state.image_prompts]
            }
        )
        self.state.edited_content = output["final_content"]
        return output

    @listen(edit_final_story)
    async def save_story(self):
        """Save the final story with all components"""
        print("Saving Final Story")
        
        # Create the complete story markdown
        story_content = f"# {self.state.title}\n\n"
        
        for section_idx, section in enumerate(self.state.story.sections):
            # Add section content
            story_content += f"## Section {section_idx + 1}\n\n"
            story_content += f"{section.content}\n\n"
            
            # Add image prompt
            story_content += f"*Image Prompt:*\n```\n{section.image_prompt.prompt}\n```\n\n"
            
            # Add dialogue notes
            if hasattr(section, 'dialogue') and section.dialogue:
                story_content += f"*Dialogue Notes:*\n```\n{section.dialogue}\n```\n\n"

        # Save to file
        filename = f"./generated_stories/{self.state.title.replace(' ', '_')}.md"
        
        # Ensure directory exists
        import os
        os.makedirs("./generated_stories", exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(story_content)

        print(f"Story saved as {filename}")
        return story_content

async def run_flow():
    """Run the story generation flow."""
    story_flow = StoryFlow()
    await story_flow.kickoff()

async def plot_flow():
    """Plot the story generation flow."""
    story_flow = StoryFlow()
    await story_flow.plot()

def main():
    asyncio.run(run_flow())

def plot():
    asyncio.run(plot_flow())

if __name__ == "__main__":
    main()