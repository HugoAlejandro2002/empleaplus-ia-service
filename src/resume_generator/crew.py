from crewai import Agent, Crew, Process, Task
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

content_source = CrewDoclingSource(
    file_paths=[
        "https://twiliofilesacceptgo.s3.us-east-1.amazonaws.com/cv_oraciones_modelo.md"
    ],
)

skills_content_source = CrewDoclingSource(
	file_paths=[
		"https://twiliofilesacceptgo.s3.us-east-1.amazonaws.com/skills_catalog.md"
	],
)


@CrewBase
class ResumeGenerator():
	"""ResumeGenerator crew."""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def cv_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['cv_writer'],
            verbose=True,
            knowledge_sources=[content_source]
		)

	@agent
	def json_formatter(self) -> Agent:
		return Agent(
            config=self.agents_config['json_formatter'],
            verbose=True
        )
	
	@agent
	def skills_extractor(self) -> Agent:
		return Agent(
			config=self.agents_config['skills_extractor'],
			verbose=True,
			knowledge_sources=[skills_content_source]
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task	
	@task
	def generate_cv(self) -> Task:
		return Task(
            config=self.tasks_config['generate_cv']
        )

	@task
	def structure_cv(self) -> Task:
		return Task(
            config=self.tasks_config['structure_cv'],
        )
	
	@task
	def extract_skills(self) -> Task:
		return Task(
			config=self.tasks_config['extract_skills'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ResumeGenerator crew."""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
