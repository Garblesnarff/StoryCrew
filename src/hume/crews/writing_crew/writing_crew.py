from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class WritingCrewCrew():
    """Crew responsible for crafting the story narrative"""

    @agent
    def narrative_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['narrative_writer'],
            verbose=True
        )

    @agent
    def scene_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['scene_architect'],
            verbose=True
        )

    @agent
    def mood_orchestrator(self) -> Agent:
        return Agent(
            config=self.agents_config['mood_orchestrator'],
            verbose=True
        )

    @task
    def craft_narrative_flow(self) -> Task:
        return Task(
            config=self.tasks_config['craft_narrative_flow'],
        )

    @task
    def design_key_scenes(self) -> Task:
        return Task(
            config=self.tasks_config['design_key_scenes'],
        )

    @task
    def weave_complete_story(self) -> Task:
        return Task(
            config=self.tasks_config['weave_complete_story'],
            output_file='story.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Writing Development crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )