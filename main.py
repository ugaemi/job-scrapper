from saramin import get_jobs as get_saramin_jobs
from jobkorea import get_jobs as get_jobkorea_jobs
from save import save_to_file

saramin_jobs = get_saramin_jobs()
jobkorea_jobs = get_jobkorea_jobs()
jobs = saramin_jobs + jobkorea_jobs
save_to_file(jobs)
