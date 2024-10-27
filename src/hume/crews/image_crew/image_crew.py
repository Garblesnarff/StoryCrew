from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ImageCrewCrew():
    """Crew responsible for visual style and image prompt generation"""

    @agent
    def style_director(self) -> Agent:
        return Agent(
            config=self.agents_config['style_director'],
            verbose=True
        )

    @agent
    def prompt_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['prompt_engineer'],
            verbose=True
        )

    @agent
    def consistency_guardian(self) -> Agent:
        return Agent(
            config=self.agents_config['consistency_guardian'],
            verbose=True
        )

    @task
    def establish_visual_style(self) -> Task:
        return Task(
            config=self.tasks_config['establish_visual_style'],
        )

    @task
    def create_scene_prompts(self) -> Task:
        return Task(
            config=self.tasks_config['create_scene_prompts'],
        )

    @task
    def ensure_visual_consistency(self) -> Task:
        return Task(
            config=self.tasks_config['ensure_visual_consistency'],
            output_file='image_prompts.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Image Generation crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )