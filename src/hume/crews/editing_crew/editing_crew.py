from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class EditingCrewCrew():
    """Crew responsible for comprehensive story editing and refinement"""

    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['content_editor'],
            verbose=True
        )

    @agent
    def style_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['style_editor'],
            verbose=True
        )

    @agent
    def continuity_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['continuity_checker'],
            verbose=True
        )

    @task
    def structural_edit(self) -> Task:
        return Task(
            config=self.tasks_config['structural_edit'],
        )

    @task
    def style_revision(self) -> Task:
        return Task(
            config=self.tasks_config['style_revision'],
        )

    @task
    def final_polish(self) -> Task:
        return Task(
            config=self.tasks_config['final_polish'],
            output_file='edited_story.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Editing Development crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )