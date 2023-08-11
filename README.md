 **1.项目初始化**
 ##### db同步，创建数据库表
 ##### 执行命令：venv/bin/python3.7 manage.py db upgrade
 
 **2.本地运行项目**
 ##### 执行命令：venv/bin/python3.7 manage.py runserver
 
 **3.生成对应表的orm地址**
 ##### 执行命令：sqlacodegen --outfile=Model/TmmsDb.py mysql://root:Coh8Beyiusa7@127.0.0.1:3317/tmms
 #### flask-sqlacodegen --outfile=app/models/CiAutoTestInfoDb.py --table=ci_autotest_info  mysql://root:Coh8Beyiusa7@127.0.0.1:3317/flasky --flask
  
 **4.启动celery任务**
 # multi start w1 
 #### venv/bin/celery worker -B -A celery_worker.celery --loglevel=info -Q for_search_story_task -n task_schedule
 #### venv/bin/celery worker -A celery_worker.celery --loglevel=info -Q for_run_case_task
 #### venv/bin/celery worker -A celery_worker.celery --loglevel=info -Q for_build_task -n build_task
 
 **5.初始化环境**
 #### venv/bin/python manage.py init
 
 **6.导出依赖**
 #### pip freeze > requirements.txt
 #### pip install -r requirements.txt 安装依赖
 #### pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  xmind2testcase库名
