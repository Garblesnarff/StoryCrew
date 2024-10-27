from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class CharacterCrewCrew():
    """Crew responsible for creating and developing story characters"""

    @agent
    def character_psychologist(self) -> Agent:
        return Agent(
            config=self.agents_config['character_psychologist'],
            verbose=True
        )

    @agent
    def backstory_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['backstory_writer'],
            verbose=True
        )

    @agent
    def character_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['character_profiler'],
            verbose=True
        )

    @task
    def develop_character_psychology(self) -> Task:
        return Task(
            config=self.tasks_config['develop_character_psychology'],
        )

    @task
    def create_character_backstory(self) -> Task:
        return Task(
            config=self.tasks_config['create_character_backstory'],
        )

    @task
    def compile_character_profile(self) -> Task:
        return Task(
            config=self.tasks_config['compile_character_profile'],
            output_file='character_profile.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Character Development crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )