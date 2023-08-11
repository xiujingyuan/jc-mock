

def get_publish_email_content(program, story_name, story_url, username, iteration_name,
                              iteration_url, testing_time, publish_time,
                              developer, create_time, tester):
    """
    返回发布邮件内容
    :param program: 系统名
    :param story_name: 需求名
    :param story_url: 需求地址
    :param username: 发布者
    :param iteration_url: 迭代地址
    :param iteration_name: 迭代名称
    :param testing_time: 提测时间
    :param publish_time: 发布时间
    :param create_time: 创建时间
    :param developer: 开发人员
    :param tester: 测试人员
    :return:
    """
    return f'''
<!DOCTYPE html>  
<html>  
<head>  
<meta charset="UTF-8">  
<title>[{program}]-{story_name}-上线啦！！！</title>  
</head>
<body leftmargin="8" marginwidth="0" topmargin="8" marginheight="4" offset="0">  
    <h1>[{program}]-{story_name}-上线啦！！！</h1>
    <div>
    <table cellpadding="0" cellspacing="0" width="100%" style="margin-left:15px;margin-right:15px;width:100%">
        <tbody>
            <tr>
                <td style="min-width:100%">
                    <div id="m_-8380925815570357119detail_1_workitem_content" style="overflow-x:auto">
                        <table cellpadding="0" cellspacing="0" class="m_-8380925815570357119report-chart__table" 
width="100%" style="width:100%;margin-top:0;margin-bottom:0;margin-left:0;margin-right:0">
                            <thead>
                                <tr>
                                    <th nowrap="" align="left" width="350" style="width:350px" class="m_
-8380925815570357119first"> 需求名</th>
                                    <th nowrap="" align="left" width="100" style="width:100px"> 状态</th>
                                    <th nowrap="" align="left" width="160" style="width:160px"> 迭代</th>
                                    <th nowrap="" align="left" width="200" style="width:100px"> 开发人员</th>
                                    <th nowrap="" align="left" width="200" style="width:100px"> 测试人员</th>
                                    <th nowrap="" align="left" width="200" style="width:100px"> 创建时间</th>
                                    <th nowrap="" align="left" width="200" style="width:100px"> 提测时间</th>
                                    <th nowrap="" align="left" width="120" style="width:120px"> 发布人</th>
                                    <th nowrap="" align="left" width="120" style="width:120px"> 发布时间</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td nowrap="" align="left" class="m_-8380925815570357119first">
                                        <a title="{story_name}" href="{story_url}" target="_blank" >{story_name}</a>
                                    </td>
                                        <td nowrap="" align="left">
                                            <span style="color:#3582fb">已发布</span>
                                        </td>
                                        <td nowrap="" align="left">
                                            <a href="{iteration_url}" target="_blank" >{iteration_name}</a>
                                        </td>
                                        <td nowrap="" align="left"> {developer}</td>
                                        <td nowrap="" align="left"> {tester}</td>
                                        <td nowrap="" align="left"> {create_time}</td>
                                        <td nowrap="" align="left"> {testing_time}</td>
                                        <td nowrap="" align="left"> {username}</td>
                                        <td nowrap="" align="left"> {publish_time}</td>
                                </tr>
                            </tbody>
                        </table>  
                    </div>         
                </td>
            </tr>        
        </tbody>
    </table>
    </div>
</body>  
</html>
'''
