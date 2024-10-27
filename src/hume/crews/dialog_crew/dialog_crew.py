from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class DialogCrewCrew():
    """Crew responsible for creating authentic and engaging dialogue"""

    @agent
    def dialogue_stylist(self) -> Agent:
        return Agent(
            config=self.agents_config['dialogue_stylist'],
            verbose=True
        )

    @agent
    def voice_curator(self) -> Agent:
        return Agent(
            config=self.agents_config['voice_curator'],
            verbose=True
        )

    @agent
    def dialogue_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['dialogue_editor'],
            verbose=True
        )

    @task
    def create_dialogue_style(self) -> Task:
        return Task(
            config=self.tasks_config['create_dialogue_style'],
        )

    @task
    def develop_character_voices(self) -> Task:
        return Task(
            config=self.tasks_config['develop_character_voices'],
        )

    @task
    def refine_dialogue(self) -> Task:
        return Task(
            config=self.tasks_config['refine_dialogue'],
            output_file='dialogue_output.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Dialogue Development crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )