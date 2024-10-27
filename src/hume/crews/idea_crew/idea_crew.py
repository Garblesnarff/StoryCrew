from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class IdeaCrewCrew():
    """Crew responsible for creative ideation and story concept development"""

    @agent
    def concept_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['concept_generator'],
            verbose=True
        )

    @agent
    def world_builder(self) -> Agent:
        return Agent(
            config=self.agents_config['world_builder'],
            verbose=True
        )

    @agent
    def plot_weaver(self) -> Agent:
        return Agent(
            config=self.agents_config['plot_weaver'],
            verbose=True
        )

    @task
    def generate_core_concepts(self) -> Task:
        return Task(
            config=self.tasks_config['generate_core_concepts'],
        )

    @task
    def develop_story_world(self) -> Task:
        return Task(
            config=self.tasks_config['develop_story_world'],
        )

    @task
    def craft_plot_possibilities(self) -> Task:
        return Task(
            config=self.tasks_config['craft_plot_possibilities'],
            output_file='story_concept.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Idea Generation crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )