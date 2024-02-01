import utils

def allocator(jobs, runners,  max_wait, max_online): 

    pending_jobs = [job for job in jobs if job['state'] == 'pending']
    idle_runners = [runner for runner in runners if runner['state'] == 'online' ]

    pending_jobs.sort(key=lambda x: x['wait'], reverse=True)
    idle_runners.sort(key=lambda x: x['idle'], reverse=True)

    #Print pending jobs and idle runners
    for job in pending_jobs:
        print('Pending job: {}, wait time: {}, tags: {}'.format(job['id'], job['wait'], job['tag']))
    print(' ')
    for runner in idle_runners:
        print('Idle runner: {}, idle time: {}, tags: {}'.format(runner['id'], runner['idle'], runner['tags']))
    print(' ')

    #Assign jobs to runners with matching tags
    for job in pending_jobs:
        for runner in idle_runners:
            if job['tag'] in runner['tags']:
                job['state'] = 'running'
                runner['state'] = 'busy'
                runner['idle'] = 0
                print('Job {} is running on runner {}'.format(job['id'], runner['id']))
                pending_jobs.remove(job)
                idle_runners.remove(runner)

    #Assign jobs to runners with no matching tags in which the job has waited too long
    for job in pending_jobs:
        if job['wait'] > max_wait and len(idle_runners) > 0:
            job['state'] = 'running'
            runner = idle_runners.pop()
            runner['state'] = 'busy'
            runner['idle'] = 0
            runner['tags'].append(job['tag'])
            print('Job {} is running on runner {}'.format(job['id'], runner['id']))
            pending_jobs.remove(job)
            idle_runners.remove(runner)

    #Assign jobs to runners with no matching tags in which the runner has been idle too long
    for runner in idle_runners:
        if runner['idle'] > max_online and len(pending_jobs) > 0:
            runner['state'] = 'busy'
            runner['idle'] = 0
            job = pending_jobs.pop()
            job['state'] = 'running'
            runner['tags'].append(job['tag'])
            print('Job {} is running on runner {}'.format(job['id'], runner['id']))
            pending_jobs.remove(job)
            idle_runners.remove(runner)